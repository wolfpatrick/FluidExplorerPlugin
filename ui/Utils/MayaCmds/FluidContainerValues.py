import maya.cmds as cmds

class ContainerValuesUtils():
    
    def __init__(self, fluidName):
        self.fluidName = fluidName
        print "KONS"
        
    def setFluidContainerParameter(self, property, paramterValue):
        tmpCmd = self.fluidName + '.' + property
        print tmpCmd
        #cmds.setAttr(tmpCmd, paramterValue)
        
    def getFluidContainerParamter(self, property):
        tmpCmd = self.fluidName + '.' + property
        #paramterValue = cmds.getAttr(tmpCmd)
        paramterValue = 9.0
        return paramterValue
        
# Test Code
# containerValues = ContainerValues('fluid1')
# containerValues.setFluidContainerParameter('velocitySwirl', 3)

class ContainerValuesList():

    def __init__(self):
        self.velocitySwirl = None




