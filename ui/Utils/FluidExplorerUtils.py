import os
import ConfigParser
import xml.etree.cElementTree as ET


class FluidExplorerUtils(object):

    @staticmethod
    def dirExists(path):
        exists = os.path.exists(path)
        return exists

    @staticmethod
    def readAttributeFromConfigurationFile(choosenDir, category, attribute):
        config = ConfigParser.ConfigParser()
        config.read(choosenDir)

        result = config.get(category, attribute)
        return result

    @staticmethod
    def readAttributeFromXmlConfigurationsFile(xml_file, childName):
        try:
            tree = ET.ElementTree(file=xml_file)
            root = tree.getroot()

            for child in root:
                if child.tag.lower() == childName.lower():
                    el_child_text = child.text
                    #print el_child_text
                    return el_child_text
        except:
            print("Warning: Cannot read XML attribute")
