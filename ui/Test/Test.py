import logging
import os
import maya.cmds as cmds

#######################################################################################################################
# READ ME - Test Configuration
# 1) Set animation start and end time
#       FluidMain.py: Set runTests=True (line 62/63)
#       Ses animation start time to 1
#       Ses animation end time to 15
# 2) Check if folder 'TestProjects' exist: e.g.: FluidExplorerPlugin/ui/Test/TestProjects -> delete TestProjects
# 3) Create an empty fluid container (with emitter)
# 4) Run test -> Create Simulation Button
#######################################################################################################################

class Test():

    def __init__(self):
        # TODO: Path to log file
        self.workDir = ""
        self.LOG_PATH = ""

        self.projectName = ""
        self.projectPath = ""
        self.numberOfSamples = ""
        self.simulation_start = ""
        self.simulation_end = ""
        self.cam_perspective = False
        self.cam_viewcube = False
        self.cam_custom = False
        self.cam_custom_name = ""

        self.numberOfFilesInSimulation = 16
        self.numberOfRenderedImages = 15

    def initTest(self, workDir, containerName):
        self.workDir = workDir
        self.LOG_PATH = self.workDir + '/' + 'LOG_FILE.log'
        cmds.playbackOptions(animationStartTime=1.00)
        cmds.playbackOptions(animationEndTime=15.00)

        # Camera
        import maya.mel as mel
        str1 = 'camera -centerOfInterest 5 -focalLength 35 -lensSqueezeRatio 1 -cameraScale 1 -horizontalFilmAperture 1.4173 -horizontalFilmOffset 0 -verticalFilmAperture 0.9449 -verticalFilmOffset 0 -filmFit Fill -overscan 1 -motionBlur 0 -shutterAngle 144 -nearClipPlane 0.1 -farClipPlane 10000 -orthographic 0 -orthographicWidth 30 -panZoomEnabled 0 -horizontalPan 0 -verticalPan 0 -zoom 1; objectMoveCommand; cameraMakeNode 1 "";'
        str2 = 'move -r 0 -3 10'
        res = mel.eval(str1)
        mel.eval(str2)
        self.cam_custom_name = res
        str3 = 'select -r ' + containerName + ';'
        mel.eval(str3)


    def setUpLogger(self):
        # Create logger
        self.lgr = logging.getLogger('FluidExplorerPlugin')
        #self.lgr.setLevel(logging.DEBUG)

        # Add a file handler
        self.fh = logging.FileHandler(self.LOG_PATH, mode='w')
        #self.fh.setLevel(logging.WARNING)

        # Create a formatter and set the formatter for the handler.
        self.frmt = logging.Formatter('%(asctime)s - %(message)s')
        self.fh.setFormatter(self.frmt)

        # Add the Handler to the logger
        self.lgr.addHandler(self.fh)

        # Logging
        """
        self.lgr.debug('debug message') # This won't print to myapp.log
        self.lgr.info('info message') # Neither will this.
        self.lgr.warn('Checkout this warning.') # This will show up in the log file.
        self.lgr.error('An error goes here.') # and so will this.
        self.lgr.critical('Something critical happened.') # and this one too.
        """

    def logResult(self, state, name):
        if state:
            strMeg = str("Test instance - " + name + " - successfully executed")
            self.lgr.info(strMeg)
        else:
            strMeg = str("Test instance - " + name + " - failed")
            self.lgr.error(strMeg)

    def directory_jpg(self, path):
        list_dir = []
        list_dir = os.listdir(path)
        count = 0
        for file in list_dir:
            if file.endswith('jpg'):
                count += 1
        return count

    def directory_mc_xml(self, path):
        list_dir = []
        list_dir = os.listdir(path)
        count = 0
        for file in list_dir:
            if file.endswith('mc') or file.endswith('xml'):
                count += 1
        return count

    #
    # TESTS INSTANCES
    #

    # -----------------------------------------------------------------------------------------------------------------
    # Test Instance: wrong_projectName
    def wrong_projectName(self):
        t = Test()
        t.projectName = "TestProject?"
        t.cam_perspective = False
        return t

    def evaluate_wrong_projectName(self, testResult):
        if testResult == None:
            self.logResult(True, 'wrong_projectName')
        else:
            self.logResult(False, 'wrong_projectName')
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # Test Instance: empty_projectName
    def empty_projectName(self):
        t = Test()
        t.projectName = ""
        return t

    def evaluate_empty_projectName(self, testResult):
        if testResult == None:
            self.logResult(True, 'empty_projectName')
        else:
            self.logResult(False, 'empty_projectName')
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # Test Instance: wrong_projectPath
    def wrong_projectPath(self):
        t = Test()
        t.projectName = "TestProject"
        t.projectPath = "E:/T?MP/"
        return t

    def evaluate_wrong_projectPath(self, testResult):
        if testResult == None:
            self.logResult(True, 'wrong_projectPath')
        else:
            self.logResult(False, 'wrong_projectPath')
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # Test Instance: empty_projectPath
    def empty_projectPath(self):
        t = Test()
        t.projectName = "TestProject"
        t.projectPath = ""
        return t

    def evaluate_empty_projectPath(self, testResult):
        if testResult == None:
            self.logResult(True, 'empty_projectPath')
        else:
            self.logResult(False, 'empty_projectPath')
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # Test Instance: create_sumulation_cache_only
    def create_sumulation_cache_only(self):
        t = Test()
        t.projectName = "TestProject1"
        t.projectPath = self.workDir + '/TestProjects/'
        t.numberOfSamples = "2"
        t.cam_perspective = False
        cmds.playbackOptions(animationStartTime=1.00)
        cmds.playbackOptions(animationEndTime=15.00)

        return t

    def evaluate_create_sumulation_cache_only(self, projectPath, projectName, numberOfSamples):

        # Evaluation - project file exists
        tmp = projectPath + "/" + projectName + "/" + projectName + '.fxp'
        if os.path.exists(tmp):
            self.logResult(True, 'project_file_exists')
        else:
            self.logResult(False, 'project_file_exists')

        # Evaluation - number of simulations
        projectDirsOk = True
        for i in range(0, int(numberOfSamples)):
            tmp = projectPath + "/" + projectName + "/" + str(i)

            if not os.path.exists(tmp):
                projectDirsOk = FalseprojectDirsOk = False

        if projectDirsOk:
            self.logResult(True, 'simulation_folders_exist')
        else:
            self.logResult(False, 'simulations_folders_exist')

        # Evaluation - number of cache files correct
        numberOK = True
        for i in range(0, int(numberOfSamples)):
            tmp = projectPath + "/" + projectName + "/" + str(i)
            if self.directory_mc_xml(tmp) == self.numberOfFilesInSimulation:
                #print self.directory_mc_xml(tmp)
                pass
            else:
                numberOK = False

        if numberOK:
            self.logResult(True, 'number_of_cache_files_correct')
        else:
            self.logResult(False, 'number_of_cache_files_correct')
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # Test Instance: create_sumulation_cache_and_images_perspective
    def create_sumulation_cache_and_images_perspective(self):
        t = Test()
        t.projectName = "TestProject2"
        t.projectPath = self.workDir + '/TestProjects/'
        t.numberOfSamples = "2"
        t.cam_perspective = True
        cmds.playbackOptions(animationStartTime=1.00)
        cmds.playbackOptions(animationEndTime=15.00)

        return t

    def evaluate_create_sumulation_cache_and_images_perspective(self, projectPath, projectName, numberOfSamples):
        # Evaluation - number of rendered images correct
        numberOK = True
        for i in range(0, int(numberOfSamples)):
            tmp = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/perspective/"
            if self.directory_jpg(tmp) == self.numberOfRenderedImages:
                pass
            else:
                numberOK = False

        if numberOK:
            self.logResult(True, 'number_of_rendered_images_correct-perspective_camera')
        else:
            self.logResult(False, 'number_of_rendered_images_correct-perspective_camera')

        # Evaluation - gif animation
        gifAnimationExists = True
        for i in range(0, int(numberOfSamples)):
            pathToGif = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/perspective/animation.gif"
            if os.path.exists(pathToGif):
                pass
            else:
                gifAnimationExists = False

        if gifAnimationExists:
            self.logResult(True, 'gif_animation_exists-perspective_camera')
        else:
            self.logResult(False, 'gif_animation_exists-perspective_camera')
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # Test Instance: create_sumulation_cache_and_images_viewcube
    def create_sumulation_cache_and_images_viewcube(self):
        t = Test()
        t.projectName = "TestProject3"
        t.projectPath = self.workDir + '/TestProjects/'
        t.numberOfSamples = "2"
        t.cam_perspective = False
        t.cam_viewcube = True
        cmds.playbackOptions(animationStartTime=1.00)
        cmds.playbackOptions(animationEndTime=15.00)

        return t

    def evaluate_create_sumulation_cache_and_images_viewcube(self, projectPath, projectName, numberOfSamples):
        # Evaluation - number of rendered images correct
        numberFrontOK = True
        numberSideOK = True
        numberTopOK = True
        for i in range(0, int(numberOfSamples)):

            # FRONT
            tmpFront = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/viewcube/front"
            if self.directory_jpg(tmpFront) == self.numberOfRenderedImages:
                print "NUMBER FRONT: " + str(self.directory_jpg(tmpFront))
            else:
                numberFrontOK = False

            # SIDE
            tmpSide = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/viewcube/side"
            if self.directory_jpg(tmpSide) == self.numberOfRenderedImages:
                print "NUMBER SIDE: " + str(self.directory_jpg(tmpSide))
            else:
                numberSideOK = False

            # TOP
            tmpTop = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/viewcube/top"
            if self.directory_jpg(tmpTop) == self.numberOfRenderedImages:
                print "NUMBER TOP: " + str(self.directory_jpg(tmpTop))
            else:
                numberTopOK = False

        if numberFrontOK:
            self.logResult(True, 'number_of_rendered_images_correct-viewcube_camera_front')
        else:
            self.logResult(False, 'number_of_rendered_images_correct-viewcube_camera_front')

        if numberSideOK:
            self.logResult(True, 'number_of_rendered_images_correct-viewcube_camera_side')
        else:
            self.logResult(False, 'number_of_rendered_images_correct-viewcube_camera_side')

        if numberTopOK:
            self.logResult(True, 'number_of_rendered_images_correct-viewcube_camera_top')
        else:
            self.logResult(False, 'number_of_rendered_images_correct-viewcube_camera_top')

        # Evaluation - gif animation
        gifAnimationExistsFront = True
        gifAnimationExistsSide = True
        gifAnimationExistsTop = True
        for i in range(0, int(numberOfSamples)):
            pathToGifFront = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/viewcube/front/animation.gif"
            pathToGifSide = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/viewcube/side/animation.gif"
            pathToGifTop = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/viewcube/top/animation.gif"

            if not os.path.exists(pathToGifFront):
                gifAnimationExistsFront = False
            if not os.path.exists(pathToGifSide):
                gifAnimationExistsFront = False
            if not os.path.exists(pathToGifTop):
                gifAnimationExistsTop = False

        if gifAnimationExistsFront:
            self.logResult(True, 'gif_animations_exists-viewcube_camera_front')
        else:
            self.logResult(False, 'gif_animations_exists-viewcube_camera_front')

        if gifAnimationExistsSide:
            self.logResult(True, 'gif_animations_exists-viewcube_camera_side')
        else:
            self.logResult(False, 'gif_animations_exists-viewcube_camera_side')

        if gifAnimationExistsTop:
            self.logResult(True, 'gif_animations_exists-viewcube_camera_top')
        else:
            self.logResult(False, 'gif_animations_exists-viewcube_camera_top')
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # Test Instance: create_sumulation_cache_and_images_custom
    def create_sumulation_cache_and_images_custom(self):
        t = Test()
        t.projectName = "TestProject3"
        t.projectPath = self.workDir + '/TestProjects/'
        t.numberOfSamples = "2"
        t.cam_perspective = False
        t.cam_viewcube = False
        t.cam_custom = True
        t.cam_custom_name = self.cam_custom_name
        cmds.playbackOptions(animationStartTime=1.00)
        cmds.playbackOptions(animationEndTime=15.00)

        return t

    def evaluate_create_sumulation_cache_and_images_custom(self, projectPath, projectName, numberOfSamples):
        # Evaluation - number of rendered images correct
        numberOK = True
        for i in range(0, int(numberOfSamples)):
            tmp = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/custom/"
            if self.directory_jpg(tmp) == self.numberOfRenderedImages:
                pass
            else:
                numberOK = False

        if numberOK:
            self.logResult(True, 'number_of_rendered_images_correct-custom_camera')
        else:
            self.logResult(False, 'number_of_rendered_images_correct-custom_camera')

        # Evaluation - gif animation
        gifAnimationExists = True
        for i in range(0, int(numberOfSamples)):
            pathToGif = projectPath + "/" + projectName + "/" + str(i) + "/" + "images/custom/animation.gif"
            if os.path.exists(pathToGif):
                pass
            else:
                gifAnimationExists = False

        if gifAnimationExists:
            self.logResult(True, 'gif_animation_exists-custom_camera')
        else:
            self.logResult(False, 'gif_animation_exists-custom_camera')
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    # Test Instance: create_sumulation_cache_and_images_rotation
    # TODO
    # -----------------------------------------------------------------------------------------------------------------

