#!/usr/bin/env python2.7

"""
Works with Maya 2018
Given a a complete edge loop or enclosure of edges,
this script will select all faces within the edge perimeter

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel


def faceCut():
    edgesel = cmds.ls(sl=True, fl=True)
    objs = cmds.ls(sl=True, o=True)

    # checks for face selection(mask 34) & vertices(mask 31)
    if cmds.filterExpand(edgesel, selectionMask=31):
        cmds.error("Must select edges")
    if cmds.filterExpand(edgesel, selectionMask=34):
        mel.eval('invertSelection;')
        return

    # create extra UV set to work in, and project new UVs
    cmds.polyUVSet(create=True, uvSet="facecut")
    cmds.polyUVSet(currentLastUVSet=True)
    cmds.polyProjection(objs[0], type='Planar', md='p')
    cmds.polyMapCut(edgesel)

    # select edge and select a related face, then grow selection to shell
    cmds.select(edgesel[0])
    cmds.textureWindow("polyTexturePlacementPanel1", e=True, selectRelatedFaces=True)
    cmds.polyListComponentConversion(fe=True, fuv=True)
    facesel = cmds.ls(sl=True, fl=True)[-1]
    cmds.select(facesel, r=True)
    cmds.ConvertSelectionToUVShell()

    # delete extra UV set, convert to edges then back to faces to allow invertSelection;
    cmds.polyUVSet(delete=True)
    cmds.ConvertSelectionToEdges()
    cmds.ConvertSelectionToContainedFaces()
    mel.eval('BakeNonDefHistory;')
   
faceCut()
