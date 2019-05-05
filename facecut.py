#!/usr/bin/env python2.7

"""
Given a a complete edge loop or enclosure of edges,
this script will select all faces within the edge perimeter

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel

def faceCut():
	edgeSel = cmds.ls(sl=True, fl=True)
	objs = cmds.ls(sl=True, o=True)

	# checks for face selection(mask 34) & vertices(mask 31)
	if (cmds.filterExpand(edgeSel, selectionMask=31)):
		cmds.error("Must select edges")
	if (cmds.filterExpand(edgeSel, selectionMask=34)):
		mel.eval('invertSelection;')
		return

	# create extra UV set to work in, and project new UVs
	cmds.polyUVSet(create=True, uvSet="facecut")
	cmds.polyUVSet(currentLastUVSet=True)
	projection= cmds.polyProjection(objs[0], type='Planar', md='p')
	cut=cmds.polyMapCut(edgeSel)

	# select edge and select a related face, then grow selection to shell
	cmds.select(edgeSel[0])
	cmds.textureWindow("polyTexturePlacementPanel1", e=True, selectRelatedFaces=True)
	cmds.polyListComponentConversion(fe=True, fuv=True)
	faceSel=cmds.ls(sl=True, fl=True)[-1]
	cmds.select(faceSel, r=True)
	cmds.ConvertSelectionToUVShell()

	# delete extra UV set, convert to edges then back to faces to allow invertSelection;
	cmds.polyUVSet(delete=True)
	cmds.ConvertSelectionToEdges()
	cmds.ConvertSelectionToContainedFaces()
	cmds.delete(projection)
	cmds.delete(cut)

if __name__ == '__main__':
	faceCut()


def getBiggest(array=None):
	biggestVol=0
	biggestItem=None
	for i in array:
		bbox = cmds.exactWorldBoundingBox(i)
		dimensions = [bbox[3]-bbox[0], bbox[4]-bbox[1], bbox[5]-bbox[2]]
		volume = dimensions[0]*dimensions[1]*dimensions[2]
		if volume > biggestVol:
			biggestVol = volume
			biggestItem = i

	return biggestItem
