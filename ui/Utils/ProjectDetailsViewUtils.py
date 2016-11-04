import os
import sys
import xml.etree.cElementTree as ET
import subprocess
import logging

import maya.cmds as cmds


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
        self.fluidExplorerArgs = ''


class ProjectDetailsViewUtils():

    def __init__(self):
        self.lgr = logging.getLogger('FluidExplorerPlugin')
        pass

    @staticmethod
    def readAttributeFromXmlConfigurationsFile(xml_file, childName):
        lgr = logging.getLogger('FluidExplorerPlugin')

        if os.path.exists(xml_file):
            try:
                tree = ET.ElementTree(file=xml_file)
                root = tree.getroot()

                for child in root:
                    if child.tag.lower() == childName.lower():
                        el_child_text = child.text
                        return el_child_text
            except Exception as e:
                lgr.warning('Cannot read XML attribute')
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
            errorTxt = "Cannot read project attributes! Details: " + str(e.message)
            self.lgr.error(errorTxt)
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
        lgr = logging.getLogger('FluidExplorerPlugin')

        canSetTime = True
        try:
            cmds.playbackOptions(animationStartTime=start)
            cmds.playbackOptions(animationEndTime=end)
            lgr.info('Set animation start time: %s', start)
            lgr.info('Set animation end time: %s', end)
        except Exception as e:
            logging.warning("Cannot set start/end time: %s", e.message)
            canSetTime = False

        return canSetTime

    @staticmethod
    def checkIfProcessIsRunning_WIN(processnameArg):
        lgr = logging.getLogger('FluidExplorerPlugin')

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
                lgr.info('Process "%s" is running', processname)
                processFound = True
            else:
                lgr.info('%s', str(tlout[0]))
                lgr.info('Process "%s" is NOT running', processname)

        return processFound

    @staticmethod
    def checkIfProcessExistsAndClose(processName):
        if ProjectDetailsViewUtils != None:
            ProjectDetailsViewUtils.killProcess_WIN(processName)

    @staticmethod
    def checkIfCorrectSceneIsOpened(currentScenePath, scenePathConfigFile):
        lgr = logging.getLogger('FluidExplorerPlugin')

        lgr.info('Current scene: %s', str(currentScenePath))
        lgr.info('Maya scene: %s', str(scenePathConfigFile))

        pr1 = ProjectDetailsViewUtils.getPrpjectNameFromString(currentScenePath)
        pr2 = ProjectDetailsViewUtils.getPrpjectNameFromString(scenePathConfigFile)

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
            pos = ProjectDetailsViewUtils.find(tmp, '/')

            if pos >= 2:
                index = pos[len(pos)-1]
                projectName = path[index:posSceneName]
                if projectName.endswith('/'): projectName = projectName[0:len(projectName)-1]
                if projectName.startswith('/'): projectName = projectName[1:len(projectName)]

        return projectName

    @staticmethod
    def find(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]


    @staticmethod
    def getPathFluidExplorer():
        filePathMain = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filePathMainParent = os.path.abspath(os.path.join(os.path.dirname(filePathMain)))
        filename = os.path.join(filePathMainParent, 'lib/fluidexplorer/')
        fxPathRel = os.path.abspath(filename)

        '''
        if sys.platform.startswith('win'):
            fxPathRel = fxPathRel + '/fluidexplorer.exe'
            fxPathRel = os.path.abspath(fxPathRel)
        elif sys.platform.startswith(''):
            # TODO: UNIX
            pass
        '''

        return fxPathRel

    @staticmethod
    def getPathSettingsFile():
        pass

    @staticmethod
    def getPathCacheFiles(pathFromDialog):
        # Parent directory
        parDir = os.path.dirname(pathFromDialog)
        # print parDir

        return parDir