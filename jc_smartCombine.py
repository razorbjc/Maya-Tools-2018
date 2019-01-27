import maya.cmds as cmds

def jc_smartCombine():
	selection = cmds.ls(sl=True)

	#gather name, pivot, and layer information
	name = selection[0]
	print ("name is" + str(name)) 
	pivot = cmds.xform(name, q=True, worldSpace=True, rotatePivot=True)
	display_layers = cmds.listConnections(name, type="displayLayer")
	#combine with no history (empty transforms)
	new_mesh = cmds.polyUnite(ch=False) 
	# re-add name, pivot, and display layers
	cmds.xform(new_mesh, rotatePivot=pivot)
	if display_layers:
		cmds.editDisplayLayerMembers(display_layers[0], new_mesh)
		cmds.rename(new_mesh, name) 

jc_smartCombine()
