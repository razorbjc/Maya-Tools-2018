#!/usr/bin/env python2.7

"""
Works with Maya 2018
Increases the clipping plane range of all cameras in the scene to
10cm - 1,000,000cm. Clicking again will toggle all cameras back to default range
May 2019
__author__: James Chan
"""

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI


def camcliptoggle():
    view = OpenMayaUI.M3dView.active3dView()
    cam = OpenMaya.MDagPath()
    view.getCamera(cam)
    campath = cam.fullPathName()
    camlist = cmds.ls(cameras=True)

    if cmds.getAttr(str(campath + ".nearClipPlane")) == .1:
        for i in camlist:
            cmds.inViewMessage(amg='<hl>Large</hl> Clipping Planes set to 10cm - 1000000cm',
                               pos='topCenter', fade=True )
            cmds.setAttr(str(i+".nearClipPlane"), 10)
            cmds.setAttr(str(i+".farClipPlane"), 1000000)

    elif cmds.getAttr(str(campath+".nearClipPlane")) == 10:
        for i in camlist:
            cmds.inViewMessage(amg='<hl>Default</hl> Clipping Planes set to 0.1cm - 10000cm',
                               pos='topCenter', fade=True )
            cmds.setAttr(str(i+".nearClipPlane"), .1)
            cmds.setAttr(str(i+".farClipPlane"), 10000)

    else:
        for i in camlist:
            cmds.inViewMessage(amg='<hl>Default</hl> Clipping Planes set to 0.1cm - 10000cm',
                               pos='topCenter', fade=True )
            cmds.setAttr(str(i+".nearClipPlane"), .1)
            cmds.setAttr(str(i+".farClipPlane"), 10000)
