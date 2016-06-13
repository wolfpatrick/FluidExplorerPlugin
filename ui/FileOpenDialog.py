import os
import maya.cmds as cmds

from PySide import QtGui
from FluidExplorerPlugin.ui.Utils.FluidExplorerUtils import FluidExplorerUtils


class FileOpenDialog(QtGui.QDialog):

    global buttonStyleBold
    buttonStyleBold = "QMessageBox { }" #font-size: 12px;

    global WORKING_DIRECTORY
    global FX_RELATIVE_PATH
    WORKING_DIRECTORY = os.getcwd()
    PATH_FLUIDEXPLORER_APP = "E:/FluidExplorer_Code/Releas/"
    FX_RELATIVE_PATH = '/FluidExplorerPlugin/tmp/README.txt' 

    
    def openSimulation(self, choosenFile):
        import subprocess
       
        if not os.path.exists(self.PATH_FLUIDEXPLORER_APP):
            msgBox = QtGui.QMessageBox()
            errorMsg = "Unable to start the Fluid Explorer application!" + "\n" + "Please check if the executable file is available."
            msgBox.setText(errorMsg)
            msgBox.setWindowTitle("Warning - Start Fluid Explorer")
            msgBox.setIcon(QtGui.QMessageBox.Warning)
            msgBox.setStyleSheet(buttonStyleBold)
            msgBox.exec_()

        else:
            simulationDataPath = self.readSimulationDataPath(choosenFile)
            
            try:
                path = os.getcwd()
                os.chdir(self.PATH_FLUIDEXPLORER_APP)

                # Path to the raw data for the fluid explorer
                str_load_path = "/load path=" + simulationDataPath

                # Path to the settings file
                str_settings_path = "/load path=" + choosenFile
                
                print("Load Path    : ", str_load_path)         # -> /load path=E:/FluidExplorer_Code/FlameShape//FlameShape1
                print("Settings File: ", str_settings_path)     # -> E:/TMP/test.fxp
                
                #
                pid = subprocess.Popen(["fluidexplorer.exe", str_load_path], shell=True) # call subprocess
                #print pid
                #

            except Exception as e:
               
                msgBox = QtGui.QMessageBox()
                errorMsg = "Unable to start the Fluid Explorer application!" + "\nDetails: " + e.message
                msgBox.setText(errorMsg)
                msgBox.setWindowTitle("Error - Start Fluid Explorer")
                msgBox.setIcon(QtGui.QMessageBox.Critical)
                msgBox.setStyleSheet(buttonStyleBold)
                msgBox.exec_()
            finally:
                subprocess._cleanup()
               
            os.chdir(path)

            # TODO 
            # Open Port
            #FluidExplorerUtils.openMayaPort()


    def checkPrjRoot(self, choosenDir, currentScene):
        isSameScene = True
        isNumberOk = True
        canReadConfigFile = True

        try:
            tmpSimulationName = FluidExplorerUtils.readAttributeFromXmlConfigurationsFile(choosenDir, 'MayaFile')
        except:
            canReadConfigFile = False
            errorText = "Error while reading the project file!"
            return [ canReadConfigFile, isNumberOk, isSameScene, errorText ]


        if tmpSimulationName == "" or tmpSimulationName == None:
            canReadConfigFile = False
            errorText = "Error while reading the project file properties!"
            return [ canReadConfigFile, isNumberOk, isSameScene, errorText ]

        """
        # Check numner of samples
        dirname, filename = os.path.split(os.path.abspath(choosenDir))
        file_list = next(os.walk(dirname))[1]

       
        #numDirs = 0
        #for index, item in enumerate(file_list):
        #    #print str(index) + " " + str(item)
        #    tmp = str(item)
        #    if not tmp.startswith('.'):
        #        numDirs += 1;

        #if int(tmpNumberSamples) != int(numDirs):
        #    print "Not the same number of Samples!"
        #    errorTxt = "Not the same number of Samples!"
        #    isNumberOk = False
        """

        # Check if same scene opened
        tmpSimulationName_low = tmpSimulationName.lower()
        currentScene_low = currentScene.lower()

        if tmpSimulationName_low != currentScene_low:
            isSameScene = False
            errorTxt = "Please load the correct scene first\nPath: " + tmpSimulationName + "."

            return [ canReadConfigFile, isNumberOk, isSameScene, errorTxt ]

        return [ canReadConfigFile, isNumberOk, isSameScene, "" ]


    def openDirDialog(self, currentSceneName, fxPathRoot):
        # currentSceneName: e.g. E:/Tmp/test.mb
        # fxPath: e.g.: .../maya/2014-x64/scripts

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
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText(errorText)
                    msgBox.setWindowTitle("Error - Load Project")
                    msgBox.setIcon(QtGui.QMessageBox.Critical)
                    msgBox.setStyleSheet(buttonStyleBold)
                    msgBox.exec_()

                else:
                    if not isSameScene:
                            # TODO : MessageBox - Open the right file...
                            msgBox = QtGui.QMessageBox()
                            msgBox.setText(errorText)
                            msgBox.setWindowTitle("Warning - Load Project")
                            msgBox.setIcon(QtGui.QMessageBox.Warning)
                            msgBox.setStyleSheet(buttonStyleBold)
                            msgBox.exec_()
                    else:
                        try:
                            import exceptions

                            fluidExplorerPath = self.getFXPath(fxPathRoot, FX_RELATIVE_PATH)

                            if not fluidExplorerPath == "":
                                self.openSimulation(choosenDir)
                            else:
                                raise Exception("Fluid Explorer executable file not found")
                            
                            # return "started"

                        except Exception as e:
                            msgBox = QtGui.QMessageBox()
                            errorMsg = "Unable to start the Fluid Explorer application!" + "\nDetails: " + e.message
                            msgBox.setText(errorMsg)
                            msgBox.setWindowTitle("Error - Load Project")
                            msgBox.setIcon(QtGui.QMessageBox.Critical)
                            msgBox.setStyleSheet(buttonStyleBold)
                            msgBox.exec_()

                        #FluidExplorerUtils.openMayaPort()
                        return strStarted   # return started -> everything fine!


    def openDirDialogQuick(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setWindowTitle(self.tr("Fluid Explorer - Choose Project Directory"))
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dir = cmds.workspace(q=True, dir=True)
        dialog.setDirectory(dir)
        dialog.setViewMode(QtGui.QFileDialog.List) # or Detail

        if dialog.exec_():
            fileA = dialog.selectedFiles()
            if  len(fileA) == 1:
                choosenDir = fileA[0]
                
                isOk = True
                if isOk:
                    return choosenDir
                else:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText("Please select a valid directory!")
                    msgBox.setWindowTitle("Warning - Load Project")
                    msgBox.setIcon(QtGui.QMessageBox.Warning)
                    msgBox.setStyleSheet(buttonStyleBold)
                    msgBox.exec_()


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