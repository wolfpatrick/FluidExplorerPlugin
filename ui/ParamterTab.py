from PySide import QtGui
from PySide import QtCore
from RangeSlider.HRangeSlider import QHRangeSlider
from SliderContainers.ParamterTabDefaultValues import ParameterTabDefaultValues

import maya.cmds as cmds


class SliderContainer(object):

        #def __init__(self, propertyName, sliderMinValue, sliderMaxValue, sliderDefaultValue, fieldName):
        def __init__(self, property, propertyName, nodeName, fullPropertyName=""):

            self.propertyName = propertyName

            self.groupBox_Box = QtGui.QWidget()
            gridLayout_Box = QtGui.QGridLayout()
            self.groupBox_Box.setLayout(gridLayout_Box)

            # Box elements
            txt = "<span style=\" font-size:8pt;\">" + property + "</span>"
            txt = property
            self.label = QtGui.QLabel(txt)
            tmp = " Property Name: " + propertyName + " \n"
            QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))



            self.checkBox = QtGui.QCheckBox("")
            print "--------------------------"
            print propertyName
            print nodeName

            [sliderMinValue, sliderMaxValue, sliderDefValue] = self.getFielDefaultValues(propertyName, nodeName)
            isAttrLocked = self.chekIfAttrIsLocked(propertyName, nodeName)
            self.isContainerLocked = isAttrLocked

            print isAttrLocked
            print "--------------------------"
            if len(fullPropertyName) > 0:
                toolTipTxt = "Full Name: " + fullPropertyName + ' '
                self.label.setToolTip(toolTipTxt)


            self.lineEditMin = QtGui.QLineEdit(str(sliderMinValue))
            self.lineEditMax = QtGui.QLineEdit(str(sliderMaxValue))
            self.lineEditDefault = QtGui.QLineEdit(str(sliderDefValue))
            self.rangeSlider = QHRangeSlider(self.lineEditMin, self.lineEditMax, self.lineEditDefault, range = [sliderMinValue, sliderMaxValue], enabledFlag=True)
            self.rangeSlider.defaultSingleValue = sliderDefValue
            self.lineEditMin.setFixedWidth(35), self.lineEditMin.setAlignment(QtCore.Qt.AlignCenter)
            self.lineEditMax.setFixedWidth(35), self.lineEditMax.setAlignment(QtCore.Qt.AlignCenter)
            self.lineEditDefault.setFixedWidth(35), self.lineEditDefault.setAlignment(QtCore.Qt.AlignRight)
            self.rangeSlider.setValues([sliderMinValue, sliderMaxValue])
            self.rangeSlider.setEmitWhileMoving(True)

            # Lock icon
            self.pix = QtGui.QPixmap(":/icon_lock_3.png").scaled(12, 12)
            self.lockImage = QtGui.QLabel()
            self.lockImage.setPixmap(self.pix)
            self.lockImage.setAlignment(QtCore.Qt.AlignLeft);

            self.resetButton = QtGui.QPushButton("Reset all Values")

            self.createConnections()
            self.initialComponents()
            self.iniSliderValues2()

        def setContainerLockedState(self, state):
            if not state:
                #self.rangeSlider.setVisible = state
                #self.rangeSlider.update()
                self.label.setEnabled(state)
                self.checkBox.setEnabled(state)
                self.lineEditDefault.setEnabled(state)
                self.lineEditMin.setEnabled(state)
                self.lineEditMax.setEnabled(state)
                self.rangeSlider.setEnabled(state)
                self.rangeSlider.enabledFlag = state

        def iniSliderValues2(self):
            self.rangeSlider.setValues([float(self.lineEditMin.text()), float(self.lineEditMax.text())])
            self.rangeSlider.update()

        def initialComponents(self):
            self.lineEditDefault.setEnabled(True)
            self.lineEditMin.setEnabled(False)
            self.lineEditMax.setEnabled(False)
            self.lineEditMin.setMaxLength(5)
            self.lineEditMax.setMaxLength(4)
            self.lineEditDefault.setMaxLength(4)
            self.checkBox.setChecked(False)
            self.rangeSlider.isRangeActive = False

        def addToLayout(self, gridLayout_Box, position):
            gridLayout_Box.addWidget(self.label, position, 0, 1, 2, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            gridLayout_Box.addWidget(self.checkBox, position, 2, QtCore.Qt.AlignCenter)
            gridLayout_Box.addWidget(self.lineEditDefault, position, 4, QtCore.Qt.AlignCenter)
            gridLayout_Box.addWidget(self.lineEditMin, position, 5, QtCore.Qt.AlignCenter)
            gridLayout_Box.addWidget(self.rangeSlider, position, 6, 1, 9-2)
            gridLayout_Box.addWidget(self.lineEditMax, position, 15-2, QtCore.Qt.AlignCenter)

            if self.isContainerLocked:
                gridLayout_Box.addWidget(self.lockImage, position, 0, 1, 2, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                self.checkBox.setEnabled(False)
                self.lineEditDefault.setEnabled(False)
                self.lineEditMin.setEnabled(False)
                self.rangeSlider.setEnabled(False)
                self.rangeSlider.changeSliderEnabled(False)
                self.lineEditMax.setEnabled(False)

                if self.propertyName == "densityScale":
                    self.label.setText("Dens. Scale")
                if self.propertyName == "tensionForce":
                    self.label.setText("Tension F.")
                if self.propertyName == "reactionSpeed":
                    self.label.setText("Reac. Sp.")

                self.label.update()


        def createConnections(self):
            self.checkBox.clicked.connect(self.checkBoxModeChanged_Event)
            self.lineEditDefault.editingFinished.connect(self.leaveLineEditDef_A)
            self.lineEditMin.editingFinished.connect(self.leaveLineEditMin_A)
            self.lineEditMax.editingFinished.connect(self.leaveLineEditMax_A)
            self.resetButton.clicked.connect(self.resetValues)

        # --------------------------------------------------------------------------------------------------------------

        @QtCore.Slot()
        def checkBoxModeChanged_Event(self):
            self.changeSliderMode(self.rangeSlider, self.checkBox, self.lineEditDefault, self.lineEditMin, self.lineEditMax)

        @QtCore.Slot()
        def leaveLineEditDef_A(self):
            self.leaveLineEditEvent(self.lineEditDefault,  self.rangeSlider)

        @QtCore.Slot()
        def leaveLineEditMin_A(self):
            self.leaveLineEditMinEvent(self.lineEditMin, self.lineEditMax, self.rangeSlider)

        @QtCore.Slot()
        def leaveLineEditMax_A(self):
            self.leaveLineEditMaxEvent(self.lineEditMin, self.lineEditMax,  self.rangeSlider)

        # --------------------------------------------------------------------------------------------------------------

        def changeSliderMode(self, slider, checkBox, lineEditDefault, lineEditMin, lineEditMax):
            if checkBox.checkState():
                # Range is active
                slider.isRangeActive = True
                slider.setValues([slider.rangeValues[0], slider.rangeValues[1]])
                slider.update()
                slider.repaint()
                lineEditDefault.setEnabled(False)
                lineEditMin.setEnabled(True)
                lineEditMax.setEnabled(True)
                lineEditMin.setText(str(format(slider.rangeValues[0], '.2f')))
                lineEditMax.setText(str(format(slider.rangeValues[1], '.2f')))
                lineEditMin.setFocus()
                lineEditDefault.setText(str(format(slider.defaultSingleValue, '.2f')))
            else:
                # Range is not active
                slider.isRangeActive = False
                lineEditDefault.setText(str(format(slider.defaultSingleValue, '.2f')))
                lineEditDefault.setEnabled(True)
                lineEditMin.setEnabled(False)
                lineEditMax.setEnabled(False)
                lineEditDefault.setFocus()
                slider.setValues([float(slider.defaultSingleValue), float(slider.defaultSingleValue)])
                slider.update()
                slider.repaint()
                lineEditMin.setText(str(format(slider.rangeValues[0], '.2f')))
                lineEditMax.setText(str(format(slider.rangeValues[1], '.2f')))

        def leaveLineEditMinEvent(self, lineEditMin, lineEditMax, slider):
                v_str = lineEditMin.text()
                try:
                    v = float(v_str)

                    if v < float(slider.rangeValues[0]):
                        #print "error to small"
                        lineEditMin.setText(str(format(slider.rangeValues[0], '.2f')))
                    elif v > float(slider.rangeValues[1]):
                        #print "error to big"
                        lineEditMin.setText(str(format(slider.rangeValues[1], '.2f')))
                        lineEditMax.setText(str(format(slider.rangeValues[1], '.2f')))
                    else:
                        #print "ok"
                        pass

                except ValueError:
                    lineEditMin.setText(str(format(slider.rangeValues[0], '.2f')))

                v1 = float(lineEditMin.text())
                v2 = float(lineEditMax.text())

                # Update slider and line edit
                slider.setValues([v1, v2])
                slider.update()
                lineEditMin.setText(str(format(v1, '.2f')))

        def leaveLineEditMaxEvent(self, lineEditMin, lineEditMax, slider):
            v_str = lineEditMax.text()
            try:
                v = float(v_str)

                if v < float(slider.rangeValues[0]):
                    #print "error to small"
                    lineEditMax.setText(str(format(slider.rangeValues[0], '.2f')))
                    lineEditMin.setText(str(format(slider.rangeValues[0], '.2f')))
                elif v > float(slider.rangeValues[1]):
                    #print "error to big"
                    lineEditMax.setText(str(format(slider.rangeValues[1], '.2f')))
                else:
                    #print "ok"
                    pass

            except ValueError:
                lineEditMax.setText(str(format(slider.rangeValues[1], '.2f')))

            v1 = float(lineEditMin.text())
            v2 = float(lineEditMax.text())

            # Update slider
            slider.setValues([v1, v2])
            slider.update()
            lineEditMax.setText(str(format(v2, '.2f')))

        def leaveLineEditEvent(self, lineEdit, slider):
            v_str = lineEdit.text()
            try:
                v = float(v_str)
                v = round(v, 2)

                if v < float(slider.rangeValues[0]):
                    #print "error to small"
                    lineEdit.setText(str(format(slider.rangeValues[0], '.2f')))
                    v = slider.rangeValues[0]
                elif v > float(slider.rangeValues[1]):
                    #print "error to big"
                    lineEdit.setText(str(format(slider.rangeValues[1], '.2f')))
                    v = slider.rangeValues[1]
                else:
                    pass
                    #print "OK"

            except ValueError:
                lineEdit.setText(str(format(slider.defaultSingleValue, '.2f')))
                v = float(slider.defaultSingleValue)

            # Set value
            slider.setValues([float(v), 0])
            slider.update()
            lineEdit.setText(str(format(v, '.2f')))

        def resetValues(self):
            if self.rangeSlider.isRangeActive:
                self.rangeSlider.setValues([self.rangeSlider.rangeValues[0], self.rangeSlider.rangeValues[1]])
                self.lineEditMin.setText(str(format(self.rangeSlider.rangeValues[0], '.2f')))
                self.lineEditMax.setText(str(format(self.rangeSlider.rangeValues[1], '.2f')))
            else:
                self.rangeSlider.setEmitWhileMoving(True)
                self.rangeSlider.setValues([self.rangeSlider.defaultSingleValue, 0])
                self.lineEditDefault.setText(str(format(self.rangeSlider.defaultSingleValue, '.2f')))
                self.rangeSlider.setValues([float(self.rangeSlider.defaultSingleValue), float(self.rangeSlider.defaultSingleValue)])

            self.rangeSlider.update()
            self.rangeSlider.repaint()

        def getFielDefaultValues(self, fieldName, nodeName):

            [minSoft, maxSoft] = ParameterTabDefaultValues.setSoftMinMaxValue(fieldName, nodeName)

            cmdStr = nodeName + '.' + fieldName
            currentValue = cmds.getAttr(cmdStr)

            return [minSoft, maxSoft, currentValue]

        def chekIfAttrIsLocked(self, fieldName, nodeName):

            isFieldLocked = False
            cmdStr = nodeName + '.' + fieldName
            try:
                isFieldLocked = cmds.getAttr(cmdStr, lock=True)
                return isFieldLocked
            except ValueError:
                print("Warning: Cannot get lock state of attribute: ", cmdStr)
                return isFieldLocked


class ParameterTab(object):

    def __init__(self, boxName):
        self.fluidBoxName = boxName
        self.setupTabWidget()

    def initialToolBoxComponents(self):
        for itemIndex in range(0, self.toolBox.count()):
            self.toolBox.setItemIcon(itemIndex, QtGui.QIcon(':/arrow_small_1.png'))
        self.toolBox.setItemIcon(0, QtGui.QIcon(':/arrow_small_2.png'))

    def setupTabWidget(self):

        #from SliderContainerLayouts import DiffusionLayout

        from SliderContainers.DensityLayout import DensityLayout
        from SliderContainers.VelocityLayout import VelocityLayout
        from SliderContainers.TurbulenceLayout import TurbulenceLayout
        from SliderContainers.TemperatureLayout import TemperatureLayout
        from SliderContainers.FuelLayout import FuelLayout
        from SliderContainers.ColorLayout import ColorLayout
        from SliderContainers.DynamicSimulationLayout import DynamicSimulationLayout

        # --------------------------------------------------------------------------------------------------------------
        #DiffusionBox = QtGui.QGroupBox()
        #self.DiffusionLayout = DiffusionLayout()
        #self.DiffusionLayout.setFluidBoxName(self.fluidBoxName)
        #DiffusionBox.setLayout(self.DiffusionLayout.getLayout())


        DensityBox = QtGui.QGroupBox()
        self.DensityLayout = DensityLayout()
        self.DensityLayout.setFluidBoxName(self.fluidBoxName)
        DensityBox.setLayout(self.DensityLayout.getLayout())

        VelocityBox = QtGui.QGroupBox()
        self.VelocityLayout = VelocityLayout()
        self.VelocityLayout.setFluidBoxName(self.fluidBoxName)
        VelocityBox.setLayout(self.VelocityLayout.getLayout())

        TurbulenceBox = QtGui.QGroupBox()
        self.TurbulenceLayout = TurbulenceLayout()
        self.TurbulenceLayout.setFluidBoxName(self.fluidBoxName)
        TurbulenceBox.setLayout(self.TurbulenceLayout.getLayout())

        TemperatureBox = QtGui.QGroupBox()
        self.TemperatureLayout = TemperatureLayout()
        self.TemperatureLayout.setFluidBoxName(self.fluidBoxName)
        TemperatureBox.setLayout(self.TemperatureLayout.getLayout())


        FuelBox = QtGui.QGroupBox()
        self.FuelLayout = FuelLayout()
        self.FuelLayout.setFluidBoxName(self.fluidBoxName)
        FuelBox.setLayout(self.FuelLayout.getLayout())

        ColorBox = QtGui.QGroupBox()
        self.ColorLayout = ColorLayout()
        self.ColorLayout.setFluidBoxName(self.fluidBoxName)
        ColorBox.setLayout(self.ColorLayout.getLayout())


        DynamicSimulationBox = QtGui.QGroupBox()
        self.DynamicSimulationLayout = DynamicSimulationLayout()
        self.DynamicSimulationLayout.setFluidBoxName(self.fluidBoxName)
        DynamicSimulationBox.setLayout(self.DynamicSimulationLayout.getLayout())


        # --------------------------------------------------------------------------------------------------------------

        # The toolbox stores all slider containers
        self.toolBox = QtGui.QToolBox()
        self.toolBox.addItem(DynamicSimulationBox, "Dynamic Simulation")
        self.toolBox.addItem(DensityBox, "Density")
        self.toolBox.addItem(VelocityBox, "Velocity")
        self.toolBox.addItem(TurbulenceBox, "Turbulence")
        self.toolBox.addItem(TemperatureBox, "Temperature")
        self.toolBox.addItem(FuelBox, "Fuel")
        self.toolBox.addItem(ColorBox, "Color")

        # Disable tool box items if method is set to 0 in maya
        self.toolBox.setItemEnabled(1, self.isItemEbabled(self.fluidBoxName + '.' + 'densityMethod'))
        self.toolBox.setItemEnabled(2, self.isItemEbabled(self.fluidBoxName + '.' + 'velocityMethod'))
        self.toolBox.setItemEnabled(4, self.isItemEbabled(self.fluidBoxName + '.' + 'temperatureMethod'))
        self.toolBox.setItemEnabled(5, self.isItemEbabled(self.fluidBoxName + '.' + 'fuelMethod'))
        self.toolBox.setItemEnabled(6, self.isItemEbabled(self.fluidBoxName + '.' + 'colorMethod'))

        #self.toolBox.addItem(DiffusionBox, " Menu_1")
        self.toolBox.currentChanged.connect(self.toolBoxChanged_Event)
        self.initialToolBoxComponents()

        vBoxlayout = QtGui.QVBoxLayout()
        vBoxlayout.addWidget(self.toolBox)

        self.parameterTab = QtGui.QWidget()
        self.parameterTab.setLayout(vBoxlayout)

    def createConnections(self):
        pass

    def getSelectedValuesFromSlider(self):
        from Utils.RangeSliderSpan import SliderSpanSelected

        self.selectedSliderValues = SliderSpanSelected(self.DynamicSimulationLayout, self.DensityLayout, self.VelocityLayout, self.TurbulenceLayout, self.TemperatureLayout, self.FuelLayout, self.ColorLayout)

        print "**********************************************"
        print self.selectedSliderValues
        print "**********************************************"

        return self.selectedSliderValues

    def randomValuesSnapshot(self):
        return self.VelocityLayout.containerSwirl.getSliderValues()

    def toolBoxChanged_Event(self):
        currentTabIndex = self.toolBox.currentIndex()
        for itemIndex in range(self.toolBox.count()):
            self.toolBox.setItemIcon(itemIndex, QtGui.QIcon(':/arrow_small_1.png'))
            if itemIndex == currentTabIndex:
                self.toolBox.setUpComponentsItemIcon(itemIndex, QtGui.QIcon(':/arrow_small_2.png'))

        self.initAllSlidersOfTheBox()

    def getTab(self):
        return self.parameterTab

    def initAllSlidersOfTheBox(self):
        pass

    def isItemEbabled(self, cmdStr):
        try:
            flag = cmds.getAttr(cmdStr)
            print("Flag", flag)
            if flag == 0:
                return False
            else:
                return True
        except ValueError:
            return True




