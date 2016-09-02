class ProjectSubSettings():

    def __init__(self):
        self.projectName = ''
        self.projectPath = ''
        self.mayaFilePath = ''
        self.fluidContainerName = ''
        self.animationStartTime = ''
        self.animationEndTime = ''
        self.numberOfSimulations = ''
        self.cam_persp = '0'    # 0/1
        self.cam_vc = '0'       # 0/1


class ExternalCallSetting():
    def __init__(self):
        self.pathToFluidExplorer = ''
        self.fluidExplorerCmd = ''
        self.fluidExplorerArgs = ''


import os,sys
import xml.etree.cElementTree as ET
import maya.cmds as cmds
import shlex
import subprocess


class ProjectDetailsViewUtils():

    def __init__(self):
        pass

    @staticmethod
    def readAttributeFromXmlConfigurationsFile(xml_file, childName):
        if os.path.exists(xml_file):
            try:
                tree = ET.ElementTree(file=xml_file)
                root = tree.getroot()

                for child in root:
                    if child.tag.lower() == childName.lower():
                        el_child_text = child.text
                        #print el_child_text
                        return el_child_text
            except Exception as e:
                print("Warning: Cannot read XML attribute")
                errorMsg = "Cannot read project attributes from confuration file! Details: " + str(e.message)
                raise Exception(errorMsg)
        else:
            raise Exception("Cannot find project configuration file")

    def getProjectSubSettings(self, xml_file):
        projectSettings = ProjectSubSettings()
        try:
            projectSettings.projectName = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'ProjectName')
            projectSettings.projectPath = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'ProjectPath')
            projectSettings.mayaFilePath = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'MayaFilePath')
            projectSettings.fluidContainerName = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'FluidBoxName')
            projectSettings.numberOfSimulations = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'Samples')
            projectSettings.animationStartTime = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'AnimationStartTime')
            projectSettings.animationEndTime = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'AnimationEndTime')
            projectSettings.cam_persp = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'PerspectiveCamera')
            projectSettings.cam_vc = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'ViewCubeCamera')

        except Exception as e:
            print "Error: Cannot read project attributes! Details: " + str(e.message)
            raise Exception(e.message)

        return projectSettings

    @staticmethod
    def getPathToXMLFile(path):
        list_dir = []
        files_xml = []
        list_dir = os.listdir(path)
        count = 0
        for file in list_dir:
            if file.endswith('xml'):
                count += 1
                tmp = path + file
                pathNew = os.path.abspath(tmp)
                files_xml.append(pathNew.replace('\\','/'))

        return files_xml

    @staticmethod
    def getGIFHashMap(projectSettings):
        hashMapToGIF = {}

        try:
            num = int(projectSettings.numberOfSimulations)
        except:
            num = 0

        if num > 0:
            for i in range(num):
                if projectSettings.cam_persp == '1':
                    tmp = '{0}/{1}/{2}/{3}/{4}'.format(projectSettings.projectPath, i, 'images', 'perspective', 'animation.gif')

                    path = os.path.abspath(tmp)
                    path = path.replace('\\', '/')
                    if os.path.exists(path):
                        print path
                        hashMapToGIF[i] = path

                elif projectSettings.cam_vc == '1':
                    tmp = '{0}/{1}/{2}/{3}/{4}/{5}'.format(projectSettings.projectPath, i, 'images', 'viewcube', 'front', 'animation.gif')
                    path = os.path.abspath(tmp)
                    path = path.replace('\\', '/')
                    if os.path.exists(path):
                        hashMapToGIF[i] = path

        return hashMapToGIF

    @staticmethod
    def setAnimationStartEndTime(start, end):
        canSetTime = True
        print start
        print end
        try:
            cmds.playbackOptions(animationStartTime=start)
            cmds.playbackOptions(animationEndTime=end)
        except Exception as e:
            print("Warning: Cannot set start/end time")
            print e.message
            canSetTime = False

        return canSetTime

    @staticmethod
    def checkIfProcessIsRunning_WIN(processnameArg):
        processFound = False

        # Check if windows is the os
        if sys.platform.startswith('win'):

            processname = processnameArg + '.exe'
            processFound = False

            tlcall = 'TASKLIST', '/FI', 'imagename eq %s' % processname
            # communicate() - gets the result of the tasklist command
            tlproc = subprocess.Popen(tlcall, shell=True, stdout=subprocess.PIPE)
            # trimming it to the actual lines with information
            tlout = tlproc.communicate()[0].strip().split('\r\n')
            # if TASKLIST returns single line without processname: process is not running
            if len(tlout) > 1 and processname in tlout[-1]:
                print('Process "%s" is running.' % processname)
                processFound = True
            else:
                print(tlout[0])
                print('Process "%s" is NOT running.' % processname)

        return processFound

    @staticmethod
    def killProcess_WIN(processnameArg):

        processname = processnameArg + '.exe'

        # Check if windows is os
        if sys.platform.startswith('win'):

            # Check if PF is running
            processFound = ProjectDetailsViewUtils.checkIfProcessIsRunning_WIN(processnameArg)

            if processFound:

                """
                # Close by number
                cmdProcessPidCmd = 'wmic process where caption=' + '\"' + processname + '\"' + ' get processid'
                cmdProcessPid = subprocess.Popen(cmdProcessPidCmd, stdout=subprocess.PIPE, shell=True)
                pid = cmdProcessPid.communicate()[0].strip().split('\r\n')

                print('Process PID: for "%s" found ' % processname)
                #for p in pid:
                #    print p
                """

                # Close the process
                try:
                    #processname = processnameArg + '.exe'
                    cmdStr = 'taskkill /im' + ' ' + processname
                    #os.system(cmdStr)
                    kill = subprocess.Popen(cmdStr, shell=True, stdout=subprocess.PIPE)
                    print('Process "%s" closed ' % processname)

                except Exception as e:
                    print('Error: Process "%s" not closed' % processname)
                    print('Details: "%s"' % e.message)
                    pass

    @staticmethod
    def checkIfProcessExistsAndClose(processName):
        ProjectDetailsViewUtils.killProcess_WIN(processName)

    @staticmethod
    def checkIfCorrectSceneIsOpened(currentScenePath, scenePathConfigFile):
        print 'CURRENT SCENE:' + str(currentScenePath)
        print 'MAYA SCENE:' + str(scenePathConfigFile)

        pr1 = ProjectDetailsViewUtils.getPrpjectNameFromString(currentScenePath)
        pr2 = ProjectDetailsViewUtils.getPrpjectNameFromString(scenePathConfigFile)

        print pr1
        print pr2

        if pr1 and pr2:
            if pr1.lower() == pr2.lower():
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def getPrpjectNameFromString(path):
        projectName = ''

        posSceneName = path.find('fluid_simulation_scene.mb')
        if not posSceneName == -1:
            tmp = path[0:posSceneName-1]
            print tmp
            pos = ProjectDetailsViewUtils.find(tmp, '/')
            print pos
            if pos >= 2:
                index = pos[len(pos)-1]
                print index
                projectName = path[index:posSceneName]
                if projectName.endswith('/'): projectName = projectName[0:len(projectName)-1]
                if projectName.startswith('/'): projectName = projectName[1:len(projectName)]

        return projectName

    @staticmethod
    def find(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]