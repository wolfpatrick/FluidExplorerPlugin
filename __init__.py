import subprocess
import os
import sys

"""
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 9991)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:

    # Send data
    message = 'This is the message.  It will be repeated.'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

"""
"""
def killProcess(processname):

    # Check if windows is running
    if sys.platform.startswith('win'):

        processFound = False

        tlcall = 'TASKLIST', '/FI', 'imagename eq %s' % processname
        # communicate() - gets the tasklist command result
        tlproc = subprocess.Popen(tlcall, shell=True, stdout=subprocess.PIPE)
        # trimming it to the actual lines with information
        tlout = tlproc.communicate()[0].strip().split('\r\n')
        # if TASKLIST returns single line without processname: it's not running
        if len(tlout) > 1 and processname in tlout[-1]:
            print('Process "%s" is running .' % processname)
            processFound = True
        else:
            print(tlout[0])
            print('Process "%s" is NOT running.' % processname)
            #return False

        if processFound:


            # Close by number
            cmdProcessPidCmd = 'wmic process where caption=' + '\"' + processname + '\"' + ' get processid'
            cmdProcessPid = subprocess.Popen(cmdProcessPidCmd, stdout=subprocess.PIPE, shell=True)
            pid = cmdProcessPid.communicate()[0].strip().split('\r\n')

            print('Process PID: for "%s" found ' % processname)
            #for p in pid:
            #    print p


            # Close the process
            try:
                os.system("taskkill /im notepad++.exe")
                print('Process "%s" closed ' % processname)

            except Exception as e:
                print('Error: Process "%s" not closed' % processname)
                print('Details: "%s"' % e.message)
                pass


# Close the process with the name 'cmdName'
cmdName = 'notepad++.exe'
killProcess(cmdName)
"""

# use PyQt to play an animated gif
# added buttons to start and stop animation
# tested with PyQt4.4 and Python 2.5
# also tested with PyQt4.5 and Python 3.0
# vegaseat
import sys
# too lazy to keep track of QtCore or QtGui
from PySide import QtCore
from PySide import QtGui


class ProjectSubInfo():

    def __init__(self):
        self.projRootPath = ''
        self.perspectiveCameraAvailable = ''   # (1/0) -> 1 = True, 0 = False


class MoviePlayer(QtGui.QWidget):

    PERSPECTIVE_CAMERA_AVAILABLE = '1'
    PERSPECTIVE_CAMERA_NOT_AVAILABLE = '0'

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.projSubSetting = ProjectSubInfo()
        self.setProjectSubSetting()



        self.comboBoxSimulations = QtGui.QComboBox(self)
        self.comboBoxSimulations.addItem("Select Simulation ...")
        self.comboBoxSimulations.addItem("Simulation 1")
        self.comboBoxSimulations.addItem("Simulation 2")
        self.comboBoxSimulations.addItem("Simulation 3")
        self.comboBoxSimulations.addItem("Simulation 4")

        self.previewCheckBox = QtGui.QCheckBox("Show Preview")


        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("QMovie to show animated gif")



        if self.projSubSetting.perspectiveCameraAvailable == self.PERSPECTIVE_CAMERA_AVAILABLE:

            # set up the movie screen on a label
            self.movie_screen = QtGui.QLabel()
            # expand and center the label
            self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)
            self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
            self.main_layout.addWidget(self.movie_screen)

            self.movie = QtGui.QMovie("", QtCore.QByteArray(), self)
            self.movie.setCacheMode(QtGui.QMovie.CacheAll)
            #self.movie.setSpeed(100)
            self.movie_screen.setStyleSheet("background-color: rgb(85, 170, 255);")
            self.movie_screen.setMovie(self.movie)
            #self.movie.start()
            size = self.movie_screen.size()
            w = size.width() / 2
            h = size.height() / 2

            a = QtCore.QSize(w,h)

            self.movie.setScaledSize(a)
            self.connect(self.movie, QtCore.SIGNAL("frameChanged(int)"), self.frameChangedHandler)


        btn_start = QtGui.QPushButton("Start Animation")
        self.connect(btn_start, QtCore.SIGNAL("clicked()"), self.start)
        self.connect(self.previewCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.previewCheckBoxChanged)
        btn_stop = QtGui.QPushButton("Stop Animation")
        self.connect(btn_stop, QtCore.SIGNAL("clicked()"), self.stop)

        self.labelFrame = QtGui.QLabel("Frame: ")

        self.connect(self.comboBoxSimulations, QtCore.SIGNAL("currentIndexChanged(QString)"), self.comboBoxSimulationsValueChanges)
        main_layout = QtGui.QVBoxLayout()
        if self.projSubSetting.perspectiveCameraAvailable == self.PERSPECTIVE_CAMERA_AVAILABLE:
            main_layout.addWidget(self.movie_screen)
        main_layout.addWidget(btn_start)
        main_layout.addWidget(btn_stop)
        main_layout.addWidget(self.comboBoxSimulations)
        main_layout.addWidget(self.previewCheckBox)
        main_layout.addWidget(self.labelFrame)

        self.setLayout(main_layout)

        # use an animated gif file you have in the working folder
        # or give the full file path




        self.setPreviewVisibility()

    def setProjectSubSetting(self):
        self.projSubSetting.projRootPath = "E:\\TMP\\ANNAANNA1\\"
        self.projSubSetting.perspectiveCameraAvailable = '1'

    def start(self):
        """sart animnation"""
        self.movie.start()

    def stop(self):
        """stop the animation"""
        self.movie.stop()

    def previewCheckBoxChanged(self, state):

        print "changed"


        if state:
            # movie screen is visible
            self.movie_screen.setVisible(True)
            currentSelectedIndex = self.comboBoxSimulations.currentIndex() - 1
            self.playAnimation(currentSelectedIndex)
        if not state:
            self.movie_screen.setVisible(False)
            self.stopPlayingAnimation()



    def comboBoxSimulationsValueChanges(self, index):
        currentIndex = self.comboBoxSimulations.currentIndex() - 1
        self.playAnimation(currentIndex)

    def playAnimation(self, simulationIndex):

        if self.projSubSetting.perspectiveCameraAvailable == self.PERSPECTIVE_CAMERA_NOT_AVAILABLE:
            return

        if simulationIndex == -1:
            self.stopPlayingAnimation()
            return

        fileName = os.path.abspath("E:/TMP/ANNAANNA/" + str(simulationIndex) + "/images/perspective/animation.gif")
        if not os.path.exists(fileName):
            self.movie_screen.setText("<b>[ Cannot find animaiton ... ]</b>")
            self.stopPlayingAnimation()
            return
        else:
            self.movie_screen.setMovie(self.movie)

        currentState = self.movie.state()

        if currentState == QtGui.QMovie.Running:
            print '1'
            self.movie.stop()
            fileName = "E:/TMP/ANNAANNA/" + str(simulationIndex) + "/images/perspective/animation.gif"
            self.movie.setFileName(fileName)
            self.movie.start()
            print fileName
        elif currentState == QtGui.QMovie.NotRunning:
            print '2'
            fileName = "E:/TMP/ANNAANNA/" + str(simulationIndex) + "/images/perspective/animation.gif"
            print fileName
            self.movie.setFileName(fileName)
            self.movie.start()

    def frameChangedHandler(self, frameNumber):
        print frameNumber
        labelText = 'Frame: {}'.format(frameNumber)
        self.labelFrame.setText(labelText)

    def stopPlayingAnimation(self):
        self.movie.stop()
        print "here"
        self.movie_screen.setText("<b>[ No animation selected ... ]</b>")

    def setPreviewVisibility(self):
        perspectiveGifIsAvailable = self.searchPerspectiveGif(self.projSubSetting.projRootPath)


        if perspectiveGifIsAvailable:
            self.previewCheckBox.setEnabled(True)
            self.previewCheckBox.setChecked(True)
        else:
            pass
            self.previewCheckBox.setEnabled(False)
            self.previewCheckBox.setChecked(False)

    def searchPerspectiveGif(self, rootPath):
        pathToGif = rootPath + '/0/images/perspective/animation.gif'
        absPathToGig = os.path.abspath(pathToGif)
        absPathToGig = absPathToGig.replace('\\', '/')
        print absPathToGig
        print ";;;;;;;;;;;;;;;;;;;;;;;;"
        if os.path.exists(absPathToGig):
            return True
        else:
            return False
"""
app = QtGui.QApplication(sys.argv)
player = MoviePlayer()
player.show()
sys.exit(app.exec_())
"""