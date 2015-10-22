import sys
import webbrowser

from PySide import QtGui
from PySide import QtCore
from ui.MainWindow import Ui_MainWindow
from ui.FileOpenDialog import FileOpenDialog
from ui.CreateProjectDialog import CreateProjectDialog
from ui.DefaultUIValues import DefaultUIParameters
from ui.Icons import icons
import os


def main(argv):
    app = QtGui.QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


class MyMainWindow(QtGui.QMainWindow):

    def __init__(self,  *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) #self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)

        icons.qInitResources()
        self.createConnections()
        self.createButtonIcons()

        # Load the dark.orange stylesheet for the entire project (stored in ui/resources folder)
        f = open('ui/resources/darkorange.stylesheet', 'r')
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

        icon_win = QtGui.QIcon(QtGui.QPixmap(':/logo.png'))
        self.setWindowIcon(icon_win)
        self.setIconSize(QtCore.QSize(30, 30))

    @QtCore.Slot()
    def buttonLoadSimulation_Event(self):
        self.hide()
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
        currentSceneName = "E:/FluidExplorer_Code/Maya_Fluids/scene_1/scene1.mb"
        fileDialog = FileOpenDialog(self)
        fileDialog.openDirDialog(currentSceneName)  # fileDialog.openDirectoryDialog()
        self.show()

    @QtCore.Slot()
    def buttonNewProject_Event(self):
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)

        # createDialog = CreateProjectDialog(self) # TOTO delete the followig line
        createDialog = CreateProjectDialog(self, "TODO")
        createDialog.exec_()
        self.show()

    @QtCore.Slot()
    def buttonHelpMain_Event(self):
        print "[ Help Button clicked: " + "Help" + " ]"
        webbrowser.open(DefaultUIParameters.URL, new=1)

    def dirExists(self, path):
        exists = os.path.exists(path)
        return exists

# -- Call main function --
if __name__ == '__main__':
    print "[ FluidExplorer started ]"
    main(sys.argv)


