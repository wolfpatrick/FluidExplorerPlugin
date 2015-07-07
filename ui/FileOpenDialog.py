__author__ = 'Patrick'

import os
import  subprocess

from PySide import QtGui
from PySide import QtCore

class FileOpenDialog(QtGui.QDialog):

    global WORKING_DIRECTORY
    WORKING_DIRECTORY = os.getcwd()

    def openDirectoryDialog(self, version):


        """
        Opens a dialog to allow user to choose a directory
        """
        flags = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Fluid Explorer - Choose Project Directory"),
                                                           os.getcwd(), flags)
        if directory:
            print "[ Selected directory: " + directory + " ]"
            self.openSimulation()

        else:
            print "[ No directory selected ]"

    def openSimulation(self):
        print "[ Open Simulation ]"

        #subprocess.call(["E:/FluidExplorer_Code/Release/fluidexplorer.exe"], shell=True)
        print os.getcwd()
        path = os.getcwd()
        os.chdir("E:/FluidExplorer_Code/Release/")
        os.system("fluidexplorer.exe")
        #subprocess.call(["fluidexplorer.exe"])
        os.chdir(path)
        print os.getcwd()

    def checkPrjRoot(self):
        isOk = False

        # TODO check if directory is ok
        if (1==1):
            isOk = True

        return isOk


    def openDirDialog(self):

        dialog = QtGui.QFileDialog(self)
        dialog.setWindowTitle(self.tr("Fluid Explorer - Choose Project Directory"))
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dialog.setDirectory(WORKING_DIRECTORY)
        dialog.setViewMode(QtGui.QFileDialog.List) # or Detail
        #dialog.setWindowIcon(QtGui.QIcon(self.tr("ui/icons/icon_add_30px.png")))

        if dialog.exec_():

            #self._playlistview.addElements(dialog.selectedFiles()) ??
            fileA  = dialog.selectedFiles()
            print len(fileA)
            if  ( len(fileA) == 1 ) :
                choosenDir = fileA[0]
                print "[ Selected directory: " + choosenDir + " ]"

                isOk = self.checkPrjRoot()
                if (isOk == True):
                    print "ok"
                    self.openSimulation()
                else:
                    print "not ok..."
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("Please select a valid directory!")
                    msgBox.setWindowTitle("Warning - Load Project")
                    msgBox.setIcon(QtGui.QMessageBox.Warning)
                    msgBox.exec_()

    def openDirDialogQuick(self):

        dialog = QtGui.QFileDialog(self)
        dialog.setWindowTitle(self.tr("Fluid Explorer - Choose Project Directory"))
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dialog.setDirectory(WORKING_DIRECTORY)
        dialog.setViewMode(QtGui.QFileDialog.List) # or Detail
        #dialog.setWindowIcon(QtGui.QIcon(self.tr("ui/icons/icon_add_30px.png")))

        if dialog.exec_():

            #self._playlistview.addElements(dialog.selectedFiles()) ??
            fileA  = dialog.selectedFiles()
            if  ( len(fileA) == 1 ) :
                choosenDir = fileA[0]
                print "[ Selected directory: " + choosenDir + " ]"

                isOk = True
                if (isOk == True):
                    print "ok"
                    return choosenDir

                else:
                    print "not ok"
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("Please select a valid directory!")
                    msgBox.setWindowTitle("Warning - Load Project")
                    msgBox.setIcon(QtGui.QMessageBox.Warning)
                    msgBox.exec_()