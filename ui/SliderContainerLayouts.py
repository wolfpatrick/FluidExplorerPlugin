from PySide import QtGui
from PySide import QtCore
from ParamterTab import SliderContainer
from ParamterTabDefaultValues import ParameterTabDefaultValues
from Utils.MayaCmds.FluidContainerValues import ContainerValuesUtils
from Utils.MayaCmds.SliderState import SliderState


class SliderContainerLayout(object):

    def __init__(self):

        self.DEF_VALUES = ParameterTabDefaultValues()

        # Header
        self.gridLayout_Box = QtGui.QGridLayout()
        self.gridLayout_Box.setSpacing(8)
        self.gridLayout_Box.addWidget(QtGui.QLabel("Range  "), 0, 2, QtCore.Qt.AlignCenter)
        self.gridLayout_Box.addWidget(QtGui.QLabel("Default"), 0, 4, QtCore.Qt.AlignCenter)
        self.gridLayout_Box.addWidget(QtGui.QLabel("MIN"), 0, 5, QtCore.Qt.AlignCenter)
        self.gridLayout_Box.addWidget(QtGui.QLabel("MAX"), 0, 16, QtCore.Qt.AlignCenter)

        self.resetButton = QtGui.QPushButton("Reset all Values")
        self.resetButton.clicked.connect(self.resetButton_Event)

        self.sliderList = list()
        self.fluidBoxName = ""

    def resetButton_Event(self, sliderList):
        self.reset(sliderList)

    def reset(self, sliderList):
        for listItem in sliderList:
            listItem.resetValues()

    def setFluidBoxName(self, boxName):
        self.fluidBoxName = boxName


class DiffusionLayout(SliderContainerLayout):

    def getLayout(self):
        self.initializeSliderDefaultValues()


        """
        self.containerA = SliderContainer("TEST1", 0.0, 1.1, 0.5)
        self.containerA.addToLayout(self.gridLayout_Box, 1)
        self.containerB = SliderContainer("TEST2 ", 0.0, 3.1, 0.5)
        self.containerB.addToLayout(self.gridLayout_Box, 2)
        self.containerC = SliderContainer("TEST3 ", 1.0, 2.0, 1.5)
        self.containerC.addToLayout(self.gridLayout_Box, 3)
        self.containerD = SliderContainer("TEST3 ", 1.0, 2.0, 1.5)
        self.containerD.addToLayout(self.gridLayout_Box, 4)
        self.containerE = SliderContainer("TEST3 ", 1.0, 2.0, 1.5)
        self.containerE.addToLayout(self.gridLayout_Box, 5)

        self.containerF = SliderContainer("TEST3 ", 1.0, 2.0, 1.5)
        self.containerF.addToLayout(self.gridLayout_Box, 6)

        self.containerG = SliderContainer("TEST3 ", 1.0, 2.0, 1.5)
        self.containerG.addToLayout(self.gridLayout_Box, 7)

        self.containerH = SliderContainer("TEST3 ", 1.0, 2.0, 1.5)
        self.containerH.addToLayout(self.gridLayout_Box, 8)

        self.containerI = SliderContainer("TEST3 ", 1.0, 2.0, 1.5)
        self.containerI.addToLayout(self.gridLayout_Box, 9)

        self.gridLayout_Box.addWidget(self.resetButton,  10, 13, 1, 4)
        self.gridLayout_Box.addWidget(QtGui.QSplitter(QtCore.Qt.Vertical), 11, 0)

        # List which stores all slider containers

        self.sliderList.append(self.containerA)
        self.sliderList.append(self.containerB)
        """
        # TODO

        return self.gridLayout_Box

    def resetButton_Event(self):
        self.reset(self.sliderList)

    def initializeSliderDefaultValues(self):
        fluidContainerObj = ContainerValuesUtils(self.fluidBoxName)

        #TODO

        del fluidContainerObj

class VelocityLayout(SliderContainerLayout):

    def getLayout(self):
        self.initializeSliderDefaultValues()

        self.containerSwirl = SliderContainer("Swirl", self.DEF_VALUES.velocitySwirl_RANGE[0], self.DEF_VALUES.velocitySwirl_RANGE[1], self.DEF_VALUES.velocitySwirl_DEF, self.DEF_VALUES.velocitySwirl_VISIBILITY)
        self.containerSwirl.addToLayout(self.gridLayout_Box, 1)

        # TODO Add new items

        self.gridLayout_Box.addWidget(self.resetButton,  3, 13, 1, 4)
        self.gridLayout_Box.addWidget(QtGui.QSplitter(QtCore.Qt.Vertical), 4, 0)
        self.sliderList.append(self.containerSwirl)

        self.setAllValues(self.sliderList)  # Set all values to start position

        return self.gridLayout_Box

    def resetButton_Event(self):
        self.reset(self.sliderList)

    def initializeSliderDefaultValues(self):
        fluidContainerObj = ContainerValuesUtils(self.fluidBoxName)
        print self.fluidBoxName
        self.DEF_VALUES.velocitySwirl_DEF = fluidContainerObj.getFluidContainerParamter(self.DEF_VALUES.velocitySwirl_NAME)
        self.DEF_VALUES.velocitySwirl_VISIBILITY = fluidContainerObj.getSliderStatusFromMaya(self.DEF_VALUES.velocitySwirl_SN, self.DEF_VALUES.velocitySwirl_NAME)
        print "////////////AA/////////////////"
        try:
            a = SliderState()
            l = 'Swirl'
            sliderStatusEnabled = a.findAEFieldByLabel(l).getEnable()
            print "BB: " + str(sliderStatusEnabled)
        except:
            sliderStatusEnabled = True
        print self.DEF_VALUES.velocitySwirl_VISIBILITY

        del fluidContainerObj

    def setAllValues(self, sliderList):
        for sliderItem in sliderList:
            sliderItem.resetValues()

    def setInitialVisibility(self, sliderList):
        for sliderItem in sliderList:
            sliderItem.resetValues()












