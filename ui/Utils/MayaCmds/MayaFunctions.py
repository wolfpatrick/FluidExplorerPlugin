#from ui.MayaCacheCommandParameters import MayaCacheCommand
#from FluidExplorerPlugin.ui.MayaCacheCommandParameters import MayaCacheCommand


#from FluidExplorerPlugin.ui.MayaCacheCmdSettings import MayaCacheCmdSettings

#from ui.MayaCacheCmdSettings import MayaCacheCmdSettings
#from ui.MayaCacheCmdSettings import MayaCacheCmdSettings

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel


import os
from FluidExplorerPlugin.ui.Utils.MayaCmds.FluidContainerValues import ContainerValuesList
#from ui.Utils.MayaCmds.FluidContainerValues import ContainerValuesList
import thread
import threading

class MayaFunctionUtils(object):

    def __init__(self):
        self.finished = False
        pass

    def getObjType(self, selection):
        t = cmds.objectType(selection)
        if t == "fluidShape":
            return t
        else:
            #objType = `listRelatives -s $selection`;
            objType = cmds.listRelatives(selection, s=True)
            if objType == None:
                return ""
            else:
                return cmds.nodeType(objType[0])

    def getSelectedContainerPy(self):
        selectedObjName = cmds.ls(sl=True)

        count_fluidShape = 0
        index_fluidShape = -1

        lenSelObj = len(selectedObjName)

        for i, item in enumerate(selectedObjName):
            res = self.getObjType(str(item))
            if res == "fluidShape":
                count_fluidShape += 1
                index_fluidShape = i

        currentObj = ""
        if int(lenSelObj) == 0:
            return [False, "Please select an object first!"]
        elif int(count_fluidShape) >= 2:
            return [False, "Please select one Fluid Container only!"]
        else:
            if int(count_fluidShape) == 1:
                print str(index_fluidShape)
                currentObj = selectedObjName[int(index_fluidShape)]
                containerName = currentObj
                return [True, containerName]
            else:
                return [False, "Please select one Fluid Container only!"]

    def createFluid(self, cmdStr, progressbar):
        #progressbar.setLabelText(progressbar.labelText() + "\n\n" + "Caching Simulations...")
        pm.mel.eval(cmdStr)


    def setSampledValue(self, fluidName, values):
        """
        :type values: ContainerValuesList
        """
        members = [attr for attr in dir(values) if not callable(values) and not attr.startswith("__")]
        for item in members:
            tmpCmd = fluidName + "." + str(item)
            attributeValue = float(getattr(values, item))
            cmds.setAttr(tmpCmd, attributeValue)

    def changeToPerspCam(self):
        currentCam = cmds.lookThru(q=True)
        if currentCam != 'persp':
            # Select the perspective camera (default = modelPfloatanel4)attributeValue
            cmdStr = "lookThroughModelPanel" + " " + "persp" + " " + "modelPanel4;"
            mel.eval(cmdStr)
            cmds.lookThru('persp')

    def viewFromCamPosition(self, positionName, containerName):
        self.changeToPerspCam()

        cmd = ""
        if (positionName =='PERSPECTIVE'):
            cmd = "viewSet -animate `optionVar -query animateRollViewCompass` -p"
            #cmds.viewSet(p=True, an=False);
        elif (positionName == 'TOP'):
            cmd = "viewSet -animate `optionVar -query animateRollViewCompass` -top"
        elif (positionName == 'BOTTOM'):
            cmd = "viewSet -animate `optionVar -query animateRollViewCompass` -bottom"
        elif (positionName == 'RIGHT'):
            cmd = "viewSet -animate `optionVar -query animateRollViewCompass` -rightSide"
        elif (positionName == 'LEFT'):
            cmd = "viewSet -animate `optionVar -query animateRollViewCompass` -leftSide"
        elif (positionName == 'FRONT'):
            cmd = "viewSet -animate `optionVar -query animateRollViewCompass` -front"
        elif (positionName == 'BACK'):
            cmd = "viewSet -animate `optionVar -query animateRollViewCompass` -back"

        cmds.select(containerName)

        # Execute MEL command
        mel.eval(cmd)
        #mel.eval('FrameSelectedInAllViews')
        cmds.viewFit(an=False)

        # if (positionName =='PERSPECTIVE'):
        #     cmds.dolly(d=-10)

    def renderImagesFromCameras(self, generalSettings, fluidIndex, progress):
        """
        :type generalSettings: MayaCacheCmdSettings
        """
        #progress.setLabelText(progress.labelText() + "\n\n" + "Rendering Images...")
        self.viewFromCamPosition('PERSPECTIVE', generalSettings.fluidBoxName)

        renderImageFlag = False    # True --> Images are rendered
        if (generalSettings.cam_perspective) == True | (generalSettings.cam_viewcube == True) | (generalSettings.cam_custom_name != None) | (generalSettings.cam_rotation != 0):
            renderImageFlag = True

        # Create image folder
        path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/"
        if not os.path.exists(path) & renderImageFlag:
            os.mkdir(path)

        # Settings
        fileName = "image"
        start = str(int(round(generalSettings.animationStartTime)))
        end = str(int(round(generalSettings.animationEndTime)))
        resW = 640
        resH = 480

        if generalSettings.cam_perspective:
            self.viewFromCamPosition('PERSPECTIVE', generalSettings.fluidBoxName)
            path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/perspective/"
            os.mkdir(path)
            self.executeMELRemderCmd(path, fileName, start, end, resW, resH)

        if (generalSettings.cam_viewcube == True):
            os.mkdir(generalSettings.outputPath + "/" + str(fluidIndex) + "/images/viewcube/")

            # TOP
            self.viewFromCamPosition('TOP', generalSettings.fluidBoxName)
            path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/viewcube/TOP/"
            os.mkdir(path)
            self.executeMELRemderCmd(path, fileName, start, end, resW, resH)

            # BOTTOM
            #self.viewFromCamPosition('BOTTOM', generalSettings.fluidBoxName)
            #path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/viewcube/BOTTOM/"
            #os.mkdir(path)
            #self.executeMELRemderCmd(path, fileName, start, end, resW, resH)

            # RIGHT
            self.viewFromCamPosition('RIGHT', generalSettings.fluidBoxName)
            path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/viewcube/RIGHT/"
            os.mkdir(path)
            self.executeMELRemderCmd(path, fileName, start, end, resW, resH)

            # LEFT
            self.viewFromCamPosition('LEFT', generalSettings.fluidBoxName)
            path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/viewcube/LEFT/"
            os.mkdir(path)
            self.executeMELRemderCmd(path, fileName, start, end, resW, resH)

            # FRONT
            self.viewFromCamPosition('FRONT', generalSettings.fluidBoxName)
            path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/viewcube/FRONT/"
            os.mkdir(path)
            self.executeMELRemderCmd(path, fileName, start, end, resW, resH)

            # BACK
            self.viewFromCamPosition('BACK', generalSettings.fluidBoxName)
            path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/viewcube/BACK/"
            os.mkdir(path)
            self.executeMELRemderCmd(path, fileName, start, end, resW, resH)

        if (generalSettings._cam_custom_name != None):
            # View from camera
            cmdStr = "lookThroughModelPanel" + " " + str(generalSettings._cam_custom_name) + " " + "modelPanel4;"
            mel.eval(cmdStr)
            cmds.select(generalSettings.fluidBoxName)

            path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/custom/"
            os.mkdir(path)

            self.executeMELRemderCmd(path, fileName, start, end, resW, resH)
            self.viewFromCamPosition('PERSPECTIVE', generalSettings.fluidBoxName)

        if generalSettings.cam_rotation != 0:
            # Change to perspective camera
            self.viewFromCamPosition('PERSPECTIVE', generalSettings.fluidBoxName)
            cmds.viewFit('persp', an=False)

            path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/rotation/"
            os.mkdir(path)

            # Rotate
            stepAcc = 0
            valueY = int(round(float(generalSettings.cam_rotation)))

            while stepAcc < 360:
                print "value: " + str(stepAcc)
                # Rotate camera
                cmds.setAttr('persp.rotateY',  stepAcc)
                cmds.viewFit('persp', an=False)
                cmds.dolly(d=-15)

                path = generalSettings.outputPath + "/" + str(fluidIndex) + "/images/rotation/" + "deg_" + str(stepAcc) + "/"
                os.mkdir(path)
                self.executeMELRemderCmd(path, fileName, start, end, resW, resH)
                stepAcc = stepAcc + valueY

        cmds.viewFit('persp', an=False)


    def rotateCamerY(valueY):
        stepAcc = 0
        while stepAcc < 360:
            print "value: " + str(stepAcc)
            stepAcc = stepAcc + valueY
            cmds.setAttr('persp.rotateY',  stepAcc)
            cmds.viewFit('persp', an=False)

    def startPosition(self, generalSettings):
        self.viewFromCamPosition('PERSPECTIVE', generalSettings.fluidBoxName)

    def executeMELRemderCmd(self, path, fileName, start, end, resW, resH):
        cmd = "renderImagesMEL(" + "\"" + path + "\"" + "," + "\"" + fileName + "\"" + "," + str(start) + "," + str(end) + "," + str(resW) + "," + str(resH) + ")"
        # Execute the mell command
        mel.eval(cmd)