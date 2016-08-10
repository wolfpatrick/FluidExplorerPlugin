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
from FluidExplorerPlugin.ui.Utils.ProjectDetailsViewUtils import XMLReader

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

    def __init__(self, args):
        QtGui.QDialog.__init__(self, args)

        # Stores configuration attributes
        self.projectSettings = None

        # Set up the user interface from the ui file
        self.ui = Ui_ProjectDetailsView()
        self.ui.setupUi(self)
        #self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowState(QtCore.Qt.WindowMinimizeButtonHint)

        # Move window to the 'modelPanel1' position
        [xPos, yPos] = self.moveWindowToPanel()
        self.move(xPos, yPos)

        # Create connections
        self.createConnections()

        # Initialize widget
        self.initializewidget()
        self.setWindowHeightWithoutPreview()
        self.initializeComponentss()
        self.setWindowTitle('Fluid Explorer - Simulation Details View')

        # Set values from project configuration file
        self.projectSettings = self.readProjectProperties('E:/TMP/ANNAANNA/ANNAANNA.fxp')
        self.setValuesFromConfigurationFile(self.projectSettings)
        print self.projectSettings.projectName

        #####################################################
        self.ui.comboBox_simulations.addItem('a')
        self.ui.comboBox_simulations.addItem('a')
        self.ui.comboBox_simulations.addItem('a')

        self.setWindowFlags(self.windowFlags() |
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowStaysOnTopHint)




    def moveWindowToPanel(self):
        try:
            panelPtr = omui.MQtUtil.findControl('modelPanel1')
            print panelPtr
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
        self.setMinimumHeight(622)
        self.setMaximumHeight(622)

    def setWindowHeightWithoutPreview(self):
        self.setMinimumHeight(360-1)
        self.setMaximumHeight(360-1)

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

    def setValuesFromConfigurationFile(self, projectSettings):
         if projectSettings:
            self.ui.lineEdit_projectName.setText(projectSettings.projectName)
            self.ui.lineEdit_projectPath.setText(projectSettings.projectPath)
            self.ui.lineEdit_fluidContainer.setText(projectSettings.fluidContainerName)
            self.ui.lineEdit_startTime.setText(projectSettings.animationStartTime)
            self.ui.lineEdit_endTime.setText(projectSettings.animationEndTime)


    def createConnections(self):
        self.connect(self.ui.pushButton_applyCache, QtCore.SIGNAL("clicked()"), self.applyCacheClicked)
        self.connect(self.ui.pushButton_exploreSimulations, QtCore.SIGNAL("clicked()"), self.exploreSimulationsClicked)
        self.connect(self.ui.checkBox_showPreview, QtCore.SIGNAL("stateChanged(int)"), self.checkBoxPreviewValueChanged)
        self.connect(self.ui.comboBox_simulations, QtCore.SIGNAL("currentIndexChanged(QString)"), self.comboBoxSimulationsIndexChanged)
        self.connect(self.ui.pushButton_help, QtCore.SIGNAL("clicked()"), self.helpButtonClicked)

    # - Event handlers -
    @QtCore.Slot()
    def applyCacheClicked(self):
        print 'applyCacheClicked clicked'

    @QtCore.Slot()
    def exploreSimulationsClicked(self):
        print 'exploreSimulationsClicked'

    @QtCore.Slot()
    def checkBoxPreviewValueChanged(self, state):
        print 'checkBoxPreviewValueChanged'
        print self.ui.checkBox_showPreview.checkState()
        # State starts with 0

        if self.ui.checkBox_showPreview.checkState() == QtCore.Qt.Checked:
            print "CHECKED"
            self.setWindowHeightWithPreview()
        elif self.ui.checkBox_showPreview.checkState() == QtCore.Qt.Unchecked:
            print "NOT CHECKED"
            self.setWindowHeightWithoutPreview()

    @QtCore.Slot()
    def comboBoxSimulationsIndexChanged(self, index):
        print 'ecomboBoxSimulationsIndexChanged'
        print self.ui.comboBox_simulations.currentIndex()

    @QtCore.Slot()
    def helpButtonClicked(self):
        print 'help'
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
        xmReader = XMLReader()

        projectSettings = None
        try:
            projectSettings = xmReader.getProjectSubSettings(pathToXMLFile)
        except Exception as e:
            errorText = "An error occured while loading the project configuration file!\nDetails: " + str(e.message)
            self.showMessageBox(errorText, 'warning')
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