import os
import subprocess

from PySide import QtGui
import maya.cmds as cmds
from FluidExplorerPlugin.ui.Utils.FluidExplorerUtils import FluidExplorerUtils
from FluidExplorerPlugin.ui.Utils.DefaultUIValues import DefaultUIParameters

class FileOpenDialog(QtGui.QDialog):

    global WORKING_DIRECTORY
    global FX_RELATIVE_PATH
    WORKING_DIRECTORY = cmds.workspace(q=True, dir=True)

    PATH_FLUIDEXPLORER_APP = "E:/FluidExplorer_Code/Release/"
    FX_RELATIVE_PATH = '/FluidExplorerPlugin/tmp/README.txt' 

    def openSimulation(self, choosenFile, fxPathRoot):
        # choosenFile: Path to the .fxp file
        # fxPathRoot: script folder

        #print WORKING_DIRECTORY
        #print fxPathRoot

        if not os.path.exists(self.PATH_FLUIDEXPLORER_APP):
            errorMsg = "Cannot find the FluidExplorer application executable!" + "\n" + "Please check if  the executable file is available."
            self.showMessageBox(errorMsg, 'warning')

        else:
            simulationDataPath = self.readSimulationDataPath(choosenFile)
            try:
                path = os.getcwd()
                os.chdir(self.PATH_FLUIDEXPLORER_APP)

                # Path to the raw data for the fluid explorer
                str_load_path = "/load path=" + simulationDataPath

                # Path to the settings file
                str_settings_path = "/load path=" + choosenFile

                print("Open FluidExplorer application ...", "")
                print("   Load Path    : ", str_load_path)  # -> /load path=E:/FluidExplorer_Code/FlameShape//FlameShape1
                print("   Settings File: ", str_settings_path)  # -> E:/TMP/test.fxp
                
                # Call Subprocess
                pid = subprocess.Popen(["fluidexplorer.exe", str_load_path], shell=True) # call subprocess


            except Exception as e:

                errorMsg = "Unable to start the FluidExplorer application!" + "\nDetails: " + e.message
                self.showMessageBox(errorMsg, 'critical')

                os.chdir(os.path.abspath(path))

            finally:
                subprocess._cleanup()

            # Return back to root directory
            os.chdir(os.path.abspath(path))
            print("Changed directory back after calling FluidExplorer app: ", os.path.abspath(path))

            # TODO 
            # Open Port
            # FluidExplorerUtils.openMayaPort()

    def checkPrjRoot(self, choosenDir, currentScene):
        isSameScene = True
        isNumberOk = True
        canReadConfigFile = True

        try:
            tmpSimulationName = FluidExplorerUtils.readAttributeFromXmlConfigurationsFile(choosenDir, 'MayaFilePath')
            print("Path of the maya file to load: ", tmpSimulationName)
        except:
            canReadConfigFile = False
            errorText = "An error occured while loading the project file!"
            return [canReadConfigFile, isNumberOk, isSameScene, errorText ]

        if tmpSimulationName == "" or tmpSimulationName == None:
            canReadConfigFile = False
            errorText = "An error occured while loading the project file!\nProperty: 'MayaFilePath'"
            return [canReadConfigFile, isNumberOk, isSameScene, errorText ]

        # Check if same scene opened
        tmpSimulationName_low = tmpSimulationName.lower()
        currentScene_low = currentScene.lower()

        if tmpSimulationName_low != currentScene_low:
            isSameScene = False
            errorTxt = "Please load the correct maya scene file first!\nPath: " + tmpSimulationName

            return [canReadConfigFile, isNumberOk, isSameScene, errorTxt]

        return [canReadConfigFile, isNumberOk, isSameScene, ""]

    def openDirDialog(self, currentSceneName, fxPathRoot):

        # currentSceneName: e.g. E:/Tmp/test.mb
        # fxPathRoot: e.g.: .../maya/2014-x64/scripts
        print("")
        print("Load Animation", "")
        print("")

        strStarted = "started"

        dialog = QtGui.QFileDialog(self)
        dialog.setWindowTitle(self.tr("Fluid Explorer - Choose Project Directory"))
        dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        dialog.setNameFilter("Fluid Explorer Project (*.fxp)")
        dialog.setDirectory(WORKING_DIRECTORY)
        dialog.setViewMode(QtGui.QFileDialog.List) # or Detail

        if dialog.exec_():

            selectedFile = dialog.selectedFiles()
            if len(selectedFile) == 1:
                choosenDir = selectedFile[0]
                
                # Get the current maya scene name
                [canReadConfigFile, isNumberOk, isSameScene, errorText] = self.checkPrjRoot(choosenDir, currentSceneName)
              
                if not canReadConfigFile:
                    # Can not read xml project file with
                    self.showMessageBox(errorText, 'critical')

                else:
                    if not isSameScene:
                        # Warning - not the same scene is loaded
                        self.showMessageBox(errorText, 'warning')
                        return

                    # Check if the fluid container exists in the scene
                    [nodeExists, errorMsg] = self.checkIfFluidNodeExistsInScene(choosenDir)
                    if not nodeExists:
                        self.showMessageBox(errorMsg, 'warning')
                        return

                    #        # Warning scene is loaded
                    #        self.showMessageBox(errorText, 'warning')

                    else:
                        try:
                            import exceptions

                            fluidExplorerPath = self.getFXPath(fxPathRoot, FX_RELATIVE_PATH)

                            if not fluidExplorerPath == "":
                                self.openSimulation(choosenDir, fxPathRoot)
                            else:
                                raise Exception("FluidExplorer executable file not found!")
                            
                            # return "started"

                        except Exception as e:
                            errorMsg = "Unable to start the FluidExplorer application!" + "\nDetails: " + e.message
                            self.showMessageBox(errorMsg, 'critical')

                        return strStarted   # return started -> everything fine!

    def readSimulationDataPath(self, choosenDir):
        try:
            tmpProjectName = FluidExplorerUtils.readAttributeFromXmlConfigurationsFile(choosenDir, 'ProjectName')
            tmpProjectPath = FluidExplorerUtils.readAttributeFromXmlConfigurationsFile(choosenDir, 'ProjectPath')

        except:
            return ""

        path = tmpProjectPath + '/' + tmpProjectName
        return path

    def getFXPath(self, fxPathRoot, fxRelativePath):
        fullPathToFluidExplorer = ""
       
        tmpPath = fxPathRoot + fxRelativePath
        if os.path.exists(tmpPath):
            fullPathToFluidExplorer = tmpPath

        return fullPathToFluidExplorer

    def checkIfFluidNodeExistsInScene(self, choosenFile):
        tmpFluidNodeName = FluidExplorerUtils.readAttributeFromXmlConfigurationsFile(choosenFile, 'FluidBoxName')
        print("Fluid container name from the settings file ", tmpFluidNodeName)

        if cmds.objExists(tmpFluidNodeName):
            return [True, ""]
        else:
            return [False, "Cannot find the specified Fluid Container in the opened project!\n"
                           "Please check if the the node '" + tmpFluidNodeName + "' exists."]

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

    # The dialog to get to the directory of the simulations
    def openDirDialogQuick(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setWindowTitle(self.tr("Fluid Explorer - Choose Project Directory"))
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dir = cmds.workspace(q=True, dir=True)
        dialog.setDirectory(dir)
        dialog.setViewMode(QtGui.QFileDialog.List) # or Detail

        if dialog.exec_():
            fileSelected= dialog.selectedFiles()
            if len(fileSelected) == 1:
                choosenDir = fileSelected[0]

                isOk = True
                if isOk:
                    return choosenDir
                else:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("Please select a valid directory!")
                    msgBox.setWindowTitle("Warning - Load Simulation")
                    msgBox.setIcon(QtGui.QMessageBox.Warning)
                    msgBox.setStyleSheet(DefaultUIParameters.buttonStyleBold)
                    msgBox.exec_()

