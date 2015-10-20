import os
import ConfigParser


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
        config = ConfigParser()
        config.read(choosenDir)

        result = config.get(category, attribute)
        return result