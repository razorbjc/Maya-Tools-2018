# Works with Python 2.7 Maya 2018
# given a a complete edge loop or enclosure of edges,
# this script will select all faces within the edge perimeter

import maya.cmds as cmds

def jc_smartExtract():
    selection = cmds.ls(sl=True)
    print selection
    obj = cmds.ls(sl=True, o=True)[0]
    print obj
    newMesh = cmds.polyChipOff(selection[0], kft=True, ch=False, n=obj+"_separate", dup=False)
    print newMesh
    separated = cmds.polySeparate(obj, rs=True, ch=False)
    number = 0
    for i in separated:
        cmds.xform(i, cp=True, dph=True)
        # cmds.rename(i, cmds.listRelatives(obj, p=True)+"_separated"+i)

    print separated
