#!/usr/bin/env python2.7

# Works with Python 2.7 Maya 2018
# when given two selections, will alternate the visibilities between them
# will also turn off selection highlighting for better viewing
# dualToggleOff will turn on all visibilities and turn on selection highlighting


import maya.cmds as cmds


def setModelPanel():
    # gets current panel, usually modelPanel4
    panel = cmds.getPanel(wf=True)
    if "modelPanel" not in panel:
        panel = "modelPanel4"
    # turn off selection highlighting
    cmds.modelEditor(panel, e=True, sel=False)


def dualToggle():
    setModelPanel()
    selection = cmds.ls(sl=True)
    firstObj, secondObj = selection
    firstVis = '%s.visibility' % firstObj
    secondVis = '%s.visibility' % secondObj

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


def dualToggleOff():
    # will turn on all visibilities and turn selection highlighting back on
    setModelPanel()
    selections = cmds.ls(sl=True)
    for selection in selections:
        cmds.setAttr("%s.visibility" % selection, 1)
