import maya.cmds as cmds


class ContainerValuesUtils():
    
    def __init__(self, fluidName):
        self.fluidName = fluidName

    def setFluidContainerParameter(self, property, paramterValue):
        tmpCmd = self.fluidName + '.' + property
        cmds.setAttr(tmpCmd, paramterValue)
        
    def getFluidContainerParamter(self, property):
        tmpCmd = self.fluidName + '.' + property
        paramterValue = round(cmds.getAttr(tmpCmd), 3)
        return paramterValue

    def getSliderLockedState(self, label):
        return cmds.getAttr(label, se=True)

    """
    # Checks if slider in maya ui is enabled or disabled
    def findAEFieldByLabel(self, label, field_type=pc.ui.AttrFieldSliderGrp):
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
    """

