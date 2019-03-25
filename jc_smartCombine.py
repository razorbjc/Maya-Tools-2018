# Works with Python 2.7 Maya 2018
# combine geo without construction history
# also keeping the name, hierarchy, displaylayer, and pivot of the last selected obj

import maya.cmds as cmds

def jc_smartCombine():
    selection = cmds.ls(sl=True, o=True)
    main = selection[-1] # main is reference for pivot, name, display layers, hierarchy
    parents = cmds.listRelatives(main, parent=True, fullPath=True)[0]
    display_layers = cmds.listConnections(main, type="displayLayer")

    newMesh = cmds.polyUnite(selection, ch=False, objectPivot=True) # combine with no history, keep last object pivot
    if cmds.objExists(parents):
        cmds.parent(newMesh, parents)
    if display_layers:
        cmds.editDisplayLayerMembers(display_layers[0], newMesh)
    cmds.rename(newMesh, main)
