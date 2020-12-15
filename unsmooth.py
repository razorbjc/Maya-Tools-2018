#!/usr/bin/env python2.7

"""
for Maya 2018
Unsmooths geometry that has been smoothed. Works on quad-only geo that has not
been edited since the smoothing. singular meshes only.

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel
import math


def unsmooth():
    # duplicates geo twice, once to down-res and another as a blendshape target later
    sel = cmds.ls(sl=True, o=True)
    result_list = []
    for i in sel:
        result_list.append(unsmooth_main(i))
    cmds.select(result_list)
    return


def unsmooth_main(obj):
    low = cmds.duplicate(obj, n=obj)[0]
    high = cmds.duplicate(obj, n='high')[0]

    # selects last vertex, converts to edges, grows edge selections, and deletes
    vertcount = cmds.polyEvaluate(low, v=True)
    lastvert = ("%s.vtx[%s]" % (low, vertcount))
    cmds.select(lastvert)
    cmds.ConvertSelectionToEdges()
    cmds.polyListComponentConversion(te=True)

    for i in range(3):
        mel.eval('SelectEdgeLoopSp;')
        mel.eval('polySelectEdgesEveryN "edgeRing" 2;')
    cmds.polyDelEdge(cleanVertices=True)
    cmds.delete(low, ch=True)

    # if mesh is too heavy, don't blendshape
    if vertcount > 25000:
        return

    # smooth 'high geo', then use as negative blendshape to 'unsmooth' down-res vertices
    cmds.polySmooth(high, divisions=1, keepBorder=True, ch=False)
    blendnode = cmds.blendShape(high, low, topologyCheck=False)[0]
    cmds.setAttr(blendnode + "." + str(high), -4)
    cmds.delete(low, ch=True)
    cmds.delete(high)
    return low

unsmooth()
