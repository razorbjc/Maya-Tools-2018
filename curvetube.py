#!/usr/bin/env python2.7

"""
Given a a complete edge loop or enclosure of edges,
this script will select all faces within the edge perimeter

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel


def curvetube():
    sel = cmds.ls(sl=True, l=True)
    result_list = []

    for i in sel:
        if cmds.nodeType(cmds.listRelatives(i)) == 'mesh':
            print "mesh!"
            tube_to_curve_a(i)
        elif cmds.nodeType(cmds.listRelatives(i)) == 'nurbsCurve':
            print "nurbsCurve!"
            result = curve_to_tube_a(i)
        else:
            continue

        parents = cmds.listRelatives(i, p=True, fullPath=True)
        shortname = i.split("|")[-1]
        # cmds.delete(i)  # delete original curve to replace
        if parents:
            result = cmds.parent(result, parents[0])[0]
        result = cmds.rename(result, shortname+"_tube")
        result_list.append(result)

    cmds.select(result_list)
    return

def curve_to_tube_a(sel_curve):  # original with nurb circle extrusion
    print "curve to tube"
    orig_loc = cmds.pointPosition(sel_curve+".cv[0]")
    cv_loc = cmds.pointPosition(sel_curve+".cv[1]")
    circle_var = cmds.circle(r=1, sections=6, nr=(0,1,0))[0]
    locator_var = cmds.spaceLocator(p=(0,0,0))[0]
    cmds.select(circle_var, r=True)
    cmds.move(orig_loc[0],orig_loc[1],orig_loc[2])
    cmds.select(locator_var, r=True)
    cmds.move(cv_loc[0],cv_loc[1],cv_loc[2])
    aim_constraint = cmds.aimConstraint(locator_var, circle_var, o=(0,0,90))
    cmds.reverseCurve(circle_var)
    nurb_curve = cmds.extrude(circle_var, sel_curve, et=2)[0]
    final = cmds.nurbsToPoly(nurb_curve,
                             mnd=1,
                             ch=1,
                             f=2,
                             pt=1,
                             pc=200,
                             chr=0.9,
                             ft=0.01,
                             mel=0.001,
                             d=0.1,
                             ut=3,
                             un=1,
                             vt=3,
                             vn=1,
                             uch=0,
                             ucr=0,
                             cht=0.2,
                             es=0,
                             ntr=0,
                             mrt=0,
                             uss=1)[0]
    cmds.delete(final,ch=True)
    cmds.delete(locator_var)
    cmds.delete(circle_var)
    cmds.delete(nurb_curve)

    return final


def curve_to_tube_b(sel_curve): # new with polygon face extrusion
    print "curve to tube"
    orig_loc = cmds.pointPosition(sel_curve+".cv[0]")
    cv_loc = cmds.pointPosition(sel_curve+".cv[1]")
    locator_var = cmds.spaceLocator(p=(0,0,0))[0]
    cmds.select(locator_var, r=True)
    cmds.move(cv_loc[0],cv_loc[1],cv_loc[2])
    cmds.polyDisc(sides=4, subdivisionMode=4, subdivisions=1, radius=1)
    disc_var = cmds.ls(sl=True, o=True)
    cmds.move(orig_loc[0],orig_loc[1],orig_loc[2])
    cmds.ConvertSelectionToFaces()
    targetfaces = cmds.ls(sl=True)
    aim_constraint = cmds.aimConstraint(locator_var, disc_var, o=(180,0,90))
    targetfaces = cmds.ls(sl=True)
    cmds.polyExtrudeFacet(targetfaces, divisions=24, inputCurve=sel_curve)
    cmds.delete(aim_constraint)

    return disc_var

def reparent_rename(reference, target):
    parents = cmds.listRelatives(reference, p=True, fullPath=True)[0]
    shortname = reference.split("|")[-1]
    if parents:
        newpath = cmds.parent(target, parents)[0]
    newname = cmds.rename(newpath, shortname+"_geo")
    return newname

def buildcurve(coord_array):
    print "coord_array:", coord_array
    curve_array=[]
    for i in coord_array:
        print "LOOPING:", i
        cmds.select(i)
        bbox = cmds.polyEvaluate(boundingBoxComponent=True)
        x_avg = (bbox[0][0] + bbox[0][1])/2
        y_avg = (bbox[1][0] + bbox[1][1])/2
        z_avg = (bbox[2][0] + bbox[2][1])/2
        world_coord = (x_avg, y_avg, z_avg)
        curve_array.append(world_coord)
    final_curve = cmds.curve(p=curve_array)
    return final_curve



def tube_to_curve_b(tube):
    print "tube to curve"
    cmds.select(tube)
    obj = cmds.ls(sl=True, o=True)
    cmds.ConvertSelectionToVertices()
    cmds.ShrinkPolygonSelectionRegion()
    mel.eval('ConvertSelectionToEdges;')
    cmds.InvertSelection()
    border_edge = cmds.ls(sl=True, fl=True)
    cmds.select(border_edge[0])
    cmds.polySelectSp(ring = True)
    length = len(cmds.ls(sl=True))
    print length


    cmds.select(border_edge, r=True)
    cmds.ConvertSelectionToVertices()
    curve_array = []
    black_list=[]
    for j in range(length):
        new_selection = cmds.ls(sl=True, fl=True)
        new_ring=[]
        for i in new_selection:
            if i not in black_list:
                new_ring.append(i)
        #add point to curve_array with new_ring

        cmds.select(new_ring)
        bbox = cmds.polyEvaluate(boundingBoxComponent=True)
        print "bbox:",
        x_avg = (bbox[0][0] + bbox[0][1])/2
        y_avg = (bbox[1][0] + bbox[1][1])/2
        z_avg = (bbox[2][0] + bbox[2][1])/2
        world_coord = (x_avg, y_avg, z_avg)
        curve_array.append(world_coord)
        print "new_ring:", new_ring
        combined_list = black_list + new_ring
        black_list = combined_list
        cmds.GrowPolygonSelectionRegion()

    final_curve = cmds.curve(p=curve_array)
    #buildcurve(coord_array)


def tube_to_curve_a(tube):
    print "tube to curve"
    cmds.select(tube)
    cmds.ConvertSelectionToVertices()
    cmds.ShrinkPolygonSelectionRegion()
    mel.eval('ConvertSelectionToEdges;')
    cmds.InvertSelection()
    border_edge = cmds.ls(sl=True, fl=True)
    print "borderedges:", border_edge[0]
    intVar = border_edge[0].split("[")[1]
    intVar = intVar.split("]")[0]
    cmds.polySelect(tube, edgeBorder=int(intVar), ass=True)
    edgeSel = cmds.ls(sl=True)
    objSel = cmds.ls(sl=True, o=True)
    intVar = edgeSel[0].split("[")[1]
    intVar = intVar.split("]")[0]
    spans = cmds.polySelect(objSel, edgeRing=int(intVar), ass=True)
    length = len(spans)
    print length
    cmds.select(edgeSel, r=True)
    cmds.ConvertSelectionToVertices()
    coord_array = []
    black_list=[]
    for j in range(length):
        new_selection = cmds.ls(sl=True, fl=True)
        new_ring=[]
        for i in new_selection:
            if i not in black_list:
                new_ring.append(i)
        #add point to curve_array with new_ring
        # cmds.spaceLocator(p=cmds.pointPosition(new_ring[0]))
        print "new_ring:", new_ring
        coord_array.append(new_ring)
        combined_list = black_list + new_ring
        black_list = combined_list
        print "black_list", black_list
        cmds.select(new_ring)
        #cmds.select(black_list)
        cmds.GrowPolygonSelectionRegion()

    buildcurve(coord_array)
