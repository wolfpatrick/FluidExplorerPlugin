from FluidExplorerPlugin.ui.ParamterTab import SliderContainer
from FluidExplorerPlugin.ui.SliderContainerLayouts import SliderContainerLayout
from FluidExplorerPlugin.ui.Utils.MayaCmds.FluidContainerValues import ContainerValuesUtils

class DynamicSimulationLayout(SliderContainerLayout):

    def getLayout(self):

        self.containerGravity = SliderContainer("Gravity", 'gravity', self.fluidBoxName)
        self.containerViscosity = SliderContainer("Viscosity", 'viscosity', self.fluidBoxName)
        self.containerFriction = SliderContainer("Friction", 'friction', self.fluidBoxName)
        self.containerDamp = SliderContainer("Damp", 'velocityDamp', self.fluidBoxName)

        self.containerGravity.addToLayout(self.gridLayout_Box, 1)
        self.containerViscosity.addToLayout(self.gridLayout_Box, 2)
        self.containerFriction.addToLayout(self.gridLayout_Box, 3)
        self.containerDamp.addToLayout(self.gridLayout_Box, 4)

        self.sliderList.append(self.containerGravity)
        self.sliderList.append(self.containerViscosity)
        self.sliderList.append(self.containerFriction)
        self.sliderList.append(self.containerDamp)

        self.gridLayout_Box.addWidget(self.resetButton,  5, 12-1, 1, 4-1)
        self.setAllValues(self.sliderList)  # Set all values to start position

        return self.gridLayout_Box

    def resetButton_Event(self):
        self.reset(self.sliderList)

    """
    def initializeSliderDefaultValues(self):
        fluidContainerObj = ContainerValuesUtils(self.fluidBoxName)

        self.DEF_VALUES.velocitySwirl_DEF = fluidContainerObj.getFluidContainerParamter(self.DEF_VALUES.velocitySwirl_NAME)
        #self.DEF_VALUES.velocitySwirl_VISIBILITY = fluidContainerObj.getSliderStatusFromMaya(self.DEF_VALUES.velocitySwirl_SN, self.DEF_VALUES.velocitySwirl_NAME)

        del fluidContainerObj
    """

    def setAllValues(self, sliderList):
        for sliderItem in sliderList:
            sliderItem.resetValues()

    def setInitialVisibility(self, sliderList):
        for sliderItem in sliderList:
            sliderItem.resetValues()