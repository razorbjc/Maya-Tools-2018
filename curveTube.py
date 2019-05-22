#!/usr/bin/env python2.7

"""
Works with Maya 2018
If given a curve, will produce tube geometry with spans at the curve's CVs
If given tube geometry, will create a curve with CVs at the center of the edge rings
May 2019
__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel


def curveTube():
    sel = cmds.ls(sl=True, o=True)
    result_list = []
    result = None

    for i in sel:
        parents = cmds.listRelatives(i, p=True, fullPath=True)
        shortname = i.split("|")[-1]
        pivotinfo = cmds.xform(i, q=True, pivots=True, ws=True)[:3]

        if cmds.nodeType(cmds.listRelatives(i)) == 'nurbsCurve':
            result = curve_to_tube(i)
            result = cmds.parent(result, parents[0])[0] if parents else result
            newname = shortname.replace('_curve', '_geo', 3) if '_curve' in shortname \
                else shortname+"_geo"
            result = cmds.rename(result, newname)

        else:
            result = tube_to_curve(i)
            result = cmds.parent(result, parents[0])[0] if parents else result
            newname = shortname.replace('_geo', '_curve', 3) if '_geo' in shortname \
                else shortname+"_curve"
            result = cmds.rename(result, newname)

        cmds.xform(result, pivots=pivotinfo, ws=True)
        result_list.append(result)

    cmds.select(result_list)
    return


def curve_to_tube(sel_curve):  # original with nurb circle extrusion
    resolution = 8
    radius = 1
    orig_loc = cmds.pointPosition(sel_curve+".cv[0]")
    cv_loc = cmds.pointPosition(sel_curve+".cv[1]")
    circle_var = cmds.circle(r=radius, sections=resolution, nr=(0, 1, 0))[0]
    locator_var = cmds.spaceLocator(p=(0, 0, 0))[0]

    # move circle and locator to curve points [0] and [1], aim circle, and extrude tube
    cmds.move(orig_loc[0], orig_loc[1], orig_loc[2], circle_var)
    cmds.move(cv_loc[0], cv_loc[1], cv_loc[2], locator_var)
    cmds.aimConstraint(locator_var, circle_var, o=(0, 0, 90))
    final = cmds.extrude(circle_var,
                         sel_curve,
                         ch=True,
                         rn=False,
                         po=1,
                         et=2,
                         ucp=0,
                         fpt=1,
                         upn=1,
                         rotation=0,
                         scale=1,
                         rsp=1)[0]

    # UV and delete history
    uv_tube(final)
    cmds.delete(final, ch=True)
    cmds.delete(locator_var)
    cmds.delete(circle_var)
    return final


def tube_to_curve(tube):
    # select one border edge, then store edge rings in 'spans'
    border_edge = get_border_edges(tube)
    cmds.polySelect(tube, edgeBorder=get_comp_int(border_edge[0]), ass=True)
    edge_sel = cmds.ls(sl=True, fl=True)
    spans = cmds.polySelect(tube, edgeRing=get_comp_int(edge_sel[0]), ass=True)
    length = len(spans)
    cmds.select(edge_sel, r=True)
    cmds.ConvertSelectionToVertices()
    coord_array = []
    black_list = []

    # traverse through spans by growing selection then removing vertices in the blacklist
    # then select edgeloops and store in coord_array
    for j in range(length):
        new_selection = cmds.ls(sl=True, fl=True)
        new_ring = [i for i in new_selection if i not in black_list]
        coord_array.append(new_ring)
        black_list = black_list + new_ring
        cmds.select(new_ring)
        cmds.GrowPolygonSelectionRegion()
    return buildcurve(coord_array)


def buildcurve(coord_array):
    curve_array = []
    for i in coord_array:
        cmds.select(i)
        bbox = cmds.polyEvaluate(boundingBoxComponent=True)
        x_avg = (bbox[0][0] + bbox[0][1])/2
        y_avg = (bbox[1][0] + bbox[1][1])/2
        z_avg = (bbox[2][0] + bbox[2][1])/2
        world_coord = (x_avg, y_avg, z_avg)
        curve_array.append(world_coord)
    final_curve = cmds.curve(p=curve_array)
    return final_curve


def get_border_edges(obj):
    cmds.select(obj)
    cmds.ConvertSelectionToVertices()
    cmds.ShrinkPolygonSelectionRegion()
    cmds.ConvertSelectionToEdges()
    cmds.InvertSelection()
    border_edges = cmds.ls(sl=True, fl=True)
    return border_edges


def get_comp_int(component):
    id_num = component.split("[")[1]
    id_num = id_num.split("]")[0]
    return int(id_num)


def get_lengthwise_edge(border_edge):
    cmds.select(border_edge)
    mel.eval('SelectEdgeLoopSp;')
    remove_edges = cmds.ls(sl=True, fl=True)
    cmds.GrowPolygonSelectionRegion()
    selected_edges = cmds.ls(sl=True)
    lengthwise_edges = [i for i in selected_edges if i not in remove_edges]
    return lengthwise_edges[0]


def uv_tube(obj):
    border_edges = get_border_edges(obj)
    length_edge = get_lengthwise_edge(border_edges[0])
    cmds.polySelect(obj, edgeLoop=get_comp_int(length_edge), ass=True)
    cmds.ConvertSelectionToVertices()
    vert_loop = cmds.ls(sl=True, fl=True)
    cmds.polyUVRectangle(vert_loop[0], vert_loop[-1])
    cmds.polyFlipUV(obj, pivotU=0.5)
    return obj
