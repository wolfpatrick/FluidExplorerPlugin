from PySide import QtGui
from PySide import QtCore

from CreateProjectDialogUI import Ui_CreateProjectDialog
from DefaultUIValues import DefaultUIParameters
from FileOpenDialog import FileOpenDialog
from ChooseCameraDialog import ChooseCameraDialog
from RangeSlider.HRangeSlider import QHRangeSlider
from ParameterInputBoxes import ParameterInputBoxes
from MayaCacheCmdSettings import MayaCacheCmdSettings
from Utils import FluidExplorerUtils
from MayaUiDefaultValues import MayaUiDefaultValues
from Utils.MayaCmds.ParameterSpace import MayaCacheCmd
from MayaCacheCommandParameters import MayaCacheCommand
from Utils.MayaCmds.MayaCacheCmd import MayaCacheCmdString
from Utils.MayaCmds.MayaFunctions import MayaFunctionUtils
from ParamterTab import ParameterTab
from Utils.RangeSliderSpan import FluidValueSampler
#from icons import icons
import itertools

import errno
import ConfigParser

import os
import re
import platform

import pysideuic

class CreateProjectDialog(QtGui.QDialog):

    CLICK_FLAG_CAM_PV = True
    CLICK_FLAG_CAM_VC = True
    CLICK_FLAG_CAM_SPH = False
    CLICK_FLAG_CAM_ROT = False
    choosenCamera = None

    def __init__(self, args, fluidName):
        QtGui.QDialog.__init__(self, args)
        self.fluidName = fluidName

        # Set up the user interface from Designer
        self.ui = Ui_CreateProjectDialog()
        self.ui.setupUi(self)
        self.createConnections()

        self.tabParametersfirstOpend = True
        self.setFluidName(fluidName)
        self.centre()

        self.tabParamterslasObj = None
        self.tabParamters = None

        self.simulationSettings = MayaCacheCmdSettings()
        self.setUpComponents()

    def centre(self):
        # Get the current screens' dimensions...
        screen = QtGui.QDesktopWidget().screenGeometry()
        # ... and get this windows' dimensions
        mysize = self.geometry()
        # The horizontal position is calulated as screenwidth - windowwidth /2
        hpos = ( screen.width() - mysize.width() ) / 2

        # And vertical position the same, but with the height dimensions
        vpos = ( screen.height() - mysize.height() ) / 2
        # And the move call repositions the window
        self.move(hpos + mysize.width(), vpos)

    def setFluidName(self, name):
        self.fluidName = name

    def setUpComponents(self):
        self.setAnimationStartEndTime()

        icon_open = QtGui.QIcon(QtGui.QPixmap(':/icon_help_30px.png'))
        self.ui.pushButtonNewPrjHelp.setIcon(icon_open)
        self.ui.lineEdit_SimulationName.setText(DefaultUIParameters.DEF_SIMULATION_NAME)

        workDir = os.getcwd() + "/" + "Output" + "/"
        workDir = "E:/TMP"
        if (platform.system() == "Windows"):
            self.workDir = workDir.replace("/","\\")
            #self.workDir = self.workDir + "output"
        self.ui.lineEdit_ProjPath.setText(self.workDir)

        self.ui.label.setEnabled(False)
        self.ui.spinBox_rotDeg.setEnabled(False)
        self.ui.spinBox_rotDeg.setValue(DefaultUIParameters.DEF_SPIN_ROT)
        self.ui.spinBox_rotDeg.setMinimum(DefaultUIParameters.DEF_SPIN_ROT_MIN)
        self.ui.spinBox_rotDeg.setMaximum(DefaultUIParameters.DEF_SPIN_ROT_MAX)
        self.initCamButtons()

        self.initSliderValues()
        self.addParamterTab()
        
    def addParamterTab(self):
        self.tabParamterslasObj = ParameterTab()
        self.tabParamters = self.tabParamterslasObj.getTab()
        self.ui.tabWidget.addTab(self.tabParamters, "Paramaters")

    def createConnections(self):
        self.ui.pushButtonNewPrjHelp.clicked.connect(self.buttonHelpCreateProj_Event)
        self.ui.pushButtonBrowse.clicked.connect(self.buttonBrowse_Event)
        self.ui.pushButtonCreateSimulation.clicked.connect(self.buttonCreateSimulation_Event)
        self.ui.horizontalSlider_numberSeq.valueChanged[int].connect(self.sliderNumberSequences_Event)
        self.ui.lineEdit_numberSeq.textChanged.connect(self.lineEdit_numberSeq_Event)
        self.ui.lineEdit_numberSeq.editingFinished.connect(self.lineEdit_numberSeq_EditFinished)
        self.ui.spinBox_rotDeg.valueChanged.connect(self.spinBoxRot_Event)

    def setAnimationStartEndTime(self):
        uiStatus = MayaUiDefaultValues()
        uiStatus.getAnimationStartEnd()
        begin = uiStatus._animationMinTime
        end = uiStatus._animationEndTime

        txt = str(begin) + " / " + str(end)
        self.ui.labelAnimationTimeStartEnd.setText(txt)
        self.simulationSettings.animationStartTime = begin
        self.simulationSettings.animationEndTime = end

    @QtCore.Slot()
    def buttonHelpCreateProj_Event(self):
        print "[ Button clicked: " + "Help" + " ]"

    @QtCore.Slot()
    def buttonBrowse_Event(self):
        fileDialog = FileOpenDialog(self)
        choosenDir = fileDialog.openDirDialogQuick()

        if not choosenDir == "":
            choosenDir = choosenDir + "/"
            if (platform.system() == "Windows"):
                choosenDirNew = choosenDir.replace("/","\\")
                self.ui.lineEdit_ProjPath.setText(choosenDirNew)

    @QtCore.Slot()
    def buttonCreateSimulation_Event(self):

        pathName = self.ui.lineEdit_ProjPath.text()
        projName = self.ui.lineEdit_SimulationName.text()

        pathOk = False
        [pathOk, simulationNameAbsolut] = self.checkProjectPathOk(pathName, projName)
        if not pathOk:
            return
        else:

            # Ckeck if the scene is saved
            """
            import maya.cmds as cmds
            try:
                tmpMayaFilePath = self.simulationSettings.outputPath + "/fluid_simulation_scene.mb"
                cmds.file( rename = tmpMayaFilePath )
                dialogRes = cmds.file(save=True)
                print dialogRes
            except:
                print "!!!ERROR!!!!"
                os.rmdir(self.simulationSettings.outputPath)
                return
            """

        # Get some information about the current scene
        self.simulationSettings.fluidBoxName = self.fluidName
        self.simulationSettings.numberSamples = self.ui.horizontalSlider_numberSeq.value()
        self.simulationSettings.cam_perspective = self.CLICK_FLAG_CAM_PV
        self.simulationSettings.cam_viewcube = self.CLICK_FLAG_CAM_VC
        self.setCameraButtonSelection()

        MayaCacheCmdSettings.printValues(self.simulationSettings)

        # --------------------------------------------------------------------------------------------------------------
        # Generate a set of N cache commands and a set of N random samples
        currentSpans = self.tabParamterslasObj.getSelectedValuesFromSlider()
        currentSpans
        randomSamplesList = list()
        cacheCmdList = list()

        for iIndex in range(0, self.simulationSettings.numberSamples):

            # Create samples
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
            #cacheCmd.setRenderSettingsFromMaya(self.simulationSettings.animationStartTime, self.simulationSettings.animationEndTime, pathOut, cacheName)
            #cmdStr = cacheCmd.getCacheCommandString()
            cmdStr = "TEST"
            cacheCmdList.append(cmdStr)
            del cacheCmd

        self.simulationSettings.createCacheCommandString = cacheCmdList
        self.simulationSettings.randomSliderSamples = randomSamplesList
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        mayaCallObject = MayaFunctionUtils()

        # Progress bar
        progressWasCanceled = False
        limit = 0
        progress = QtGui.QProgressDialog("Creating Fluids", None, 0, limit, self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.show()

        simulationIndex = 0
        import itertools
        for lCmd, lSamples in itertools.izip(self.simulationSettings.createCacheCommandString, self.simulationSettings.randomSliderSamples):
            # Progressbar
            progressBarText = "Creating Simulation" + " " + str(simulationIndex+1) + " " + "from" + " " + str(self.simulationSettings.numberSamples)
            progress.setLabelText(progressBarText)

            # Set the values, start the caching and create all images
            mayaCallObject.setSampledValue(self.simulationSettings.fluidBoxName, lSamples)
            mayaCallObject.createFluid(lCmd, progress)
            progress.setLabelText(progressBarText)
            mayaCallObject.renderImagesFromCameras(self.simulationSettings, simulationIndex, progress)

            simulationIndex += 1

        del mayaCallObject
        # --------------------------------------------------------------------------------------------------------------

        # Select maya default camera
        mayaCallObject.startPosition(self.simulationSettings)

        # Create configuration file
        pathConfigFile = simulationNameAbsolut + "/" + str(self.simulationSettings.prjName) + ".fxp"
        FluidExplorerUtils.FluidExplorerUtils.createConfigurationFile(self.simulationSettings, pathConfigFile)

        return






        # Sampling
        LSamples = list()
        LCmds = list()

        for iIndex in range(0, self.simulationSettings.numberSamples):

            # Paramters
            print "index: " + str(iIndex)

            e = MayaCacheCommand()
            #e.velocitySwirlFLAG = True
            sampler = MayaCacheCmd()
            sampler.sampleParameters(sliderValues, self.simulationSettings.fluidBoxName)
            sampleSet = sampler.getSampledValue(self.simulationSettings.fluidBoxName)
            LSamples.append(sampleSet)
            del sampler

            # CommandString
            cacheName = self.simulationSettings.fluidBoxName + "_" + str(iIndex)
            cacheCmd = MayaCacheCmdString()
            pathOut = self.simulationSettings.outputPath + "/" + str(iIndex)
            cacheCmd.setRenderSettingsFromMaya(self.simulationSettings.animationStartTime,
                                               self.simulationSettings.animationEndTime, pathOut,
                                               cacheName)

            cmdStr = cacheCmd.getCacheCommandString()
            LCmds.append(cmdStr)
            del cacheCmd

        self.simulationSettings.createCacheCommandString = LCmds
        self.simulationSettings.randomSliderSamples = LSamples

        # ----
        # Save to txt
        #from Utils.ConsoleUtils.ConsoleUtils import ConsoleUtils
        from ConsoleUtils import ConsoleUtils
        import pickle


        consoleObj = ConsoleUtils()
        consoleObj.createStructure(self.simulationSettings, self.simulationSettings.createCacheCommandString, self.simulationSettings.randomSliderSamples)

        #with open('E:/TMP/company_data.pkl', 'wb') as output:
            #pickle.dump(consoleObj, output, pickle.HIGHEST_PROTOCOL)

        # ----



        print "LEN: " + str(len(self.simulationSettings.randomSliderSamples))

        self.mayaCallObject = MayaFunctionUtils()
        #self.mayaCallObject.startMayaCaching(self.simulationSettings)


        # ----------------------

        cmdList = self.simulationSettings.createCacheCommandString
        samplesList = self.simulationSettings.randomSliderSamples

        # Progress bar
        progressWasCanceled = False

        limit = len(cmdList)
        progress = QtGui.QProgressDialog("Creating Fluids", None, 0, limit, self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.show()

        #consoleOb = ConsoleUtils()
        #consoleOb.createStructure(self.simulationSettings, self.cmdList)

        import itertools
        index = 0
        fluidIndex = 0
        progressIndex = 0
        for lCmd, lSamples in itertools.izip(cmdList, samplesList):

            """
            :type lSamples : MayaCacheCmd
            """
            if fluidIndex == 0:
                progress.setValue(0.5)
            else:
                progress.setValue(fluidIndex)



            # 1. Set the values
            self.mayaCallObject.setSampledValue(self.simulationSettings.fluidBoxName, lSamples)

            # 2. Call maya cache function
            self.mayaCallObject.createFluid(lCmd)

            # 3. Create the images ...
            # TODO

            self.mayaCallObject.renderImagesFromCameras(self.simulationSettings, fluidIndex)

            fluidIndex += 1
            #self.mayaCallObject.changeToPerspCam()
            #self.mayaCallObject.viewFromCamPosition('PERSPECTIVE', self.simulationSettings.fluidBoxName)

            # Update progress bar
            #progressIndex = progressIndex + 1
            #progress.setValue(progressIndex)
            index = index + 1
            print "Simulation " + str(index) + " created."
            if progress.wasCanceled():
                progressWasCanceled = True
                break
            progress.deleteLater()

        # ----------------------
        self.mayaCallObject.startPosition(self.simulationSettings)


        """
        config = ConfigParser.RawConfigParser()
        config.add_section('default_settings')
        config.set('default_settings', 'SimulationName', str(generalParams.outputPath))
        config.set('default_settings', 'NumberSamples',  None)

        tmp = simulationNameAbsolut + "/" + str(generalParams.prjName) + ".ini"
        with open(tmp, 'w') as configfile:
            config.write(configfile)
        """

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

        v1 = self.ui.horizontalSlider_numberSeq.value()
        timeValue = "Time: " + str(v1) + " h"
        self.ui.labelTime.setText(timeValue)

        timeValue = "Storage Consumtion: " + "100" + " GB"
        self.ui.labelDiskSpace.setText(timeValue)

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
                print "dsdsds"
                pass
            else:
                self.ui.lineEdit_numberSeq.setText(str(DefaultUIParameters.DEF_NUMBER_SEQUENCES))

    @QtCore.Slot()
    def pushButtonCamPV_Event(self):
        #print "1 clicked"
        flag = self.CLICK_FLAG_CAM_PV
        if not flag:
            self.ui.pushButton_CamPV.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
            self.CLICK_FLAG_CAM_PV = True
        elif flag:
            self.ui.pushButton_CamPV.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
            self.CLICK_FLAG_CAM_PV = False

    @QtCore.Slot()
    def pushButtonCamVC_Event(self):

        #print "2 clicked"
        flag = self.CLICK_FLAG_CAM_VC
        if not flag:
            self.ui.pushButton_CamVC.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
            self.CLICK_FLAG_CAM_VC = True
        elif flag:
            self.ui.pushButton_CamVC.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
            self.CLICK_FLAG_CAM_VC = False

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

    @QtCore.Slot()
    def pushButtonROT_Event(self):
        #print "4 clicked"
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

    @QtCore.Slot()
    def spinBoxRot_Event(self):
        value = int(self.ui.spinBox_rotDeg.text())

        if value < DefaultUIParameters.DEF_SPIN_ROT_MIN:
            self.ui.spinBox_rotDeg.setValue(int(DefaultUIParameters.DEF_SPIN_ROT_MIN))
        if value > DefaultUIParameters.DEF_SPIN_ROT_MAX:
            self.ui.spinBox_rotDeg.setValue(int(DefaultUIParameters.DEF_SPIN_ROT_MAX))

    def initCamButtons(self):
        self.ui.pushButton_CamPV.setIcon(QtGui.QIcon(self.tr(":/img_1.png")))
        self.ui.pushButton_CamPV.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
        self.ui.pushButton_CamVC.setIcon(QtGui.QIcon(self.tr(":/img_2.png")))
        self.ui.pushButton_CamVC.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
        self.ui.pushButton_CamSPH.setIcon(QtGui.QIcon(self.tr(":/img_3.png")))
        self.ui.pushButton_CamSPH.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
        self.ui.pushButton_ROT.setIcon(QtGui.QIcon(self.tr(":/img_4.png")))
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
            msgBox.setText("Cannot create project! Please enter a project name.")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.exec_()
            self.ui.lineEdit_SimulationName.setFocus()
            return [False, '']

        if pathName == "":
            msgBox = QtGui.QMessageBox(self)
            msgBox.setText("Cannot create project folder! Please enter a project path.")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.exec_()
            self.ui.lineEdit_ProjPath.setFocus()
            return [False, '']

        if not re.match("^[a-zA-Z0-9_]*$", projName):
            msgBox = QtGui.QMessageBox(self)
            msgBox.setText("Cannot create project! A file name cannot contain special characters!\n"
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
            print "WARNING: Directory already exists!"
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
                msgBox.setText("Cannot create project folder! " + errorText)
                msgBox.setWindowTitle("Warning - Create Simulation")
                msgBox.setIcon(QtGui.QMessageBox.Warning)

                self.ui.lineEdit_ProjPath.setFocus()
                self.ui.lineEdit_ProjPath.setText(self.workDir)
                msgBox.exec_()

                return [False, '']

        projPathFull = pathName + projName
        dirExists = FluidExplorerUtils.FluidExplorerUtils.dirExists(projPathFull)
        simulationNameAbsolut = os.path.abspath(projPathFull)

        if dirExists:
            print "WARNING: Folder for project already exists!"
            msgBox = QtGui.QMessageBox(self)
            msgBox.setText("Project already exists!\n"
                           "Please change the project name")
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
                msgBox.setText("Cannot create project! " + errorText)
                msgBox.setWindowTitle("Warning - Create Simulation")
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                self.ui.lineEdit_ProjPath.setFocus()
                self.ui.lineEdit_ProjPath.setText(self.workDir)
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
        if self.CLICK_FLAG_CAM_SPH:
            self.simulationSettings.cam_sphere = self.CLICK_FLAG_CAM_SPH
            self.simulationSettings.cam_custom_name = self.choosenCamera
        else:
            self.simulationSettings.cam_sphere = False
            self.simulationSettings.cam_custom_name = None
        if self.CLICK_FLAG_CAM_ROT:
            self.simulationSettings.cam_rotation = self.ui.spinBox_rotDeg.text()
        else:
            self.simulationSettings.cam_rotation = 0