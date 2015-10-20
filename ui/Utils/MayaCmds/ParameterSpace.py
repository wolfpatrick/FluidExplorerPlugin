__author__ = 'Patrick'

import random
#import maya.cmds as cmds

#from FluidExplorerPlugin.ui.MayaCacheCommandParameters import MayaCacheCommand


class SamplesVelocity():

    def __init__(self):
        self.velocitySwirl = None


class MayaCacheCmd(object):

    def __init__(self):
        self.densityBuoyancy = 0.0
        self.densityDissipation = 0.0
        self.densityDiffusion = 0.0
        self.velocitySwirl = 0.0
        self.turbulenceSpeed = 0.0
        self.turbulenceFrequency = 0.0
        self.turbulenceStrength = 0.0
        self.viscosity = 0.0

    def sampleParameters(self, parameterSliderSettings, fluidName):

        """
        :type parameterSliderSettings: MayaCacheCommand
        """

        # Create random values and set the maya parameters
        print str(parameterSliderSettings.velocitySwirl)
        # densityBuoyancy
        if parameterSliderSettings.densityBuoyancyFLAG:
            minV = float(parameterSliderSettings.densityBuoyancy[0])
            maxV = float(parameterSliderSettings.densityBuoyancy[1])
            randValue = round(random.uniform(minV, maxV),3)
            print "Radom Value (densityBuoyancy): " + str(randValue)
            tmp = fluidName + ".densityBuoyancy"
            cmds.setAttr(tmp, randValue)

        # densityDissipation
        if parameterSliderSettings.densityDissipationFLAG:
            minV = float(parameterSliderSettings.densityDissipation[0])
            maxV = float(parameterSliderSettings.densityDissipation[1])
            print "::--::"
            randValue = round(random.uniform(minV, maxV),3)
            print "Radom Value (densityDissipation): " + str(randValue)
            tmp = fluidName + ".densityDissipation"
            cmds.setAttr(tmp, randValue)

        # densityDiffusion
        if parameterSliderSettings.densityDiffusionFLAG:
            minV = float(parameterSliderSettings.densityDiffusion[0])
            maxV = float(parameterSliderSettings.densityDiffusion[1])
            randValue = round(random.uniform(minV, maxV),3)
            print "Radom Value (densityDiffusion: " + str(randValue)
            tmp = fluidName + ".densityDiffusion"
            cmds.setAttr(tmp, randValue)

        # velocitySwirl
        if parameterSliderSettings.velocitySwirlFLAG:
            minV = float(parameterSliderSettings.velocitySwirl[0])
            maxV = float(parameterSliderSettings.velocitySwirl[1])
            randValue = round(random.uniform(minV, maxV),3)
            print "Radom Value (velocitySwirl): " + str(randValue)
            tmp = fluidName + ".velocitySwirl"
            cmds.setAttr(tmp, randValue)
            print ":::::::::::::::::::::::::::::" + str(randValue)
            print ":::::::::::::::::::::::::::::" + str(tmp)

        # turbulenceSpeed
        if parameterSliderSettings.turbulenceSpeedFLAG:
            minV = float(parameterSliderSettings.turbulenceSpeed[0])
            maxV = float(parameterSliderSettings.turbulenceSpeed[1])
            randValue = round(random.uniform(minV, maxV),3)
            print "Radom Value (turbulenceSpeed): " + str(randValue)
            tmp = fluidName + ".turbulenceSpeed"
            cmds.setAttr(tmp, randValue)

        # turbulenceFrequency
        if parameterSliderSettings.turbulenceFrequencyFLAG:
            minV = float(parameterSliderSettings.turbulenceFrequency[0])
            maxV = float(parameterSliderSettings.turbulenceFrequency[1])
            randValue = round(random.uniform(minV, maxV),3)
            print "Radom Value (turbulenceFrequency): " + str(randValue)
            tmp = fluidName + ".turbulenceFrequency"
            cmds.setAttr(tmp, randValue)

        # turbulenceStrengthFLAG
        if parameterSliderSettings.turbulenceStrengthFLAG:
            minV = float(parameterSliderSettings.turbulenceStrength[0])
            maxV = float(parameterSliderSettings.turbulenceStrength[1])
            randValue = round(random.uniform(minV, maxV),3)
            print "Radom Value (turbulenceStrengthFLAG): " + str(randValue)
            tmp = fluidName + ".turbulenceStrength"
            cmds.setAttr(tmp, randValue)

        # viscosity
        if parameterSliderSettings.viscosityFLAG:
            minV = float(parameterSliderSettings.viscosity[0])
            maxV = float(parameterSliderSettings.viscosity[1])
            randValue = round(random.uniform(minV, maxV),3)
            print "Radom Value (viscosity): " + str(randValue)
            tmp = fluidName + ".viscosity"
            cmds.setAttr(tmp, randValue)

    def getSampledValue(self, fluidName):

        samples = MayaCacheCmd()

        tmp = fluidName + ".densityBuoyancy"
        v = cmds.getAttr(tmp)
        samples.densityBuoyancy = v
        print str(v)

        tmp = fluidName + ".densityDissipation"
        v = cmds.getAttr(tmp)
        samples.densityDissipation = v
        print str(v)

        tmp = fluidName + ".densityDiffusion"
        v = cmds.getAttr(tmp)
        samples.densityDiffusion = v
        print str(v)

        tmp = fluidName + ".velocitySwirl"
        v = cmds.getAttr(tmp)
        samples.velocitySwirl = v
        print str(v)

        tmp = fluidName + ".turbulenceSpeed"
        v = cmds.getAttr(tmp)
        samples.turbulenceSpeed = v
        print str(v)

        tmp = fluidName + ".turbulenceFrequency"
        v = cmds.getAttr(tmp)
        samples.turbulenceFrequency = v
        print str(v)

        tmp = fluidName + ".turbulenceStrength"
        v = cmds.getAttr(tmp)
        samples.turbulenceStrength = v
        print str(v)

        tmp = fluidName + ".viscosity"
        v = cmds.getAttr(tmp)
        samples.viscosity = v
        print str(v)

        return samples

    def setSampledValue(self, fluidName, values):

        """
        :type values: MayaCacheCmd
        """

        tmp = fluidName + ".densityBuoyancy"
        cmds.setAttr(tmp, values.densityBuoyancy)

        tmp = fluidName + ".densityDissipation"
        cmds.setAttr(tmp, values.densityDissipation)

        tmp = fluidName + ".densityDiffusion"
        cmds.setAttr(tmp, values.densityDiffusion)

        tmp = fluidName + ".velocitySwirl"
        cmds.setAttr(tmp, values.velocitySwirl)

        tmp = fluidName + ".turbulenceSpeed"
        cmds.setAttr(tmp, values.turbulenceSpeed)

        tmp = fluidName + ".turbulenceFrequency"
        cmds.setAttr(tmp, values.turbulenceFrequency)

        tmp = fluidName + ".turbulenceStrength"
        cmds.setAttr(tmp, values.turbulenceStrength)

        tmp = fluidName + ".viscosity"
        cmds.setAttr(tmp, values.viscosity)
