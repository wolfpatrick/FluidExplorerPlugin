import random


class SliderSpanSelected():
    def __init__(self, velocityLayout):
       # self.velocitySwirl_Span = velocityLayout.containerSwirl.checkBox.isChecked()
        self.velocitySwirl_Span = self.setSpanValues(velocityLayout.containerSwirl)

    def setSpanValues(self, container):
        if container.checkBox.isChecked():
            return [container.lineEditMin.text(), container.lineEditMax.text()]
        else:
            return [container.lineEditDefault.text(), container.lineEditDefault.text()]


class FluidContainerValues():
    def __init__(self):
        self.velocitySwirl = None


class FluidValueSampler():

    def __init__(self, sliderRanges):
        """
        :type sliderRanges: SliderSpanSelected
        """
        self.randomValuesSet = FluidContainerValues()
        self.sliderRanges = sliderRanges

    def setSldierRangeValues(self):
        self.randomValuesSet.velocitySwirl = round(random.uniform(round(float(self.sliderRanges.velocitySwirl_Span[0]), 3), round(float(self.sliderRanges.velocitySwirl_Span[1]), 3)), 3)
        print "Random V: " + str(self.randomValuesSet.velocitySwirl)

    def getSampleSet(self):
        return self.randomValuesSet