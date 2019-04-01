# Works with Python 2.7 Maya 2018
# given a a complete edge loop or enclosure of edges,
# this script will select all faces within the edge perimeter

import maya.cmds as cmds
import maya.mel as mel
def jc_faceCut():
	edgeSel = cmds.ls(sl=True, fl=True)
	objs = cmds.ls(sl=True, o=True)

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


