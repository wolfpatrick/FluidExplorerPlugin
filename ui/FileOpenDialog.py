from PySide import QtGui
import os
from FluidExplorerPlugin.ui.Utils.FluidExplorerUtils import FluidExplorerUtils
#from ui.Utils.FluidExplorerUtils import FluidExplorerUtils


class FileOpenDialog(QtGui.QDialog):

    global WORKING_DIRECTORY
    WORKING_DIRECTORY = os.getcwd()

    def openDirectoryDialog(self, version):
        flags = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Fluid Explorer - Choose Project Directory"), os.getcwd(), flags)
        if directory:
            print "[ Selected directory: " + directory + " ]"
            self.openSimulation()
        else:
            print "[ No directory selected ]"

    def openSimulation(self):
        # subprocess.call(["E:/FluidExplorer_Code/Release/fluidexplorer.exe"], shell=True)
        path = os.getcwd()
        os.chdir("E:/FluidExplorer_Code/Release/")
        os.system("fluidexplorer.exe")
        os.chdir(path)

    def checkPrjRoot(self, choosenDir, currentScene):
        isSameScene = True
        isNumberOk = True
        canReadConfigFile = True

        try:
            tmpSimulationName = FluidExplorerUtils.readAttributeFromConfigurationFile(choosenDir, 'default_settings', 'SimulatioNname')
            tmpNumberSamples = FluidExplorerUtils.readAttributeFromConfigurationFile(choosenDir,  'default_settings', 'NumberSamples')
            tmpNumberSamples = int(tmpNumberSamples)
        except:
            canReadConfigFile = False
            return [canReadConfigFile, isNumberOk, isSameScene]

        # Check numner of samples
        dirname, filename = os.path.split(os.path.abspath(choosenDir))
        file_list = next(os.walk(dirname))[1]

        numDirs = 0
        for index, item in enumerate(file_list):
            #print str(index) + " " + str(item)
            tmp = str(item)
            if not tmp.startswith('.'):
                numDirs += 1;

        if int(tmpNumberSamples) != int(numDirs):
            print "Not the same number of Samples!"
            errorTxt = "Not the same number of Samples!"
            isNumberOk = False

        # Check if same scene opened
        tmpSimulationName_low = tmpSimulationName.lower()
        currentScene_low = currentScene.lower()
        if tmpSimulationName_low != currentScene_low :
            print "Not the same scene is open!"
            errorTxt = "Not the same scene is open!"
            isSameScene = False

        return [canReadConfigFile, isNumberOk, isSameScene]

    def openDirDialog(self, currentSceneName):

        dialog = QtGui.QFileDialog(self)
        dialog.setWindowTitle(self.tr("Fluid Explorer - Choose Project Directory"))
        dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        dialog.setNameFilter("FluidExplorer Project (*.fxp)")
        dialog.setDirectory(WORKING_DIRECTORY)
        dialog.setViewMode(QtGui.QFileDialog.List) # or Detail

        if dialog.exec_():

            fileA = dialog.selectedFiles()
            if len(fileA) == 1:
                choosenDir = fileA[0]
                print "[ Selected directory: " + choosenDir + " ]"
                # Get the current maya scene name
                [canReadConfigFile, isNumberOk, isSameScene] = self.checkPrjRoot(choosenDir, currentSceneName)

                if not canReadConfigFile:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("Error while reading the project file!")
                    msgBox.setWindowTitle("Warning - Load Project")
                    msgBox.setIcon(QtGui.QMessageBox.Critical)
                    msgBox.exec_()
                else:
                    if not isNumberOk:
                            msgBox = QtGui.QMessageBox()
                            msgBox.setText("NUMBEr!")
                            msgBox.setWindowTitle("Warning - Load Project")
                            msgBox.setIcon(QtGui.QMessageBox.Warning)
                            msgBox.exec_()
                    else:
                        try:
                            self.openSimulation()
                        except:
                            msgBox = QtGui.QMessageBox()
                            msgBox.setText("Cannot start FluidExplorer application!")
                            msgBox.setWindowTitle("Error - Load Project")
                            msgBox.setIcon(QtGui.QMessageBox.Critical)
                            msgBox.exec_()

    def openDirDialogQuick(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setWindowTitle(self.tr("Fluid Explorer - Choose Project Directory"))
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dialog.setDirectory(WORKING_DIRECTORY)
        dialog.setViewMode(QtGui.QFileDialog.List) # or Detail

        if dialog.exec_():
            fileA = dialog.selectedFiles()
            if  len(fileA) == 1:
                choosenDir = fileA[0]
                print "[ Selected directory: " + choosenDir + " ]"
                isOk = True
                if isOk:
                    return choosenDir
                else:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("Please select a valid directory!")
                    msgBox.setWindowTitle("Warning - Load Project")
                    msgBox.setIcon(QtGui.QMessageBox.Warning)
                    msgBox.exec_()