import os
import sys
import xml.etree.cElementTree as ET
import subprocess
import logging

from FluidExplorerPlugin.ui.Utils.RangeSliderSpan import FluidContainerValues
from FluidExplorerPlugin.ui.Utils.FluidExplorerUtils import FluidExplorerUtils

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
            projectSettings.cam_custom = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'CustomCamera')
            projectSettings.cam_rotation = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'RotationCamera')

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
    def getGIFHashMap(projectSettings, projectPath):
        hashMapToGIF = {}

        try:
            num = int(projectSettings.numberOfSimulations)
        except:
            num = 0

        if num > 0:
            for i in range(num):
                if projectSettings.cam_persp == '1':
                    tmp = '{0}/{1}/{2}/{3}/{4}'.format(projectPath, i, 'images', 'perspective', 'animation.gif')

                    path = os.path.abspath(tmp)
                    path = path.replace('\\', '/')
                    if os.path.exists(path):
                        hashMapToGIF[i] = path

                elif projectSettings.cam_vc == '1':
                    tmp = '{0}/{1}/{2}/{3}/{4}/{5}'.format(projectPath, i, 'images', 'viewcube', 'front', 'animation.gif')
                    path = os.path.abspath(tmp)
                    path = path.replace('\\', '/')
                    if os.path.exists(path):
                        hashMapToGIF[i] = path

                elif projectSettings.cam_custom != 'None':
                    tmp = '{0}/{1}/{2}/{3}/{4}'.format(projectPath, i, 'images', 'custom', 'animation.gif')
                    path = os.path.abspath(tmp)
                    path = path.replace('\\', '/')
                    if os.path.exists(path):
                        hashMapToGIF[i] = path

                elif projectSettings.cam_rotation != '0':
                    tmp = '{0}/{1}/{2}/{3}/{4}'.format(projectPath, i, 'images', 'rotation_0', 'animation.gif')
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
        print "patrick"
        if ProjectDetailsViewUtils != None:
            print "patrick w"
            ProjectDetailsViewUtils.killProcess_WIN(processName)
            FluidExplorerUtils.killProcess("fluidexplorer")

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
        # TODO - Insert correct path
        filename = os.path.join(filePathMainParent, 'lib/fluidexplorer/')
        fxPathRel = os.path.abspath(filename)

        print filePathMainParent
        print filename
        print fxPathRel

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

        return parDir

    @staticmethod
    def applyValuesFromXMLFile(path, containerName):
        lgr = logging.getLogger('FluidExplorerPlugin')
        lgr.info("Read node propertie from xml file: %s", path)

        file = open(path, 'r')
        fileContent = file.read()

        if not fileContent:
            return

        contnetLines = fileContent.splitlines()
        members = [attr for attr in dir(FluidContainerValues()) if not callable(attr) and not attr.startswith("__")]
        for member in members:
            pattern = member + '='
            for line in contnetLines:
                if (pattern in line) and ('</extra>' in line):
                    ind = line.find(pattern)

                    ind1 = ind + len(pattern)
                    ind2 = line.find('</extra>')

                    value = line[ind1:ind2]

                    try:
                        valueInt = float(value)

                        # Set value in maya
                        import maya.cmds as cmds
                        tmpContainer = containerName + '.' + member

                        try:
                            cmds.setAttr(tmpContainer, valueInt)
                        except Exception as e:
                            lgr.warning("Cannot set maya attribute for: %s", member)

                    except Exception as e:
                        lgr.warning("Cannot read value for: %s", member)

                    finally:
                        break

    @staticmethod
    def get_favorites(proj_dir):
        file_path = proj_dir + '/fluidExplorer.favorites'
        search_pattern = 'favorites='
        if os.path.exists(file_path):

            f = open(file_path, "r")
            lines = f.readlines()
            f.close()

        if len(lines) > 0:

            for line in lines:
                if search_pattern in line:
                    favorites_str = line[line.index(search_pattern) + len(search_pattern):]
                    favorites_elements = favorites_str.split(';')

                    list_of_favorites = []
                    for element in favorites_elements:
                        if '1' in element:
                            list_of_favorites.append(True)
                        else:
                            list_of_favorites.append(False)

            return list_of_favorites

        else:
            return []

    @staticmethod
    def get_selection_from_file(proj_dir):
        file_path = proj_dir + '/fluidExplorer.currentselection'
        search_pattern = 'currentselection='
        if os.path.exists(file_path):

            f = open(file_path, "r")
            lines = f.readlines()
            f.close()

        if len(lines) > 0:

            for line in lines:
                if search_pattern in line:
                    favorites_str = line[line.index(search_pattern) + len(search_pattern):]
                    try:
                        number = int(favorites_str)
                    except ValueError:
                        number = 0

            return number

        else:
            return 0