#!/usr/bin/env python2.7

"""
Works with Maya 2018
Toggles imageplane visibility of current camera
May 2019
__author__: James Chan
"""

import maya.cmds as cmds


def imageplanetoggle():
    current_cam = cmds.modelPanel(cmds.getPanel(wf=True), q=True, cam=True)
    current_cam_shape = cmds.listRelatives(current_cam, c=True, f=True)
    imgplanetrans = cmds.listConnections(current_cam_shape)
    imgplanes = cmds.listRelatives(imgplanetrans, shapes=True)

    plane_alpha = cmds.getAttr(str(imgplanes[0]) + ".alphaGain")
    if plane_alpha == 1:
            for i in imgplanes:
                cmds.setAttr(str(i)+".alphaGain", 0)
    elif plane_alpha == 0:
            for i in imgplanes:
                cmds.setAttr(str(i)+".alphaGain", .5)
    elif plane_alpha == .5:
            for i in imgplanes:
                cmds.setAttr(str(i)+".alphaGain", 1)
    else:
            for i in imgplanes:
                cmds.setAttr(str(i)+".alphaGain", 0)
