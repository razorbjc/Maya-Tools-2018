import maya.cmds as cmds
import maya.mel as mel

def jc_faceCut():
    edgeSel = cmds.ls(sl=True)
    objs = cmds.ls(sl=True, o=True)
    cmds.polyUVSet(create=True, uvSet="facecut")
    cmds.polyUVSet(currentLastUVSet=True)
    projection= cmds.polyProjection(objs[0], type='Planar', md='p')
    cut=cmds.polyMapCut(edgeSel)
    firstFace = (objs[0] + ".map[0]")
    cmds.select(firstFace, r=True)
    cmds.ConvertSelectionToUVShell()
    cmds.ConvertSelectionToFaces()
    cmds.polyUVSet(delete=True)
    cmds.delete(cut)
    cmds.delete(projection)
    # mel.eval('InvertSelection;')
