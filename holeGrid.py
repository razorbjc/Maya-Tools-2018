#!/usr/bin/env python2.7

"""
Works with Maya 2018
When an edge or edgloop of a hole is selected, this script will fill the hole with a grid.
After the script is run, the grid verts are selected for further averaging
The 'offset' attribute in the channel box can be adjusted to fine-tune the rotation
Created Oct 2020

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel
import math

def holeGrid():
    obj = cmds.ls(sl=True, o=True)
    obj_name = cmds.listRelatives(obj, parent=True)[0]
    cmds.ConvertSelectionToEdges()
    cmds.polySelectSp(loop=True)  # select edgeloop
    edge_outer = cmds.ls(sl=True, fl=True)

    # find shader on connected face
    cmds.select(edge_outer[0])
    cmds.ConvertSelectionToFaces()
    cmds.hyperShade(smn=True)
    shader = cmds.ls(sl=True)[0]

    # create plane and combine with original geo
    new_plane = create_plane(edge_outer)
    cmds.select(new_plane)
    cmds.hyperShade(assign=shader)
    new_geo_name = cmds.polyUnite(obj, new_plane, n=obj_name)[0]
    cmds.delete(new_geo_name, ch=True)
    cmds.isolateSelect(cmds.paneLayout('viewPanes', q=True, pane1=True), addSelected=True)

    # select last edge of combined geo, update names for the outer edge
    last_edge = (cmds.polyEvaluate(new_geo_name, e=True))-1
    last_edge_string = str(new_geo_name)+".e["+str(last_edge)+"]"
    new_edge_outer = []
    for i in edge_outer:
        new_edge_outer.append(i.replace(obj_name, new_geo_name))

    # select inner and outer edge
    cmds.select(last_edge_string)
    cmds.polySelectSp(loop=True)
    edge_inner = cmds.ls(sl=True, fl=True)
    mel.eval('polySelectBorderShell 0;')
    cmds.ConvertSelectionToFaces()
    faces_inner = cmds.ls(sl=True)
    cmds.select(edge_inner)
    cmds.select(new_edge_outer, add=True)

    # run bridge
    # average inner verts depending on # of edges in selected edge loop
    bridge_node = cmds.polyBridgeEdge(ch=1, divisions=0, bridgeOffset=0)[0]
    cmds.select(faces_inner)
    cmds.ConvertSelectionToVertices()
    avg_num = 7 + int(len(edge_outer)*0.3)
    for i in range(avg_num):
        cmds.polyAverageVertex(iterations=10, ch=True)
    cmds.setAttr(str(bridge_node) + ".bridgeOffset", k=1)
    cmds.select(bridge_node, addFirst=True)


def create_plane(edge_sel):
    # find world position and width of new plane
    cmds.select(edge_sel)
    obj = cmds.ls(sl=True, o=True)
    obj_name = cmds.listRelatives(obj, parent=True)[0]
    bbox = cmds.exactWorldBoundingBox()
    center_x = (bbox[3]+bbox[0])/2
    center_y = (bbox[4]+bbox[1])/2
    center_z = (bbox[5]+bbox[2])/2
    widths = {bbox[3]-bbox[0], bbox[4]-bbox[1], bbox[5]-bbox[2]}
    plane_width = sorted(widths)[-1]  # sort widths and use the widest

    # find subd values of new plane
    edge_num = len(edge_sel)
    subd_width = math.ceil(edge_num/4.0)
    subd_height = math.ceil((edge_num-(2*subd_width))/2.0)

    # create plane geo
    cmds.select(edge_sel)
    cmds.polyCloseBorder()
    fill_hole = "%s.f[%s]" % (obj_name, cmds.polyEvaluate(obj_name, f=True)-1)
    new_plane = cmds.polyPlane(sx=subd_width,
                               sy=subd_height,
                               w=plane_width*0.7,
                               h=plane_width*0.7,
                               ch=False)

    # compare inner & outer edgeloops, collapse edge if they don't match
    cmds.select(new_plane)
    cmds.ConvertSelectionToEdgePerimeter()
    new_plane_edge = cmds.ls(sl=True, fl=True)
    if len(new_plane_edge) > len(edge_sel):
        cmds.select(new_plane_edge[-1])
        cmds.polyCollapseEdge()

    # move plane to position, delete hole_fill and history
    cmds.move(center_x, center_y, center_z, new_plane)
    constraint_var = cmds.normalConstraint(fill_hole,
                                           new_plane,
                                           aimVector=(0, 1, 0),
                                           worldUpType=0)
    cmds.delete(new_plane, ch=True)
    cmds.delete(constraint_var)
    cmds.delete(fill_hole)

    return new_plane

holeGrid()
