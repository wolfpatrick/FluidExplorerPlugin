from PySide import QtGui
from PySide import QtCore
from RangeSlider.HRangeSlider import QHRangeSlider


class SliderContainer(object):

        def __init__(self, propertyName, sliderMinValue, sliderMaxValue, sliderDefaultValue):

            self.groupBox_Box = QtGui.QWidget()
            gridLayout_Box = QtGui.QGridLayout()
            self.groupBox_Box.setLayout(gridLayout_Box)

            # Box elements
            txt = "<b>" + propertyName + "</b>"
            self.label = QtGui.QLabel(txt)
            self.checkBox = QtGui.QCheckBox("")
            self.checkBox.setChecked(True)
            self.lineEditMin = QtGui.QLineEdit(str(sliderMinValue))
            self.lineEditMax = QtGui.QLineEdit(str(sliderMaxValue))
            self.lineEditDefault = QtGui.QLineEdit(str(sliderDefaultValue))
            self.rangeSlider = QHRangeSlider(self.lineEditMin, self.lineEditMax, self.lineEditDefault, range = [sliderMinValue, sliderMaxValue], enabledFlag=True)
            self.rangeSlider.defaultSingleValue = sliderDefaultValue
            self.lineEditMin.setFixedWidth(40), self.lineEditMin.setAlignment(QtCore.Qt.AlignCenter)
            self.lineEditMax.setFixedWidth(40), self.lineEditMax.setAlignment(QtCore.Qt.AlignCenter)
            self.lineEditDefault.setFixedWidth(39), self.lineEditDefault.setAlignment(QtCore.Qt.AlignCenter)
            self.rangeSlider.setValues([sliderMinValue, sliderMaxValue])  # --> 2 ??
            self.rangeSlider.setEmitWhileMoving(True)
            self.rangeSlider.update()

            self.resetButton = QtGui.QPushButton("Reset all Values")

            self.createConnections()
            self.initialComponents()

        def iniSliderValues(self, min, max):
            self.rangeSlider.setValues([min, max])
            self.rangeSlider.update()

        def initialComponents(self):
            self.lineEditDefault.setEnabled(False)

        def addToLayout(self, gridLayout_Box, position):
            gridLayout_Box.addWidget(self.label, position, 0, 1, 2, QtCore.Qt.AlignRight)
            gridLayout_Box.addWidget(self.checkBox, position, 2, QtCore.Qt.AlignCenter)
            gridLayout_Box.addWidget(self.lineEditDefault, position, 4, QtCore.Qt.AlignCenter)
            gridLayout_Box.addWidget(self.lineEditMin, position, 5, QtCore.Qt.AlignCenter)
            gridLayout_Box.addWidget(self.rangeSlider, position, 6, 1, 10)
            gridLayout_Box.addWidget(self.lineEditMax, position, 16, QtCore.Qt.AlignCenter)

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
                lineEditDefault.setEnabled(False)
                lineEditMin.setEnabled(True)
                lineEditMax.setEnabled(True)
                lineEditMin.setText(str(slider.rangeValues[0]))
                lineEditMax.setText(str(slider.rangeValues[1]))
                lineEditMin.setFocus()
                lineEditDefault.setText(str(slider.defaultSingleValue))
            else:
                # Range is not active
                slider.isRangeActive = False
                lineEditDefault.setText(str(slider.defaultSingleValue))
                lineEditDefault.setEnabled(True)
                lineEditMin.setEnabled(False)
                lineEditMax.setEnabled(False)
                lineEditDefault.setFocus()
                slider.setValues([float(slider.defaultSingleValue), float(slider.defaultSingleValue)])
                lineEditMin.setText(str(slider.rangeValues[0]))
                lineEditMax.setText(str(slider.rangeValues[1]))

            slider.update()

        def leaveLineEditMinEvent(self, lineEditMin, lineEditMax, slider):
                v_str = lineEditMin.text()
                try:
                    v = float(v_str)

                    if v < float(slider.rangeValues[0]):
                        #print "error to small"
                        lineEditMin.setText(str(slider.rangeValues[0]))
                    elif v > float(slider.rangeValues[1]):
                        #print "error to big"
                        lineEditMin.setText(str(slider.rangeValues[1]))
                        lineEditMax.setText(str(slider.rangeValues[1]))
                    else:
                        #print "ok"
                        pass

                except ValueError:
                    lineEditMin.setText(str(slider.rangeValues[0]))

                v1 = float(lineEditMin.text())
                v2 = float(lineEditMax.text())

                # Update slider
                slider.setValues([v1, v2])
                slider.update()

        def leaveLineEditMaxEvent(self, lineEditMin, lineEditMax, slider):
            v_str = lineEditMax.text()
            try:
                v = float(v_str)

                if v < float(slider.rangeValues[0]):
                    #print "error to small"
                    lineEditMax.setText(str(slider.rangeValues[0]))
                    lineEditMin.setText(str(slider.rangeValues[0]))
                elif v > float(slider.rangeValues[1]):
                    #print "error to big"
                    lineEditMax.setText(str(slider.rangeValues[1]))
                else:
                    #print "ok"
                    pass

            except ValueError:
                lineEditMax.setText(str(slider.rangeValues[1]))

            v1 = float(lineEditMin.text())
            v2 = float(lineEditMax.text())

            # Update slider
            slider.setValues([v1, v2])
            slider.update()

        def leaveLineEditEvent(self, lineEdit, slider):
            v_str = lineEdit.text()
            try:
                v = float(v_str)

                if v < float(slider.rangeValues[0]):
                    #print "error to small"
                    lineEdit.setText(str(slider.rangeValues[0]))
                    v = slider.rangeValues[0]
                elif v > float(slider.rangeValues[1]):
                    #print "error to big"
                    lineEdit.setText(str(slider.rangeValues[1]))
                    v = slider.rangeValues[1]
                else:
                    pass
                    #print "OK"

            except ValueError:
                lineEdit.setText(str(float(slider.defaultSingleValue)))
                v = float(slider.defaultSingleValue)

            # Set value
            slider.setValues([float(v), 0])
            slider.update()

        def resetValues(self):
            print 'dasdsddas'
            if self.rangeSlider.isRangeActive:
                self.rangeSlider.setValues([self.rangeSlider.rangeValues[0], self.rangeSlider.rangeValues[1]])
                self.lineEditMin.setText(str(self.rangeSlider.rangeValues[0]))
                self.lineEditMax.setText(str(self.rangeSlider.rangeValues[1]))
            else:
                self.rangeSlider.setValues([self.rangeSlider.defaultSingleValue, 0])
                self.lineEditDefault.setText(str(self.rangeSlider.defaultSingleValue))

            self.rangeSlider.update()


class ParameterTab(object):

    def __init__(self):
        self.setupTabWidget()

    def initialToolBoxComponents(self):
        for itemIndex in range(0,self.toolBox.count()):
            self.toolBox.setItemIcon(itemIndex, QtGui.QIcon(':/arrow_small_1.png'))
        self.toolBox.setItemIcon(0, QtGui.QIcon(':/arrow_small_2.png'))

    def setupTabWidget(self):

        from SliderContainerLayouts import DiffusionLayout
        from SliderContainerLayouts import VelocityLayout

        DiffusionBox = QtGui.QGroupBox()
        self.DiffusionLayout = DiffusionLayout()
        DiffusionBox.setLayout(self.DiffusionLayout.getLayout())

        VelocityBox = QtGui.QGroupBox()
        self.VelocityLayout = VelocityLayout()
        VelocityBox.setLayout(self.VelocityLayout.getLayout())

        # The toolbox stores all slider containers
        self.toolBox = QtGui.QToolBox()
        self.toolBox.addItem(DiffusionBox, " Menu_1")
        self.toolBox.addItem(VelocityBox, " Velocity")
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

        self.selectedSliderValues = SliderSpanSelected(self.VelocityLayout)
        return self.selectedSliderValues

    def randomValuesSnapshot(self):
        return self.VelocityLayout.containerSwirl.getSliderValues()

    def toolBoxChanged_Event(self):
        currentTabIndex = self.toolBox.currentIndex()
        for itemIndex in range(self.toolBox.count()):
            self.toolBox.setItemIcon(itemIndex, QtGui.QIcon(':/arrow_small_1.png'))
            if itemIndex == currentTabIndex:
                self.toolBox.setItemIcon(itemIndex, QtGui.QIcon(':/arrow_small_2.png'))

    def getTab(self):
        return self.parameterTab