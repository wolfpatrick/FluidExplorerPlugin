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
from FluidExplorerPlugin.ui.Utils.ProjectDetailsViewUtils import ProjectSubSettings
from FluidExplorerPlugin.ui.Utils.ProjectDetailsViewUtils import ProjectDetailsViewUtils
import os

from maya import OpenMayaUI as omui
from shiboken import wrapInstance
#import maya.cmds as cmds

"""
class windowTest(baseClass, widgetForm):
    def __init__(self, parent = None):
        super(windowTest, self).__init__(parent)
        self.setupUi(self)
"""
class ProjectDetailsView(QtGui.QDialog):

    PERSPECTIVE_CAMERA_AVAILABLE = '1'
    PERSPECTIVE_CAMERA_NOT_AVAILABLE = '0'

    def __init__(self, args, pathToXMLFile):
        QtGui.QDialog.__init__(self, args)

        # Stores th path to the XML file
        self.pathToXMLFile = pathToXMLFile

        # Members
        self.projectSettings = None
        self.hashMapToXMLProjectFile = {}
        self.hashMapToGIF = {}
        self.currentAnimationLoaded = None

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
        self.setWindowTitle('Fluid Explorer - Simulation Details View')

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

    def scaleMovieLabel(self):
        # Is supposed to be: 960x540
        # Width = 300
        size = self.ui.label_moviePreview.size()
        newSize = QtCore.QSize(300, 169)
        self.movie.setScaledSize(newSize)

    def setValuesFromConfigurationFile(self, projectSettings):
        canReadAllAttributes = True

        print("Read projects attributes for:\n")
        for attr, value in projectSettings.__dict__.iteritems():
            print attr, ": ", value
            if value == None:
                canReadAllAttributes = False
                print("Warning: Cannot read attribute", attr)

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
        self.ui.comboBox_simulations.addItem('Select Simulation ...')

        try:
            num = int(projectSettings.numberOfSimulations)
        except:
            num = 0

        if num > 0:
            for i in range(num):

                # Firste entry
                tmpNameForElement = 'Simulation ' + str(i+1)

                # Folders
                tmp = projectSettings.projectPath + "/" + str(i) + "/"
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
        currentIndex = self.ui.comboBox_simulations.currentIndex()
        if currentIndex >= 1:
            pathToXMLFile = self.hashMapToXMLProjectFile[currentIndex-1]
            if pathToXMLFile == self.currentAnimationLoaded:
                # Do not load the cache which is already loaded! -> pass
                pass
            else:
                print('Load cache file', pathToXMLFile)
                self.currentAnimationLoaded = pathToXMLFile


    @QtCore.Slot()
    def exploreSimulationsClicked(self):
        print 'exploreSimulationsClicked'

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
        print 'help'

    @QtCore.Slot()
    def frameChangedHandler(self, frameNumber):
        pass
        #print frameNumber

    # - Event handlers end -

    # - Help functions -
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
            return projectSettings

        print projectSettings.projectName

        return projectSettings

    def showMessageBox(self, errorMsg, type):
        msgBox = QtGui.QMessageBox(self)
        msgBox.setText(errorMsg)
        if type == 'critical':
            msgBox.setWindowTitle("Error - Load Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Critical)
        if type == 'warning':
            msgBox.setWindowTitle("Warning - Load Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)

        msgBox.setStyleSheet(DefaultUIParameters.buttonStyleBold)
        msgBox.exec_()
    # - Help functions end -