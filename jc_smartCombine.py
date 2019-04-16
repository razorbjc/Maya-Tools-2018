#!/usr/bin/env python2.7

"""
will run combine while retaining the pivot, name, hierarchy, and display layer of the last selected object
history is deleted
__author__: James Chan
"""

import maya.cmds as cmds

def jc_smartCombine():
    selection = cmds.ls(sl=True, o=True)
    main = selection[-1] # main is reference for pivot, name, display layers, hierarchy
    parents = cmds.listRelatives(main, parent=True, fullPath=True)
    display_layers = cmds.listConnections(main, type="displayLayer")
    pivotInfo = cmds.xform(main, q=True, pivots=True, ws=True)[:3]

    #run combine
    newMesh = cmds.polyUnite(selection, ch=True)[0] # combine w/ history, keep last object pivot

    # add to original heirarchy
    if parents:
        newName = cmds.parent(newMesh, parents[0])
        newMesh = newName

    # delete history
    cmds.delete(newMesh, ch=True)

    # add to original display layer
    if display_layers:
        cmds.editDisplayLayerMembers(display_layers[0], newMesh)

    # set pivot to original pivot
    cmds.xform(newMesh, pivots=[pivotInfo[0], pivotInfo[1], pivotInfo[2]], ws=True)

    # add original name
    cmds.rename(newMesh, main)
