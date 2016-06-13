import maya.cmds as cmds
import math

class MayaUiDefaultValues(object):

    def __init__(self):
        self._sliderViscosity = True
        self._sliderVelocitySwirl = True
        self._sliderDensityDiffusion = True
        self._sliderDensityDissipation = True
        self._sliderDensityBuoyancy = False
        # The remaining sliders (speed, frequency, strength) are always true!

        self._animationMinTime = 0;
        self._animationEndTime = 0;

        self._cameraList = None

    def getSliderStatus(self, shapeNode):
        return True # TODO delete
        # viscosity
        tmp = shapeNode + ".velocityMethod"
        value = cmds.getAttr(tmp)
        if (value != 2):
            self._sliderViscosity = False

        # swirl velocitySwirl
        tmp = shapeNode + ".velocityMethod"
        value = cmds.getAttr(tmp)
        if (value != 2):
            self._sliderVelocitySwirl = False

        # densityDiffusion
        tmp = shapeNode + ".densityMethod"
        value = cmds.getAttr(tmp)
        if (value != 2):
            self._sliderDensityDiffusion = False

        # densityDissipation
        tmp = shapeNode + ".densityMethod"
        value = cmds.getAttr(tmp)
        if (value == 0) or (value == 3):
            self._sliderDensityDissipation = False

        # densityBuoyancy
        tmp = shapeNode + ".velocityMethod"
        value1 = cmds.getAttr(tmp)
        tmp = shapeNode + ".densityMethod"

        value2 = cmds.getAttr(tmp)
        if (value1 == 2) and (value2 == 1 or value2 == 2 or value2 == 3):
            self._sliderDensityBuoyancy = True


    def isAttributeSettable(self, shapeNode, attribute):
        return True # TODO delete
        tmp = shapeNode + "." + attribute
        settable = cmds.getAttr(tmp, se=True)

        #return settable
        return True


    def getAnimationStartEnd(self):
        minValue = cmds.playbackOptions(q=True, animationStartTime=True)
        maxValue = cmds.playbackOptions(q=True, animationEndTime=True)

        self._animationMinTime = math.floor(minValue)
        self._animationEndTime = math.floor(maxValue)


    def getCamerasFromMaya(self):
        # camerasList = ["CamA", "camB"]
        allCameras = cmds.listCameras()
        camerasList = allCameras

        return camerasList