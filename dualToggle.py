#!/usr/bin/env python2.7

"""
Works with Maya 2018
When given two selectioned objects, dualToggle will key their visbilities on different frames. 
For easy comparison between two models. Will also turn off selection highlighting for easier viewing.

__author__: James Chan
"""

import maya.cmds as cmds


def set_model_panel():
    # gets current panel, usually modelPanel4
    panel = cmds.getPanel(wf=True)
    if "modelPanel" not in panel:
        panel = "modelPanel4"
    # turn off selection highlighting
    cmds.modelEditor(panel, e=True, sel=False)


def dualToggle_on():
    # set_model_panel()
    selection = cmds.ls(sl=True)
    first_obj , second_obj = selection
    firstVis = '%s.visibility' % first_obj
    secondVis = '%s.visibility' % second_obj

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


def dualToggle_off():
    # will turn on all visibilities and turn selection highlighting back on
    panel = cmds.getPanel(wf=True)
    if "modelPanel" not in panel:
        panel = "modelPanel4"
    cmds.modelEditor(panel, e=True, sel=True)
    selections = cmds.ls(sl=True)
    for selection in selections:
        cmds.setAttr("%s.visibility" % selection, 1)
