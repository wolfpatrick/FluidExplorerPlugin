# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\WorkspacePython\FluidExplorerPlugin\ui\CreateProjectDialogUI.ui'
#
# Created: Wed Jul 15 13:37:17 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CreateProjectDialog(object):
    def setupUi(self, CreateProjectDialog):
        CreateProjectDialog.setObjectName("CreateProjectDialog")
        CreateProjectDialog.resize(620, 670)
        CreateProjectDialog.setMinimumSize(QtCore.QSize(620, 670))
        CreateProjectDialog.setMaximumSize(QtCore.QSize(620, 670))
        self.pushButtonNewPrjHelp = QtGui.QPushButton(CreateProjectDialog)
        self.pushButtonNewPrjHelp.setGeometry(QtCore.QRect(560, 16, 40, 40))
        self.pushButtonNewPrjHelp.setStyleSheet("")
        self.pushButtonNewPrjHelp.setText("")
        self.pushButtonNewPrjHelp.setIconSize(QtCore.QSize(30, 30))
        self.pushButtonNewPrjHelp.setObjectName("pushButtonNewPrjHelp")
        self.labelMain = QtGui.QLabel(CreateProjectDialog)
        self.labelMain.setGeometry(QtCore.QRect(21, 20, 211, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(20)
        font.setItalic(False)
        font.setStrikeOut(False)
        self.labelMain.setFont(font)
        self.labelMain.setObjectName("labelMain")
        self.lineEdit_SimulationName = QtGui.QLineEdit(CreateProjectDialog)
        self.lineEdit_SimulationName.setGeometry(QtCore.QRect(20, 100, 580, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_SimulationName.setFont(font)
        self.lineEdit_SimulationName.setObjectName("lineEdit_SimulationName")
        self.label_Name = QtGui.QLabel(CreateProjectDialog)
        self.label_Name.setGeometry(QtCore.QRect(20, 80, 170, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_Name.setFont(font)
        self.label_Name.setObjectName("label_Name")
        self.label_Location = QtGui.QLabel(CreateProjectDialog)
        self.label_Location.setGeometry(QtCore.QRect(20, 140, 170, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_Location.setFont(font)
        self.label_Location.setObjectName("label_Location")
        self.lineEdit_ProjPath = QtGui.QLineEdit(CreateProjectDialog)
        self.lineEdit_ProjPath.setGeometry(QtCore.QRect(20, 160, 501, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_ProjPath.setFont(font)
        self.lineEdit_ProjPath.setObjectName("lineEdit_ProjPath")
        self.pushButtonBrowse = QtGui.QPushButton(CreateProjectDialog)
        self.pushButtonBrowse.setGeometry(QtCore.QRect(529, 160, 71, 25))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.pushButtonBrowse.setFont(font)
        self.pushButtonBrowse.setStyleSheet("")
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.tabWidget = QtGui.QTabWidget(CreateProjectDialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(20, 210, 581, 381))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        self.tabSampling = QtGui.QWidget()
        self.tabSampling.setObjectName("tabSampling")
        self.groupBoxCameras = QtGui.QGroupBox(self.tabSampling)
        self.groupBoxCameras.setGeometry(QtCore.QRect(22, 10, 530, 201))
        self.groupBoxCameras.setObjectName("groupBoxCameras")
        self.pushButton_CamPV = QtGui.QPushButton(self.groupBoxCameras)
        self.pushButton_CamPV.setGeometry(QtCore.QRect(20, 46, 100, 100))
        self.pushButton_CamPV.setText("")
        self.pushButton_CamPV.setIconSize(QtCore.QSize(90, 90))
        self.pushButton_CamPV.setObjectName("pushButton_CamPV")
        self.pushButton_CamVC = QtGui.QPushButton(self.groupBoxCameras)
        self.pushButton_CamVC.setGeometry(QtCore.QRect(150, 46, 100, 100))
        self.pushButton_CamVC.setText("")
        self.pushButton_CamVC.setIconSize(QtCore.QSize(90, 90))
        self.pushButton_CamVC.setObjectName("pushButton_CamVC")
        self.pushButton_CamSPH = QtGui.QPushButton(self.groupBoxCameras)
        self.pushButton_CamSPH.setGeometry(QtCore.QRect(280, 46, 100, 100))
        self.pushButton_CamSPH.setText("")
        self.pushButton_CamSPH.setIconSize(QtCore.QSize(90, 90))
        self.pushButton_CamSPH.setObjectName("pushButton_CamSPH")
        self.pushButton_ROT = QtGui.QPushButton(self.groupBoxCameras)
        self.pushButton_ROT.setGeometry(QtCore.QRect(410, 46, 100, 100))
        self.pushButton_ROT.setText("")
        self.pushButton_ROT.setIconSize(QtCore.QSize(90, 90))
        self.pushButton_ROT.setObjectName("pushButton_ROT")
        self.spinBox_rotDeg = QtGui.QSpinBox(self.groupBoxCameras)
        self.spinBox_rotDeg.setGeometry(QtCore.QRect(411, 156, 51, 22))
        self.spinBox_rotDeg.setMinimum(10)
        self.spinBox_rotDeg.setMaximum(90)
        self.spinBox_rotDeg.setProperty("value", 45)
        self.spinBox_rotDeg.setObjectName("spinBox_rotDeg")
        self.label = QtGui.QLabel(self.groupBoxCameras)
        self.label.setGeometry(QtCore.QRect(477, 156, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.groupBoxCameras)
        self.label_2.setGeometry(QtCore.QRect(20, 23, 101, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(self.groupBoxCameras)
        self.label_3.setGeometry(QtCore.QRect(150, 23, 101, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(self.groupBoxCameras)
        self.label_4.setGeometry(QtCore.QRect(280, 23, 101, 20))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(self.groupBoxCameras)
        self.label_5.setGeometry(QtCore.QRect(410, 23, 101, 20))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_selectedCam = QtGui.QLabel(self.groupBoxCameras)
        self.label_selectedCam.setGeometry(QtCore.QRect(254, 156, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_selectedCam.setFont(font)
        self.label_selectedCam.setText("")
        self.label_selectedCam.setAlignment(QtCore.Qt.AlignCenter)
        self.label_selectedCam.setObjectName("label_selectedCam")
        self.labelNumberSeq = QtGui.QLabel(self.tabSampling)
        self.labelNumberSeq.setGeometry(QtCore.QRect(24, 226, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        self.labelNumberSeq.setFont(font)
        self.labelNumberSeq.setObjectName("labelNumberSeq")
        self.labelTime = QtGui.QLabel(self.tabSampling)
        self.labelTime.setGeometry(QtCore.QRect(24, 288, 521, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        self.labelTime.setFont(font)
        self.labelTime.setObjectName("labelTime")
        self.labelDiskSpace = QtGui.QLabel(self.tabSampling)
        self.labelDiskSpace.setGeometry(QtCore.QRect(24, 318, 521, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        self.labelDiskSpace.setFont(font)
        self.labelDiskSpace.setObjectName("labelDiskSpace")
        self.horizontalSlider_numberSeq = QtGui.QSlider(self.tabSampling)
        self.horizontalSlider_numberSeq.setGeometry(QtCore.QRect(291, 226, 261, 20))
        self.horizontalSlider_numberSeq.setStyleSheet(" QSlider::groove:horizontal {\n"
"     border: 1px solid #999999;\n"
"     height: 8px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
"     background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);\n"
"     margin: 2px 0;\n"
" }\n"
"\n"
" QSlider::handle:horizontal {\n"
"     background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
"     border: 1px solid #5c5c5c;\n"
"     width: 18px;\n"
"     margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"     border-radius: 3px;\n"
" }\n"
"\n"
"QSlider::sub-page:qlineargradient {\n"
"     border: 1px solid #999999;\n"
"     height: 8px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
"     background: rgb(255, 160, 47);\n"
"     margin: 2px 0;\n"
"}")
        self.horizontalSlider_numberSeq.setMinimum(1)
        self.horizontalSlider_numberSeq.setMaximum(500)
        self.horizontalSlider_numberSeq.setPageStep(1)
        self.horizontalSlider_numberSeq.setProperty("value", 128)
        self.horizontalSlider_numberSeq.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_numberSeq.setObjectName("horizontalSlider_numberSeq")
        self.lineEdit_numberSeq = QtGui.QLineEdit(self.tabSampling)
        self.lineEdit_numberSeq.setGeometry(QtCore.QRect(201, 224, 71, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(50)
        font.setBold(False)
        self.lineEdit_numberSeq.setFont(font)
        self.lineEdit_numberSeq.setObjectName("lineEdit_numberSeq")
        self.labelAnimationTime = QtGui.QLabel(self.tabSampling)
        self.labelAnimationTime.setGeometry(QtCore.QRect(24, 258, 261, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        self.labelAnimationTime.setFont(font)
        self.labelAnimationTime.setObjectName("labelAnimationTime")
        self.labelAnimationTimeStartEnd = QtGui.QLabel(self.tabSampling)
        self.labelAnimationTimeStartEnd.setGeometry(QtCore.QRect(290, 258, 261, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        self.labelAnimationTimeStartEnd.setFont(font)
        self.labelAnimationTimeStartEnd.setObjectName("labelAnimationTimeStartEnd")
        self.tabWidget.addTab(self.tabSampling, "")
        self.tabParameters = QtGui.QWidget()
        self.tabParameters.setEnabled(True)
        self.tabParameters.setObjectName("tabParameters")
        self.scrollArea = QtGui.QScrollArea(self.tabParameters)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 561, 311))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 559, 309))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.widget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.widget.setGeometry(QtCore.QRect(0, 0, 561, 311))
        self.widget.setObjectName("widget")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tabParameters, "")
        self.pushButtonCreateSimulation = QtGui.QPushButton(CreateProjectDialog)
        self.pushButtonCreateSimulation.setGeometry(QtCore.QRect(20, 610, 579, 40))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.pushButtonCreateSimulation.setFont(font)
        self.pushButtonCreateSimulation.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/ico_search.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCreateSimulation.setIcon(icon)
        self.pushButtonCreateSimulation.setIconSize(QtCore.QSize(30, 30))
        self.pushButtonCreateSimulation.setObjectName("pushButtonCreateSimulation")

        self.retranslateUi(CreateProjectDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CreateProjectDialog)

    def retranslateUi(self, CreateProjectDialog):
        CreateProjectDialog.setWindowTitle(QtGui.QApplication.translate("CreateProjectDialog", "Fluid Explorer - Create Simulation", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMain.setText(QtGui.QApplication.translate("CreateProjectDialog", "Create Simulation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_Name.setText(QtGui.QApplication.translate("CreateProjectDialog", "Simulation Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_Location.setText(QtGui.QApplication.translate("CreateProjectDialog", "Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBrowse.setText(QtGui.QApplication.translate("CreateProjectDialog", "Browse ...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxCameras.setTitle(QtGui.QApplication.translate("CreateProjectDialog", "Select one or more Cameras", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CreateProjectDialog", "deg.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CreateProjectDialog", "Perspective", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CreateProjectDialog", "View Cube", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("CreateProjectDialog", "Custom", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("CreateProjectDialog", "Rotation", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNumberSeq.setText(QtGui.QApplication.translate("CreateProjectDialog", "Number of Sequences:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTime.setText(QtGui.QApplication.translate("CreateProjectDialog", "Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDiskSpace.setText(QtGui.QApplication.translate("CreateProjectDialog", "Storage Consumtion:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_numberSeq.setText(QtGui.QApplication.translate("CreateProjectDialog", "128", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAnimationTime.setText(QtGui.QApplication.translate("CreateProjectDialog", "Animation [Start Time / End Time]:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAnimationTimeStartEnd.setText(QtGui.QApplication.translate("CreateProjectDialog", "1.00 / 50.00", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSampling), QtGui.QApplication.translate("CreateProjectDialog", "Sampling", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabParameters), QtGui.QApplication.translate("CreateProjectDialog", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCreateSimulation.setText(QtGui.QApplication.translate("CreateProjectDialog", "Start Simulation", None, QtGui.QApplication.UnicodeUTF8))

