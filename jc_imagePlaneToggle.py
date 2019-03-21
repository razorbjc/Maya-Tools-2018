# Works with Python 2.7 Maya 2018
# toggles transparency of 1st image plane attached to current camera( from 0 to .5. to 1

import maya.cmds as cmds


def jc_imagePlaneToggle():
    #modelPanel just returns the full path name of the getPanel
    #getPanel returns the name of current panel with focus
    currentCam = cmds.modelPanel(cmds.getPanel(wf=True), q=True, cam=True)
    currentCamShape = cmds.listRelatives(currentCam,c=True,f=True)
    #imagePlaneTrans gets the transform node of the imagePlane connected to the cameraShape
    imagePlaneTrans = cmds.listConnections(currentCamShape[0])
    #imagePlaneTrans gets the Shape node of the imagePlane, which is returned by listRelatives
    #the shape node is then dropped into "myImagePlane": which would be imagePlaneShape1
    array = cmds.listRelatives(imagePlaneTrans[0], shapes=True)
    myImagePlane = array[0]

    if myImagePlane:
        planeAlphaState = cmds.getAttr(str(myImagePlane) + ".alphaGain")
        if planeAlphaState != 0 and planeAlphaState != .5 and planeAlphaState != 1:
            cmds.setAttr(str(myImagePlane)+".alphaGain",0)
        elif planeAlphaState == 1:
            cmds.setAttr(str(myImagePlane)+".alphaGain",0)
        elif planeAlphaState == 0:
            cmds.setAttr(str(myImagePlane)+".alphaGain",.5)
        elif planeAlphaState == .5:
            cmds.setAttr(str(myImagePlane)+".alphaGain",1)
