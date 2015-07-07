__author__ = 'patrick'

#!/usr/bin/python

# Import PySide classes
import sys
import webbrowser

from PySide import QtGui
from PySide import QtCore
from PySide import QtDeclarative
from ui.MainWindow import Ui_MainWindow
from ui.FileOpenDialog import FileOpenDialog
from ui.CreateProjectDialog import CreateProjectDialog
from ui.ParameterInputBoxes import ParameterInputBoxes
from ui.icons import icons
from ui.icons import logo
import os


def main(argv):
    print "dadas"
    app = QtGui.QApplication(sys.argv)

    mainWindow = MyMainWindow()
    mainWindow.show()

    #view = QtDeclarative.QDeclarativeView(mainWindow)
    #view.setResizeMode(QtDeclarative.QDeclarativeView.SizeViewToRootObject)
    #view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    sys.exit(app.exec_())


class MyMainWindow(QtGui.QMainWindow):

    def __init__(self,  *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.createConnections()
        #self.setWindowIcon(QtGui.QIcon('a.png'))
        self.createButtonIcons()

        f = open('ui/icons/darkorange.stylesheet', 'r')
        styleData = f.read()
        f.close()
        self.setStyleSheet(styleData)

    def createConnections(self):
        self.ui.pushButtonLoadSimulation.clicked.connect(self.buttonLoadSimulation_Event)
        self.ui.pushButtonNewProject.clicked.connect(self.buttonNewProject_Event)
        self.ui.pushButtonHelpMain.clicked.connect(self.buttonHelpMain_Event)

    def createButtonIcons(self):

        icon_open = QtGui.QIcon(QtGui.QPixmap(':/icon_open_30px.png'))
        icon_create = QtGui.QIcon(QtGui.QPixmap(':/icon_add_30px.png'))
        icon_help = QtGui.QIcon(QtGui.QPixmap(':/icon_help_30px.png'))

        self.ui.pushButtonNewProject.setIcon(icon_create)
        self.ui.pushButtonLoadSimulation.setIcon(icon_open)
        self.ui.pushButtonHelpMain.setIcon(icon_help)

        # Window icon

        icon_win = QtGui.QIcon(QtGui.QPixmap(':/logo.png'))

        self.setWindowIcon(icon_win)
        self.setIconSize(QtCore.QSize(30,30))

    @QtCore.Slot()
    def buttonLoadSimulation_Event(self):

        """
        path = "E:\Literatur\?"
        pr = "Untitled"

        dirExists = self.dirExists(path)
        if (dirExists):
            print "WARNING: Directory already exists!"
        else:
            try:
                os.mkdir(path)
            except:
                print "WARNING: Please check name of directory!"
        print "RES: " + str(dirExists)
        """
        print "[ Button clicked: " + self.sender().text() + "]"
        fileDialog = FileOpenDialog(self)
        #fileDialog.openDirectoryDialog()
        fileDialog.openDirDialog()


    @QtCore.Slot()
    def buttonNewProject_Event(self):
        print "[ Button clicked: " + self.sender().text() + "]"
        createDialog = CreateProjectDialog(self)
        createDialog.exec_()
        #createDialog = QtGui.QDialog(self)
        #ui_dialog = Ui_CreateProjectDialog()
        #ui_dialog.setupUi(createDialog)
        #createDialog.exec_()

    @QtCore.Slot()
    def buttonHelpMain_Event(self):
        print "[ Help Button clicked: " + "Help" + " ]"
        url = "http://google.de"
        webbrowser.open(url, new=1)

    def dirExists(self, path):
        exists = False
        exists = os.path.exists(path)
        return exists


# call main function
if __name__ == '__main__':
    print "[ FluidExplorer started ]"




    from ui.MayaCacheCommandParameters import MayaCacheCommand

    cmd = MayaCacheCommand()
    cmd.outputPath = "test"

    cmd.densityDissipationFLAG = True
    cmd.densityBuoyancyFLAG = True
    cmd.viscosityFLAG = True
    cmd.densityDiffusionFLAG = True
    cmd.viscosityFLAG = True
    cmd.velocitySwirlFLAG = False
    cmd.turbulenceFrequencyFLAG = True
    cmd.turbulenceSpeedFLAG = True
    cmd.turbulenceStrengthFLAG = True

    print "Value: " + str(cmd.outputPath)
    print "Value: " + str(cmd.numberSamples)

    print "Value: " + str(cmd.densityDissipationFLAG)
    print "Value: " + str(cmd.densityBuoyancyFLAG)
    print "Value: " + str(cmd.viscosityFLAG)
    print "Value: " + str(cmd.turbulenceStrengthFLAG)
    print "Value: " + str(cmd.turbulenceFrequencyFLAG)
    print "Value: " + str(cmd.turbulenceSpeedFLAG)
    print "Value: " + str(cmd.turbulenceStrengthFLAG)
    print "Value: " + str(cmd.velocitySwirlFLAG)


    print "Value1: " + str(cmd.densityBuoyancy)
    print "Value1: " + str(cmd.densityDissipation)
    print "Value1: " + str(cmd.densityDiffusion)

    print "Value1: " + str(cmd.viscosity)

    print "Value1: " + str(cmd.velocitySwirl)

    print "Value11: " + str(cmd.turbulenceStrength)
    print "Value12: " + str(cmd.turbulenceSpeed)
    print "Value31: " + str(cmd.turbulenceFrequency)

    cmdStr = cmd.createMELCommand(cmd)
    print "The Command: " + cmdStr


    a = True
    b = False

    print "BOOL: " + str((a and b))
    main(sys.argv)

