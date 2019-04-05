#!/usr/bin/env python2.7

"""
Given a a complete edge loop or enclosure of edges, 
this script will select all faces within the edge perimeter

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel


def faceCut():
    # collect selected edges and obj name
    edgeSel = cmds.ls(sl=True)
    objs = cmds.listRelatives(cmds.ls(sl=True, o=True), p=True)

    # creates extra uv set to work in
    cmds.polyUVSet(create=True, uvSet="facecut")
    cmds.polyUVSet(currentLastUVSet=True)

    # runs planar projection for basic UVs, cuts selected edges
    projection= cmds.polyProjection(objs[0], type='Planar', md='p')
    cut=cmds.polyMapCut(edgeSel)

    # select a face and convert selection to shell, select faces
    firstFace = (objs[0] + ".map[0]")
    cmds.select(firstFace, r=True)
    cmds.ConvertSelectionToUVShell()
    cmds.ConvertSelectionToFaces()
    cmds.polyUVSet(delete=True)
    cmds.delete(cut)
    cmds.delete(projection)


if __name__ == '__main__':
    faceCut()
