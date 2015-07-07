__author__ = 'patrick'

from PySide import QtGui
from PySide import QtCore

from RangeSlider.HRangeSlider import QHRangeSlider
from DefaultUIValues import DefaultUIParameters
from MayaCacheCommandParameters import MayaCacheCommand

class ParameterInputBoxes(QtGui.QMainWindow):

    def __init__(self):
        pass

    def createBox_DENSITY(self, paramEnabled_Buoyancy, paramEnabled_Dissipation, paramEnabled_Diffusion):

        myBox_density = QtGui.QGroupBox("Density")
        myBox_density_layout = QtGui.QGridLayout()

        myBox_density_layout.addWidget(QtGui.QLabel("Default"),        0, 1, QtCore.Qt.AlignCenter)
        myBox_density_layout.addWidget(QtGui.QLabel("MIN"),            0, 2, QtCore.Qt.AlignCenter)
        myBox_density_layout.addWidget(QtGui.QLabel("MAX"),            0, 9, QtCore.Qt.AlignCenter)

        # ----- BUOYANCY -----
        self.lineEdit_BUOYANY_MIN = QtGui.QLineEdit(DefaultUIParameters.DEF_BUOYANCY_MIN)
        self.lineEdit_BUOYANY_MIN.setFixedWidth(40)
        self.lineEdit_BUOYANY_MIN.setAlignment(QtCore.Qt.AlignCenter)

        self.lineEdit_BUOYANY_MAX = QtGui.QLineEdit(DefaultUIParameters.DEF_BUOYANCY_MAX)
        self.lineEdit_BUOYANY_MAX.setFixedWidth(40)
        self.lineEdit_BUOYANY_MAX.setAlignment(QtCore.Qt.AlignCenter)

        if paramEnabled_Buoyancy == False:
            self.lineEdit_BUOYANY_MIN.setEnabled(False)
            self.lineEdit_BUOYANY_MAX.setEnabled(False)

        txt = "<b>Buoyancy</b>"
        if paramEnabled_Buoyancy == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_density_layout.addWidget(QtGui.QLabel(txt), 1, 0, QtCore.Qt.AlignRight)    # --> The first lable should have a fixed size of 11 characters --> FIX

        txt = " 1.0 "
        if paramEnabled_Buoyancy == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_density_layout.addWidget(QtGui.QLabel(txt), 1, 1, QtCore.Qt.AlignCenter)

        self.slider_BUOYANY = QHRangeSlider(self.lineEdit_BUOYANY_MIN, self.lineEdit_BUOYANY_MAX,
                                                range = [float(DefaultUIParameters.DEF_BUOYANCY_MIN),
                                                float(DefaultUIParameters.DEF_BUOYANCY_MAX)],
                                                enabledFlag=paramEnabled_Buoyancy)

        self.slider_BUOYANY.setValues([-5, 10])  # --> 10 ??
        self.slider_BUOYANY.setEmitWhileMoving(True)
        if paramEnabled_Buoyancy == False:
            self.slider_BUOYANY.setEnabled(False)

        myBox_density_layout.addWidget(self.slider_BUOYANY, 1, 3, 1, 6 )
        myBox_density_layout.addWidget(self.lineEdit_BUOYANY_MIN, 1, 2, QtCore.Qt.AlignCenter)
        myBox_density_layout.addWidget(self.lineEdit_BUOYANY_MAX, 1, 9, QtCore.Qt.AlignCenter)
        self.slider_BUOYANY.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # ----- BUOYANCY -----

        # ----- Dissipation -----
        self.lineEdit_Dissipation_MIN = QtGui.QLineEdit(DefaultUIParameters.DEF_DISSIPATION_MIN)
        self.lineEdit_Dissipation_MIN.setFixedWidth(40)
        self.lineEdit_Dissipation_MIN.setAlignment(QtCore.Qt.AlignCenter)

        self.lineEdit_Dissipation_MAX = QtGui.QLineEdit(DefaultUIParameters.DEF_DISSIPATION_MAX)
        self.lineEdit_Dissipation_MAX.setFixedWidth(40)
        self.lineEdit_Dissipation_MAX.setAlignment(QtCore.Qt.AlignCenter)

        if paramEnabled_Dissipation == False:
            self.lineEdit_Dissipation_MIN.setEnabled(False)
            self.lineEdit_Dissipation_MAX.setEnabled(False)

        txt = "<b>Dissipation</b>"
        if paramEnabled_Dissipation == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_density_layout.addWidget(QtGui.QLabel(txt), 2, 0, QtCore.Qt.AlignRight)

        txt = " 0.0 "
        if paramEnabled_Dissipation == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_density_layout.addWidget(QtGui.QLabel(txt), 2, 1, QtCore.Qt.AlignCenter)

        self.slider_Dissipation = QHRangeSlider(self.lineEdit_Dissipation_MIN, self.lineEdit_Dissipation_MAX,
                                                    range = [float(DefaultUIParameters.DEF_DISSIPATION_MIN),
                                                    float(DefaultUIParameters.DEF_DISSIPATION_MAX)],
                                                    enabledFlag=paramEnabled_Dissipation)

        self.slider_Dissipation.setValues([0, 1.5])  # --> 2 ??
        self.slider_Dissipation.setEmitWhileMoving(True)
        if paramEnabled_Dissipation == False:
            self.slider_Dissipation.setEnabled(False)

        myBox_density_layout.addWidget(self.slider_Dissipation, 2, 3, 1, 6 )
        myBox_density_layout.addWidget(self.lineEdit_Dissipation_MIN, 2, 2, QtCore.Qt.AlignCenter)
        myBox_density_layout.addWidget(self.lineEdit_Dissipation_MAX, 2, 9, QtCore.Qt.AlignCenter)
        self.slider_Dissipation.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # ----- Dissipation -----

        # ----- Diffusion -----
        self.lineEdit_DIFFUSION_MIN = QtGui.QLineEdit(DefaultUIParameters.DEF_DIFFUSION_MIN)
        self.lineEdit_DIFFUSION_MIN.setFixedWidth(40)
        self.lineEdit_DIFFUSION_MIN.setAlignment(QtCore.Qt.AlignCenter)

        self.lineEdit_DIFFUSION_MAX = QtGui.QLineEdit(DefaultUIParameters.DEF_DIFFUSION_MAX)
        self.lineEdit_DIFFUSION_MAX.setFixedWidth(40)
        self.lineEdit_DIFFUSION_MAX.setAlignment(QtCore.Qt.AlignCenter)

        if paramEnabled_Diffusion == False:
            self.lineEdit_DIFFUSION_MIN.setEnabled(False)
            self.lineEdit_DIFFUSION_MAX.setEnabled(False)

        txt = "<b>Diffusion</b>"
        if paramEnabled_Diffusion == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_density_layout.addWidget(QtGui.QLabel(txt), 3, 0, QtCore.Qt.AlignRight)

        txt = " 0.0 "
        if paramEnabled_Diffusion == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_density_layout.addWidget(QtGui.QLabel(txt), 3, 1, QtCore.Qt.AlignCenter)

        self.slider_DIFFUSION = QHRangeSlider(self.lineEdit_DIFFUSION_MIN, self.lineEdit_DIFFUSION_MAX,
                                                range = [float(DefaultUIParameters.DEF_DIFFUSION_MIN),
                                                float(DefaultUIParameters.DEF_DIFFUSION_MAX)],
                                                enabledFlag=paramEnabled_Diffusion)

        self.slider_DIFFUSION.setValues([0, 3])  # --> 3 ??
        self.slider_DIFFUSION.setEmitWhileMoving(True)

        if paramEnabled_Diffusion == False:
            self.slider_DIFFUSION.setEnabled(False)

        myBox_density_layout.addWidget(self.slider_DIFFUSION, 3, 3, 1, 6 )
        self.slider_DIFFUSION.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        myBox_density_layout.addWidget(self.lineEdit_DIFFUSION_MIN, 3, 2, QtCore.Qt.AlignCenter)
        myBox_density_layout.addWidget(self.lineEdit_DIFFUSION_MAX, 3, 9, QtCore.Qt.AlignCenter)
        # ----- Dissipation -----

        # Set to layout
        myBox_density.setLayout(myBox_density_layout)

        return  [ myBox_density,
                  self.lineEdit_BUOYANY_MIN, self.lineEdit_BUOYANY_MAX, self.slider_BUOYANY,
                  self.slider_Dissipation, self.lineEdit_Dissipation_MIN, self.lineEdit_Dissipation_MAX,
                  self.slider_DIFFUSION, self.lineEdit_DIFFUSION_MIN, self.lineEdit_DIFFUSION_MAX ]

    def createBox_VELOCITY(self, paramEnabled_SWIRL):

        self.myBox_velocity = QtGui.QGroupBox("Velocity")
        self.myBox_velocity_layout = QtGui.QGridLayout()

        self.myBox_velocity_layout.addWidget(QtGui.QLabel("Default"),        0, 1, QtCore.Qt.AlignCenter)
        self.myBox_velocity_layout.addWidget(QtGui.QLabel("MIN"),            0, 2, QtCore.Qt.AlignCenter)
        self.myBox_velocity_layout.addWidget(QtGui.QLabel("MAX"),            0, 9, QtCore.Qt.AlignCenter)
        self.myBox_velocity.setLayout(self.myBox_velocity_layout)

        # ----- SWIRL -----
        self.lineEdit_SWIRL_MIN = QtGui.QLineEdit(DefaultUIParameters.DEF_SWIRL_MIN)
        self.lineEdit_SWIRL_MIN.setFixedWidth(40)
        self.lineEdit_SWIRL_MIN.setAlignment(QtCore.Qt.AlignCenter)

        self.lineEdit_SWIRL_MAX = QtGui.QLineEdit(DefaultUIParameters.DEF_SWIRL_MAX)
        self.lineEdit_SWIRL_MAX.setFixedWidth(40)
        self.lineEdit_SWIRL_MAX.setAlignment(QtCore.Qt.AlignCenter)

        txt = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        txt = txt + "<b>Swirl</b>"
        if paramEnabled_SWIRL == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        self.myBox_velocity_layout.addWidget(QtGui.QLabel(txt), 1, 0, QtCore.Qt.AlignRight)    # --> The first lable should have a fixed size of 11 characters --> FIX

        txt = " 0.0 "
        if paramEnabled_SWIRL == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        self.myBox_velocity_layout.addWidget(QtGui.QLabel(txt), 1, 1, QtCore.Qt.AlignCenter)

        if paramEnabled_SWIRL == False:
            self.lineEdit_SWIRL_MIN.setEnabled(False)
            self.lineEdit_SWIRL_MAX.setEnabled(False)

        self.slider_SWIRL = QHRangeSlider(self.lineEdit_SWIRL_MIN, self.lineEdit_SWIRL_MAX,
                                            range = [float(DefaultUIParameters.DEF_SWIRL_MIN),
                                            float(DefaultUIParameters.DEF_SWIRL_MAX)],
                                            enabledFlag=paramEnabled_SWIRL)

        self.slider_SWIRL.setValues([0, 15])  # --> 20 ??
        self.slider_SWIRL.setEmitWhileMoving(True)
        self.slider_SWIRL.setToolTip("Slider Range: 0 - 10 ")
        if paramEnabled_SWIRL == False:
            self.slider_SWIRL.setEnabled(False)

        self.myBox_velocity_layout.addWidget(self.slider_SWIRL, 1, 3, 1, 6 )
        self.myBox_velocity_layout.addWidget(self.lineEdit_SWIRL_MIN, 1, 2, QtCore.Qt.AlignCenter)
        self.myBox_velocity_layout.addWidget(self.lineEdit_SWIRL_MAX, 1, 9, QtCore.Qt.AlignCenter)
        self.slider_SWIRL.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # ----- SWIRL -----

        return [ self.myBox_velocity, self.slider_SWIRL, self.lineEdit_SWIRL_MIN, self.lineEdit_SWIRL_MAX ]


    def createBox_TURBULENCE(self, paramEnabled_SPEED, paramEnabled_FREQUENCY, paramEnabled_STRENGTH):

        myBox_turbulence = QtGui.QGroupBox("Turbulence")
        myBox_turbulence_layout = QtGui.QGridLayout()

        myBox_turbulence_layout.addWidget(QtGui.QLabel("Default"),        0, 1, QtCore.Qt.AlignCenter)
        myBox_turbulence_layout.addWidget(QtGui.QLabel("MIN"),            0, 2, QtCore.Qt.AlignCenter)
        myBox_turbulence_layout.addWidget(QtGui.QLabel("MAX"),            0, 9, QtCore.Qt.AlignCenter)

        # ----- SPEED -----
        self.lineEdit_SPEED_MIN = QtGui.QLineEdit(DefaultUIParameters.DEF_SPEED_MIN)
        self.lineEdit_SPEED_MIN.setFixedWidth(40)
        self.lineEdit_SPEED_MIN.setAlignment(QtCore.Qt.AlignCenter)

        self.lineEdit_SPEED_MAX = QtGui.QLineEdit(DefaultUIParameters.DEF_SPEED_MAX)
        self.lineEdit_SPEED_MAX.setFixedWidth(40)
        self.lineEdit_SPEED_MAX.setAlignment(QtCore.Qt.AlignCenter)

        txt = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        txt = txt + "<b>Speed</b>"
        if paramEnabled_SPEED == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_turbulence_layout.addWidget(QtGui.QLabel(txt), 1, 0, QtCore.Qt.AlignRight)

        txt = "0.2"
        if paramEnabled_SPEED == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_turbulence_layout.addWidget(QtGui.QLabel(txt), 1, 1, QtCore.Qt.AlignCenter)

        self.slider_SPEED = QHRangeSlider(self.lineEdit_SPEED_MIN, self.lineEdit_SPEED_MAX,
                                          range = [float(DefaultUIParameters.DEF_SPEED_MIN),
                                          float(DefaultUIParameters.DEF_SPEED_MAX)],
                                          enabledFlag=paramEnabled_SPEED)

        self.slider_SPEED.setValues([0, 3])  # --> 10 ??
        self.slider_SPEED.setEmitWhileMoving(True)

        myBox_turbulence_layout.addWidget(self.slider_SPEED, 1, 3, 1, 6 )
        self.slider_SPEED.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        myBox_turbulence_layout.addWidget(self.lineEdit_SPEED_MIN, 1, 2, QtCore.Qt.AlignCenter)
        myBox_turbulence_layout.addWidget(self.lineEdit_SPEED_MAX, 1, 9, QtCore.Qt.AlignCenter)
        if paramEnabled_SPEED == False:
            self.slider_SPEED.setEnabled(False)
            self.lineEdit_SPEED_MAX.setEnabled(False)
            self.lineEdit_SPEED_MIN.setEnabled(False)
        # ----- SPEED -----

        # ----- FREQUENCY -----
        self.lineEdit_FREQUENCY_MIN = QtGui.QLineEdit(DefaultUIParameters.DEF_FREQ_MIN)
        self.lineEdit_FREQUENCY_MIN.setFixedWidth(40)
        self.lineEdit_FREQUENCY_MIN.setAlignment(QtCore.Qt.AlignCenter)

        self.lineEdit_FREQUENCY_MAX = QtGui.QLineEdit(DefaultUIParameters.DEF_FREQ_MAX)
        self.lineEdit_FREQUENCY_MAX.setFixedWidth(40)
        self.lineEdit_FREQUENCY_MAX.setAlignment(QtCore.Qt.AlignCenter)

        txt = "<b>Frequency</b>"
        if paramEnabled_FREQUENCY == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_turbulence_layout.addWidget(QtGui.QLabel(txt), 2, 0, QtCore.Qt.AlignRight)

        txt = " 0.2 "
        if paramEnabled_FREQUENCY == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_turbulence_layout.addWidget(QtGui.QLabel(txt), 2, 1, QtCore.Qt.AlignCenter)

        self.slider_FREQUENCY = QHRangeSlider(self.lineEdit_FREQUENCY_MIN, self.lineEdit_FREQUENCY_MAX,
                                                range = [float(DefaultUIParameters.DEF_FREQ_MIN),
                                                float(DefaultUIParameters.DEF_FREQ_MAX)],
                                                enabledFlag=paramEnabled_FREQUENCY)

        self.slider_FREQUENCY.setValues([0, 3])  # --> 2 ??
        self.slider_FREQUENCY.setEmitWhileMoving(True)
        myBox_turbulence_layout.addWidget(self.slider_FREQUENCY, 2, 3, 1, 6 )
        self.slider_FREQUENCY.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        myBox_turbulence_layout.addWidget(self.lineEdit_FREQUENCY_MIN, 2, 2, QtCore.Qt.AlignCenter)
        myBox_turbulence_layout.addWidget(self.lineEdit_FREQUENCY_MAX, 2, 9, QtCore.Qt.AlignCenter)

        if paramEnabled_FREQUENCY == False:
            self.lineEdit_FREQUENCY_MIN.setEnabled(False)
            self.lineEdit_FREQUENCY_MAX.setEnabled(False)
            self.slider_FREQUENCY.setEnabled(False)
        # ----- FREQUENCY -----

        # ----- STRENGTH -----
        self.lineEdit_STRENGTH_MIN = QtGui.QLineEdit(DefaultUIParameters.DEF_STRENGTH_MIN)
        self.lineEdit_STRENGTH_MIN.setFixedWidth(40)
        self.lineEdit_STRENGTH_MIN.setAlignment(QtCore.Qt.AlignCenter)

        self.lineEdit_STRENGTH_MAX = QtGui.QLineEdit(DefaultUIParameters.DEF_STRENGTH_MAX)
        self.lineEdit_STRENGTH_MAX.setFixedWidth(40)
        self.lineEdit_STRENGTH_MAX.setAlignment(QtCore.Qt.AlignCenter)

        self.slider_STRENGTH = QHRangeSlider(self.lineEdit_STRENGTH_MIN, self.lineEdit_STRENGTH_MAX,
                                                range = [float(DefaultUIParameters.DEF_STRENGTH_MIN),
                                                float(DefaultUIParameters.DEF_STRENGTH_MAX)],
                                                enabledFlag=paramEnabled_STRENGTH)

        self.slider_STRENGTH.setValues([0, 1.5])  # --> 3 ??
        self.slider_STRENGTH.setEmitWhileMoving(True)
        self.slider_STRENGTH.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        txt = "<b>Strength</b>"
        if paramEnabled_STRENGTH == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_turbulence_layout.addWidget(QtGui.QLabel(txt), 3, 0, QtCore.Qt.AlignRight)

        txt = " 0.0 "
        if paramEnabled_STRENGTH == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_turbulence_layout.addWidget(QtGui.QLabel(txt), 3, 1, QtCore.Qt.AlignCenter)

        myBox_turbulence_layout.addWidget(self.slider_STRENGTH, 3, 3, 1, 6 )
        myBox_turbulence_layout.addWidget(self.lineEdit_STRENGTH_MIN, 3, 2, QtCore.Qt.AlignCenter)
        myBox_turbulence_layout.addWidget(self.lineEdit_STRENGTH_MAX, 3, 9, QtCore.Qt.AlignCenter)

        if paramEnabled_STRENGTH == False:
            self.lineEdit_STRENGTH_MIN.setEnabled(False)
            self.lineEdit_STRENGTH_MAX.setEnabled(False)
            self.slider_STRENGTH.setEnabled(False)
        # ----- STRENGTH -----
        # Set to layout
        myBox_turbulence.setLayout(myBox_turbulence_layout)

        return  [ myBox_turbulence,
                  self.slider_SPEED, self.lineEdit_SPEED_MIN, self.lineEdit_SPEED_MAX,
                  self.slider_FREQUENCY, self.lineEdit_FREQUENCY_MIN, self.lineEdit_FREQUENCY_MAX ]


    def createBox_DYNAMIC_SIM(self, parameterEnabled_VISCOSITY):

        myBox_dynamicsim = QtGui.QGroupBox("Dynamic Simulation")
        myBox_dynamicsim_layout = QtGui.QGridLayout()

        myBox_dynamicsim_layout.addWidget(QtGui.QLabel("Default"),        0, 1, QtCore.Qt.AlignCenter)
        myBox_dynamicsim_layout.addWidget(QtGui.QLabel("MIN"),            0, 2, QtCore.Qt.AlignCenter)
        myBox_dynamicsim_layout.addWidget(QtGui.QLabel("MAX"),            0, 9, QtCore.Qt.AlignCenter)
        myBox_dynamicsim.setLayout(myBox_dynamicsim_layout)

       # ----- SWIRL -----
        self.lineEdit_VISCOSITY_MIN = QtGui.QLineEdit("0.0")
        self.lineEdit_VISCOSITY_MIN.setFixedWidth(40)
        self.lineEdit_VISCOSITY_MIN.setAlignment(QtCore.Qt.AlignCenter)

        self.lineEdit_VISCOSITY_MAX = QtGui.QLineEdit("1.0")
        self.lineEdit_VISCOSITY_MAX.setFixedWidth(40)
        self.lineEdit_VISCOSITY_MAX.setAlignment(QtCore.Qt.AlignCenter)

        self.slider_VISCOSITY = QHRangeSlider(self.lineEdit_VISCOSITY_MIN, self.lineEdit_VISCOSITY_MAX,
                                                range = [float(DefaultUIParameters.DEF_VISCOSITY_MIN),
                                                float(DefaultUIParameters.DEF_VISCOSITY_MAX)],
                                                enabledFlag=parameterEnabled_VISCOSITY)

        self.slider_VISCOSITY.setValues([0, 1.5])  # --> 1.5 ??
        self.slider_VISCOSITY.setEmitWhileMoving(True)

        txt = "&nbsp;&nbsp;&nbsp;&nbsp;"
        txt = txt + "<b>Viscosity</b>"
        if parameterEnabled_VISCOSITY == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_dynamicsim_layout.addWidget(QtGui.QLabel(txt), 1, 0, QtCore.Qt.AlignRight)

        txt = " 0.0 "
        if parameterEnabled_VISCOSITY == False:
            txt = "<font style='color: #505050 ;'>" + txt + "</font>"
        myBox_dynamicsim_layout.addWidget(QtGui.QLabel(txt), 1, 1, QtCore.Qt.AlignCenter)

        """
        tmp = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        tmp = "&nbsp;&nbsp;&nbsp;&nbsp;"
        myBox_dynamicsim_layout.addWidget(QtGui.QLabel(tmp+"<b>Viscosity</b>"),   1, 0, QtCore.Qt.AlignRight)    # --> The first lable should have a fixed size of 11 characters --> FIX
        #myBox_dynamicsim_layout.addWidget(QtGui.QLabel(" 0 | 1"),            1, 1, QtCore.Qt.AlignCenter)
        myBox_dynamicsim_layout.addWidget(QtGui.QLabel(" 0.0 "),            1, 1, QtCore.Qt.AlignCenter)
        """

        myBox_dynamicsim_layout.addWidget(self.slider_VISCOSITY, 1, 3, 1, 6 )
        self.slider_VISCOSITY.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        myBox_dynamicsim_layout.addWidget(self.lineEdit_VISCOSITY_MIN, 1, 2, QtCore.Qt.AlignCenter)
        myBox_dynamicsim_layout.addWidget(self.lineEdit_VISCOSITY_MAX, 1, 9, QtCore.Qt.AlignCenter)

        if parameterEnabled_VISCOSITY == False:
            self.slider_VISCOSITY.setEnabled(False)
            self.lineEdit_VISCOSITY_MIN.setEnabled(False)
            self.lineEdit_VISCOSITY_MAX.setEnabled(False)
        # ----- SWIRL -----

        return [ myBox_dynamicsim, self.slider_VISCOSITY, self.lineEdit_VISCOSITY_MIN, self.lineEdit_VISCOSITY_MAX ]


    @QtCore.Slot()
    def pushButtonReset_Event(self):
        print "Reset"
        # Update all values
        self.lineEdit_BUOYANY_MIN.setText(DefaultUIParameters.DEF_BUOYANCY_MIN)
        self.lineEdit_BUOYANY_MAX.setText(DefaultUIParameters.DEF_BUOYANCY_MAX)
        self.lineEdit_Dissipation_MIN.setText(DefaultUIParameters.DEF_DISSIPATION_MIN)
        self.lineEdit_Dissipation_MAX.setText(DefaultUIParameters.DEF_DISSIPATION_MAX)
        self.lineEdit_Dissipation_MAX.setText(DefaultUIParameters.DEF_DISSIPATION_MAX)
        self.lineEdit_DIFFUSION_MIN.setText(DefaultUIParameters.DEF_DIFFUSION_MIN)
        self.lineEdit_DIFFUSION_MAX.setText(DefaultUIParameters.DEF_DIFFUSION_MAX)

        self.lineEdit_SWIRL_MIN.setText(DefaultUIParameters.DEF_SWIRL_MIN)
        self.lineEdit_SWIRL_MAX.setText(DefaultUIParameters.DEF_SWIRL_MAX)

        self.lineEdit_SPEED_MIN.setText(DefaultUIParameters.DEF_SPEED_MIN)
        self.lineEdit_SPEED_MAX.setText(DefaultUIParameters.DEF_SPEED_MAX)
        self.lineEdit_FREQUENCY_MIN.setText(DefaultUIParameters.DEF_FREQ_MIN)
        self.lineEdit_FREQUENCY_MAX.setText(DefaultUIParameters.DEF_FREQ_MAX)
        self.lineEdit_STRENGTH_MIN.setText(DefaultUIParameters.DEF_STRENGTH_MIN)
        self.lineEdit_STRENGTH_MAX.setText(DefaultUIParameters.DEF_STRENGTH_MAX)

        self.lineEdit_VISCOSITY_MIN.setText(DefaultUIParameters.DEF_VISCOSITY_MIN)
        self.lineEdit_VISCOSITY_MAX.setText(DefaultUIParameters.DEF_VISCOSITY_MAX)

        # Update all sliders
        self.slider_BUOYANY.setValues([float(DefaultUIParameters.DEF_BUOYANCY_MIN), float(DefaultUIParameters.DEF_BUOYANCY_MAX)])
        self.slider_BUOYANY.update()
        self.slider_Dissipation.setValues([float(DefaultUIParameters.DEF_DISSIPATION_MIN), float(DefaultUIParameters.DEF_DISSIPATION_MAX)])
        self.slider_Dissipation.update()
        self.slider_DIFFUSION.setValues([float(DefaultUIParameters.DEF_DIFFUSION_MIN), float(DefaultUIParameters.DEF_DIFFUSION_MAX)])
        self.slider_DIFFUSION.update()

        self.slider_SWIRL.setValues([float(DefaultUIParameters.DEF_SWIRL_MIN), float(DefaultUIParameters.DEF_SWIRL_MAX)])
        self.slider_SWIRL.update()

        self.slider_SPEED.setValues([float(DefaultUIParameters.DEF_SPEED_MIN), float(DefaultUIParameters.DEF_SPEED_MAX)])
        self.slider_SPEED.update()
        self.slider_FREQUENCY.setValues([float(DefaultUIParameters.DEF_FREQ_MIN), float(DefaultUIParameters.DEF_FREQ_MAX)])
        self.slider_FREQUENCY.update()
        self.slider_STRENGTH.setValues([float(DefaultUIParameters.DEF_STRENGTH_MIN), float(DefaultUIParameters.DEF_STRENGTH_MAX)])
        self.slider_STRENGTH.update()

        self.slider_VISCOSITY.setValues([float(DefaultUIParameters.DEF_VISCOSITY_MIN), float(DefaultUIParameters.DEF_VISCOSITY_MAX)])
        self.slider_VISCOSITY.update()


    def lineEdit_SWIRL_MIN_Leafe(self):

        v_str = self.lineEdit_BUOYANY_MIN.text()
        try:
            v = float(v_str)

            if v > float(self.lineEdit_BUOYANY_MAX.text()):
                print "error"
                v = float(self.lineEdit_BUOYANY_MAX.text())
                self.lineEdit_BUOYANY_MIN.setText(self.lineEdit_BUOYANY_MAX.text())

            else:
                if v < float(DefaultUIParameters.DEF_BUOYANCY_MIN):
                    v = float(DefaultUIParameters.DEF_BUOYANCY_MIN)
                    self.lineEdit_BUOYANY_MIN.setText(DefaultUIParameters.DEF_BUOYANCY_MIN)

        except ValueError:
            v = float(DefaultUIParameters.DEF_BUOYANCY_MIN)
            self.lineEdit_BUOYANY_MIN.setText(DefaultUIParameters.DEF_BUOYANCY_MIN)

        self.slider_BUOYANY.setValues([v, float(self.lineEdit_BUOYANY_MAX.text())])
        self.slider_BUOYANY.update()


    def lineEdit_SWIRL_MAX_Leafe(self):

        v_str = self.lineEdit_BUOYANY_MAX.text()
        try:
            v = float(v_str)

            if v < float(self.lineEdit_BUOYANY_MIN.text()):
                print "error"
                v = float(self.lineEdit_BUOYANY_MIN.text())
                self.lineEdit_BUOYANY_MAX.setText(self.lineEdit_BUOYANY_MIN.text())

            else:
                if v > float(DefaultUIParameters.DEF_BUOYANCY_MAX):
                    print "dasdsadasdsdasdasdas"
                    v = float(DefaultUIParameters.DEF_BUOYANCY_MAX)
                    print v
                    self.lineEdit_BUOYANY_MAX.setText(DefaultUIParameters.DEF_BUOYANCY_MAX)

        except ValueError:
            v = float(DefaultUIParameters.DEF_BUOYANCY_MAX)
            self.lineEdit_BUOYANY_MAX.setText(DefaultUIParameters.DEF_BUOYANCY_MAX)

        self.slider_BUOYANY.setValues([float(self.lineEdit_BUOYANY_MIN.text()), v])
        self.slider_BUOYANY.update()


    def getSamplingValues(self, paramBox):

        valuesParameters = MayaCacheCommand()

        valuesParameters.densityBuoyancy = [paramBox.lineEdit_BUOYANY_MIN.text(), paramBox.lineEdit_BUOYANY_MAX.text()]
        valuesParameters.densityDissipation = [paramBox.lineEdit_Dissipation_MIN.text(), paramBox.lineEdit_Dissipation_MAX.text()]
        valuesParameters.densityDiffusion = [paramBox.lineEdit_DIFFUSION_MIN.text(), paramBox.lineEdit_DIFFUSION_MAX.text()]
        valuesParameters.velocitySwirl = [paramBox.lineEdit_SWIRL_MIN.text(), paramBox.lineEdit_SWIRL_MAX.text()]
        valuesParameters.turbulenceSpeed = [paramBox.lineEdit_SPEED_MIN.text(), paramBox.lineEdit_SPEED_MAX.text()]
        valuesParameters.turbulenceFrequency = [paramBox.lineEdit_FREQUENCY_MIN.text(), paramBox.lineEdit_FREQUENCY_MAX.text()]
        valuesParameters.turbulenceSpeed = [paramBox.lineEdit_SPEED_MIN.text(), paramBox.lineEdit_SPEED_MAX.text()]
        valuesParameters.turbulenceStrength = [paramBox.lineEdit_STRENGTH_MIN.text(), paramBox.lineEdit_STRENGTH_MAX.text()]
        valuesParameters.viscosity = [paramBox.lineEdit_VISCOSITY_MIN.text(), paramBox.lineEdit_VISCOSITY_MAX.text()]

        return valuesParameters


    def printSamplingValues(self, tmp):
        print "-- Sampling Paramters --"

        print "\tBuoyancy   : " + str(tmp.densityBuoyancy[0]) + " / " + str(tmp.densityBuoyancy[1])
        print "\tDissipation: " + str(tmp.densityDissipation[0]) + " / " + str(tmp.densityDissipation[1])
        print "\tDiffusion  : " + str(tmp.densityDiffusion[0]) + " / " + str(tmp.densityDiffusion[1])
        print "\tSwirl      : " + str(tmp.velocitySwirl[0]) + " / " + str(tmp.velocitySwirl[1])
        print "\tSpeed      : " + str(tmp.turbulenceSpeed[0]) + " / " + str(tmp.turbulenceSpeed[1])
        print "\tFrequency  : " + str(tmp.turbulenceFrequency[0]) + " / " + str(tmp.turbulenceFrequency[1])
        print "\tStrength   : " + str(tmp.turbulenceStrength[0]) + " / " + str(tmp.turbulenceStrength[1])
        print "\tViscosity  : " + str(tmp.viscosity[0]) + " / " + str(tmp.viscosity[1])