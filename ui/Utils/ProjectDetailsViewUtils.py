class ProjectSubSettings():

    def __init__(self):
        self.projectName = ''
        self.projectPath = ''
        self.fluidContainerName = ''
        self.animationStartTime = ''
        self.animationEndTime = ''
        self.numberOfSimulations = ''
        self.cam_persp = '0'    # 0/1
        self.cam_vc = '0'       # 0/1


import os
import xml.etree.cElementTree as ET

class ProjectDetailsViewUtils():

    def __init__(self):
        pass

    @staticmethod
    def readAttributeFromXmlConfigurationsFile(xml_file, childName):
        #xml_file = "E:/TMP/ANNAANNA/ANNAANNA.fxp"
        #childName = "MayaFilePath"

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
            projectSettings.fluidContainerName = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'FluidBoxName')
            projectSettings.numberOfSimulations = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'Samples')
            projectSettings.animationStartTime = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'TODO')
            projectSettings.animationEndTime = ProjectDetailsViewUtils.readAttributeFromXmlConfigurationsFile(xml_file, 'TODO')
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
                    print tmp
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