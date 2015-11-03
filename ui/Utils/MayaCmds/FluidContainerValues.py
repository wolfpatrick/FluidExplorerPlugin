from FluidExplorerPlugin.ui.Utils.MayaCmds.SliderState import SliderState
import maya.cmds as cmds
import pymel.core as pc

class ContainerValuesUtils():
    
    def __init__(self, fluidName):
        self.fluidName = fluidName

        # TODO
        
    def setFluidContainerParameter(self, property, paramterValue):
        tmpCmd = self.fluidName + '.' + property
        cmds.setAttr(tmpCmd, paramterValue)
        
    def getFluidContainerParamter(self, property):
        tmpCmd = self.fluidName + '.' + property
        paramterValue = round(cmds.getAttr(tmpCmd), 3)
        return paramterValue

    def findAEFieldByLabel(self, label, field_type=pc.ui.AttrFieldSliderGrp):
        print "NOW IN THE METHOD " + str(label)
        for i in pc.ui.PyUI('MainAttributeEditorLayout').walkChildren():
            if isinstance(i, pc.ui.RowLayout):
                name = i.name()
                try:
                    grp = field_type(name)
                    print grp
                    if grp.getLabel() == label:
                        print grp
                        return grp
                except:
                    pass

    def getSliderLockedState(self, label):
        return cmds.getAttr(label, se=True)

    def getSliderStatusFromMaya(self, SliderName, propertyName):
        sliderState = SliderState()

        try:
            sliderStatusEnabled = sliderState.findAEFieldByLabel(SliderName).getEnable()
            print 'sliderStateEn ' + str(sliderStatusEnabled)
        except:
            sliderStatusEnabled = True


        try:
            sliderNotLockedState = sliderState.getLockedStatus(self.fluidName, propertyName)
            print 'sliderNotLockedState ' + str(sliderNotLockedState)
        except:
            sliderNotLockedState = True

        return sliderStatusEnabled and sliderNotLockedState
        
# Test Code
# containerValues = ContainerValues('fluid1')
# containerValues.setFluidContainerParameter('velocitySwirl', 3)

class ContainerValuesList():

    def __init__(self):
        self.velocitySwirl = None




