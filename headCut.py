#!/usr/bin/env python2.7

"""
for Maya 2018
Selected faces or vertices will be ordered to have the first vertex IDs.
Used for reordering character models so that the head consists of the first vertIDs

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel
import math


def headCut():
    # convert selection to vertices and collect name, transform, hierarchy, pivots
    cmds.ConvertSelectionToContainedFaces()
    sel = cmds.ls(sl=True, fl=True)
    obj = cmds.ls(sl=True, o=True)
    name = cmds.listRelatives(obj, p=True, fullPath=True)[0]
    parents = cmds.listRelatives(name, parent=True, fullPath=True)
    pivotinfo = cmds.xform(name, q=True, pivots=True, ws=True)[:3]

    # dup original obj to transfer UVs later, get boundingbox minx to identify head later
    # run chipoff and separate. pop off separate node to leave list of remaining objs
    dup = cmds.duplicate(obj, name='uv_ref')[0]
    target_minx = format(cmds.xform(sel, q=True, bb=True)[0], '.5f')
    target_miny = format(cmds.xform(sel, q=True, bb=True)[1], '.5f')
    cmds.polyChipOff(ch=1, kft=1, dup=0)
    separate = cmds.polySeparate(obj, rs=1, ch=1)
    separate.pop()

    if len(separate) != 2:
        cmds.delete(dup)
        cmds.error("more than 2 objects")

    # see if bounding matches original selection to identify the head
    head = None
    body = None
    for i in separate:
        temp_minx = format(cmds.xform(i, q=True, bb=True)[0], '.5f')
        temp_miny = format(cmds.xform(i, q=True, bb=True)[1], '.5f')
        if temp_minx == target_minx and temp_miny == target_miny:
            head = i
        else:
            body = i
    vertcount = cmds.polyEvaluate(head, v=True)

    # merge head and body (head first to retain vert order)
    result = cmds.polyUnite(head, body, ch=True)[0]
    cmds.polyMergeVertex(result, d=0.001, am=1, ch=True)
    cmds.select(result)
    cmds.polyNormalPerVertex(ufn=True)

    # transfer UVs/normals, delete duplicate, re-parent, reset pivot, rename, select first verts
    cmds.transferAttributes(dup, result, transferPositions=1, transferNormals=1, transferUVs=2,
                            sampleSpace=0, sourceUvSpace="map1", targetUvSpace="map1",
                            searchMethod=3, flipUVs=0, colorBorders=1)
    cmds.delete(result, ch=True)
    cmds.delete(dup)
    if parents:
        result = cmds.parent(result, parents)
    cmds.xform(result, pivots=pivotinfo, ws=True)
    cmds.rename(result, name.split("|")[-1])
    cmds.select(cmds.ls(sl=True, long=True)[0] + '.vtx[0:' + str(vertcount-1) + ']')
    cmds.inViewMessage(amg='<hl>Vertices Reordered</hl> - Head Selected',
                       pos='topCenter', fst=5000, fade=True)

headCut()    
