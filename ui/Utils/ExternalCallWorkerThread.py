import shlex
import subprocess
import os
from PySide import QtCore


class WorkThread(QtCore.QThread):

    def __init__(self, externalCallSettings):
        QtCore.QThread.__init__(self)
        self.running = True
        self.SEARCH_PATTERN_CMD = 'PATRICK'

        self.pathToFXApp = externalCallSettings.pathToFluidExplorer
        self.cmdFXAPP = externalCallSettings.fluidExplorerCmd
        self.cmdFXArg = externalCallSettings.fluidExplorerArgs

    def run(self):
        """
        #os.chdir('E:/Workspace_VisualStudio/fluidexplorer/Backup/fluidexplorer/bin/Win32/Debug/')
        #a = "/load path=E:\FluidExplorer_Code\FlameShape\FlameShape1"
        #cmd = 'E:/Workspace_VisualStudio/fluidexplorer/Backup/fluidexplorer/bin/Win32/Debug/fluidExplorer.exe'
        os.chdir(self.pathToFXApp)
        #process = subprocess.Popen([shlex.split(self.cmdFXAPP), self.cmdFXArg], stdout=subprocess.PIPE, shell=False)
        process = subprocess.Popen(["fluidexplorer.exe", self.cmdFXArg], stdout=subprocess.PIPE, shell=False) # call subprocess
        #subprocess._cleanup()

        while self.running:

            output = process.stdout.readline()
            if output.startswith(self.SEARCH_PATTERN_CMD):
                print ""
                print "##########################"
                print "#         CALL           #"
                print "##########################"
                print ""

                # ------------------------------------------------------------------------------------------------------
                # Send signal to the plugin which created the worker thread
                import random
                changeIndexStr = random.randint(1, 5)
                self.emit(QtCore.SIGNAL('update(QString)'), str(changeIndexStr))
                # ------------------------------------------------------------------------------------------------------

            if output == '' and process.poll() is not None:
                break

            if output:
                print output.strip()

        rc = process.poll()
        return rc
        """
        """
        print "1"
        if not os.path.exists(self.pathToFXApp):
            print "3"
            errorMsg = "Cannot find the FluidExplorer application executable!" + "\n" + "Please check if  the executable file is available."
            self.showMessageBox(errorMsg, 'warning')

        else:
            print "2"
            #simulationDataPath = self.readSimulationDataPath(choosenFile)
            try:
                path = os.getcwd()
                os.chdir(self.pathToFXApp)

                # Path to the raw data for the fluid explorer
                #str_load_path = "/load path=" + simulationDataPath

                # Path to the settings file
                #str_settings_path = "/load path=" + choosenFile

                print("Open FluidExplorer application ...", "")
                #print("   Load Path    : ", str_load_path)  # -> /load path=E:/FluidExplorer_Code/FlameShape//FlameShape1
                #print("   Settings File: ", str_settings_path)  # -> E:/TMP/test.fxp

                # Call Subprocess
                pid = subprocess.Popen(["fluidexplorer.exe", self.cmdFXArg], stdout=subprocess.PIPE, shell=True) # call subprocess

                print "FluidExplorer started ..."


            except Exception as e:

                errorMsg = "Unable to start the FluidExplorer application!" + "\nDetails: " + e.message
                self.showMessageBox(errorMsg, 'critical')

                #os.chdir(os.path.abspath(path))

            finally:
                subprocess._cleanup()

            # Return back to root directory
            #os.chdir(os.path.abspath(path))
            print("Changed directory back after calling FluidExplorer app: ", os.path.abspath(path))
        """

        currentDir = os.getcwd()

        try:
            os.chdir(self.pathToFXApp)
            process = subprocess.Popen([shlex.split(self.cmdFXAPP), self.cmdFXArg], shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            print("Error: Cannot execute open fluid explorer app!")
            print("Details:", e.message)
            self.emit(QtCore.SIGNAL('update(QString)'), "ERROR")
            return

        finally:
            os.chdir(currentDir)

        while self.running:

            output = process.stdout.readline()
            if output.startswith('PATRICK'):

                print "-----------------"
                print "NICE"
                print "-----------------"

            if output == '' and process.poll() is not None:
                break
            if output:
                print output.strip()
        rc = process.poll()
        return rc

    def stop(self):
        # Stop the loop
        self.running = False