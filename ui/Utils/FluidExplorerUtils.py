import os
import ConfigParser
import subprocess
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

    @staticmethod
    def checkIfFFmpgeIsExectuable(pathToFFmpeg):
        if os.name == 'nt':
            pathToFFmpeg = pathToFFmpeg + "/ffmpeg.exe"
        else:
            # TODO: Unix path
            pass

        try:
            subprocess.call([pathToFFmpeg], shell=False)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                # Handle file not found error.
                print("Fatal Error: Cannot find ffmpeg. Details: ", e.message)
                print("Please check if executable file exists in /lib/ffmpeg/")
                return False
            else:
                # Something else went wrong while trying to run ffmpeg
                print("Fatal Error: Cannot execute ffmpeg. Details: ", e.message)
                return False

        return True

    @staticmethod
    def checkIfFluidExplorerIsExectuable(pathToFluidExplorer):
        if os.name == 'nt':
            pass
        else:
            # TODO: Unix path
            pass
        """
        try:
            subprocess.call([pathToFFmpeg], shell=False)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                # Handle file not found error.
                print("Fatal Error: Cannot find ffmpeg. Details: ", e.message)
                return False
            else:
                # Something else went wrong while trying to run ffmpeg
                print("Fatal Error: Cannot execute ffmpeg. Details: ", e.message)
                return False
        """

        return True