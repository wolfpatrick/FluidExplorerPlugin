"""
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

"""

# --------------------------------------------------------------------------------------------

import maya.cmds as cmds
import os
import maya.mel as mel
#import pymel.core as pm
#import maya.mel
#import maya.utils

class LoadFluidCacheFile():

    @staticmethod
    def applyCacheFile(pathToCacheXMLFile, nodeName):

        print "Selected Object: " + str(nodeName)
        print "Cache Path: " + str(pathToCacheXMLFile)

        # 1. Select the fluid container
        try:
            cmds.select(nodeName, r=True)
        except:
            errorMsg = "Fluid Container '" + str(nodeName) + "' does not exist!\nPlease visit the help page more information."
            raise Exception(errorMsg)

        # Check if path is available and executable
        if os.path.isfile(pathToCacheXMLFile) and os.access(pathToCacheXMLFile, os.R_OK):
            print ("Load fluid cache file: ", "Path to xml file is correct")
            pass
        else:
            raise Exception("Path to cache file is not correct or files are not accessible.")

        # 2. Delete current cache node
        # Catch Quiet: Otherwise, an error occurs if no cache is loaded!
        if cmds.objExists(nodeName):
            strCmd = 'catchQuiet (`deleteCacheFile 2 { "keep", "" }`) '
            try:
                mel.eval(strCmd)
            except Exception as e:
                errorMsg = "Cannot delete the current cache for '" + str(nodeName) + "'!\nPlease visit the help page more information.\nDetails: " + e.message
                raise Exception(errorMsg)
        else:
            errorMsg = "Fluid Container '" + str(nodeName) + "' does not exist!\nPlease visit the help page more information."
            raise Exception(errorMsg)

        # 3. Finally, attach the existing cache file
        try:
            lineToEval = 'doImportFluidCacheFile("{0}", "xmlcache", {{"{1}"}}, {{}});'.format(pathToCacheXMLFile, nodeName)
            mel.eval(lineToEval)
        except Exception as e:
            errorMsg = "Cannot attach the cached file for '" + str(nodeName) + "'!\nPlease visit the help page more information.\nDetails: " + e.message
            raise Exception(errorMsg)

    """
    #####################################################################################################################
    # Maya Command
    pathToCacheXMLFile = "E:/TMP/ANNAANNA/0/flameShape_0.xml"
    nodeName = "flameShape"
    try:
        # lineToEval = 'doImportFluidCacheFile("{0}", "xmlcache", {{"{1}"}}, {{}});'.format( pathCache1, fluidsSel)
        applyCacheFile(pathToCacheXMLFile, nodeName)
    except Exception as e:
        print e.message
    #####################################################################################################################
    """

