import pymel.core as pc
import maya.cmds as cmds


class SliderState(object):

    def __init__(self):
        pass

    def findAEFieldByLabel(self, label, field_type=pc.ui.AttrFieldSliderGrp):
        for i in pc.ui.PyUI('MainAttributeEditorLayout').walkChildren():
            if isinstance(i, pc.ui.RowLayout):
                name = i.name()
                try:
                    grp = field_type(name)
                    print "--"
                    print str(grp.getLabel())
                    if grp.getLabel() == label:
                        return grp
                except:
                    pass

    def getLockedStatus(self, fluidName, propertyName):
        fluidAttr = fluidName + '.' + propertyName
        sliderNotLockedState = cmds.getAttr(fluidAttr, se=True)

        return sliderNotLockedState
