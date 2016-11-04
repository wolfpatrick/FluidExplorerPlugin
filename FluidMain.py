########################################################################################################################
#                                                                                                                      #
#   This file calls the FluidExplorer Plugin and has to be stord in:                                                   #
#                                                                                                                      #
#       Windows: maya\2014-x64\scripts\FluidMain.py                                                                    #
#                                                                                                                      #
#   Path of the FluidExplorer Plugin:                                                                                  #
#                                                                                                                      #
#       Windows: maya\2014-x64\scripts\FluidExplorerPlugin\                                                            #
#                                                                                                                      #
########################################################################################################################

import sys
import os
import webbrowser
import logging

from PySide import QtCore, QtGui
from shiboken import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

from FluidExplorerPlugin.ui.FileOpenDialog import FileOpenDialog
from FluidExplorerPlugin.ui.CreateProjectDialog import CreateProjectDialog
from FluidExplorerPlugin.ui.Utils.MayaCmds.MayaFunctions import MayaFunctionUtils
from FluidExplorerPlugin.ui.Utils.MayaCmds import MayaFunctions
from FluidExplorerPlugin.ui.Utils.FluidExplorerUtils  import FluidExplorerUtils
from FluidExplorerPlugin.ui.Utils import settings
from FluidExplorerPlugin.ui.Icons import icons
from FluidExplorerPlugin.ui.ProjectDetailsView import ProjectDetailsView
import FluidExplorerPlugin.ui.MainWindow as mainUi

FLUID_EXPLORER_URL = "http://www.google.de"


# Get the maya main window as a QMainWindow instance
def getMayaWindow():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow= wrapInstance(long(mayaMainWindowPtr), QtGui.QDialog)


#
# Main window control called from maya app
#
class ControlMainWindow(QtGui.QMainWindow):

    def __init__(self, parent = getMayaWindow()):

        # Initialize qt window
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  mainUi.Ui_MainWindow()
        self.ui = mainUi.Ui_MainWindow()
        self.ui.setupUi(self)

        # Show always on top
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Set up dark_orange style sheet
        self.setStyleSheet( ControlMainWindow.getStyleSheet() )

        # Url for the help page
        self.url = FLUID_EXPLORER_URL

        # Initialize connections and icons for the buttons
        self.createConnections()
        self.setupButtons()

        # Position of the plugin main window in the maya app
        self.centre()

        # Subprocess number
        self.pid = None

        # Close fluidexp if running
        FluidExplorerUtils.killProcess("fluidexplorer")

        # Details View
        self.detailsView = None
        if self.detailsView:
            self.detailsView.close()

        # For tests only
        runTests = True
        #runTests = False
        if runTests:
            import maya.mel as mel

            # Animation Start/End Time
            cmds.playbackOptions(animationStartTime=1.00)
            cmds.playbackOptions(animationEndTime=15.00)

        # Logging
        self.lgr = logging.getLogger('FluidExplorerPlugin')


    # Places the plugin in the maya app
    def centre(self):
        #panelPtr = omui.MQtUtil.findControl('toolBar2')
        panelPtr = omui.MQtUtil.findControl('modelPanel1')

        if panelPtr == None:
            """
            Center the main window on the screen. This implemention will handle the window
            being resized or the screen resolution changing.
            """
            # Get the current screens' dimensions...
            screen = QtGui.QDesktopWidget().screenGeometry()
            # ... and get this windows' dimensions
            mysize = self.geometry()
            # The horizontal position is calulated as screenwidth - windowwidth /2
            hpos = ( screen.width() - mysize.width() ) / 2
            # And vertical position the same, but with the height dimensions
            vpos = ( screen.height() - mysize.height() ) / 2
            # And the move call repositions the window
            self.move(hpos + 300, vpos - 100)
        else:
            panel = wrapInstance(long(panelPtr), QtGui.QWidget)
            position =  panel.mapToGlobal(panel.pos())
            #self.move(position.x(), position.y() + (panel.geometry().height() / 2 - self.geometry().height() / 2) + 5)
            self.move(position.x(), position.y())

            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    # Read the dark orange stylesheet
    @staticmethod
    def getStyleSheet():
        style_sheet_file = os.path.join(settings.PKG_RESOURCE_PATH, 'darkorange.stylesheet')
        custome_style_sheet = open(style_sheet_file, 'r')
        sheet = custome_style_sheet.read()
        custome_style_sheet.close()

        return sheet

    # Connect buttons and event listeners
    def createConnections(self):
        self.ui.pushButtonLoadSimulation.clicked.connect(self.buttonLoadSimulation_Event)
        self.ui.pushButtonNewProject.clicked.connect(self.buttonNewProject_Event)
        self.ui.pushButtonHelpMain.clicked.connect(self.buttonHelpMain_Event)

    # Initialize buttons (icons)
    def setupButtons(self):
        icon_open = QtGui.QIcon(QtGui.QPixmap(':/open_icon_orange.png'))
        icon_create = QtGui.QIcon(QtGui.QPixmap(':/new_icon_orange.png'))
        icon_help = QtGui.QIcon(QtGui.QPixmap(':/help_icon_orange.png'))
        icon_fluidExplorer = QtGui.QIcon(QtGui.QPixmap(':/help_icon_orange.png'))
        icon_fluidExplorer_black = QtGui.QIcon(QtGui.QPixmap(':/icon_fluidexplorer_black.png'))
        pixmap_help = QtGui.QPixmap(':/icon_fluidexplorer.png')
        pixmap_help_scaled = pixmap_help.scaled(30, 30, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.ui.pushButtonNewProject.setIcon(icon_create)
        self.ui.pushButtonLoadSimulation.setIcon(icon_open)
        self.ui.pushButtonHelpMain.setIcon(icon_help)
        self.ui.labelIcon.setText("")
        self.ui.labelIcon.setPixmap(pixmap_help_scaled)
        self.setWindowIcon(icon_fluidExplorer_black)

        buttonStyleBold = "QPushButton { font-weight: bold; }"
        self.ui.pushButtonNewProject.setStyleSheet(buttonStyleBold)
        self.ui.pushButtonLoadSimulation.setStyleSheet(buttonStyleBold)


    # Eventhandler - Load simulation
    @QtCore.Slot()
    def buttonLoadSimulation_Event(self):
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        self.close()

        # Get current scene name
        currentSceneName = cmds.file(q=True, sceneName=True)

        # Path of the Fluid Explorer folder
        #filePathMain = repr(__file__)
        filePathMain = os.path.dirname(os.path.abspath(__file__))
        fxPathRel = os.path.abspath(filePathMain)

        self.openDialog = FileOpenDialog()
        [dialogResult, selectedDir, pid] = self.openDialog.openDirDialog(currentSceneName, fxPathRel)

        # Scene opened flag
        sceneOpened = False

        # cancel --> Show dialog again, result=started --> call fluid explorer
        if not dialogResult == "started":

            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.centre()
            self.show()
        else:
            self.lgr.info("Scene %s successfully opened", selectedDir)
            sceneOpened = True
            self.pid = pid


        # --------------------------------------------------------------------------------------
        # Create scene details window
        if sceneOpened:

            #self.detailsView.close()
            self.detailsView = ProjectDetailsView(self, selectedDir)
            self.detailsView.show()
        # --------------------------------------------------------------------------------------


    # Eventhandler - create simulation
    @QtCore.Slot()
    def buttonNewProject_Event(self):

        # Chek if pne fluid container is selected
        helpFunc = MayaFunctionUtils()
        [status, errorMsg, transformNode] = helpFunc.getSelectedContainerPy()

        self.lgr.info("Selected container (type: - transform node): %s",  transformNode)

        if status == False:
            errorMsg = errorMsg
            #QtGui.QMessageBox.information(self, 'Information1', str(errorMsg), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            self.lgr.warning("%s", errorMsg)
            self.showMessageBox(errorMsg, 'warning')

        else:

            fluidShapeName = errorMsg   # errorMsg: stores the name of the selected fluid
            try:
                cmds.select(fluidShapeName, r=True)

                self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)    # Hide main window
                self.lgr.info("Selected container (type: - transform node): %s",  errorMsg)

                # Show create simulation dialog
                # errorMsg -> fluidName or error message
                # transformNode -> transform node
                createDialog = CreateProjectDialog(self, errorMsg, transformNode)
                createDialog.setFluidName(errorMsg)
                dialogCode = createDialog.exec_()

                # Dialog canceled
                if dialogCode == QtGui.QDialog.Rejected:
                    self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)    # Show main window again
                    self.show()

            except ValueError as er:
                errorMsg = "Cannot use selected fluid container '"+ fluidShapeName + "'" + ".\nDetails: " + er.message
                self.lgr.error("Cannot use selected fluid container: %s",  er.message)
                self.showMessageBox(errorMsg, 'critical')

    # Eventhandler - Help button
    @QtCore.Slot()
    def buttonHelpMain_Event(self):
        _url = self.url
        webbrowser.open(_url, new=1)

    def showMessageBox(self, text, type):
        msgBox = QtGui.QMessageBox(self)
        msgBox.setStyleSheet("QPushButton{min-width: 70px;} QMessageBox{font-size: 12px;}")
        msgBox.setText(text)

        if type== 'warning':
            msgBox.setWindowTitle("Warning")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
        if type== 'critical':
            msgBox.setWindowTitle("Error")
            msgBox.setIcon(QtGui.QMessageBox.Critical)

        msgBox.exec_()

    def closeEvent(self, event):
        # close (x button) event
        FluidExplorerUtils.killProcess("fluidexplorer")


def main():

    # Logger
    lgr = logging.getLogger('FluidExplorerPlugin')

    # Check if maya version is correct (>= 2014)
    isVersionOK = checkMayaVersion()
    isPlattformOK = checkPlatform()

    lgr.info(' ')
    lgr.info('Maya version correct: %s', isVersionOK)
    lgr.info('Platform correct: %s', isVersionOK)

    if not isPlattformOK:
        showMessageBoxPlugin("The current operating system not supported!\nPlease use a Windows based version.", "warning")
        lgr.error('The current operating system not supported')
        return None

    if not isVersionOK:
        showMessageBoxPlugin("The current Maya version is not supported!\nPlease install version 2014 or higher.", "warning")
        lgr.error('The current Maya version is not supported')
        return None

    if isVersionOK and isPlattformOK:

        # Check if a window has already been opened. If yes, close it. Otherwise create new maya main window
        if cmds.window("FluidExplorer",ex=True) == 1:
            cmds.deleteUI("FluidExplorer")

        # Initialize main window and show in maya
        mainWin = ControlMainWindow( parent = getMayaWindow() )
        lgr.info('FluidExplorer plugin started')
        lgr.info(' ')

        return mainWin


def helpButtonToolBar():
    webbrowser.open(FLUID_EXPLORER_URL, new=1)

def checkMayaVersion():
    versionStr = cmds.about(version=True)
    if len(versionStr) >= 4:
        version = versionStr[0:4]
        try:
            versionInteger = int(version)
        except ValueError:
            versionIsOk = False
        finally:
            if versionInteger >= 2014:
                versionIsOk = True
            else:
                versionIsOk = False

    else:
        versionIsOk = False

    return versionIsOk

def checkPlatform():
    currentPlatfromOK = cmds.about(win=True)  # Check if paltform is windows based

    return currentPlatfromOK

def showMessageBoxPlugin(text, type):
    msgBox = QtGui.QMessageBox()
    msgBox.setStyleSheet("QPushButton{min-width: 70px;} QMessageBox{font-size: 12px;}")
    msgBox.setText(text)

    if type== 'warning':
        msgBox.setWindowTitle("Warning")
        msgBox.setIcon(QtGui.QMessageBox.Warning)
    if type== 'critical':
        msgBox.setWindowTitle("Error")
        msgBox.setIcon(QtGui.QMessageBox.Critical)

    msgBox.exec_()



