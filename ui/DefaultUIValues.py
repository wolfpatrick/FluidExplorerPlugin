__author__ = 'Patrick'

class DefaultUIParameters(object):

    StyleSheet_Button_Off = "QPushButton { background-color: None; border: 3px solid grey; border-radius: 5px; }"
    #StyleSheet_Button_On = "QPushButton { background-color: rgb(255,160,47); border: 3px solid grey; border-radius: 5px; }"
    StyleSheet_Button_On = "QPushButton { background-color: None; border: 3px solid rgb(255,160,47); border-radius: 5px;s}"
    # Project name
    DEF_SIMULATION_NAME = "Untitled"

    # Camera rotations (degrees)
    DEF_SPIN_ROT_MIN = 10
    DEF_SPIN_ROT_MAX = 90
    DEF_SPIN_ROT = 45

    # Slider: Number of Sequences
    DEF_NUMBER_SEQUENCES = 128
    DEF_NUMBER_SEQUENCES_MIN = 1
    DEF_NUMBER_SEQUENCES_MAX = 500

    # Parameter values
    DEF_BUOYANCY_MIN = "-5.0"
    DEF_BUOYANCY_MAX = "5.0"
    DEF_DISSIPATION_MIN = "0.0"
    DEF_DISSIPATION_MAX = "1.0"
    DEF_DIFFUSION_MIN = "0.0"
    DEF_DIFFUSION_MAX = "2.0"

    DEF_SWIRL_MIN = "0.0"
    DEF_SWIRL_MAX = "10.0"

    DEF_SPEED_MIN = "0.0"
    DEF_SPEED_MAX = "2.0"
    DEF_FREQ_MIN = "0.0"
    DEF_FREQ_MAX = "2.0"
    DEF_STRENGTH_MIN = "0.0"
    DEF_STRENGTH_MAX = "1.0"

    DEF_VISCOSITY_MIN = "0.0"
    DEF_VISCOSITY_MAX = "1.0"
