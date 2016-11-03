import os
import ConfigParser
import subprocess
import xml.etree.cElementTree as ET
import sys
import logging

import maya.cmds as cmds


class FluidExplorerUtils(object):

    @staticmethod
    def dirExists(path):
        exists = os.path.exists(path)
        return exists

    @staticmethod
    def readAttributeFromConfigurationFile(choosenDir, category, attribute):
        config = ConfigParser.ConfigParser()
        config.read(choosenDir)

        result = config.get(category, attribute)
        return result

    @staticmethod
    def readAttributeFromXmlConfigurationsFile(xml_file, childName):
        try:
            tree = ET.ElementTree(file=xml_file)
            root = tree.getroot()

            for child in root:
                if child.tag.lower() == childName.lower():
                    el_child_text = child.text

                    return el_child_text
        except:
            logging.warning("Cannot read XML attribute")

    @staticmethod
    def containerIsCorrect(containerName):

        nodeName = containerName
        objectExists = cmds.objExists(nodeName)
        attrExists = cmds.attributeQuery('gravity', node=nodeName, exists=True)

        containerOK = objectExists and attrExists

        if not containerOK:
            logging.error("Cannot select container attribute! Please check the nodeName and the container type")

        return containerOK

    @staticmethod
    def checkIfFFmpgeIsExectuable(pathToFFmpeg):
        if sys.platform.startswith('win'):
            pathToFFmpeg = pathToFFmpeg + "/ffmpeg.exe"
        else:
            # TODO: Unix path
            pass

        try:
            subprocess.call([pathToFFmpeg], shell=False)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                # Handle file not found error.
                logging.error("Fatal Error: Cannot find ffmpeg. Details: %s", e.message)
                logging.error("Please check if executable file exists in /lib/ffmpeg/")

                return False
            else:
                # Something else went wrong while trying to run ffmpeg
                logging.error("Cannot execute ffmpeg. Details: %s", e.message)

                return False

        return True

    @staticmethod
    def checkIfFluidExplorerIsExectuable(pathToFluidExplorer):
        if sys.platform.startswith('win'):
            pathToFluidExplorer = pathToFluidExplorer + '/fluidexplorer.exe'
        else:
            # TODO: Unix
            pass
        print pathToFluidExplorer
        """
        try:
            subprocess.call([pathToFluidExplorer], shell=False)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                # Handle file not found error.
                print("Fatal Error: Cannot find ffmpeg. Details: ", e.message)
                return False
            else:
                # Something else went wrong while trying to run ffmpeg
                print("Fatal Error: Cannot execute ffmpeg. Details: ", e.message)
                return False
        """

        return True

    @staticmethod
    def lockNodes(fluidNode, transformNOde):
        if not fluidNode == "":
            cmds.lockNode(fluidNode)
        if not transformNOde == "":
            cmds.lockNode(transformNOde)

    #
    #

    @staticmethod
    def killProcess(processnameArg):
        if sys.platform.startswith('win'):
            FluidExplorerUtils.killProcess_WIN(processnameArg)
        elif sys.platform.startswith(''):
            # TODO: Unix path
            pass

    @staticmethod
    def killProcess_WIN(processnameArg):

        processname = processnameArg + '.exe'
        processFound = False

        tlcall = 'TASKLIST', '/FI', 'imagename eq %s' % processname
        # communicate() - gets the tasklist command result
        tlproc = subprocess.Popen(tlcall, shell=True, stdout=subprocess.PIPE)
        # trimming it to the actual lines with information
        tlout = tlproc.communicate()[0].strip().split('\r\n')
        # if TASKLIST returns single line without processname: it's not running
        if len(tlout) > 1 and processname in tlout[-1]:
            # print('Process "%s" is running .' % processname)
            logging.info('Process "%s" is running', processname)
            processFound = True
        else:
            # print('Process "%s" is NOT running.' % processname)
            logging.info('Process "%s" is not running', processname)

        if processFound:

            """
            # Close by number
            cmdProcessPidCmd = 'wmic process where caption=' + '\"' + processname + '\"' + ' get processid'
            cmdProcessPid = subprocess.Popen(cmdProcessPidCmd, stdout=subprocess.PIPE, shell=True)
            pid = cmdProcessPid.communicate()[0].strip().split('\r\n')

            print('Process PID: for "%s" found ' % processname)
            #for p in pid:
            #    print p
            """

            # Close the process
            try:
                cmdStr = 'taskkill /im' + ' ' + processname

                kill = subprocess.Popen(cmdStr, shell=True, stdout=subprocess.PIPE)
                # print('Process "%s" closed ' % processname)
                logging.info('Process "%s" closed ', processname)

            except Exception as e:
                logging.error('Process "%s" not closed', processname)
                logging.error('Details: %s', e.message)
