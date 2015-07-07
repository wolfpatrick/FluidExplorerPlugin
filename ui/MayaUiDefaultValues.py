__author__ = 'Patrick'

#import maya.cmds as cmds

class MayaUiDefaultValues(object):

    def __init__(self):
        self._sliderViscosity = True
        self._sliderVelocitySwirl = True
        self._sliderDensityDiffusion = True
        self._sliderDensityDissipation = True
        self._sliderDensityBuoyancy = False
        # The remaining sliders (speed, frequency, strength) are always true!

    def getSliderStatus(self, shapeNode):

        # viscosity
        tmp = shapeNode + ".velocityMethod"
        value = maya.cmds.getAttr(tmp)
        if (value != 2):
            self._sliderViscosity = False

        # swirl velocitySwirl
        tmp = shapeNode + ".velocityMethod"
        value = maya.cmds.getAttr(tmp)
        if (value != 2):
            self._sliderVelocitySwirl = False

        # densityDiffusion
        tmp = shapeNode + ".densityMethod"
        value = maya.cmds.getAttr(tmp)
        if (value != 2):
            self._sliderDensityDiffusion = False

        # densityDissipation
        tmp = shapeNode + ".densityMethod"
        value = maya.cmds.getAttr(tmp)
        if (value == 0) or (value == 3):
            self._sliderDensityDissipation = False

        # densityBuoyancy
        tmp = shapeNode + ".velocityMethod"
        value1 = maya.cmds.getAttr(tmp)
        tmp = shapeNode + ".densityMethod"

        value2 = maya.cmds.getAttr(tmp)
        if (value1 == 2) and (value2 == 1 or value2 == 2 or value2 == 3):
            self._sliderDensityBuoyancy = True


    def isAttributeSettable(self, shapeNode, attribute):

        tmp = shapeNode + "." + attribute
        settable = cmds.getAttr(tmp, se=True)

        #return settable
        return Ture