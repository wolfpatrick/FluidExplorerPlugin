import maya.cmds as cmds

class ContainerValuesUtils():
    
    def __init__(self, fluidName):
        self.fluidName = fluidName
        self.fluidName = 'fluid1'

        # TODO
        
    def setFluidContainerParameter(self, property, paramterValue):
        tmpCmd = self.fluidName + '.' + property
        cmds.setAttr(tmpCmd, paramterValue)
        
    def getFluidContainerParamter(self, property):
        tmpCmd = self.fluidName + '.' + property
        paramterValue = round(cmds.getAttr(tmpCmd), 3)
        return paramterValue
        
# Test Code
# containerValues = ContainerValues('fluid1')
# containerValues.setFluidContainerParameter('velocitySwirl', 3)

class ContainerValuesList():

    def __init__(self):
        self.velocitySwirl = None




