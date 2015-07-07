__author__ = 'Patrick'

########################################################
#
# Dialog to create a new simulation
#
########################################################

from PySide import QtGui
from PySide import QtCore

from CreateProjectDialogUI import Ui_CreateProjectDialog
from DefaultUIValues import DefaultUIParameters
from FileOpenDialog import FileOpenDialog
from RangeSlider.HRangeSlider import QHRangeSlider
from ParameterInputBoxes import ParameterInputBoxes
from MayaCacheCmdSettings import MayaCacheCmdSettings
from Utils import FluidExplorerUtils
from MayaUiDefaultValues import MayaUiDefaultValues
import os
import re
import platform

import pysideuic

class CreateProjectDialog(QtGui.QDialog):

    CLICK_FLAG_CAM_PV = True
    CLICK_FLAG_CAM_VC = True
    CLICK_FLAG_CAM_SPH = False
    CLICK_FLAG_CAM_ROT = False
    test = ""

    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)

        # Set up the user interface from Designer
        self.ui = Ui_CreateProjectDialog()
        self.ui.setupUi(self)

        # Apply designs and default values
        self.setUpComponents()

        # Create connections
        self.createConnections()

        #inputBoxes = ParameterInputBoxes()
        #self.createTabValues()
        self.tabParametersfirstOpend = True




    def setUpComponents(self):
        print "dasdasdsadsad"
        self.createTabValues2()
        self.ui.pushButtonNewPrjHelp.setIcon(QtGui.QIcon(self.tr("ui/icons/icon_help_30px.png")))
        self.ui.lineEdit_SimulationName.setText(DefaultUIParameters.DEF_SIMULATION_NAME)
        self.initCamButtons()

        workDir = os.getcwd() + "/" + "Output" + "/"
        if (platform.system() == "Windows"):
            self.workDir = workDir.replace("/","\\")
            #self.workDir = self.workDir + "output"
        self.ui.lineEdit_ProjPath.setText(self.workDir)

        self.initSliderValues()
        self.ui.label.setEnabled(False)
        self.ui.spinBox_rotDeg.setEnabled(False)
        self.ui.spinBox_rotDeg.setValue(DefaultUIParameters.DEF_SPIN_ROT)
        self.ui.spinBox_rotDeg.setMinimum(DefaultUIParameters.DEF_SPIN_ROT_MIN)
        self.ui.spinBox_rotDeg.setMaximum(DefaultUIParameters.DEF_SPIN_ROT_MAX)
        #self.ui.spinBox_rotDeg.setSingleStep(5)

        self.ui.tabWidget.setCurrentIndex(0)


        # Create own tab in tabWidget
        #self.createTabValues2()






        self.calculateTimeSpave()
        """
        # RangeSlider
        a = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        b = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        """
        #hslider1 = QHRangeSlider(range = [-5.0, 5.0], values = [-5, -4])
        #hslider1.setValues([-5, 5])

        #hslider1.setEmitWhileMoving(True)
        #hslider1.show()
        #self.ui.verticalLayout1.addWidget(hslider1)

        #hslider2 = QHRangeSlider(range = [-5.0, 5.0], values = [-5, -4])
        #hslider2.setValues([-5, 5])


        #slider2.setEmitWhileMoving(False)
        #self.ui.verticalLayout2.addWidget(hslider2)


    def createConnections(self):
        self.ui.pushButtonNewPrjHelp.clicked.connect(self.buttonHelpCreateProj_Event)
        self.ui.pushButtonBrowse.clicked.connect(self.buttonBrowse_Event)
        self.ui.pushButtonCreateSimulation.clicked.connect(self.buttonCreateSimulation_Event)
        self.ui.horizontalSlider_numberSeq.valueChanged[int].connect(self.sliderNumberSequences_Event)
        self.ui.lineEdit_numberSeq.textChanged.connect(self.lineEdit_numberSeq_Event)
        self.ui.lineEdit_numberSeq.editingFinished.connect(self.lineEdit_numberSeq_EditFinished)
        self.ui.spinBox_rotDeg.valueChanged.connect(self.spinBoxRot_Event)
        #self.ui.pushButton_CamPV.clicked.connect(self.pushButtonCamPV_Event)

        #self.ui.tabWidget.connect(self.ui.tabWidget,QtCore.SIGNAL("currentChanged(int)"),self.ui.tabWidget,QtCore.SIGNAL("tabChangedSlot(int)"))
        self.ui.tabWidget.currentChanged.connect(self.onChange) #changed!


        #self.ui.tabParameters.setVisible(False)
        #self.ui.tabSampling.hide()
        #self.ui.tabWidget.removeTab(1)

    @QtCore.Slot()
    def onChange(self,i): #changed!

        if i==1 and self.tabParametersfirstOpend==True:
            print "babb"
            self.tabParametersfirstOpend = False
            self.inputBoxes.pushButtonReset_Event()
            self.tabParametersfirstOpend = False


    def createTabValues2(self):


        """
        tab3 = QtGui.QScrollArea()
        tab3.setWidget(QtGui.QWidget())
        tab3_layout = QtGui.QVBoxLayout(tab3.widget())
        tab3.setWidgetResizable(True)
        self.ui.tabWidget.addTab(tab3, "Parameters2")

        mygroupbox = QtGui.QGroupBox()
        mygroupbox = QtGui.QWidget()
        myform = QtGui.QFormLayout()
        self.ui.tabParameters.setLayout(tab3_layout)


        scroll = QtGui.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        #scroll.setFixedHeight(460)

        tab3_layout.addWidget(scroll)
        bar = scroll.verticalScrollBar()



        pushButtonReset = QtGui.QPushButton("Reset values")

        pushButtonReset2 = QtGui.QPushButton("Reset values")



        self.inputBoxes = ParameterInputBoxes()
        isSliderAktiv_Buoyancy= True
        isSliderAktiv_Dissipation=True
        isSliderAktiv_Diffusion=True
        [boxDensity, lineEdit_BUOYANY_MIN, lineEdit_BUOYANY_MAX, slider_BUOYANY, slider_Dissipation,
            lineEdit_Dissipation_MIN, lineEdit_Dissipation_MAX, slider_DIFFUSION, lineEdit_DIFFUSION_MIN,
            lineEdit_DIFFUSION_MAX] = self.inputBoxes.createBox_DENSITY(isSliderAktiv_Buoyancy, isSliderAktiv_Dissipation, isSliderAktiv_Diffusion)

        myform.addWidget(pushButtonReset)
        myform.addWidget(pushButtonReset2)
        myform.addWidget(boxDensity)
        myform.addWidget(boxDensity)
        mygroupbox.setLayout(myform)
        """


        """
        scrolllayout = QtGui.QVBoxLayout()
        scrollwidget = QtGui.QWidget()
        scrollwidget.setLayout(scrolllayout)

        scroll = QtGui.QScrollArea()
        scroll.setWidgetResizable(True)  # Set to make the inner widget resize with scroll area
        scroll.setFixedHeight(260)
        scroll.setWidget(scrollwidget)
        self.ui.tabWidget.addTab(scrollwidget, "Parameters2")
        bar = scroll.verticalScrollBar()

        #scroll.addScrollBarWidget(scrollwidget, QtCore.Qt.AlignCenter)

        self.groupboxes = []  # Keep a reference to groupboxes for later use
        for i in range(1):    # 8 groupboxes with textedit in them
            groupbox = QtGui.QGroupBox('%d' % i)
            grouplayout = QtGui.QHBoxLayout()
            grouptext = QtGui.QTextEdit()
            grouplayout.addWidget(grouptext)
            groupbox.setLayout(grouplayout)
            scrolllayout.addWidget(groupbox)
            #elf.groupboxes.append(groupbox)


        aa = QtGui.QPushButton("dsds")
        scrolllayout.addWidget(aa)

        self.inputBoxes = ParameterInputBoxes()
        isSliderAktiv_Buoyancy= True
        isSliderAktiv_Dissipation=True
        isSliderAktiv_Diffusion=True
        [boxDensity, lineEdit_BUOYANY_MIN, lineEdit_BUOYANY_MAX, slider_BUOYANY, slider_Dissipation,
            lineEdit_Dissipation_MIN, lineEdit_Dissipation_MAX, slider_DIFFUSION, lineEdit_DIFFUSION_MIN,
            lineEdit_DIFFUSION_MAX] = self.inputBoxes.createBox_DENSITY(isSliderAktiv_Buoyancy, isSliderAktiv_Dissipation, isSliderAktiv_Diffusion)
        scrolllayout.addWidget(boxDensity)


       # b = QtGui.QPushButton("dsadsad")
        #grouplayout.addWidget(b)

        self.buttonbox = QtGui.QDialogButtonBox()
        self.buttonbox.setOrientation(QtCore.Qt.Vertical)
        self.buttonbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(scroll)

        #ayout.addWidget(self.buttonbox)
        #elf.setLayout(layout)
        """
        self.inputBoxes = ParameterInputBoxes()

       # Get the current state (enabled/disabled) from the maya ui elements
        uiStatus = MayaUiDefaultValues()

        # Create Density box
        isSliderAktiv_Buoyancy = ( uiStatus._sliderDensityBuoyancy and uiStatus.isAttributeSettable("fluidShape1", "TODO") )
        isSliderAktiv_Dissipation = True
        isSliderAktiv_Diffusion = False

        [boxDensity, lineEdit_BUOYANY_MIN, lineEdit_BUOYANY_MAX, slider_BUOYANY, slider_Dissipation,
            lineEdit_Dissipation_MIN, lineEdit_Dissipation_MAX, slider_DIFFUSION, lineEdit_DIFFUSION_MIN,
            lineEdit_DIFFUSION_MAX] = self.inputBoxes.createBox_DENSITY(isSliderAktiv_Buoyancy, isSliderAktiv_Dissipation, isSliderAktiv_Diffusion)


        # Create Velocity box
        isSliderAktiv_SWIRL = True
        [ boxVelocity, slider_SWIRL, lineEdit_SWIRL_MIN, lineEdit_SWIRL_MAX ] = self.inputBoxes.createBox_VELOCITY(isSliderAktiv_SWIRL)

        # Create Box_Dynamic_sim box
        isSliderAktiv_VICOSITY = False
        [ boxDynamicsim, slider_VISCOSITY, lineEdit_VISCOSITY_MIN, lineEdit_VISCOSITY_MAX ] = self.inputBoxes.createBox_DYNAMIC_SIM(isSliderAktiv_VICOSITY)

        # Create Turbulence box
        isSliderAktiv_SPEED = False
        isSliderAktiv_FREQUENCY = True
        isSliderAktiv_STRENGTH = True
        [boxTurbulence, slider_SPEED, self.lineEdit_SPEED_MIN, lineEdit_SPEED_MAX,
                slider_FREQUENCY, lineEdit_FREQUENCY_MIN, lineEdit_FREQUENCY_MAX] = self.inputBoxes.createBox_TURBULENCE(isSliderAktiv_SPEED, isSliderAktiv_FREQUENCY, isSliderAktiv_STRENGTH)

        pushButtonReset = QtGui.QPushButton("Reset values")
        pushButtonReset.setMinimumWidth(160)
        #self.lineEdit_SPEED_MIN.setText("hallo1")
        pushButtonReset.clicked.connect(self.inputBoxes.pushButtonReset_Event)

        tab1 = QtGui.QScrollArea()

        aa = QtGui.QWidget()
        aa_layout = QtGui.QVBoxLayout()

        aa_layout.addWidget(boxDensity)
        aa_layout.addWidget(boxVelocity)
        aa_layout.addWidget(boxTurbulence)
        aa_layout.addWidget(boxDynamicsim)

        #aa_layout.addWidget(boxVelocity)
        aa#_layout.addWidget(boxVelocity, QtCore.Qt.AlignRight)
        #b.setMaximumWidth(200)

        aa_layout.addWidget(pushButtonReset)
        aa_layout.setAlignment(pushButtonReset, QtCore.Qt.AlignRight)
        aa.setLayout(aa_layout)

        tab1.setWidget(aa)
        tab1_layout = QtGui.QVBoxLayout(tab1.widget())

        tab1.setWidgetResizable(True)
        #tab1.setFixedHeight(300)
        b = QtGui.QPushButton("dsadsad")
#
        #self.inputBoxes = ParameterInputBoxes()
        #isSliderAktiv_Buoyancy= True
        #isSliderAktiv_Dissipation=True
        #isSliderAktiv_Diffusion=True
        #[boxDensity, lineEdit_BUOYANY_MIN, lineEdit_BUOYANY_MAX, slider_BUOYANY, slider_Dissipation,
        #    lineEdit_Dissipation_MIN, lineEdit_Dissipation_MAX, slider_DIFFUSION, lineEdit_DIFFUSION_MIN,
        #    lineEdit_DIFFUSION_MAX] = self.inputBoxes.createBox_DENSITY(isSliderAktiv_Buoyancy, isSliderAktiv_Dissipation, isSliderAktiv_Diffusion)

        #tab1_layout.addWidget(b)
        #tab1_layout.addWidget(boxDensity)


        self.ui.tabWidget.addTab(tab1, "Parameters2")
        self.inputBoxes.pushButtonReset_Event()
        print "dasdsadsasd"

        #self.ui.tabParameters.setVisible(False)
        #self.ui.tabSampling.hide()
        self.ui.tabWidget.removeTab(1)

    def createTabValues(self):

        #from MayaUiDefaultValues import MayaUiDefaultValues
        #a=MayaUiDefaultValues()
        #a.getSliderStatus()

        #print "::::::::: " + str(a._sliderDensityBuoyancy)
        self.inputBoxes = ParameterInputBoxes()

        # Add the tab
        tab3 = QtGui.QScrollArea()
        tab3.setWidget(QtGui.QWidget())
        tab3_layout = QtGui.QVBoxLayout(tab3.widget())
        tab3.setWidgetResizable(True)
        self.ui.tabWidget.addTab(tab3, "Parameters2")

        #
        #self.ui.tabParameters.setLayout(tab3_layout)



        degree_sign = u'\N{DEGREE SIGN}'

        self.ui.spinBox_rotDeg.setToolTip("Range: 10" + degree_sign + "- 90" + degree_sign + " ")
        # Create a widget for the tab

        mygroupbox = QtGui.QGroupBox()
        mygroupbox = QtGui.QWidget()
        myform = QtGui.QFormLayout()
        myform.setFormAlignment(QtCore.Qt.AlignAbsolute)



        #self.ui.tabParameters.setLayout(tab3_layout)

        """
        scroll = QtGui.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(460)
        """
        #tab3_layout.addWidget(scroll)
        #bar = scroll.verticalScrollBar()

        #self.ui.tabParameters.setLayout(tab3_layout)


        # -- Box 2 (VELOCITY) --
        """
        lineEdit_SWIRL_MIN = QtGui.QLineEdit("0")
        lineEdit_SWIRL_MIN.setFixedWidth(40)
        lineEdit_SWIRL_MIN.setAlignment(QtCore.Qt.AlignCenter)

        lineEdit_SWIRL_MAX = QtGui.QLineEdit("10")
        lineEdit_SWIRL_MAX.setFixedWidth(40)
        lineEdit_SWIRL_MAX.setAlignment(QtCore.Qt.AlignCenter)

        #slider_SWIRL = QHRangeSlider(range = [0.0, 10.0])
        #slider_SWIRL.setValues([0, 1])
        #slider_SWIRL.setEmitWhileMoving(True)
        #slider_SWIRL.setValues([0, 15])   # 152 --> ??
        #slider_SWIRL.setEmitWhileMoving(True)

        myBox_velocity = QtGui.QGroupBox("Velocity")
        myBox_velocity_layout = QtGui.QGridLayout()
        myBox_velocity.setLayout(myBox_velocity_layout)
        myBox_velocity_layout.addWidget(QtGui.QLabel("Default"),        0, 1, QtCore.Qt.AlignCenter)
        myBox_velocity_layout.addWidget(QtGui.QLabel("MIN"),            0, 2, QtCore.Qt.AlignCenter)
        myBox_velocity_layout.addWidget(QtGui.QLabel("MAX"),            0, 9, QtCore.Qt.AlignCenter)
        myBox_velocity_layout.addWidget(QtGui.QLabel("<b>Dissipation</b>"),   1, 0, QtCore.Qt.AlignRight)
        myBox_velocity_layout.addWidget(QtGui.QLabel("0 | 10"),         1, 1, QtCore.Qt.AlignCenter)
        #myBox_velocity_layout.addWidget(slider_SWIRL,                   1, 3, 1, 6 )
        #slider_SWIRL.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        myBox_velocity_layout.addWidget(lineEdit_SWIRL_MIN,             1, 2, QtCore.Qt.AlignCenter)
        myBox_velocity_layout.addWidget(lineEdit_SWIRL_MAX,             1, 9, QtCore.Qt.AlignCenter)

        #myBox_velocity_layout.addWidget(QtGui.QLabel("<b>Dissi</b>"),   2, 0, QtCore.Qt.AlignRight)
        #slider_SWIRL1 = QHRangeSlider(range = [0.0, 10.0])
        #slider_SWIRL1.setValues([0, 1])
        #slider_SWIRL1.setEmitWhileMoving(True)
        #slider_SWIRL1.setValues([0, 15])   # 152 --> ??
        #slider_SWIRL1.setEmitWhileMoving(True)
        #myBox_velocity_layout.addWidget(slider_SWIRL1,                   2, 3, 2, 6 )
        """

        self.inputBoxes = ParameterInputBoxes()

        #boxDensity = self.inputBoxes.createBox_DENSITY()



        # Get the current state (enabled/disabled) from the maya ui elements
        uiStatus = MayaUiDefaultValues()

        # Create Density box
        isSliderAktiv_Buoyancy = ( uiStatus._sliderDensityBuoyancy and uiStatus.isAttributeSettable("fluidShape1", "TODO") )
        isSliderAktiv_Dissipation = True
        isSliderAktiv_Diffusion = False

        [boxDensity, lineEdit_BUOYANY_MIN, lineEdit_BUOYANY_MAX, slider_BUOYANY, slider_Dissipation,
            lineEdit_Dissipation_MIN, lineEdit_Dissipation_MAX, slider_DIFFUSION, lineEdit_DIFFUSION_MIN,
            lineEdit_DIFFUSION_MAX] = self.inputBoxes.createBox_DENSITY(isSliderAktiv_Buoyancy, isSliderAktiv_Dissipation, isSliderAktiv_Diffusion)


        # Create Velocity box
        isSliderAktiv_SWIRL = True
        [ boxVelocity, slider_SWIRL, lineEdit_SWIRL_MIN, lineEdit_SWIRL_MAX ] = self.inputBoxes.createBox_VELOCITY(isSliderAktiv_SWIRL)

        # Create Box_Dynamic_sim box
        isSliderAktiv_VICOSITY = False
        [ boxDynamicsim, slider_VISCOSITY, lineEdit_VISCOSITY_MIN, lineEdit_VISCOSITY_MAX ] = self.inputBoxes.createBox_DYNAMIC_SIM(isSliderAktiv_VICOSITY)

        # Create Turbulence box
        isSliderAktiv_SPEED = False
        isSliderAktiv_FREQUENCY = True
        isSliderAktiv_STRENGTH = True
        [boxTurbulence, slider_SPEED, self.lineEdit_SPEED_MIN, lineEdit_SPEED_MAX,
                slider_FREQUENCY, lineEdit_FREQUENCY_MIN, lineEdit_FREQUENCY_MAX] = self.inputBoxes.createBox_TURBULENCE(isSliderAktiv_SPEED, isSliderAktiv_FREQUENCY, isSliderAktiv_STRENGTH)

        pushButtonReset = QtGui.QPushButton("Reset values")
        #pushButtonReset.setMaximumWidth(120)
        #self.lineEdit_SPEED_MIN.setText("hallo1")
        pushButtonReset.clicked.connect(self.inputBoxes.pushButtonReset_Event)

        # Add the boxes to the layout
        myform.addWidget(boxDensity)
        #myform.addWidget(boxVelocity)
        #myform.addWidget(boxTurbulence)
        #myform.addWidget(boxDynamicsim)

        #myform.setFormAlignment(QtCore.Qt.AlignRight)
        #myform.addWidget(pushButtonReset)

        mygroupbox.setLayout(myform)

        # Add scroll area
        scroll = QtGui.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(460)

        tab3_layout.addWidget(scroll)
        bar = scroll.verticalScrollBar()

        #lineEdit_BUOYANY_MIN.setText("XXX")
        lineEdit_BUOYANY_MIN.editingFinished.connect(self.inputBoxes.lineEdit_SWIRL_MIN_Leafe)
        lineEdit_BUOYANY_MAX.editingFinished.connect(self.inputBoxes.lineEdit_SWIRL_MAX_Leafe)
        #print("--------------VALUE : " + self.inputBoxes.lineEdit_BUOYANY_MIN.text())



    # Eventhandlers

    @QtCore.Slot()
    def buttonHelpCreateProj_Event(self):
        self.lineEdit_SPEED_MIN.setText("hallo1")
        print "[ Button clicked: " + "Help" + " ]"

    @QtCore.Slot()
    def buttonHelpCreateProj1_Event(self, a):
        print "[ Button clicked: " + "Help" + " ]"

    @QtCore.Slot()
    def buttonBrowse_Event(self):
        print "[ Button clicked: " + self.sender().text() + " ]"

        fileDialog = FileOpenDialog(self)
        choosenDir = fileDialog.openDirDialogQuick() #+ "/"

        if choosenDir == None:
            print "asdsada"
        else:
            print "babbel: " + choosenDir
            choosenDir = choosenDir + "/"
            choosenDirNew = choosenDir + "/"
            if (platform.system() == "Windows"):
                choosenDirNew = choosenDir.replace("/","\\")

                print(choosenDirNew)

                self.ui.lineEdit_ProjPath.setText(choosenDirNew)
                self.test = choosenDir



    @QtCore.Slot()
    def buttonCreateSimulation_Event(self):
        #print "[ Button clicked: " + self.sender().text() + " ]"

        # Objects which holds the general project settings
        generalParams = MayaCacheCmdSettings()



        # Check if paths are correct
        pathName = self.ui.lineEdit_ProjPath.text()
        projName = self.ui.lineEdit_SimulationName.text()

        if pathName == "":
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Cannot create project! Please enter a project name.")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.exec_()
            self.ui.lineEdit_SimulationName.setFocus()
            return

        if projName == "":
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Cannot create project folder! Please enter a project path.")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.exec_()
            self.ui.lineEdit_SimulationName.setFocus()
            return

        if not re.match("^[a-zA-Z0-9_]*$", projName):
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Cannot create project! A file name cannot contain special characters!\n"
                           "Valid characters: numbers, letters, - and _ ")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            self.ui.lineEdit_SimulationName.setFocus()
            self.ui.lineEdit_SimulationName.setText("")
            msgBox.exec_()
            return

        # Check project folder
        dirExists = FluidExplorerUtils.FluidExplorerUtils.dirExists(pathName)
        if (dirExists):
            print "WARNING: Directory already exists!"
            pathPrjAbsolut = os.path.abspath(pathName)
        else:
            try:#
                os.mkdir(pathName)
                pathPrjAbsolut = os.path.abspath(pathName)
            except:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Cannot create project! A file name cannot contain special characters!\n"
                               "Valid characters: numbers, letters, - and _ ")
                msgBox.setWindowTitle("Warning - Create Simulation")
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                self.ui.lineEdit_ProjPath.setFocus()
                self.ui.lineEdit_ProjPath.setText(self.workDir)
                msgBox.exec_()
                return

        projPathFull =  pathName + projName
        print "AL: " + os.path.expanduser(projPathFull)
        dirExists = FluidExplorerUtils.FluidExplorerUtils.dirExists(projPathFull)
        simulationNameAbsolut = os.path.abspath(projPathFull)
        if (dirExists):
            print "WARNING: Folder for project already exists!"
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Project already exists!\n"
                           "Please change the project name")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            self.ui.lineEdit_SimulationName.setFocus()
            self.ui.lineEdit_SimulationName.setText("")
            msgBox.exec_()
            simulationNameAbsolut = os.path.abspath(projPathFull)
            return
        else:
            try:
                os.mkdir(simulationNameAbsolut)
            except:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Cannot create project! A file name cannot contain special characters!\n"
                               "Valid characters: numbers, letters, - and _ ")
                msgBox.setWindowTitle("Warning - Create Simulation")
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                self.ui.lineEdit_ProjPath.setFocus()
                self.ui.lineEdit_ProjPath.setText(self.workDir)
                msgBox.exec_()
                return
            finally:
                generalParams.outputPath = projPathFull
                index = projPathFull.rfind(projName)
                generalParams.prjName = projPathFull[index:]


        # Get the camera parameters
        generalParams.cam_perspective = self.CLICK_FLAG_CAM_PV
        generalParams.cam_viewcube = self.CLICK_FLAG_CAM_VC
        generalParams.cam_sphere = self.CLICK_FLAG_CAM_SPH

        if self.CLICK_FLAG_CAM_ROT:
            generalParams.cam_rotation = self.ui.spinBox_rotDeg.text()

        print "RES: " + simulationNameAbsolut
        MayaCacheCmdSettings.printValues(generalParams)




        return




        print self.ui.lineEdit_numberSeq.text()
        print "HERE"
        tmpCmd = ParameterInputBoxes()
        paramsSamplng = tmpCmd.getSamplingValues(self.inputBoxes)

        tmpCmd.printSamplingValues(paramsSamplng)


        generalParams = MayaCacheCmdSettings()
        generalParams.numberSamples = self.ui.horizontalSlider_numberSeq.value()
        generalParams.outputPath = self.ui.lineEdit_ProjPath.text()
        generalParams.prjName =  self.ui.lineEdit_SimulationName.text()

        MayaCacheCmdSettings.printValues(generalParams)

        # Check if directory exists and path ok
        dirName = self.ui.lineEdit_ProjPath.text() + "/" + self.ui.lineEdit_SimulationName.text()

        if self.ui.lineEdit_SimulationName.text() == "":
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Cannot create project! Please enter a project name.")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.exec_()
            self.ui.lineEdit_SimulationName.setFocus()
            return

        if self.ui.lineEdit_ProjPath.text() == "":
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Cannot create project folder! Please enter a project path.")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.exec_()
            self.ui.lineEdit_ProjPath.setFocus()
            return

        tmpPrjName = self.ui.lineEdit_SimulationName.text()
        tmpPrjPath = self.ui.lineEdit_ProjPath.text()

        print tmpPrjName
        if not re.match("^[a-zA-Z0-9_]*$", tmpPrjName):
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Cannot create project! A file name cannot contain special characters!\n"
                           "Valid characters: numbers, letters, - and _ ")
            msgBox.setWindowTitle("Warning - Create Simulation")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            self.ui.lineEdit_SimulationName.setFocus()
            self.ui.lineEdit_SimulationName.setText("")
            msgBox.exec_()
            return

        if not os.path.exists(tmpPrjPath):
            try:
                a = os.mkdir(tmpPrjPath)
                print "A:" + a
            except:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Cannot create project folder! A file name cannot contain any of \n"
                               "the following characters: \ / : * ? \" < > | # { } % ~ ")
                msgBox.setWindowTitle("Warning - Create Simulation")
                msgBox.setIcon(QtGui.QMessageBox.Warning)
                self.ui.lineEdit_SimulationName.setFocus()
                self.ui.lineEdit_SimulationName.setText("")
                msgBox.exec_()

        generalParams.outputPath = tmpPrjPath + projName
        print generalParams.outputPath

    @QtCore.Slot()
    def lineEdit_numberSeq_EditFinished(self):

        print self.ui.lineEdit_numberSeq.text()
        if not self.ui.lineEdit_numberSeq.text():
            self.ui.lineEdit_numberSeq.setText(str(DefaultUIParameters.DEF_NUMBER_SEQUENCES))


    @QtCore.Slot()
    def sliderNumberSequences_Event(self):
        print self.ui.horizontalSlider_numberSeq.value()

        tmp = str(self.ui.horizontalSlider_numberSeq.value())
        self.ui.lineEdit_numberSeq.setText(tmp)

        v1 = self.ui.horizontalSlider_numberSeq.value()
        timeValue = "Time: " + str(v1) + " h"
        self.ui.labelTime.setText(timeValue)

        timeValue = "Storage Consumtion: " + "100" + " GB"
        self.ui.labelDiskSpace.setText(timeValue)

        self.calculateTimeSpave()


    @QtCore.Slot()
    def lineEdit_numberSeq_Event(self):
        numberSeq = self.ui.lineEdit_numberSeq.text()

        try:
            val = int(numberSeq)
            print "NOW: " + str(val)
            self.ui.horizontalSlider_numberSeq.setValue(val)
        except ValueError:
            if numberSeq == "":
                pass
            else:
                print("That's not an int!")
                self.ui.lineEdit_numberSeq.setText(str(DefaultUIParameters.DEF_NUMBER_SEQUENCES))

        #self.ui.horizontalSlider_numberSeq.update()


    @QtCore.Slot()
    def lineEdit_numberSeq_EventLeafe(self):
        """
        numberSeq = self.ui.lineEdit_numberSeq.text()

        try:
            val = int(numberSeq)
        except ValueError:
                self.ui.lineEdit_numberSeq.setText(str(DefaultUIParameters.DEF_NUMBER_SEQUENCES))
"""

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

        self.calculateTimeSpave()
        #self.ui.pushButton_CamPV.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)

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

        self.calculateTimeSpave()

    @QtCore.Slot()
    def pushButtonCamSPH_Event(self):
        #print "3 clicked"
        flag = self.CLICK_FLAG_CAM_SPH
        if not flag:
            self.ui.pushButton_CamSPH.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
            self.CLICK_FLAG_CAM_SPH = True
        elif flag:
            self.ui.pushButton_CamSPH.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
            self.CLICK_FLAG_CAM_SPH = False

        self.calculateTimeSpave()

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

        self.calculateTimeSpave()

    @QtCore.Slot()
    def spinBoxRot_Event(self):
        self.calculateTimeSpave()
        value = int(self.ui.spinBox_rotDeg.text())

        if value < DefaultUIParameters.DEF_SPIN_ROT_MIN:
            self.ui.spinBox_rotDeg.setValue(int(DefaultUIParameters.DEF_SPIN_ROT_MIN))

        if value > DefaultUIParameters.DEF_SPIN_ROT_MAX:
            self.ui.spinBox_rotDeg.setValue(int(DefaultUIParameters.DEF_SPIN_ROT_MAX))


    # Utils
    def initCamButtons(self):
        self.ui.pushButton_CamPV.setIcon(QtGui.QIcon(self.tr("ui/icons/ico_pv.png")))
        self.ui.pushButton_CamPV.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
        self.ui.pushButton_CamVC.setIcon(QtGui.QIcon(self.tr("ui/icons/ico_pv.png")))
        self.ui.pushButton_CamVC.setStyleSheet(DefaultUIParameters.StyleSheet_Button_On)
        self.ui.pushButton_CamSPH.setIcon(QtGui.QIcon(self.tr("ui/icons/ico_pv.png")))
        self.ui.pushButton_CamSPH.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
        self.ui.pushButton_ROT.setIcon(QtGui.QIcon(self.tr("ui/icons/ico_pv.png")))
        self.ui.pushButton_ROT.setStyleSheet(DefaultUIParameters.StyleSheet_Button_Off)
        self.ui.pushButton_CamPV.clicked.connect(self.pushButtonCamPV_Event)
        self.ui.pushButton_CamVC.clicked.connect(self.pushButtonCamVC_Event)
        self.ui.pushButton_CamSPH.clicked.connect(self.pushButtonCamSPH_Event)
        self.ui.pushButton_ROT.clicked.connect(self.pushButtonROT_Event)

    def initSliderValues(self):
        self.ui.horizontalSlider_numberSeq.setMinimum(DefaultUIParameters.DEF_NUMBER_SEQUENCES_MIN)
        self.ui.horizontalSlider_numberSeq.setMaximum(DefaultUIParameters.DEF_NUMBER_SEQUENCES_MAX)
        self.ui.horizontalSlider_numberSeq.setValue(DefaultUIParameters.DEF_NUMBER_SEQUENCES)

    # TODO Calculate Values
    def calculateTimeSpave(self):
        totalTime = 2 * self.ui.horizontalSlider_numberSeq.value()
        totalSpace = 2 * self.ui.horizontalSlider_numberSeq.value() / 3

        """
        numSeq = int(self.ui.lineEdit_numberSeq.text())
        camPos = 0
        if self.CLICK_FLAG_CAM_PV:
            camPos = camPos + 1
        if self.CLICK_FLAG_CAM_VC:
            camPos = camPos + 6
        if self.CLICK_FLAG_CAM_SPH:
            camPos = camPos + 100
        if self.CLICK_FLAG_CAM_ROT:
            tmp = round(camPos + (1 * (360/int(self.ui.spinBox_rotDeg.text()))))
            tmp = int(tmp)
            camPos = camPos + tmp

        if camPos > 0:
            totalTime  = numSeq * camPos
        else:
            totalTime = numSeq

        """
        timeValue = "Time: " + str(totalTime) + " h"
        self.ui.labelTime.setText(timeValue)


        spaveValue = "Storage Consumtion: " + str(totalSpace) + " GB"
        self.ui.labelDiskSpace.setText(spaveValue)

