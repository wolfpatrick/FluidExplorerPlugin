from PySide import QtCore, QtGui
import os

import maya.cmds as cmds
import maya.utils
import maya.mel as mel
import pymel.core as pm

class LoadFluidCacheFile():


    #
    # [errorState, errorMsg] = loadCacheFile("flameShape", "E:/TMP/annawolf2/0/flameShape_0.xml")
    # print errorState
    # print errorMsg
    #
    def loadCacheFile(self, selectedObject, cachPath):
        print "[ --- METHOD CALLED ---]"
        print "Selected Object: " + str(selectedObject)
        print "Cache Path: " + str(cachPath)

        # 1. Select the fluid container
        try:
            cmds.select(selectedObject)
        except:
            errorMsg = "Fluid Container - " + str(selectedObject) + " - does not exist!"
            return [False, errorMsg]
        print "[ --- METHOD CALLED ---1]"
        myCacheNode = cmds.ls(cmds.listHistory(selectedObject), type='cacheFile')
        print myCacheNode

        # 2. Load Cache
        # myCachePath = cmds.getAttr(myCacheNode[cacheIndex] + '.cachePath') + cmds.getAttr(myCacheNode[0] + '.cacheName') + '.xml'
        myCachePath = cachPath
        print myCachePath
        print "dddddddddddddd"
        if os.path.isfile(myCachePath) and os.access(myCachePath, os.R_OK):
            print "OKK"
            print selectedObject
            print myCachePath
            print selectedObject


            myCacheNode = cmds.ls(cmds.listHistory(selectedObject), type='cacheFile')
            print myCacheNode
            print ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;"

            # Finally, load the cache
            pm.mel.doImportCacheFile(myCachePath, "", [selectedObject], list())

        else:
            return [False, "Can not load cache file!"]

        return [True, ""]
        # 1. Select the fluid container

        # 2. Load Cache

        # 3. Show message box of something fails
        msgBox = QtGui.QMessageBox()
        msgBox.setTextFormat(QtCore.Qt.RichText);
        msgBox.setStyleSheet("QPushButton{min-width: 70px;} QMessageBox{font-size: 14px;}")
        msgBox.setWindowTitle("Critical Error!")
        errorStr = "An error occured while the application tried to load the cached fluid file! Please load the cache file manually.<br/><br/>Please follow the instructions on: <a href=\"http://www.such-and-such.com\">http://www.such-and-such.com</a>"
        msgBox.setText(errorStr)
        msgBox.setIcon(QtGui.QMessageBox.Critical)
        msgBox.show()

