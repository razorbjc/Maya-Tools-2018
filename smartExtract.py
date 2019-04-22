#!/usr/bin/env python2.7

"""
Works with Maya 2018
meant to replace Maya's extract
if objects with separate meshes are selected, smartExtract will separate them

if given a face selection, smartExtract will extract faces but retain the name and pivot
of the base geometry. The extracted pieces will be named/numbered and pivots centered

if given an completed edge loop, smartExtract will run faceCut and then extract faces

if given vertices, the vertex selection will be converted to a face select and extract

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel
import jc_faceCut

def smartExtract():
	sel = cmds.ls(sl=True)

	# object selected: run separate
	if cmds.nodeType(sel[0])=='transform':
		parents = cmds.listRelatives(parent=True, fullPath=True)
		for obj in sel:
			separateObj = cmds.polySeparate(obj, ch=False)
			rebuild(separateObj, "separate", parents)
			cmds.delete(obj)
		return

	if cmds.nodeType(sel[0])!='mesh':
		return

	# get transform name, parents/hierachy
	name = cmds.listRelatives(cmds.ls(sl=True, o=True), p=True, fullPath=True)[0]
	parents = cmds.listRelatives(name, parent=True, fullPath=True)

	# Run face extraction, then pop off the Separate node, and remove original geo
	toFaces(sel)
	cmds.ExtractFace()
	extracted = cmds.ls(sl=True, o=True)
	extracted.pop(-1) # Removes separate node
	if len(extracted)<2:
		cmds.error("Must select a completed edge loop")
		return False

	original = [getBiggest(extracted)]
	extracted.remove(original[0]) #remove the biggest piece, which will keep original name

	#Restore hierarchy, center piv, rename, del history
	cmds.rename(cmds.listRelatives(original[0], p=True, fullPath=True)[0], "xxx")
	new_original = rebuild(original, name.split("|")[-1], parents, True)
	new_extracted = rebuild(extracted, "extract", parents)
	cmds.select(new_original, r=True)
	cmds.select(new_extracted, add=True)
	cmds.setToolTo('moveSuperContext')
	cmds.SelectToggleMode()
	return


def smartDuplicate():
	sel = cmds.ls(sl=True)

	# object selected: run separate
	if cmds.nodeType(sel[0])=='transform':
		mel.eval('Duplicate;')
		return

	if cmds.nodeType(sel[0])!='mesh':
		return

	# get transform name, parents/hierachy
	name = cmds.listRelatives(cmds.ls(sl=True, o=True), p=True, fullPath=True)[0]
	parents = cmds.listRelatives(name, parent=True, fullPath=True)
	pivotInfo = cmds.xform(name, q=True, pivots=True, ws=True)[:3]

	toFaces(sel)
	cmds.DuplicateFace()
	duplicated = cmds.ls(sl=True, o=True)
	duplicated.pop(-1) # Removes polySeparate Node
	if len(duplicated)<2:
		cmds.error("Must select a completed edge loop")
		return False

	original = [getBiggest(duplicated)]
	duplicated.remove(original[0])

	#Restore hierarchy, center piv, rename, del history
	cmds.rename(cmds.listRelatives(original[0], p=True, fullPath=True)[0], "xxx")
	rebuild(array = original,
			name = name.split("|")[-1],
			group = parents,
			primary = True,
			freeze = False,
			pivot = pivotInfo)
	new_duplicated = rebuild(array=duplicated, name="duplicate", group=parents)
	cmds.select(new_duplicated, add=True)
	cmds.setToolTo('moveSuperContext')
	cmds.SelectToggleMode()
	return


def rebuild(array=None, name=None, group=None, primary=False, freeze=True, pivot=None):
	finalArray = []
	count=1001
	for i in array:
		newname = cmds.parent(i,group) if group else cmds.parent(i,world=True)
		if freeze:
			cmds.makeIdentity(newname, apply=True, r=True, s=True, t=True)
		if pivot:
			cmds.xform(newname, pivots=pivot, ws=True)
		else:
			cmds.xform(newname,cp=True)
		cmds.delete(newname,ch=True)
		final = cmds.rename(newname,name) if primary else cmds.rename(newname,name + "_%0*d" % (4, count))
		finalArray.append(final)
		count += 1

	return finalArray


def getBiggest(array=None):
	biggestVol=0
	biggestItem=array[0]
	for i in array:
		bbox = cmds.exactWorldBoundingBox(i)
		dimensions = [bbox[3]-bbox[0], bbox[4]-bbox[1], bbox[5]-bbox[2]]
		volume = dimensions[0]*dimensions[1]*dimensions[2]
		if volume >= biggestVol:
			biggestVol = volume
			biggestItem = i

	return biggestItem


def toFaces(sel):
	# checks for edge selection(mask 32) & vertices(mask 31), then converts them to faces
	if (cmds.filterExpand(sel[0], selectionMask=31)):
		cmds.ConvertSelectionToContainedFaces()
	if (cmds.filterExpand(sel[0], selectionMask=32)):
		jc_faceCut.faceCut()
	cmds.ConvertSelectionToFaces()
	return


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
	smartExtract()


