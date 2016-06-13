__author__ = 'babbel'

# Code adapted from
#
# Widget Range slider widget.
#
# Hazen 4/09
#

from PySide import QtCore, QtGui
import sys

class QHRangeSlider(QtGui.QWidget):

    def __init__(self, lineEditElement_MIN = None, lineEditElement_MAX = None, lineEdit_DEF = None,  range = None,
                 values = None, parent = None, enabledFlag = None):

        QtGui.QWidget.__init__(self, parent)

        if not parent:
            self.setGeometry(200, 200, 293, 20)


        self.emit_while_moving = 0
        self.scale = 0
        self.setMouseTracking(False)
        self.moving = "none"

        # LineEdit values
        self.lineEditElement_MIN = lineEditElement_MIN
        self.lineEditElement_MAX = lineEditElement_MAX
        self.lineEditElement_DEF = lineEdit_DEF

        # Width of the bar
        self.bar_width = 10

        if range:
            self.setRange(range)
        if values:
            self.setValues(values)
        else:
            pass
            #self.setValues([0.3, 0.6])

        # Store values
        self.maxValue = range[1]
        self.rangeValues = range
        #self.defaultSingleValue = 1 # Stored the current value from Maya

        # Additional flags tho control the style
        self.enabledFlag = enabledFlag
        self.isRangeActive = True
        self.maxReached = False
        print range
        print ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"
        """
        if not self.isRangeActive:
            print self.defaultSingleValue
            tmpRange = [0, 1]
            self.update()
        """

        self.setMinimumWidth(295)
        self.setMaximumWidth(295)

    def changeStyle(self):
        if self.isRangeActive:
            tmpRange = [self.defaultSingleValue, 0]
            hslider.setValues(tmpRange)
            self.isRangeActive = False
        elif not self.isRangeActive:
            tmpRange = [self.rangeValues[0], self.rangeValues[1]]
            hslider.setValues(tmpRange)
            self.isRangeActive = True

        hslider.update()
        hslider.repaint()

        print "SOZE: " + hslider.size()

    def changeSliderEnabled(self, flag):
        self.enabledFlag = flag
        self.update()

    def emitRange(self):
        w = float(self.width() - 2 * self.bar_width - 1)
        if self.scale:
            fmin = (float(self.rmin - self.bar_width)/((w+1.0) * self.scale) + self.start)
            fmax = (float(self.rmax - self.bar_width)/(w * self.scale) + self.start)
        else:
            fmin = float(self.rmin - self.bar_width)/(w+1.0)
            fmax = float(self.rmax - self.bar_width)/w

        if self.isRangeActive:
            print "Range:", fmin, fmax
        else:
            sliderValue = fmin
            if self.maxReached == True:
                sliderValue = self.maxValue

            print "Value: ", sliderValue

        # Update the QLineEdit elements
        if self.isRangeActive:
            self.lineEditElement_MIN.setMaxLength(4)
            self.lineEditElement_MAX.setMaxLength(4)

            if fmin < 0:
                self.lineEditElement_MIN.setMaxLength(5)
            if fmax < 0:
                self.lineEditElement_MAX.setMaxLength(5)

            self.lineEditElement_MIN.setText(str(format(fmin, '.2f')))
            self.lineEditElement_MAX.setText(str(format(fmax, '.2f')))

        elif not self.isRangeActive:
            self.lineEditElement_DEF.setMaxLength(4)
            if sliderValue < 0:
                self.lineEditElement_DEF.setMaxLength(5)

            self.lineEditElement_DEF.setText(str(format(sliderValue, '.2f')))

        print 'MAX: ' + str(fmax)
        print 'MIN: ' + str(fmin)


    def paintEvent(self, event):

        if self.isRangeActive:
            painter = QtGui.QPainter(self)
            rmin = self.rmin
            rmax = self.rmax
            w = self.width()
            h = self.height()

            # Background
            g1 = QtGui.QColor(64, 64, 64)
            if self.enabledFlag == False:
                 g1 = QtGui.QColor(QtCore.Qt.transparent) # delete this

            painter.setPen(g1)
            painter.setBrush(QtCore.Qt.lightGray)

            if self.enabledFlag == False:
                 painter.setBrush(QtCore.Qt.transparent) # delete this

            painter.drawRect(2, 2, w-4, h-4)

            # Range bar
            lb = QtGui.QColor(215, 128, 26)

            if self.enabledFlag == False:
                lb = QtGui.QColor(QtCore.Qt.transparent) # delete this

            painter.setPen(QtCore.Qt.darkGray)

            if self.enabledFlag == False:
                painter.setPen(QtCore.Qt.black)

            painter.setBrush(lb)
            painter.drawRect(rmin-0, 5, rmax-rmin+0, h-10)

            # min & max tabs
            painter.setPen(QtCore.Qt.black)
            painter.setBrush(QtCore.Qt.darkGray)
            painter.setBrush(lb)
            x=QtGui.QColor(215, 128, 26)

            if self.enabledFlag == False:
                painter.setBrush(QtCore.Qt.transparent)

            painter.drawRect(rmin-self.bar_width, 1, 10, h-2)
            painter.setBrush(lb)

            if self.enabledFlag == False:
                painter.setBrush(QtCore.Qt.transparent)

            painter.drawRect(rmax, 1, self.bar_width, h-2)

        else:

            painter = QtGui.QPainter(self)
            rmin = self.rmin
            rmax = self.rmax
            w = self.width()
            h = self.height()

            # Background
            g1 = QtGui.QColor(64, 64, 64)
            if self.enabledFlag == False:
                 g1 = QtGui.QColor(QtCore.Qt.black)

            painter.setPen(g1)
            painter.setBrush(QtCore.Qt.lightGray)

            if self.enabledFlag == False:
                 painter.setBrush(QtCore.Qt.transparent)

            painter.drawRect(2, 2, w-4, h-4)

            # Bar
            lb = QtGui.QColor(215, 128, 26)

            if self.enabledFlag == False:
                lb = QtGui.QColor(QtGui.QColor(90, 90, 90))     # Color when slider is dissabled

            painter.setPen(QtCore.Qt.darkGray)

            if self.enabledFlag == False:
                painter.setPen(QtCore.Qt.black)

            painter.setBrush(lb)


            if self.isRangeActive == True:
                painter.drawRect(rmin-0, 5, rmax-rmin+0, h-10)

            # Min tab
            painter.setPen(QtCore.Qt.black)
            painter.setBrush(QtGui.QColor(211, 211, 1))
            painter.setBrush(lb)
            x = QtGui.QColor(QtGui.QColor(211, 211, 211))

            if self.isRangeActive == True:
                painter.setBrush(x)

            if self.enabledFlag == False:
                painter.setBrush(lb)

            painter.drawRect(rmin-self.bar_width, 1, 20, h-2)
            painter.setBrush(QtCore.Qt.red)

            if self.enabledFlag == False:
                painter.setBrush(QtCore.Qt.transparent)

    def mouseMoveEvent(self, event):
        if self.isRangeActive:
            w = self.width()
            diff = self.start_x - event.x()

            if self.moving == "min":
                temp = self.start_rmin - diff
                if (temp >= self.bar_width) and (temp < w - self.bar_width):
                    self.rmin = temp
                    if self.rmax < self.rmin:
                        self.rmax = self.rmin
                    self.update()
                    if self.emit_while_moving:
                        self.emitRange()
            elif self.moving == "max":
                temp = self.start_rmax - diff
                if (temp >= self.bar_width) and (temp < w - self.bar_width):
                    self.rmax = temp
                    if self.rmax < self.rmin:
                        self.rmin = self.rmax
                    self.update()
                    if self.emit_while_moving:
                        self.emitRange()
            elif self.moving == "bar":
                temp = self.start_rmin - diff
                if (temp >= self.bar_width) and (temp < w - self.bar_width - (self.start_rmax - self.start_rmin)):
                    self.rmin = temp
                    self.rmax = self.start_rmax - diff
                    self.update()
                    if self.emit_while_moving:
                        self.emitRange()

        else:

            w = self.width()
            diff = self.start_x - event.x()

            res = self.rmin + self.bar_width

            if self.moving == "min":

                temp = self.start_rmin - diff
                print temp
                #if temp >= self.rmax:
                if res >= self.width()-1:
                    # Max reached
                    self.maxReached = True
                    print "REACHED"
                    #maxV = round(float(self.lineEditElement_DEF.text()))
                    maxV = self.rangeValues[1]
                    print "MAXV" + str(maxV)
                    self.lineEditElement_DEF.setText(format(maxV, '.2f'))
                else:
                    self.maxReached = False

                if (temp >= self.bar_width) and (temp < w - self.bar_width):
                    self.rmin = temp
                    if self.rmax < self.rmin:
                        self.rmax = self.rmin
                    self.update()
                    if self.emit_while_moving:
                        self.emitRange()

    def mousePressEvent(self, event):
        x = event.x()
        if abs(self.rmin - 0.5 * self.bar_width - x) < (0.5 * self.bar_width+10):   # Edited !!
            self.moving = "min"
        elif abs(self.rmax + 0.5 * self.bar_width - x) < (0.5 * self.bar_width):
            self.moving = "max"
        elif (x > self.rmin) and (x < self.rmax):
            self.moving = "bar"
        self.start_rmin = self.rmin
        self.start_rmax = self.rmax
        self.start_x = x

    def mouseReleaseEvent(self, event):
        if not (self.moving == "none"):
            self.emitRange()
        self.moving = "none"

    def setRange(self, range):
        self.start = range[0]
        self.scale = 1.0/(range[1] - range[0])

    def setValues(self, values):
        w = float(self.width() - 2 * self.bar_width - 1)
        if self.scale:
            self.rmin = int(w * (values[0] - self.start) * self.scale) + self.bar_width
            self.rmax = int(w * (values[1] - self.start) * self.scale) + self.bar_width
        else:
            self.rmin = int(w * values[0]) + self.bar_width
            self.rmax = int(w * values[1]) + self.bar_width

    def setEmitWhileMoving(self, bool):
        if bool:
            self.emit_while_moving = 1
        else:
            self.emit_while_moving = 0


# -----------------
# RangeSlider Test
# -----------------

if __name__ == "__main__":

    class Parameters:
        def __init__(self):
            #self.x_pixels = 200
            #self.y_pixels = 200

            self.flag = True

    def change():
        print hslider.size()
        print hslider.geometry()
        print "Style changed ..."
        hslider.changeStyle()

    def changeEnabled():
        print "Enabled/Disabled"
        hslider.changeSliderEnabled(False)

    app = QtGui.QApplication(sys.argv)
    # hslider = QHRangeSlider()

    # Slider
    hslider = QHRangeSlider(range = [0, 2], values = [0, 2])
    hslider.setMinimumWidth(300)
    hslider.setMaximumWidth(300)
    hslider.setMinimumWidth(400)
    hslider.setMaximumWidth(400)
    hslider.setMinimumWidth(300)
    hslider.setMaximumWidth(300)
    hslider.setValues([0, 2])
    ss = hslider.width()
    print ss



    # PushButton
    button = QtGui.QPushButton("Change Style")
    button.show()
    button.clicked.connect(change)

    #button1 = QtGui.QPushButton("Change Enabled/Dissable")
    #button1.show()
    #button1.clicked.connect(changeEnabled)

    hslider.setEmitWhileMoving(True)
    hslider.show()
    sys.exit(app.exec_())


#
# The MIT License
#
# Copyright (c) 2009 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#