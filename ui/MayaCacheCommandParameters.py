__author__ = 'Patrick'

class MayaCacheCommand(object):

    def __init__(self):
        self._outputPath = ""
        self._numberSamples = 128
        self._densityDissipationFLAG = False
        self._densityDiffusionFLAG = False
        self._densityBuoyancyFLAG = False
        self._viscosityFLAG = False
        self._turbulenceStrengthFLAG = False
        self._turbulenceFrequencyFLAG = False
        self._turbulenceSpeedFLAG = False
        self._velocitySwirlFLAG = False

        self._densityBuoyancy = [-5, 5]
        self._densityDissipation = [0, 1]
        self._densityDiffusion = [0, 2]

        self._viscosity = [0, 1]
        self._velocitySwirl = [0, 10]

        self._turbulenceStrength = [0, 1]
        self._turbulenceSpeed = [0, 2]
        self._turbulenceFrequency = [0, 2]

    @property
    def outputPath(self):
        return self._outputPath

    @outputPath.setter
    def outputPath(self, value):
        print("in the setter: ")
        self._outputPath = value


    @property
    def numberSamples(self):
        return self._numberSamples

    @numberSamples.setter
    def numberSamples(self, value):
        self._numberSamples = value


    @property
    def densityDissipationFLAG(self):
        return self._densityDissipationFLAG

    @densityDissipationFLAG.setter
    def densityDissipationFLAG(self, value):
        self._densityDissipationFLAG = value

    @property
    def densityDiffusionFLAG(self):
        return self._densityDiffusionFLAG

    @densityDiffusionFLAG.setter
    def densityDiffusionFLAG(self, value):
        self._densityDiffusionFLAG = value

    @property
    def densityBuoyancyFLAG(self):
        return self._densityBuoyancyFLAG

    @densityBuoyancyFLAG.setter
    def densityBuoyancyFLAG(self, value):
        self._densityBuoyancyFLAG = value

    @property
    def viscosityFLAG(self):
        return self._viscosityFLAG

    @viscosityFLAG.setter
    def viscosityFLAG(self, value):
        self._viscosityFLAG = value

    @property
    def turbulenceStrengthFLAG(self):
        return self._turbulenceStrengthFLAG

    @turbulenceStrengthFLAG.setter
    def turbulenceStrengthFLAG(self, value):
        self._turbulenceStrengthFLAG = value

    @property
    def turbulenceFrequencyFLAG(self):
        return self._turbulenceFrequencyFLAG

    @turbulenceFrequencyFLAG.setter
    def turbulenceFrequencyFLAG(self, value):
        self._turbulenceFrequencyFLAG = value

    @property
    def turbulenceSpeedFLAG(self):
        return self._turbulenceSpeedFLAG

    @turbulenceSpeedFLAG.setter
    def turbulenceSpeedFLAG(self, value):
        self._turbulenceSpeedFLAG = value

    @property
    def velocitySwirlFLAG(self):
        return self._velocitySwirlFLAG

    @velocitySwirlFLAG.setter
    def velocitySwirlFLAG(self, value):
        self._velocitySwirlFLAG = value


    # ----------------------------------------------------------
    @property
    def densityBuoyancy(self):
        return self._densityBuoyancy

    @densityBuoyancy.setter
    def densityBuoyancy(self, value):
        self._densityBuoyancy = value

    @property
    def densityDissipation(self):
        return self._densityDissipation

    @densityDissipation.setter
    def densityDissipation(self, value):
        self._densityDissipation = value

    @property
    def densityDiffusion(self):
        return self._densityDiffusion

    @densityDiffusion.setter
    def densityDiffusion(self, value):
        self._densityDiffusion = value
    # ----------------------------------------------------------


    # ----------------------------------------------------------
    @property
    def viscosity(self):
        return self._viscosity

    @viscosity.setter
    def viscosity(self, value):
        self._viscosity = value
    # ----------------------------------------------------------


    # ----------------------------------------------------------
    @property
    def velocitySwirl(self):
        return self._velocitySwirl

    @velocitySwirl.setter
    def velocitySwirl(self, value):
        self._velocitySwirl = value
    # ----------------------------------------------------------


    # ----------------------------------------------------------
    @property
    def turbulenceStrength(self):
        return self._turbulenceStrength

    @turbulenceStrength.setter
    def turbulenceStrength(self, value):
        self._turbulenceStrength = value

    @property
    def turbulenceSpeed(self):
        return self._turbulenceSpeed

    @turbulenceSpeed.setter
    def turbulenceSpeed(self, value):
        self._turbulenceSpeed = value

    @property
    def turbulenceFrequency(self):
        return self._turbulenceFrequency

    @turbulenceFrequency.setter
    def turbulenceFrequency(self, value):
        self._turbulenceFrequency = value
    # ----------------------------------------------------------


    def createMELCommand(self, MayaCacheCommand):

        spaceStr = " "
        cmdStr = "fluidExplorer"

        # Path and number of samples
        cmdStr = cmdStr + spaceStr + "-p " + self.outputPath
        cmdStr = cmdStr + spaceStr + "-s " + str(self.numberSamples)

        # Fluid chache parameters
        if self.densityBuoyancyFLAG:
            cmdStr = cmdStr + spaceStr + "-a densityBuoyancy" + spaceStr + str(self.densityBuoyancy[0]) + spaceStr + str(self.densityBuoyancy[1])

        if self.densityDissipationFLAG:
            cmdStr = cmdStr + spaceStr + "-a densityDissipation" + spaceStr + str(self.densityDissipation[0]) + spaceStr + str(self.densityDissipation[1])

        if self.densityDiffusionFLAG:
            cmdStr = cmdStr + spaceStr + "-a densityDiffusion" + spaceStr + str(self.densityDiffusion[0]) + spaceStr + str(self.densityDiffusion[1])

        if self.viscosityFLAG:
            cmdStr = cmdStr + spaceStr + "-a viscosity" + spaceStr + str(self.viscosity[0]) + spaceStr + str(self.viscosity[1])

        if self.velocitySwirlFLAG:
            cmdStr = cmdStr + spaceStr + "-a velocitySwirl" + spaceStr + str(self.velocitySwirl[0]) + spaceStr + str(self.velocitySwirl[1])

        if self.turbulenceStrengthFLAG:
            cmdStr = cmdStr + spaceStr + "-a turbulenceStrength" + spaceStr + str(self.turbulenceStrength[0]) + spaceStr + str(self.turbulenceStrength[1])

        if self.turbulenceSpeedFLAG:
            cmdStr = cmdStr + spaceStr + "-a turbulenceSpeed" + spaceStr + str(self.turbulenceSpeed[0]) + spaceStr + str(self.turbulenceSpeed[1])

        if self.turbulenceFrequencyFLAG:
            cmdStr = cmdStr + spaceStr + "-a turbulenceFrequency" + spaceStr + str(self.turbulenceFrequency[0]) + spaceStr + str(self.turbulenceFrequency[1])

        return cmdStr

"""
    //
	// Description:
	//	Create cache files on disk for the select fluid object(s) according
	//  to the specified flags described below.
	//
	// $version == 1:
	//	$args[0] = time range mode:
	//		time range mode = 0 : use $args[1] and $args[2] as start-end
	//		time range mode = 1 : use render globals
	//		time range mode = 2 : use timeline
	//  $args[1] = start frame (if time range mode == 0)
	//  $args[2] = end frame (if time range mode == 0)
	//
	// $version == 2:
	//  $args[3] = cache file distribution, either "OneFile" or "OneFilePerFrame"
	//	$args[4] = 0/1, whether to refresh during caching
	//  $args[5] = directory for cache files, if "", then use project data dir
	//	$args[6] = 0/1, whether to create a cache per geometry
	//	$args[7] = name of cache file. An empty string can be used to specify that an auto-generated name is acceptable.
	//	$args[8] = 0/1, whether the specified cache name is to be used as a prefix
	// $version == 3:
	//  $args[9] = action to perform: "add", "replace", "merge" or "mergeDelete"
	//  $args[10] = force save even if it overwrites existing files
	//	$args[11] = simulation rate, the rate at which the fluid simulation is forced to run
	//	$args[12] = sample mulitplier, the rate at which samples are written, as a multiple of simulation rate.
	// $version == 4:
	//	$args[13] = 0/1, whether modifications should be inherited from the cache about to be replaced.
	//	$args[14] = 0/1, whether to store doubles as floats
	//	$args[15] = name of cache format
	//
	// $version == 5:
	//	$args[16] = 0/1, whether density should be cached
	//	$args[17] = 0/1, whether velocity should be cached
	//	$args[18] = 0/1, whether temperature should be cached
	//	$args[19] = 0/1, whether fuel should be cached
	//	$args[20] = 0/1, whether color should be cached
	//	$args[21] = 0/1, whether texture coordinates should be cached
	//	$args[22] = 0/1, whether falloff should be cached
	//
"""

