import os
import ConfigParser
import xml.etree.cElementTree as ET
import xml.etree.ElementTree as xml


class FluidExplorerUtils(object):

    @staticmethod
    def dirExists(path):
        exists = os.path.exists(path)
        return exists

    @staticmethod
    def createConfigurationFile(settings, path):
        """
        :type settings : MayaCacheCmdSettings
        """
        config = ConfigParser.RawConfigParser()
        config.add_section('default_settings')
        config.set('default_settings', 'FluidName', str(settings.fluidBoxName))             # name of the fluid container
        config.set('default_settings', 'SimulationName', str(settings.prjName))             # name of the project
        config.set('default_settings', 'SimulationPath', str(settings.outputPath))          # path of the project
        config.set('default_settings', 'NumberSamples', str(settings.numberSamples))        # number of samples
        config.set('default_settings', 'AnimationStart',  str(settings.animationStartTime)) # start time
        config.set('default_settings', 'AnimationEnd',  str(settings.animationEndTime))     # end time
        config.set('default_settings', 'CameraPerspective',  str(settings.cam_perspective)) # camera perspective
        config.set('default_settings', 'CameraViewcube',  str(settings.cam_viewcube))    # camera cube
        config.set('default_settings', 'CameraRotation',  str(settings.cam_rotation))    # camera rotation
        config.set('default_settings', 'CameraCustom',  str(settings.cam_custom_name)) # camera custome

        # Save file
        with open(path, 'w') as configfile:
            config.write(configfile)

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
            print "ERROR"



    @staticmethod
    def openMayaPort():

        import maya.cmds as cmds

        connectionOK = False
        loopCount = 0

        while connectionOK == False:
            loopCount = loopCount + 1
            print loopCount
            # if it was already open under another configuration
            try:
                cmds.commandPort(name=":7002", close=True)
                connectionOK = True
            except:
                connectionOK = False
                pass

            # now open a new port
            try:
                cmds.commandPort(name=":7002", sourceType="python")
                connectionOK = True
            except:
                connectionOK = False

            if loopCount == 1000:
                print "break"
                break
