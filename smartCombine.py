#!/usr/bin/env python2.7

"""
Works with Maya 2018
will combine while retaining the pivot, name, hierarchy, and display layer of the last
selected object. history is deleted

__author__: James Chan
"""

import maya.cmds as cmds


def smartCombine():
    selection = cmds.ls(sl=True, o=True)
    main = selection[0]  # main is reference for pivot, name, display layers, hierarchy
    parents = cmds.listRelatives(main, parent=True, fullPath=True)
    display_layers = cmds.listConnections(main, type="displayLayer")
    pivotinfo = cmds.xform(main, q=True, pivots=True, ws=True)[:3]

    # run combine, add to original heirarchy
    newmesh = cmds.polyUnite(selection, ch=True)[0]
    if parents:
        newname = cmds.parent(newmesh, parents[0])
        newmesh = newname

    # delete history, original, add to display layer, set pivot, add original name
    cmds.delete(newmesh, ch=True)
    if display_layers:
        cmds.editDisplayLayerMembers(display_layers[0], newmesh)
    cmds.xform(newmesh, pivots=pivotinfo, ws=True)
    if cmds.objExists(main):
        cmds.delete(main)
    cmds.rename(newmesh, main.split("|")[-1])
    return
