"""
from PySide import QtGui, QtCore
import maya.cmds as cmds

from PySide import QtCore, QtGui
from maya import OpenMayaUI as omui
from shiboken import wrapInstance


class ProjectDetailsView(QtGui.QDockWidget):

    def __init__(self):
        super(ProjectDetailsView, self).__init__()
        self.initUI()
        print "Window created"

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Icon')

        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(100, 200)

        panelPtr = omui.MQtUtil.findControl('modelPanel1')
        panel = wrapInstance(long(panelPtr), QtGui.QWidget)

        position = panel.mapToGlobal(panel.pos())

        self.move(position.x(), position.y())

"""

from PySide import QtCore, QtGui
from ProjectDetailsViewUI import Ui_ProjectDetailsView

from FluidExplorerPlugin.ui.Utils.DefaultUIValues import DefaultUIParameters
from FluidExplorerPlugin.ui.Utils.ProjectDetailsViewUtils import ProjectDetailsViewUtils
from FluidExplorerPlugin.ui.Utils.ProjectDetailsViewUtils import ExternalCallSetting
from FluidExplorerPlugin.ui.Utils.LoadFluidCacheFile import LoadFluidCacheFile
from FluidExplorerPlugin.ui.Utils.ExternalCallWorkerThread import WorkThread
from FluidExplorerPlugin.ui.Utils.FluidExplorerUtils import FluidExplorerUtils

from maya import OpenMayaUI as omui
import maya.cmds as cmds
from shiboken import wrapInstance
import os
import sys
import logging


class ProjectDetailsView(QtGui.QDialog):

    PERSPECTIVE_CAMERA_AVAILABLE = '1'
    PERSPECTIVE_CAMERA_NOT_AVAILABLE = '0'

    def __init__(self, args, pathToXMLFile):

        QtGui.QDialog.__init__(self, args)

        # Logger
        self.lgr = logging.getLogger('FluidExplorerPlugin')

        # Stores th path to the XML file
        self.pathToXMLFile = pathToXMLFile
        self.PathToXMLCache = ''

        # Members
        self.projectSettings = None
        self.hashMapToXMLProjectFile = {}
        self.hashMapToGIF = {}
        self.currentAnimationLoaded = None

        # Thread which starts the FX app
        self.workThread = None
        self.FLUIDEXPLORER_APP_NAME = "fluidexplorer"

        # Set up the user interface from the ui file
        self.ui = Ui_ProjectDetailsView()
        self.ui.setupUi(self)

        # Move window to the 'modelPanel1' position
        [xPos, yPos] = self.moveWindowToPanel()
        self.move(xPos, yPos)

        # QMovie
        self.movie = QtGui.QMovie(self)

        # Create connections
        self.createConnections()

        # Initialize widget
        self.initializewidget()
        self.setWindowHeightWithoutPreview()
        self.initializeComponentss()
        self.setWindowTitle('Fluid Explorer - Project View')

        # Window flags - top and buttons
        self.setWindowFlags(self.windowFlags() |
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowStaysOnTopHint)

        self.show()

        # Set values from project configuration file
        statusCode = self.projectSettings = self.readProjectProperties(self.pathToXMLFile)
        if statusCode:
            canSetAllFields = self.setValuesFromConfigurationFile(self.projectSettings)
            if not canSetAllFields:
                self.showMessageBox('Could not read all project attributes from the\nconfiguration file!', 'warning')
        else:
            self.setAllFieldsEnabled()

        # Initialize the combo box and the preview functionality
        if self.projectSettings:
            self.initComboBoxSimulations(self.projectSettings)
            self.initPreview(self.projectSettings)

        # Register scriptJob
        self.FXScriptJob()
        self._rcwin = 1

        # External call
        self.externalCall = ExternalCallSetting()
        self.setupExternallCall()

        self.lgr.info('Load project view created')
        self.lgr.info('Project path: %s', pathToXMLFile)


    def setPathToProjectFile(self, path):
        self.pathToXMLFile = path

    def setAllFieldsEnabled(self):
        self.ui.pushButton_applyCache.setEnabled(False)
        self.ui.pushButton_exploreSimulations.setEnabled(False)
        self.ui.checkBox_showPreview.setEnabled(False)
        self.ui.comboBox_simulations.setEnabled(False)
        self.update()

    def moveWindowToPanel(self):
        try:
            panelPtr = omui.MQtUtil.findControl('modelPanel1')

            if not panelPtr:
                xPos = 0
                yPos = 0
            else:
                panel = wrapInstance(long(panelPtr), QtGui.QWidget)
                position = panel.mapToGlobal(panel.pos())
                if not panelPtr:
                    xPos = 0
                    yPos = 0
                else:
                    xPos = position.x()
                    yPos = position.y()
        except:
            xPos = 0
            yPos = 0

        return [xPos, yPos]

    def initializewidget(self):
        self.setMinimumWidth(340)
        self.setMaximumWidth(340)

    def setWindowHeightWithPreview(self):
        self.setMinimumHeight(620-25)
        self.setMaximumHeight(620-25)

    def setWindowHeightWithoutPreview(self):
        self.setMinimumHeight(360-0)
        self.setMaximumHeight(360-0)

    def initializeComponentss(self):
        icon_help = QtGui.QIcon(QtGui.QPixmap(':/help_icon_orange.png'))
        self.ui.pushButton_help.setIcon(icon_help)

        self.setWindowTitle('Fluid Explorer - Simulation Details View')
        self.changeHLineStyle()
        self.setLineEditEnabledAndReadOnly(self.ui.lineEdit_projectName)
        self.setLineEditEnabledAndReadOnly(self.ui.lineEdit_projectPath)
        self.setLineEditEnabledAndReadOnly(self.ui.lineEdit_fluidContainer)
        self.setLineEditEnabledAndReadOnly(self.ui.lineEdit_startTime)
        self.setLineEditEnabledAndReadOnly(self.ui.lineEdit_endTime)

        self.ui.label_moviePreview.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.label_moviePreview.setStyleSheet("background-color: black;")

        self.scaleMovieLabel()
        self.ui.label_moviePreview.setMaximumHeight(170)
        self.ui.label_moviePreview.setMinimumHeight(170)

    def setupExternallCall(self):
        # e.g. fluidexplorer.exe /settings path=E:/TMP/ANNAANNA/ANNAANNA.fxp /load path=E:/FluidExplorer_Code/FlameShape/FlameShape1

        # FluidExplorer
        self.externalCall.pathToFluidExplorer = ProjectDetailsViewUtils.getPathFluidExplorer()
        if sys.platform.startswith('win'):
            self.externalCall.fluidExplorerCmd = 'fluidExplorer.exe'
        elif sys.platform.startswith(''):
            # TODO: UNIX
            pass

        # Settings file
        settingXMLFile = self.pathToXMLFile

        # Path to cached files
        cacheFile = ProjectDetailsViewUtils.getPathCacheFiles(self.pathToXMLFile)

        # Args
        self.externalCall.fluidExplorerArgs = '/settings path=' + str(settingXMLFile) + ' ' + '/load path=' + str(cacheFile)

        # For testing
        self.externalCall.pathToFluidExplorer = 'E:/FluidExplorer_Code/Release/'
        self.externalCall.pathToFluidExplorer = 'E:/Workspace_VisualStudio/fluidexplorer/Backup/fluidexplorer/bin/Win32/Debug/'
        self.externalCall.fluidExplorerCmd = 'fluidExplorer.exe'
        self.externalCall.fluidExplorerArgs = '/load path=E:\FluidExplorer_Code\FlameShape\FlameShape1'


    def scaleMovieLabel(self):
        # Is supposed to be: 960x540
        # Width = 300
        size = self.ui.label_moviePreview.size()
        newSize = QtCore.QSize(300, 169)
        self.movie.setScaledSize(newSize)

    def setValuesFromConfigurationFile(self, projectSettings):
        canReadAllAttributes = True

        self.lgr.info('Read projects attributes:')
        for attr, value in projectSettings.__dict__.iteritems():
            # txt = attr + ": " + value
            self.lgr.info('%s : %s', attr, value)
            if value == None:
                canReadAllAttributes = False
                self.lgr.warning('Cannot read attribute %s', attr)

        if projectSettings:
            self.ui.lineEdit_projectName.setText(projectSettings.projectName)
            self.ui.lineEdit_projectPath.setText(projectSettings.projectPath)
            self.ui.lineEdit_fluidContainer.setText(projectSettings.fluidContainerName)
            self.ui.lineEdit_startTime.setText(projectSettings.animationStartTime)
            self.ui.lineEdit_endTime.setText(projectSettings.animationEndTime)

        return canReadAllAttributes

    def initComboBoxSimulations(self, projectSettings):

        # Stores animation index and path
        haspMap = {}

        # First item
        self.ui.comboBox_simulations.addItem('Select Sequence ...')

        try:
            num = int(projectSettings.numberOfSimulations)
        except:
            num = 0

        if num > 0:
            for i in range(num):

                # Firste entry
                tmpNameForElement = 'Sequence ' + str(i+1)

                # Folders
                tmpProject = projectSettings.projectName + '.fxp'
                index = self.pathToXMLFile.find(tmpProject)
                tmp = self.pathToXMLFile[0:index]
                tmp = tmp + '/' + str(i) + '/'
                #tmp = projectSettings.projectPath + "/" + str(i) + "/"
                if os.path.exists(tmp):
                    pathToXMLProjectFileList = ProjectDetailsViewUtils.getPathToXMLFile(tmp)

                    if len(pathToXMLProjectFileList) == 1:
                        if os.path.exists(pathToXMLProjectFileList[0]):
                            haspMap[i] = pathToXMLProjectFileList[0]
                            self.ui.comboBox_simulations.addItem(tmpNameForElement)

            self.hashMapToXMLProjectFile = haspMap

    def initPreview(self, projectSettings):
        if projectSettings.cam_persp == '1' or projectSettings.cam_persp == '1':
            self.hashMapToGIF = ProjectDetailsViewUtils.getGIFHashMap(projectSettings)
        else:
            self.ui.checkBox_showPreview.setEnabled(False)

    def createConnections(self):
        self.connect(self.ui.pushButton_applyCache, QtCore.SIGNAL("clicked()"), self.applyCacheClicked)
        self.connect(self.ui.pushButton_exploreSimulations, QtCore.SIGNAL("clicked()"), self.exploreSimulationsClicked)
        self.connect(self.ui.checkBox_showPreview, QtCore.SIGNAL("stateChanged(int)"), self.checkBoxPreviewValueChanged)
        self.connect(self.ui.comboBox_simulations, QtCore.SIGNAL("currentIndexChanged(QString)"), self.comboBoxSimulationsIndexChanged)
        self.connect(self.ui.pushButton_help, QtCore.SIGNAL("clicked()"), self.helpButtonClicked)
        self.connect(self.movie, QtCore.SIGNAL("frameChanged(int)"), self.frameChangedHandler)

    def playAnimation(self, simulationIndex):

        if self.hashMapToGIF == None:
            return

        # Index for the hash map
        hashIndex = simulationIndex - 1

        if simulationIndex == 0:
            self.stopPlayingAnimation()
            return

        fileName = self.hashMapToGIF[hashIndex]

        if not os.path.exists(fileName):
            self.ui.label_moviePreview.setText("<b>[ Cannot find animation ... ]</b>")
            self.stopPlayingAnimation()
            return
        else:
            self.ui.label_moviePreview.setText("")
            self.ui.label_moviePreview.setMovie(self.movie)

        # Play animation
        currentState = self.movie.state()

        if currentState == QtGui.QMovie.Running:
            self.movie.stop()
            self.movie.setFileName(fileName)
            self.movie.start()

        elif currentState == QtGui.QMovie.NotRunning:
            self.movie.setFileName(fileName)
            self.movie.start()

    def stopPlayingAnimation(self):
        self.movie.stop()
        self.ui.label_moviePreview.setText("<b>[ No Simulation selected ... ]</b>")

    # - Event handlers -
    @QtCore.Slot()
    def applyCacheClicked(self):
        # Check of corredt scene is opened
        currentSceneName = cmds.file(q=True, sceneName=True)
        sceneFromConfigFile = self.projectSettings.mayaFilePath
        isSameScene = ProjectDetailsViewUtils.checkIfCorrectSceneIsOpened(currentSceneName, sceneFromConfigFile)
        if not isSameScene:
            strError = 'Please open the correct maya scene first!\nPath: ' + sceneFromConfigFile
            self.lgr.warning('Please open the correct maya scene first! Path: %s', sceneFromConfigFile)
            self.showMessageBox(strError, 'warning')
            return

        # Same scene ...
        currentIndex = self.ui.comboBox_simulations.currentIndex()
        if currentIndex >= 1:
            self.PathToXMLCache = self.hashMapToXMLProjectFile[currentIndex-1]
            if self.PathToXMLCache == self.currentAnimationLoaded:
                # Do not load the cache which is already loaded! -> pass
                cmds.select(self.projectSettings.fluidContainerName, r=True)
                pass
            else:
                self.lgr.info('Load cache file: %s', self.PathToXMLCache)
                self.currentAnimationLoaded = self.PathToXMLCache

                # Set animation start and edn time
                canSetTime = ProjectDetailsViewUtils.setAnimationStartEndTime(self.projectSettings.animationStartTime, self.projectSettings.animationEndTime)
                if not canSetTime:
                    self.lgr.warning('Cannot set the start / end time of the animation')
                    self.showMessageBox('Cannot set the start / end time of the animation.', 'warning')

                # Load cache file
                try:
                    LoadFluidCacheFile.applyCacheFile(self.PathToXMLCache, self.projectSettings.fluidContainerName)
                except Exception as e:
                    self.lgr.error('%s', e.message)
                    self.showMessageBox(e.message, 'critical')

            # Set the values
            ProjectDetailsViewUtils.applyValuesFromXMLFile(self.PathToXMLCache, self.projectSettings.fluidContainerName)

    @QtCore.Slot()
    def exploreSimulationsClicked(self):
        self.lgr.info('Explore simulations clicked')

        # Check of corredt scene is opened
        currentSceneName = cmds.file(q=True, sceneName=True)
        sceneFromConfigFile = self.projectSettings.mayaFilePath
        isSameScene = ProjectDetailsViewUtils.checkIfCorrectSceneIsOpened(currentSceneName, sceneFromConfigFile)
        if not isSameScene:
            strError = 'Please open the correct maya scene first!\nPath: ' + sceneFromConfigFile
            self.lgr.warning('Please open the correct maya scene first! Path: %s', sceneFromConfigFile)
            self.showMessageBox(strError, 'warning')
            return

        # Check if xml files are available
        if not len(self.hashMapToXMLProjectFile) == int(self.projectSettings.numberOfSimulations) + 1:
            self.lgr.warning('Number of XML cache files is not correct')
            errorMsg = "The number of .xml cache files is not correct!\nPlease check the project folder or create the simulation again."
            self.showMessageBox(errorMsg, 'warning')
            return

        # Check if fluidexplorer app is running
        isFXProcessRunning = ProjectDetailsViewUtils.checkIfProcessIsRunning_WIN(self.FLUIDEXPLORER_APP_NAME)
        if isFXProcessRunning:
            return

        # Check if path exists
        pathToFXAPP = self.externalCall.pathToFluidExplorer + '/' + self.externalCall.fluidExplorerCmd
        if not os.path.exists(os.path.abspath(pathToFXAPP)):
            self.lgr.error('Cannot find the FluidExplorer application executable')
            errorMsg = "Cannot find the FluidExplorer application executable!" + "\n" + "Please check if  the executable file is available."
            self.showMessageBox(errorMsg, 'warning')
            return

        # Run the worker thread
        if self.workThread:
            self.workThread.stop()

            # Start thread again
            self.workThread = WorkThread(self.externalCall)
            self.connect(self.workThread, QtCore.SIGNAL("update(QString)"), self.updateIndexFromThread)
            self.workThread.start()

        else:
            # Start thread
            self.workThread = WorkThread(self.externalCall)
            self.connect(self.workThread, QtCore.SIGNAL("update(QString)"), self.updateIndexFromThread)
            self.workThread.start()


    @QtCore.Slot()
    def checkBoxPreviewValueChanged(self, state):
        # State starts with 0
        if self.ui.checkBox_showPreview.checkState() == QtCore.Qt.Checked:
            # active
            self.setWindowHeightWithPreview()
            self.playAnimation(self.ui.comboBox_simulations.currentIndex())
        elif self.ui.checkBox_showPreview.checkState() == QtCore.Qt.Unchecked:
            # not active
            self.setWindowHeightWithoutPreview()
            self.movie.stop()

    @QtCore.Slot()
    def comboBoxSimulationsIndexChanged(self, index):
        if self.ui.checkBox_showPreview.checkState() == QtCore.Qt.Checked:
            currentIndex = self.ui.comboBox_simulations.currentIndex()
            #hashMapIndex = currentIndex-1

            # Play animation
            self.playAnimation(currentIndex)

    @QtCore.Slot()
    def helpButtonClicked(self):
        self.lgr.info('Help clicked')

    @QtCore.Slot()
    def frameChangedHandler(self, frameNumber):
        pass

    # - Event handlers end -

    # - Help functions -
    def updateIndexFromThread(self, text):
        # print "UPDATE INDEX: " + text
        self.lgr.info('Update index: %s', text)

        # If the thread sends am error -> stop
        if text == "ERROR":
            self.lgr.error('Cannot execute the FluidExplorer application')
            self.showMessageBox('Cannot execute the FluidExplorer application!\nSee editor output for details.', 'critical')
            return

        # Else, update the combo box
        try:
            intIndex = int(text)
        except:
            intIndex = 0
        finally:
            # TODO
            if intIndex > 2:
                self.ui.comboBox_simulations.setCurrentIndex(0)
                self.update()
            else:
                self.ui.comboBox_simulations.setCurrentIndex(1)
                self.update()

    def setLineEditEnabledAndReadOnly(self, component):
        component.setStyleSheet(self.getStyle())
        component.setReadOnly(True)

    def changeHLineStyle(self):
        self.ui.line_1.setGeometry(20, 40, 300, 1)
        self.ui.line_2.setGeometry(20, 240, 300, 1)
        self.ui.line_3.setGeometry(20, 390, 300, 1)
        self.ui.line_1.setLineWidth(1)
        self.ui.line_2.setLineWidth(1)
        self.ui.line_3.setLineWidth(1)
        self.ui.line_1.setStyleSheet("QFrame{background-color: gray;}")
        self.ui.line_2.setStyleSheet("QFrame{background-color: gray;}")
        self.ui.line_3.setStyleSheet("QFrame{background-color: gray;}")

    def getStyle(self):
        styleEnabled = ("QLineEdit:read-only{"
            "font-size: 12px;"
            "/*font-weight: bold;*/"
            "}"
            )

        return styleEnabled

    def readProjectProperties(self, pathToXMLFile):
        xmReader = ProjectDetailsViewUtils()

        projectSettings = None
        try:
            projectSettings = xmReader.getProjectSubSettings(pathToXMLFile)
        except Exception as e:
            errorText = "An error occured while loading the project configuration file!\nDetails: " + str(e.message)
            self.showMessageBox(errorText, 'critical')
            self.lgr.error('Loading the project configuration file: %s', errorText)
            return projectSettings

        return projectSettings

    def showMessageBox(self, errorMsg, type):
        msgBox = QtGui.QMessageBox(self)
        msgBox.setText(errorMsg)
        if type == 'critical':
            msgBox.setWindowTitle("Error")
            msgBox.setIcon(QtGui.QMessageBox.Critical)
        if type == 'warning':
            msgBox.setWindowTitle("Warning")
            msgBox.setIcon(QtGui.QMessageBox.Warning)

        msgBox.setStyleSheet(DefaultUIParameters.buttonStyleBold)
        msgBox.exec_()

    def closeEvent(self, event):

        # ProjectDetailsViewUtils.killProcess_WIN('fluidexplorer')

        # Stop thread if running
        if self.workThread:
            self.workThread.stop()
            # self.workThread.terminate()
        FluidExplorerUtils.killProcess('fluidexplorer')
    # - Help functions end -

    # ScriptJob
    def FXScriptJob(self):
            #self.close()
            #import maya.cmds as cmds
            sJob = cmds.scriptJob(event=['deleteAll', self.ScriptJobMethodCall])
            sJob = cmds.scriptJob(event=['quitApplication', self.ScriptJobMethodCall])


    def ScriptJobMethodCall(self):
        if self.workThread:
            self.workThread.stop()
        ProjectDetailsViewUtils.checkIfProcessExistsAndClose(self.FLUIDEXPLORER_APP_NAME)
        self.PathToXMLCache = ''
    # ScriptJob
