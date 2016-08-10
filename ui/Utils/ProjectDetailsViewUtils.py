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

class XMLReader():

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
            projectSettings.projectName = XMLReader.readAttributeFromXmlConfigurationsFile(xml_file, 'ProjectName')
            projectSettings.projectPath = XMLReader.readAttributeFromXmlConfigurationsFile(xml_file, 'ProjectPath')
            projectSettings.fluidContainerName = XMLReader.readAttributeFromXmlConfigurationsFile(xml_file, 'FluidBoxName')
            projectSettings.animationStartTime = XMLReader.readAttributeFromXmlConfigurationsFile(xml_file, 'ProjectName')
            projectSettings.animationEndTime = XMLReader.readAttributeFromXmlConfigurationsFile(xml_file, 'ProjectName1')

        except Exception as e:
            print "Error: Cannot read project attributes! Details: " + str(e.message)
            raise Exception(e.message)

        return projectSettings