from PySide import QtGui
from PySide import QtCore
from ChooseCameraUI import Ui_DialogChooseCamer
from MayaUiDefaultValues import MayaUiDefaultValues


class ChooseCameraDialog(QtGui.QDialog):
    selectedCamera = None

    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)

        # Set up the user interface from Designer
        self.ui = Ui_DialogChooseCamer()
        self.ui.setupUi(self)
        self.ui.pushButtonSelect.setAutoDefault(True)

        # Get the cameras from Maya and fill the combo box
        listUtil = MayaUiDefaultValues()
        listCameras = listUtil.getCamerasFromMaya()

        for iIndex, iItem in enumerate(listCameras):
            self.ui.comboBox.addItem(iItem)

        # Eventhandler for the buttons
        self.ui.pushButtonSelect.clicked.connect(self.buttonSelectClicked)
        self.ui.pushButtonCancel.clicked.connect(self.buttonCancelClicked)

    @QtCore.Slot()
    def buttonSelectClicked(self):
        cam = str(self.ui.comboBox.currentText())
        print "Value: " + cam
        self.selectedCamera = cam
        self.close()

    @QtCore.Slot()
    def buttonCancelClicked(self):
        self.close()

    @property
    def getChoosenCamera(self):
        return self.selectedCamera