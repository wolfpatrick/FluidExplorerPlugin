########################################################################################################################
#                                                                                                                      #
#   This file creates the FluidExplorer icons in the toolbar and                                                       #
#   returns the main window instance.                                                                                  #
#                                                                                                                      #
#   Please execute the file from the python script editor.                                                             #
#                                                                                                                      #
########################################################################################################################

import maya.cmds as cmds
import maya.mel
import os.path

import FluidMain

"""
import FluidExplorerPlugin.ui.CreateProjectDialog
import FluidExplorerPlugin.ui.Utils.XmlFileWriter
import FluidExplorerPlugin.ui.ParamterTab
import FluidExplorerPlugin.ui.Utils.MayaCmds.MayaFunctions
import FluidExplorerPlugin.ui.Utils.RangeSliderSpan
import FluidExplorerPlugin.ui.Utils.GifCreatpr
import FluidExplorerPlugin.ui.ParamterTab
import FluidExplorerPlugin.ui.RangeSlider.HRangeSlider
import FluidExplorerPlugin.ui.FileOpenDialog
import FluidExplorerPlugin.ui.Test
import FluidExplorerPlugin.ui.ProjectDetailsView
import FluidExplorerPlugin.ui.Utils.LoadFluidCacheFile
import FluidExplorerPlugin.ui.Utils.ProjectDetailsViewUtils
"""

def get_script_folfer():
    scriptDir = cmds.internalVar(userScriptDir=True)
    path_fx = scriptDir + "tmp/fx_32px.png"
    path_help = scriptDir + "tmp/help_32px.png"
    path_icon_fx = '"' + path_fx + '"'
    path_icon_help = '"' + path_help + '"'

    if not os.path.isfile(path_fx):
       return [ "", "" ]
    if not os.path.isfile(path_help):
       return [ "", "" ]

    return [ path_icon_fx, path_icon_help ]

def create_fluidExplorer_shelf_text_only():
    maya.mel.eval('if (`shelfLayout -exists FluidExplorer `) deleteUI FluidExplorer;')
    shelfTab = maya.mel.eval('global string $gShelfTopLevel;')
    maya.mel.eval('global string $scriptsShelf;')
    maya.mel.eval('$scriptsShelf = `shelfLayout -p $gShelfTopLevel FluidExplorer`;')

    maya.mel.eval('shelfButton -parent $scriptsShelf -annotation "Fluid Explorer" ' + '-label "FluidExplorer" -sourceType "python" ' + '-command ("fluidExplorerWin = FluidMain.main(); fluidExplorerWin.show()") -style "textOnly";')
    maya.mel.eval('shelfButton -parent $scriptsShelf -annotation "Help" ' + '-label "Help" -sourceType "python" ' + '-command ("FluidMain.helpButton();") -style "textOnly";')

def create_fluidExplorer_shelf():
    try:
        maya.mel.eval('if (`shelfLayout -exists FluidExplorer `) deleteUI FluidExplorer;')
        shelfTab = maya.mel.eval('global string $gShelfTopLevel;')
        maya.mel.eval('global string $scriptsShelf;')
        maya.mel.eval('$scriptsShelf = `shelfLayout -p $gShelfTopLevel FluidExplorer`;')

        [ path_icon_fx, path_icon_help ] = get_script_folfer()
        iconFX = '-image ' + path_icon_fx
        iconHelp = '-image ' + path_icon_help

        cmd_fx = 'shelfButton -parent $scriptsShelf -annotation "Fluid Explorer" ' + '-label "FluidExplorer"' + iconFX + '-sourceType "python" ' +'-command ("fluidExplorerWin = FluidMain.main(); fluidExplorerWin.show()");'
        cmd_help = 'shelfButton -parent $scriptsShelf -annotation "Help" ' + '-label "FluidExplorer"' + iconHelp + '-sourceType "python" ' +'-command ("FluidMain.helpButtonToolBar();");'

        maya.mel.eval(cmd_fx)
        maya.mel.eval(cmd_help)

    except:
        create_fluidExplorer_shelf_text_only()

#
# --- Run FluidExplorer ---
#

reload(FluidMain)

"""
reload(FluidExplorerPlugin.ui.CreateProjectDialog)
reload(FluidExplorerPlugin.ui.Utils.XmlFileWriter)
reload(FluidExplorerPlugin.ui.ParamterTab)
reload(FluidExplorerPlugin.ui.Utils.MayaCmds.MayaFunctions)
reload(FluidExplorerPlugin.ui.Utils.RangeSliderSpan)
reload(FluidExplorerPlugin.ui.Utils.GifCreatpr)
reload(FluidExplorerPlugin.ui.ParamterTab)
reload(FluidExplorerPlugin.ui.RangeSlider.HRangeSlider)
reload(FluidExplorerPlugin.ui.FileOpenDialog)
reload(FluidExplorerPlugin.ui.Test)
reload(FluidExplorerPlugin.ui.ProjectDetailsView)
reload(FluidExplorerPlugin.ui.Utils.LoadFluidCacheFile)
reload(FluidExplorerPlugin.ui.Utils.ProjectDetailsViewUtils)
"""

# Call main function
fluidExplorerWin = FluidMain.main()

if fluidExplorerWin:
    # Show main window
    fluidExplorerWin.show()

# Create shelf buttons
create_fluidExplorer_shelf()

"""
maya.mel.eval('shelfButton -parent $scriptsShelf -annotation "FluidExplorer" ' +
  '-label "FluidExplorer"  -image "E:/TMP/aa.png" -sourceType "python" ' +
  '-command ("fluidExplorerWin = FluidMain.main(); fluidExplorerWin.show()") -style "iconOnly";')

maya.mel.eval('shelfButton -parent $scriptsShelf -annotation "FluidExplorer" ' +
  '-label "FluidExplorer"  -image "/tmp/help.png" -sourceType "python" ' +
  '-command ("FluidMain.helpButton();") -style "iconOnly";')
"""
