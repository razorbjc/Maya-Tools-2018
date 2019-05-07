import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI

view = OpenMayaUI.M3dView.active3dView()
cam = OpenMaya.MDagPath()
view.getCamera(cam)
camPath = cam.fullPathName()
print cmds.getAttr(str(camPath+".nearClipPlane"))

if (cmds.getAttr(str(camPath+".nearClipPlane"))==.1):
    cmds.setAttr(str(camPath+".nearClipPlane"),1)
    cmds.setAttr(str(camPath+".farClipPlane"),10000)
    
elif (cmds.getAttr(str(camPath+".nearClipPlane"))==1):
    cmds.setAttr(str(camPath+".nearClipPlane"),10)
    cmds.setAttr(str(camPath+".farClipPlane"),100000)

    
elif (cmds.getAttr(str(camPath+".nearClipPlane"))==10):
    cmds.setAttr(str(camPath+".nearClipPlane"),100)
    cmds.setAttr(str(camPath+".farClipPlane"),1000000)
    
elif (cmds.getAttr(str(camPath+".nearClipPlane"))==100):
    cmds.setAttr(str(camPath+".nearClipPlane"),.1)
    cmds.setAttr(str(camPath+".farClipPlane"),1000)    
    
else:
    cmds.setAttr(str(camPath+".nearClipPlane"),1)
    cmds.setAttr(str(camPath+".farClipPlane"),10000)    
