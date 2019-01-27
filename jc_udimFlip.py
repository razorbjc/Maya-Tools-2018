import maya.cmds as cmds

def jc_udimFlip():
	#get selection and convert to UVs
	selection = cmds.ls(selection=True)
	uvs = cmds.polyListComponentConversion (selection, tuv=True)

	#get first UV in returned array and round down to find the pivot of the flip 
	uvalue = cmds.polyEditUV(uvs[0], query=True )
	pivot = round(uvalue[0]-.5)

	#run polyEditUV and scale around the pivot+.5
	cmds.polyEditUV(pivotU=(pivot+.5), scaleU=-1)

jc_udimFlip()
