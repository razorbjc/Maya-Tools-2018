#modelPanel just returns the full path name of the getPanel
#getPanel returns the name of current panel with focus
#listRelative returns 'c' children and 'f' full path names
#imagePlaneTrans gets the transform note of the imagePlane connected to the cameraShape
#array recieves the Shape node of the imagePlane, which is returned by listRelatives
#the shape node is then dropped into "myImagePlane": which would be imagePlaneShape1
#the imagePlaneShape1 is finally getAttr'd for the current alphaGain number and then setAttr...
#setAttr "imagePlaneShape1.alphaGain" 0.5
import maya.cmds as cmds


def jc_imagePlaneToggle():
    currentCam = cmds.modelPanel(cmds.getPanel(wf=True), q=True, cam=True)
    currentCamShape = cmds.listRelatives(currentCam,c=True,f=True)
    imagePlaneTrans = cmds.listConnections(currentCamShape)
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


#jc_imagePlaneToggle()
