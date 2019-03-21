# Works with Python 2.7 Maya 2018
# when given two selections, will alternate the visibilities between them
# will also turn off selection highlighting for better viewing
# jc_dualToggleOff will turn on all visibilities and turn on selection highlighting


import maya.cmds as cmds
import maya.mel as mel

def jc_dualToggle():
    # gets current panel, usually modelPanel4
    panel = cmds.getPanel(wf=True)
    if "modelPanel" not in panel:
        panel = "modelPanel4"

    # turn off selection highlighting and load selections
    cmds.modelEditor(panel, e=True, sel=False)
    selection = cmds.ls(sl=True)
    firstObj = selection[0]
    secondObj = selection[1]
    firstVis = firstObj + ".visibility"
    secondVis = secondObj + ".visibility"
    firstVisValue = cmds.getAttr(firstVis)
    secondVisValue = cmds.getAttr(secondVis)

    # if both visible, turn off 2nd
    if firstVisValue and secondVisValue:
        cmds.setAttr(secondVis, 0)

    # if first is not visible, switch visibilities
    if firstVisValue and not secondVisValue:
        cmds.setAttr(firstVis, 0)
        cmds.setAttr(secondVis, 1)

    # if 2nd is not visible or both not visible, turn 1st on
    else:
        cmds.setAttr(firstVis, 1)
        cmds.setAttr(secondVis, 0)


def jc_dualToggleOff():
    # will turn on all visibilities and turn selection highlighting back on
    panel = cmds.getPanel(wf=True)
    if "modelPanel" not in panel:
        panel = "modelPanel4"
    cmds.modelEditor(panel, e=True, sel=True)

    selection = cmds.ls(sl=True)
    for i in selection:
        cmds.setAttr(i+".visibility", 1)
