import sys
import webbrowser
import os

from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.cmds as cmds
import maya.OpenMayaUI as omui
#import MainWindow as mainUi
import FluidExplorerPlugin.ui.MainWindow as mainUi
import maya.mel
import maya.utils

# UI files created with pyside-uic from qt_xml description
from FluidExplorerPlugin.ui.FileOpenDialog import FileOpenDialog
from FluidExplorerPlugin.ui.CreateProjectDialog import CreateProjectDialog
from ui.Icons import icons
from FluidExplorerPlugin.ui.Utils import settings

from FluidExplorerPlugin.ui.Utils.MayaCmds import MayaFunctions


# Get the maya main window as a QMainWindow instance    
def getMayaWindow():

    mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
    mayaMainWindow= wrapInstance(long(mayaMainWindowPtr), QtGui.QWidget) 
 

##
## Main window control called from maya app
##
class ControlMainWindow(QtGui.QMainWindow):
 
    def __init__(self, parent = getMayaWindow()):
        
        # Initialize qt window
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  mainUi.Ui_MainWindow()
        self.ui=mainUi.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Set up dark_orange style sheet
        self.setStyleSheet( ControlMainWindow.getStyleSheet() )   
        #print "TEST: " + ControlMainWindow.getStyleSheet()
        # Url
        self.url = "http://www.google.de"
        self.url = "http://homepage.univie.ac.at/patrick_wolf/beliv_2012/index.php"
		
        # Initialize buttons
        self.createConnections()

        # Initialize icons for buttons
        self.setupButtons()
		
		
		
    @staticmethod
    def getStyleSheet():
        style_sheet_file = os.path.join(settings.PKG_RESOURCE_PATH, 'darkorange.stylesheet')
        custome_style_sheet = open(style_sheet_file, 'r')
        sheet = custome_style_sheet.read()
        custome_style_sheet.close()
        
        return sheet
      
        
    # Connect Buttons and event listeners
    def createConnections(self):
        self.ui.pushButtonLoadSimulation.clicked.connect(self.buttonLoadSimulation_Event)
        self.ui.pushButtonNewProject.clicked.connect(self.buttonNewProject_Event)
        self.ui.pushButtonHelpMain.clicked.connect(self.buttonHelpMain_Event)


    # Initialize buttons (icons)
    def setupButtons(self):
        # Load icons from resource files (py-side for more information)
        icon_open = QtGui.QIcon(QtGui.QPixmap(':/icon_open_30px.png'))
        icon_create = QtGui.QIcon(QtGui.QPixmap(':/icon_add_30px.png'))
        icon_help = QtGui.QIcon(QtGui.QPixmap(':/icon_help_30px.png'))

        self.ui.pushButtonNewProject.setIcon(icon_create)
        self.ui.pushButtonLoadSimulation.setIcon(icon_open)
        self.ui.pushButtonHelpMain.setIcon(icon_help)


    # Eventhandler - load simulation
    @QtCore.Slot()
    def buttonLoadSimulation_Event(self):
        print "[ Button clicked: " + self.sender().text() + "]"

        # Get current scene name
        currentSceneName = cmds.file(q=True, sceneName=True)
        print "Current scene: " + str(currentSceneName)

        openD = FileOpenDialog(self)
        openD.openDirDialog(currentSceneName)

    # Eventhandler - create simulation
    @QtCore.Slot()
    def buttonNewProject_Event(self):
        print "[ Button clicked ... : " + self.sender().text() + "]"

        helpFunc = MayaFunctions()
        [stat, errorMsg] = helpFunc.getSelectedContainerPy
        print "STATUS: " + str(stat)
        print errorMsg

        #smaya.mel.eval("sphere -radius 3;")
        #cmd = 'fluidExplorer - s1 4 -p "C:/TMP/FE_Simulations";'
        #print "STRING: " + cmd
        #maya.mel.eval(cmd)
        cr = CreateProjectDialog(self)
        cr.exec_()
		

    # Eventhandler - help button
    @QtCore.Slot()
    def buttonHelpMain_Event(self):
        print "[ Help Button clicked: " + "Help" + " ]"
        _url = self.url
        webbrowser.open(_url, new=1)


def main():

    # Check if a window has already been opened. if yes, close it. 
    # Otherwise create new maya main window for entering              
    if cmds.window("FluidExplorer",ex=True) == 1:
        cmds.deleteUI("FluidExplorer")

    # Initialize main window and show in maya
    myWin = ControlMainWindow( parent = getMayaWindow() )
    
    return myWin


# Main function
if __name__ == "__main__":

    
    print "[ FluidExplorer Plugin started ]"
    #submit_dialog()

    
    # Check if a window has already been opened. if yes, close it. 
    # Otherwise create new maya main window for entering              
    #if cmds.window("FluidExplorer",ex=True) == 1:
    #    cmds.deleteUI("FluidExplorer")
    
    # Initialize main window and show in maya
    #myWin = ControlMainWindow( parent = getMayaWindow() )
    myWin = main()
    myWin.show()
   