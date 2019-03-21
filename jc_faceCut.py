# Works with Python 2.7 Maya 2018
# given a a complete edge loop or enclosure of edges,
# this script will select all faces within the edge perimeter

import maya.cmds as cmds
import maya.mel as mel
def jc_faceCut():
	edgeSel = cmds.ls(sl=True, fl=True)
	objs = cmds.ls(sl=True, o=True)
	objTrans = cmds.listRelatives(cmds.ls(sl=True, o=True), p=True)
	cmds.polyUVSet(create=True, uvSet="facecut")
	cmds.polyUVSet(currentLastUVSet=True)
	projection= cmds.polyProjection(objs[0], type='Planar', md='p')
	cut=cmds.polyMapCut(edgeSel)
	cmds.select(edgeSel[0])
	cmds.textureWindow("polyTexturePlacementPanel1", e=True, selectRelatedFaces=True)
	cmds.polyListComponentConversion(fe=True, fuv=True)
	faceSel=cmds.ls(sl=True, fl=True)[-1]
	cmds.select(faceSel, r=True)
	cmds.ConvertSelectionToUVShell()
	# cmds.ConvertSelectionToFaces()
	cmds.polyUVSet(delete=True)
	sel=cmds.ls(sl=True)
	print sel
	#mel.eval('InvertSelection;')
#textureWindow -e -selectRelatedFaces polyTexturePlacementPanel1;
#polyListComponentConversion -fv -fe -fuv -tf -te;

#ConvertSelectionToFaces;
#selectType -ocm -alc false;
#selectType -ocm -polymeshFace true;
#PolySelectConvert 1;

jc_faceCut()
