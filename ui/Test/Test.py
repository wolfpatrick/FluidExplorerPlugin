import logging
import os
import maya.cmds as cmds


class Test():

    def __init__(self):
        # TODO: Path to log file
        self.LOG_PATH = "E:/TMP/LOG_FILE.LOG"

        self.projectName = ""
        self.projectPath = ""
        self.numberOfSamples = ""
        self.simulation_start = ""
        self.simulation_end = ""
        self.cam_perspective = False

        self.numberOfFilesInSimulation = 16

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
        t.projectName = "A1"
        t.projectPath = "E:/TMP/"
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
            if self.directory(tmp) == self.numberOfFilesInSimulation:
                pass
            else:
                numberOK = False

        if numberOK:
            self.logResult(True, 'number_of_cache_files_correct')
        else:
            self.logResult(False, 'number_of_cache_files_correct')

    def directory(self, path):
        list_dir = []
        list_dir = os.listdir(path)
        count = 0
        for file in list_dir:
            if file.endswith('mc') or file.endswith('xml'):
                count += 1
        return count
    # -----------------------------------------------------------------------------------------------------------------

