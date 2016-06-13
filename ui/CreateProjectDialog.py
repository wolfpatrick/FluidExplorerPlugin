import string
from PySide import QtGui
from PySide import QtCore

import os
import re
import platform
import webbrowser
import errno
import time
import itertools

import maya.cmds as cmds

from CreateProjectDialogUI import Ui_CreateProjectDialog
from DefaultUIValues import DefaultUIParameters
from FileOpenDialog import FileOpenDialog
from ChooseCameraDialog import ChooseCameraDialog
from MayaCacheCmdSettings import MayaCacheCmdSettings
from Utils import FluidExplorerUtils
from MayaUiDefaultValues import MayaUiDefaultValues
from Utils.MayaCmds.ParameterSpace import MayaCacheCmd
from MayaCacheCommandParameters import MayaCacheCommand
from Utils.MayaCmds.MayaCacheCmd import MayaCacheCmdString
from Utils.MayaCmds.MayaFunctions import MayaFunctionUtils
from ParamterTab import ParameterTab
from Utils.RangeSliderSpan import FluidValueSampler
from Utils.XmlFileWriter import XmlFileWriter
from Utils.GifCreatpr import GifCreator

#import itertools
#import errno
import ConfigParser
#import pysideuic
#from RangeSlider.HRangeSlider import QHRangeSlider
#from ParameterInputBoxes import ParameterInputBoxes


class CreateProjectDialog(QtGui.QDialog):

    CLICK_FLAG_CAM_PV = True
    CLICK_FLAG_CAM_VC = False
    CLICK_FLAG_CAM_SPH = False
    CLICK_FLAG_CAM_ROT = False
    choosenCamera = None
    FLUID_EXPLORER_URL = "http://www.google.de"
    DIALOG_STYLE_SHEET = "QPushButton{min-width: 70px;} QMessageBox{font-size: 12px;}"

    def __init__(self, args, fluidName):
        QtGui.QDialog.__init__(self, args)

        self.fluidName = fluidName

        # Store settings
        self.simulationSettings = MayaCacheCmdSettings()
        self.simulationSettings.fluidBoxName = fluidName

        # Create the user interface from the ui file
        self.ui = Ui_CreateProjectDialog()
        self.ui.setupUi(self)
        self.createConnections()

        # Store the selected fluid container name
        self.setFluidName(fluidName)

        self.tabParamtersObj = None
        self.tabParamters = None

        self.setUpComponents()
        self.tabParameterValuesFirstOpened = False
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget.update()
        self.centre()
        self.setFluidNameLabel()

        self.ui.label_2.setStyleSheet("font-weight: bold;")
        self.ui.label_3.setStyleSheet("font-weight: bold;")
        self.ui.label_4.setStyleSheet("font-weight: bold;")
        self.ui.label_5.setStyleSheet("font-weight: bold;")
        self.ui.groupBoxCameras.setStyleSheet("QGroupBox{font-weight: bold;}")

        # Calculation of time
        self.isTimeCalculated = False
        self.time_Caching = 0
        self.time_Renering = 0
        self.time_GIF = 0
        self.progressSteps = 0

        # FFmpeg path
        self.ffmpegpath = self.getFFmpegPath()

        ###############
        """
        directoryImagesDir = 'E:/TMP/XXX/'
        outputGifFileDir = 'E:/WorkspacePython/GifCreator/'
        outputGifFileName = 'babb123.gif'
        #fps = 25
        #gifOptimization = True

        outputFileName = outputGifFileDir + outputGifFileName
        self.gifImageCreator = GifCreator()
        ffmpegPath = self.ffmpegpath
        isFFmpegExecutable = self.gifImageCreator.createGifFromImages(ffmpegPath, directoryImagesDir, outputGifFileDir, outputGifFileName, fps=25, gifOptimization=25)
        print("FFmpeeg executable: ", isFFmpegExecutable)
        """
        ###############

        self.setTabOrder(self.ui.lineEdit_SimulationName, self.ui.pushButtonCreateSimulation)
        self.setTabOrder(self.ui.pushButtonCreateSimulation, self.ui.label_2)

        #self.ui.tabWidget.setMinimumWidth(800)
        #self.ui.tabWidget.setMaximumWidth(800)



    def centre(self):
        # The dialog window is shifted to the right that the maya question
        # dialogs are not hidden
        screen = QtGui.QDesktopWidget().screenGeometry()
        mysize = self.geometry()
        hpos = ( screen.width() - mysize.width() ) / 2
        vpos = ( screen.height() - mysize.height() ) / 2

        self.move(hpos + (mysize.width() / 3), vpos)

    def setFluidName(self, name):
        self.fluidName = name

    def setUpComponents(self):

        self.ui.tabWidget.removeTab(1)
        self.setAnimationStartEndTime()

        icon_open = QtGui.QIcon(QtGui.QPixmap(':/help_icon_orange.png'))
        self.ui.pushButtonNewPrjHelp.setIcon(icon_open)
        self.ui.lineEdit_SimulationName.setText(DefaultUIParameters.DEF_SIMULATION_NAME)

        #self.workDirPath = "E:/TMP"
        self.workDirPath = cmds.workspace(q=True, dir=True)
        print("Workspace: ", self.workDirPath)
        # TODO - delete tmp
        self.workDirPath = "E:/TMP"

        if platform.system() == "Windows":
            self.workDirPath = self.workDirPath.replace("/", "\\")

        self.ui.lineEdit_ProjPath.setText(self.workDirPath)

        buttonStyleBold = "QPushButton { font-weight: bold; }"
        self.ui.pushButtonCreateSimulation.setStyleSheet(buttonStyleBold)
        self.ui.label.setEnabled(False)
        self.ui.spinBox_rotDeg.setEnabled(False)
        self.ui.spinBox_rotDeg.setValue(DefaultUIParameters.DEF_SPIN_ROT)
        self.ui.spinBox_rotDeg.setMinimum(DefaultUIParameters.DEF_SPIN_ROT_MIN)
        self.ui.spinBox_rotDeg.setMaximum(DefaultUIParameters.DEF_SPIN_ROT_MAX)

        self.initCamButtons()
        self.initSliderValues()
        self.addParamterTab()


    def setFluidNameLabel(self):
        self.ui.labelFluidBox_Value.setText(self.simulationSettings.fluidBoxName)
        
    def addParamterTab(self):
        self.tabParamtersObj = ParameterTab(self.simulationSettings.fluidBoxName)
        self.tabParamters = self.tabParamtersObj.getTab()
        self.ui.tabWidget.addTab(self.tabParamters, "Paramaters")

    def createConnections(self):
        self.ui.pushButtonNewPrjHelp.clicked.connect(self.buttonHelpCreateProj_Event)
        self.ui.pushButtonBrowse.clicked.connect(self.buttonBrowse_Event)
        self.ui.pushButtonCreateSimulation.clicked.connect(self.buttonCreateSimulation_Event)
        self.ui.horizontalSlider_numberSeq.valueChanged[int].connect(self.sliderNumberSequences_Event)
        self.ui.lineEdit_numberSeq.textChanged.connect(self.lineEdit_numberSeq_Event)
        self.ui.lineEdit_numberSeq.editingFinished.connect(self.lineEdit_numberSeq_EditFinished)
        self.ui.spinBox_rotDeg.valueChanged.connect(self.spinBoxRot_Event)
        self.ui.pushButtonBrowse_CalculateTime.clicked.connect(self.calculateTimeClicked)

    def setAnimationStartEndTime(self):
        uiStatus = MayaUiDefaultValues()
        uiStatus.getAnimationStartEnd()
        begin = uiStatus._animationMinTime
        end = uiStatus._animationEndTime

        txt = str(begin) + " / " + str(end)
        numberOfFrames = (end - begin) + 1

        self.ui.labelAnimationTimeStartEnd.setText(txt)
        self.simulationSettings.animationStartTime = begin
        self.simulationSettings.animationEndTime = end
        self.simulationSettings.numberOfFrames = int(numberOfFrames)

    @QtCore.Slot()
    def buttonHelpCreateProj_Event(self):
        webbrowser.open(self.FLUID_EXPLORER_URL, new=1)

    @QtCore.Slot()
    def buttonBrowse_Event(self):
        self.fileDialog = FileOpenDialog(self)
        choosenDir = self.fileDialog.openDirDialogQuick()

        if not choosenDir == "":
            choosenDir = choosenDir + "/"
            if (platform.system() == "Windows"):
                choosenDirNew = choosenDir.replace("/","\\")
            else:
                choosenDirNew = choosenDir

        self.ui.lineEdit_ProjPath.setText(choosenDirNew)

    @QtCore.Slot()
    def buttonCreateSimulation_Event(self):

        self.currentMayaSceneName = ""
        pathName = self.ui.lineEdit_ProjPath.text()
        projName = self.ui.lineEdit_SimulationName.text()

        pathOk = False
        [pathOk, simulationNameAbsolut] = self.checkProjectPathOk(pathName, projName)
        if not pathOk:
            return
        else:
            # Ckeck if the scene is saved
            self.currentMayaSceneName = cmds.file(q=True, sn=True)

            try:
                tmpMayaFilePath = self.simulationSettings.outputPath + "/fluid_simulation_scene.mb"
                cmds.file(rename = tmpMayaFilePath)
                dialogRes = cmds.file(save=True)
                self.simulationSettings.simulationNameMB = tmpMayaFilePath
            except:
                print self.currentMayaSceneName
                print len(self.currentMayaSceneName)
                if len(self.currentMayaSceneName) == 0:
                    self.currentMayaSceneName = self.currentMayaSceneName + "untitled"

                cmds.file(rename = self.currentMayaSceneName) # Old name
                self.close()
                os.rmdir(self.simulationSettings.outputPath)

        # Get some information about the current scene
        self.simulationSettings.fluidBoxName = self.fluidName
        self.simulationSettings.numberSamples = self.ui.horizontalSlider_numberSeq.value()
        self.setCameraButtonSelection()

        # Show setting parameters in console and create xml file
        MayaCacheCmdSettings.printValues(self.simulationSettings)
        self.createProjectSettingsFile(simulationNameAbsolut)

        # --------------------------------------------------------------------------------------------------------------
        # Generate a set of N cache commands and a set of N random samples
        # --------------------------------------------------------------------------------------------------------------
        currentSpans = self.tabParamtersObj.getSelectedValuesFromSlider()    # Current spans stores the min and max slider vqalues. e.g.: currentSpans.velocitySwirl_Span
        print currentSpans

        randomSamplesList = list()
        cacheCmdList = list()
        for iIndex in range(0, self.simulationSettings.numberSamples):

            # Create random samples
            fluidValueSampler = FluidValueSampler(currentSpans)
            fluidValueSampler.setSldierRangeValues()
            randomSamples = fluidValueSampler.getSampleSet()
            randomSamplesList.append(randomSamples)
            del fluidValueSampler
            del randomSamples

            # Create commands
            cacheName = self.simulationSettings.fluidBoxName + "_" + str(iIndex)
            cacheCmd = MayaCacheCmdString()
            pathOut = self.simulationSettings.outputPath + "/" + str(iIndex)
            cacheCmd.setRenderSettingsFromMaya(self.simulationSettings.animationStartTime, self.simulationSettings.animationEndTime, pathOut, cacheName)
            cmdStr = cacheCmd.getCacheCommandString()
            cacheCmdList.append(cmdStr)
            del cacheCmd

        self.simulationSettings.createCacheCommandString = cacheCmdList
        self.simulationSettings.randomSliderSamples = randomSamplesList

        """
        # Print cache command and random values
        print "\n"
        for iIndex in range(0, self.simulationSettings.numberSamples):
            print("[ Index: ", iIndex, " ]")
            print("   Command: ", self.simulationSettings.createCacheCommandString[iIndex])
            print("   velociySwirl: ", self.simulationSettings.randomSliderSamples[iIndex].velocitySwirl)
            print "\n"
        print "\n"
        """

        # --------------------------------------------------------------------------------------------------------------
        # Create the cache and render the images
        # --------------------------------------------------------------------------------------------------------------
        self.mayaCallObject = MayaFunctionUtils()

        self.progressSteps = (self.getNumberOfActiveCameras() + 1) * self.simulationSettings.numberSamples
        progress = QtGui.QProgressDialog("", None, 0, self.progressSteps, self)
        progressWasCanceled = False
        progress.setWindowTitle("Please wait ...")
        #progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setMaximum(int(self.progressSteps))
        progress.show()


        import itertools
        renderedImage = list()
        index = 0
        fluidIndex = 0
        progressIndex = 0
        for lCmd, lSamples in itertools.izip(self.simulationSettings.createCacheCommandString, self.simulationSettings.randomSliderSamples):
            """
            :type lSamples : MayaCacheCmd
            """
            progressBarText = "<b>Simulation " + str(fluidIndex) + " / " + str(self.simulationSettings.numberSamples) + " created.<b>"
            progress.setLabelText(progressBarText)

            # 1. Set the values
            self.mayaCallObject.setSampledValue(self.simulationSettings.fluidBoxName, lSamples)

            # 2. Call maya cache function
            self.mayaCallObject.createFluid(lCmd, None)
            progressIndex += 1
            progress.setValue(progressIndex)

            # 3. Create the images ...
            if self.simulationSettings.imageView:
                self.mayaCallObject.changeToPerspCam()
                self.mayaCallObject.viewFromCamPosition('PERSPECTIVE', self.simulationSettings.fluidBoxName)
            if self.simulationSettings.imageView:
                [progressIndexUpdated, renderedImageSubList] = self.mayaCallObject.renderImagesFromCameras(self.simulationSettings, fluidIndex, progress, progressIndex)
                progressIndex = progressIndexUpdated
                renderedImage.append(renderedImageSubList)

            progressBarText = "<b>Simulation " + str(fluidIndex+1) + " / " + str(self.simulationSettings.numberSamples) + " created.<b>"
            progress.setLabelText(progressBarText)

            fluidIndex += 1
            if progress.wasCanceled():
                progressWasCanceled = True
                break

        if self.simulationSettings.imageView:
            self.mayaCallObject.changeToPerspCam()
            self.mayaCallObject.viewFromCamPosition('PERSPECTIVE', self.simulationSettings.fluidBoxName)

        self.mayaCallObject = None
        progress.close()
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # Create GIF images
        # --------------------------------------------------------------------------------------------------------------
        if self.simulationSettings.imageView:
            progress = QtGui.QProgressDialog("", None, 0, self.progressSteps, self)
            progress.setWindowTitle("Please wait ...")
            progress.setMinimumDuration(0)
            progress.setMaximum(len(renderedImage))
            progress.setLabelText("<b>Creating GIF animations ...</b>")
            progress.show()
            progressIndex = 0
            for idx, val in enumerate(renderedImage):
                #print(idx, val)
                tmpList = val
                for val in tmpList:
                    progressIndex += 1
                    progress.setValue(progressIndex)

                    # val stores the path to the rendered images
                    directoryImagesDir = val
                    outputGifFileDir = val
                    outputGifFileName = 'animation.gif'
                    self.gifImageCreator = GifCreator()
                    start_time = self.simulationSettings.animationStartTime
                    isFFmpegExecutable = self.gifImageCreator.createGifFromImages(self.ffmpegpath, directoryImagesDir, outputGifFileDir, outputGifFileName, start_time, fps=25, gifOptimization=25)
            progress.close()
        # --------------------------------------------------------------------------------------------------------------

        self.msgBox = QtGui.QMessageBox(self)
        self.msgBox.setStyleSheet(self.DIALOG_STYLE_SHEET)
        self.msgBox.setWindowTitle("Information")
        text = "Simulations successfully created. " + "\n\nProject Path: " + self.simulationSettings.outputPath + ""
        self.msgBox.setText(text)
        self.msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        self.msgBox.setIcon(QtGui.QMessageBox.Information)
        self.msgBox.exec_()

        #cmds.file(save=True)
        self.close()

    @QtCore.Slot()
    def lineEdit_numberSeq_EditFinished(self):
        print self.ui.lineEdit_numberSeq.text()
        if not self.ui.lineEdit_numberSeq.text():
            self.ui.lineEdit_numberSeq.setText(str(DefaultUIParameters.DEF_NUMBER_SEQUENCES))

    @QtCore.Slot()
    def sliderNumberSequences_Event(self):
        print self.ui.horizontalSlider_numberSeq.value()
        #todo
        tmp = str(self.ui.horizontalSlider_numberSeq.value())
        self.ui.lineEdit_numberSeq.setText(tmp)

        self.setTime()

    @QtCore.Slot()
    def lineEdit_numberSeq_Event(self):
        numberSeq = self.ui.lineEdit_numberSeq.text()
        try:
            val = int(numberSeq)
            if int(numberSeq) < DefaultUIParameters.DEF_NUMBER_SEQUENCES_MIN :
                self.ui.lineEdit_numberSeq.setText(str(DefaultUIParameters.DEF_NUMBER_SEQUENCES_MIN))
                self.ui.horizontalSlider_numberSeq.setValue(DefaultUIParameters.DEF_NUMBER_SEQUENCES_MIN)
                self.ui.horizontalSlider_numberSeq.update()
            elif int(numberSeq) > DefaultUIParameters.DEF_NUMBER_SEQUENCES_MAX:
                self.ui.lineEdit_numberSeq.setText(str(DefaultUIParameters.DEF_NUMBER_SEQUENCES_MAX))
                self.ui.horizontalSlider_numberSeq.setValue(DefaultUIParameters.DEF_NUMBER_SEQUENCES_MAX)
                self.ui.horizontalSlider_numberSeq.update()
            else:
                self.ui.horizontalSlider_numberSeq.setValue(val)

        except ValueError:
            if numberSeq == "":
                pass
            else:
                self.ui.lineEdit_numberSeq.setText(str(DefaultUIParameters.DEF_NUMBER_SEQUENCES))

    @QtCore.Slot()
    def pushButtonCamPV_Event(self):
        flag = self.CLICK_FLAG_CAM_PV
        if not flag:
            self.ui.pushButton_CamPV.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
            self.CLICK_FLAG_CAM_PV = True
        elif flag:
            self.ui.pushButton_CamPV.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
            self.CLICK_FLAG_CAM_PV = False

        self.setTime()

    @QtCore.Slot()
    def pushButtonCamVC_Event(self):
        flag = self.CLICK_FLAG_CAM_VC
        if not flag:
            self.ui.pushButton_CamVC.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
            self.CLICK_FLAG_CAM_VC = True
        elif flag:
            self.ui.pushButton_CamVC.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
            self.CLICK_FLAG_CAM_VC = False

        self.setTime()

    @QtCore.Slot()
    def pushButtonCamSPH_Event(self):
        flag = self.CLICK_FLAG_CAM_SPH
        if not flag:
            chooseCameraDialog = ChooseCameraDialog(self)
            chooseCameraDialog.exec_()
            choosenCam = chooseCameraDialog.getChoosenCamera
            if choosenCam:
                self.ui.label_selectedCam.setText('[ ' + choosenCam + ' ]')
                self.choosenCamera = choosenCam
                self.ui.pushButton_CamSPH.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
                self.CLICK_FLAG_CAM_SPH = True
            else:
                pass

        elif flag:
            self.ui.pushButton_CamSPH.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
            self.ui.label_selectedCam.setText(' ')
            self.choosenCamera = None
            self.CLICK_FLAG_CAM_SPH = False

        self.setTime()

    @QtCore.Slot()
    def pushButtonROT_Event(self):
        flag = self.CLICK_FLAG_CAM_ROT
        if not flag:
            self.ui.pushButton_ROT.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
            self.CLICK_FLAG_CAM_ROT = True
            self.ui.spinBox_rotDeg.setEnabled(True)
            self.ui.label.setEnabled(True)
        elif flag:
            self.ui.pushButton_ROT.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
            self.CLICK_FLAG_CAM_ROT = False
            self.ui.spinBox_rotDeg.setEnabled(False)
            self.ui.label.setEnabled(False)

        self.setTime()

    @QtCore.Slot()
    def spinBoxRot_Event(self):
        value = int(self.ui.spinBox_rotDeg.text())

        if value < DefaultUIParameters.DEF_SPIN_ROT_MIN:
            self.ui.spinBox_rotDeg.setValue(int(DefaultUIParameters.DEF_SPIN_ROT_MIN))
        if value > DefaultUIParameters.DEF_SPIN_ROT_MAX:
            self.ui.spinBox_rotDeg.setValue(int(DefaultUIParameters.DEF_SPIN_ROT_MAX))

        self.setTime()

    def initCamButtons(self):
        self.ui.pushButton_CamPV.setIcon(QtGui.QIcon(self.tr(":/img_1.png")))
        self.ui.pushButton_CamPV.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
        self.ui.pushButton_CamVC.setIcon(QtGui.QIcon(self.tr(":/img_2.png")))
        self.ui.pushButton_CamVC.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
        self.ui.pushButton_CamSPH.setIcon(QtGui.QIcon(self.tr(":/img_3.png")))
        self.ui.pushButton_CamSPH.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
        self.ui.pushButton_ROT.setIcon(QtGui.QIcon(self.tr(":/img_5.png")))
        self.ui.pushButton_ROT.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
        self.ui.pushButton_CamPV.clicked.connect(self.pushButtonCamPV_Event)
        self.ui.pushButton_CamVC.clicked.connect(self.pushButtonCamVC_Event)
        self.ui.pushButton_CamSPH.clicked.connect(self.pushButtonCamSPH_Event)
        self.ui.pushButton_ROT.clicked.connect(self.pushButtonROT_Event)

    def initSliderValues(self):
        self.ui.horizontalSlider_numberSeq.setMinimum(DefaultUIParameters.DEF_NUMBER_SEQUENCES_MIN)
        self.ui.horizontalSlider_numberSeq.setMaximum(DefaultUIParameters.DEF_NUMBER_SEQUENCES_MAX)
        self.ui.horizontalSlider_numberSeq.setValue(DefaultUIParameters.DEF_NUMBER_SEQUENCES)

    def checkProjectPathOk(self, pathName, projName):
        if projName == "":
            msgBox = QtGui.QMessageBox(self)
            msgBox.setStyleSheet(self.DIALOG_STYLE_SHEET)
            msgBox.setText("Cannot create project! Please enter a project name.")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.exec_()
            self.ui.lineEdit_SimulationName.setFocus()
            return [False, '']

        if pathName == "":
            msgBox = QtGui.QMessageBox(self)
            msgBox.setStyleSheet(self.DIALOG_STYLE_SHEET)
            msgBox.setText("Cannot create project folder! Please enter a project path.")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.exec_()
            self.ui.lineEdit_ProjPath.setFocus()
            return [False, '']

        if not re.match("^[a-zA-Z0-9_]*$", projName):
            msgBox = QtGui.QMessageBox(self)
            msgBox.setStyleSheet(self.DIALOG_STYLE_SHEET)
            msgBox.setText("Cannot create project! A file name cannot contain special characters.\n"
                           "Valid characters: numbers, letters, - and _ ")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            self.ui.lineEdit_SimulationName.setFocus()
            self.ui.lineEdit_SimulationName.setText("")
            msgBox.exec_()
            return [False, '']

        pathName = os.path.abspath(pathName)
        if not pathName.endswith('/'):
            pathName += '/'
        if not pathName.endswith('\\'):
            pathName += '/'

        dirExists = FluidExplorerUtils.FluidExplorerUtils.dirExists(pathName)
        if (dirExists):
            pathPrjAbsolut = os.path.abspath(pathName)
        else:
            try:
                os.mkdir(pathName)
                pathPrjAbsolut = os.path.abspath(pathName)
            except OSError as exc:
                errorText = ""
                if exc.errno == errno.EACCES:
                    print "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    er = "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    self.ui.lineEdit_ProjPath.setText("")
                    self.ui.lineEdit_ProjPath.setFocus()
                elif exc.errno == 22:
                    print "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    er = "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    self.ui.lineEdit_ProjPath.setText("")
                    self.ui.lineEdit_ProjPath.setFocus()
                else:
                    print "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    er = "Error {0}: {1}" .format(exc.errno, exc.strerror)

                msgBox = QtGui.QMessageBox(self)
                msgBox.setStyleSheet(self.DIALOG_STYLE_SHEET)
                msgBox.setText("Cannot create project folder! Details: " + errorText)
                msgBox.setWindowTitle("Warning - Create Simulation")
                msgBox.setIcon(QtGui.QMessageBox.Warning)

                self.ui.lineEdit_ProjPath.setFocus()
                self.ui.lineEdit_ProjPath.setText(self.workDirPath)
                msgBox.exec_()

                return [False, '']

        projPathFull = pathName + projName
        dirExists = FluidExplorerUtils.FluidExplorerUtils.dirExists(projPathFull)
        simulationNameAbsolut = os.path.abspath(projPathFull)

        if dirExists:
            msgBox = QtGui.QMessageBox(self)
            msgBox.setStyleSheet(self.DIALOG_STYLE_SHEET)
            msgBox.setText("Project already exists! Please change the project name.")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            self.ui.lineEdit_SimulationName.setFocus()
            self.ui.lineEdit_SimulationName.setText("")
            msgBox.exec_()
            simulationNameAbsolut = os.path.abspath(projPathFull)

            return [False, '']

        else:
            try:
                os.mkdir(simulationNameAbsolut)
            except OSError as exc:
                errorText = ""

                if exc.errno == errno.EACCES:
                    print "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    errorText = "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    self.ui.lineEdit_ProjPath.setText("")
                    self.ui.lineEdit_ProjPath.setFocus()

                elif exc.errno == 22:
                    print "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    errorText = "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    self.ui.lineEdit_ProjPath.setText("")
                    self.ui.lineEdit_ProjPath.setFocus()
                else:
                    print "Error {0}: {1}" .format(exc.errno, exc.strerror)
                    errorText = "Error {0}: {1}" .format(exc.errno, exc.strerror)

                msgBox = QtGui.QMessageBox(self)
                msgBox.setStyleSheet(self.DIALOG_STYLE_SHEET)
                msgBox.setText("Cannot create project! Details: " + errorText)
                msgBox.setWindowTitle("Warning - Create Simulation")
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                self.ui.lineEdit_ProjPath.setFocus()
                self.ui.lineEdit_ProjPath.setText(self.workDirPath)
                msgBox.exec_()

                return [False, '']

            finally:
                self.simulationSettings.outputPath = os.path.abspath( projPathFull )
                self.simulationSettings.outputPath = self.simulationSettings.outputPath.replace('\\', '/')
                index = projPathFull.rfind(projName)
                self.simulationSettings.prjName = projPathFull[index:]
                self.simulationNameAbsolut = simulationNameAbsolut

                return [True, simulationNameAbsolut]

    def setCameraButtonSelection(self):
        self.simulationSettings.cam_perspective = 0;
        self.simulationSettings.cam_viewcube = 0;
        self.simulationSettings.imageView = 0

        if self.CLICK_FLAG_CAM_PV:
            self.simulationSettings.cam_perspective = 1;
            self.simulationSettings.imageView = 1

        if self.CLICK_FLAG_CAM_VC:
            self.simulationSettings.cam_viewcube = 1;
            self.simulationSettings.imageView = 1

        if self.CLICK_FLAG_CAM_SPH:
            self.simulationSettings.cam_sphere = self.CLICK_FLAG_CAM_SPH
            self.simulationSettings.cam_custom_name = self.choosenCamera
            self.simulationSettings.imageView = 1
        else:
            self.simulationSettings.cam_sphere = False
            self.simulationSettings.cam_custom_name = None

        if self.CLICK_FLAG_CAM_ROT:
            self.simulationSettings.cam_rotation = self.ui.spinBox_rotDeg.text()
            self.simulationSettings.imageView = 1
        else:
            self.simulationSettings.cam_rotation = 0

    def createProjectSettingsFile(self, simulationNameAbsolut):
        xmlSettingsWriter = XmlFileWriter()
        pathConfigFile = simulationNameAbsolut + "/" + str(self.simulationSettings.prjName) + ".fxp"
        xmlSettingsWriter.setXmlDocPath(pathConfigFile, "GlobalSettings")
        xmlSettingsWriter.writeSettingToXmlFile(self.simulationSettings)

    def calculateTimeClicked(self):
        # Delete / create output folder
        filePathMain = os.path.dirname(os.path.abspath(__file__))
        fxPathRel = os.path.dirname(os.path.abspath(filePathMain))
        outputFolder = fxPathRel + '/Output/'
        outputFolderAbs = os.path.abspath(outputFolder)
        if os.path.exists(outputFolderAbs):
            # Delete content
            filelist = [ f for f in os.listdir(outputFolderAbs) if f.endswith((".mc", ".xml", "png", "jpg", "jpeg", "gif")) ]
            for f in filelist:
                tmpPath = outputFolder + '/' + f
                tmpPathAbs = os.path.abspath(tmpPath)
                print tmpPathAbs
                os.remove(tmpPathAbs)
        else:
            os.mkdir(outputFolderAbs)

        # Caching
        start_time_cahching = time.time()

        cacheCmd = MayaCacheCmdString()
        cacheCmd.setRenderSettingsFromMaya(int(self.simulationSettings.animationStartTime), int(self.simulationSettings.animationEndTime), outputFolderAbs, "Untitled")
        self.execCommand = MayaFunctionUtils()
        self.execCommand.createFluid(cacheCmd.getCacheCommandString(), None)

        res_time_caching = time.time() - start_time_cahching

        # Rendering
        start_time_rendering = time.time()

        self.renderer = MayaFunctionUtils()
        self.renderer.renderImages(outputFolder, "None", int(self.simulationSettings.animationStartTime), int(self.simulationSettings.animationEndTime), 640, 480)

        res_time_rendering = time.time() - start_time_rendering

        # Create GIF
        start_time_gif = time.time()

        directoryImagesDir = outputFolderAbs
        outputGifFileDir = outputFolderAbs
        outputGifFileName = 'animation.gif'
        self.gifImageCreator = GifCreator()
        start_time = self.simulationSettings.animationStartTime
        isFFmpegExecutable = self.gifImageCreator.createGifFromImages(self.ffmpegpath, directoryImagesDir, outputGifFileDir, outputGifFileName, start_time, fps=25, gifOptimization=25)

        res_time_gif = time.time() - start_time_gif

        # Store results
        self.time_Caching = res_time_caching
        self.time_Renering = res_time_rendering
        self.time_GIF = res_time_gif

        # SetTime
        self.isTimeCalculated = True
        self.setTime()

    def setTime(self):

        numberSamples = int(self.ui.horizontalSlider_numberSeq.value())
        numberCameras = self.getNumberOfActiveCameras()

        # Calculate time in seconds
        timeInSeconds = (self.time_Caching + (numberCameras * (self.time_Renering+self.time_GIF))) * numberSamples

        if timeInSeconds > 300:
            str = time.strftime("%H:%M", time.gmtime(timeInSeconds))
            timeStr = str + ' h.'

        else:
            str = time.strftime("%M:%S", time.gmtime(timeInSeconds))
            timeStr = str + ' min.'

        if self.isTimeCalculated:
            self.ui.labelTime_Value.setText(timeStr)

    def getNumberOfActiveCameras(self):
        cameraCount = 0

        if self.CLICK_FLAG_CAM_PV:
            cameraCount = cameraCount + 1
        if self.CLICK_FLAG_CAM_VC:
            cameraCount = cameraCount + 3
        if self.CLICK_FLAG_CAM_SPH:
            cameraCount = cameraCount + 1
        if self.CLICK_FLAG_CAM_ROT:
            deg = 0
            count = 0
            step = int(self.ui.spinBox_rotDeg.text())

            while deg < 360:
                deg = deg + step
                count = count + 1

            cameraCount = cameraCount + count

        return cameraCount

    def getFFmpegPath(self):
        filePathMain = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.join(filePathMain, 'lib/ffmpeg/')
        fxPathRel = os.path.abspath(filename)

        return fxPathRel




