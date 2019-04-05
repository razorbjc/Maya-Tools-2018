#!/usr/bin/env python2.7

"""
A custom UV toolset that allows access to the most commonly used tools

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel
import math


class uvui(object):
    windowName = "UVUI_window"

    def launch(self):
        # checks if window is already open, closes and recreates if it is
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName, title="UV UI", minimizeButton=False,
                    maximizeButton=False, sizeable=False, rtf=True)
        self.buildUI()
        cmds.showWindow()

    # builds layout and buttons, hooks up to commands
    def buildUI(self):
        columnMain = cmds.columnLayout(columnWidth=200)
        widthb = 61
        widtha = 40
        widthc = 29
        widthe = 124

        white = [1,1,1]
        red = [.9,.45,.45]
        blue = [.5,.75,.9]
        green = [.45, .8, .45]
        yellow = [.95,.85,.5]
        orange = [.9,.6,.2]
        purple = [.65,.5,.85]

        cmds.rowLayout(numberOfColumns=3, columnAlign1="center", p=columnMain)
        cmds.button(label="Rot. L", width=widtha, bgc=white, command=self.rotateLeft)
        cmds.button(label="Orient", width=widtha, bgc=red, command=self.orientShells)
        cmds.button(label="Rot. R", width=widtha, bgc=white, command=self.rotateRight)
        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", p=columnMain)
        cmds.button(label="Flip U", width=widthb, bgc=blue, command=self.udimFlipU)
        cmds.button(label="Flip V", width=widthb, bgc=blue, command=self.udimFlipV)

        cmds.rowLayout(numberOfColumns=1, p=columnMain, height=5)

        cmds.rowLayout(numberOfColumns=3, columnAlign1="center", p=columnMain)
        cmds.text(label="", width=widtha)
        cmds.button(label="/\\", width=widtha, bgc=white, command=self.translateUp)
        cmds.text(label="", width=widtha)

        cmds.rowLayout(numberOfColumns=3, p=columnMain)
        cmds.button(label="<", width=40, bgc=white, command=self.translateLeft)
        self.transDistance = cmds.floatField(ed=True, v=1.0, precision=2, s=.25, w=40)
        cmds.button(label=">", width=40, bgc=white, command=self.translateRight)

        cmds.rowLayout(numberOfColumns=3, p=columnMain)
        cmds.text(label="", width=40)
        cmds.button(label="V", width=40, bgc=white, command=self.translateDown)
        cmds.text(label="", width=40)
        cmds.rowLayout(numberOfColumns=1, p=columnMain, height=5)

        ### arrows button ends, Layout buttons begin
        ########################################################################
        cmds.rowLayout(numberOfColumns=2, p=columnMain)
        cmds.button(label="Center", width=widthb, bgc=green, command=self.udimCenter)
        cmds.button(label="Maximize", width=widthb, bgc=green, command=self.udimMax)

        cmds.rowLayout(numberOfColumns=2, p=columnMain)
        cmds.button(label="Get TD", width=widthb, bgc=yellow, command=self.getTD)
        cmds.button(label="Set TD", width=widthb, bgc=yellow, command=self.setTD)

        cmds.rowLayout(numberOfColumns=3, p=columnMain)
        cmds.button(label="Stack", width=widthb, bgc=purple, command=self.stackShells)
        cmds.button(label="U", width=widthc, bgc=purple, command=self.distributeU)
        cmds.button(label="V", width=widthc, bgc=purple, command=self.distributeV)

        cmds.rowLayout(numberOfColumns=1, p=columnMain)
        cmds.button(label="Layout", width=widthe, bgc=white, 
                    command=self.layoutUnfold3d)
        cmds.rowColumnLayout(numberOfColumns=2, p=columnMain)
        self.layoutScaleBox=cmds.checkBox(label="Scale", value=True)
        self.layoutRotateBox=cmds.checkBox(label="Rotate")

        ### Layout button ends, UV edit buttons begin
        ########################################################################
        cmds.rowLayout(numberOfColumns=1, p=columnMain, height=6)

        cmds.rowLayout(numberOfColumns=3, p=columnMain)
        cmds.button(label="Unfold", width=widthb, bgc=blue, command=self.unfoldUV)
        cmds.button(label="U", width=widthc, bgc=blue, command=self.unfoldU)
        cmds.button(label="V", width=widthc, bgc=blue, command=self.unfoldV)

        cmds.rowLayout(numberOfColumns=3, p=columnMain)
        cmds.button(label="Straighten", width=widthb, bgc=red, command=self.straighten)
        cmds.button(label="U", width=widthc, bgc=red, command=self.straightenU)
        cmds.button(label="V", width=widthc, bgc=red,  command=self.straightenV)

        cmds.rowLayout(numberOfColumns=2, p=columnMain)
        cmds.button(label="Symmetry", width=widthb, bgc=yellow, command=self.symmetrize)
        cmds.button(label="Mirror", width=widthb, bgc=yellow, command=self.mirror)

        cmds.rowLayout(numberOfColumns=2, p=columnMain)
        cmds.button(label="CutSew", width=widthb, bgc=green, command=self.cutsew3d)
        cmds.button(label="AutoSeam", width=widthb, bgc=purple, command=self.autoSeams)

        cmds.rowLayout(numberOfColumns=1, p=columnMain, height=4)

        cmds.rowLayout(numberOfColumns=2, p=columnMain)
        cmds.text(label="Transfer UVs", width=90, align="left")
        cmds.rowLayout(numberOfColumns=2, p=columnMain)
        cmds.button(label="Topo", width=widthb, bgc=white, command=self.transUVTopo,
                    ann="Transfers UVs from the last selected object \
                        to the rest of your selected objects")
        cmds.button(label="World", width=widthb, bgc=white, command=self.transUVWorld)
        ### End
        ########################################################################

    def rotateLeft(self, *args):
        mel.eval('polyRotateUVs 45 1;')

    def rotateRight(self, *args):
        mel.eval('polyRotateUVs -45 1;')

    def getDistance(self, *args):
        distance = cmds.floatField(self.transDistance, q=True, v=True)
        return distance

    def translateUp(self, *args):
        distance = getDistance()
        cmds.polyEditUV(u=0, v=distance)
        mel.eval('texPivotCycle selection middle;')

    def translateRight(self, *args):
        distance = getDistance()
        cmds.polyEditUV(u=distance, v=0)
        mel.eval('texPivotCycle selection middle;')

    def translateLeft(self, *args):
        distance = getDistance()
        cmds.polyEditUV(u=-(distance), v=0)
        mel.eval('texPivotCycle selection middle;')

    def translateDown(self, *args):
        distance = getDistance()
        cmds.polyEditUV(u=0, v=-(distance))
        mel.eval('texPivotCycle selection middle;')

    def stackShells(self, *args):
        sel = cmds.ls(sl=True)
        mel.eval('texStackShells {};')
        cmds.select(sel)

    def orientShells(self, *args):
        mel.eval('texOrientShells;')

    def getTD(self, *args):
        mel.eval('uvTkDoGetTexelDensity;')

    def setTD(self, *args):
        mel.eval('uvTkDoSetTexelDensity;')

    def udimFlipU(self, *args):
        udim = self.getUdim()
        tilecenter = udim[0] +.5
        cmds.polyEditUV(pivotU=tilecenter, scaleU=-1)
        mel.eval('texPivotCycle selection middle;')

    def udimFlipV(self, *args):
        udim = self.getUdim()
        tilecenter = udim[1] +.5
        cmds.polyEditUV(pivotV=tilecenter, scaleV=-1)
        mel.eval('texPivotCycle selection middle;')

    def udimCenter(self, *args):
        center = self.getCenter()
        udim = self.getUdim()
        utarget = udim[0] +.5 # find center of udim
        vtarget = udim[1] +.5
        cmds.polyEditUV(u=(utarget-center[0]), v=(vtarget-center[1]))
        mel.eval('texPivotCycle selection middle;')

    def udimMax(self, *args):
        center = self.getCenter()
        uminmax, vminmax, = cmds.polyEvaluate(bc2=True)
        width = math.fabs(uminmax[0] - uminmax[1])
        height = math.fabs(vminmax[0] - vminmax[1])
        if (width > height):
            factor = .98/width
        else:
            factor = .98/height
        cmds.polyEditUV(pivotU=center[0], pivotV=center[1], 
                        scaleV=factor, scaleU=factor)
        mel.eval('texPivotCycle selection middle;')

    def symmetrize(self, *args):
        udim = self.getUdim()
        cmds.setToolTo("texSymmetrizeUVContext")
        cmds.optionVar(fv=('polySymmetrizeUVAxisOffset',udim[0]+.5))

    def layoutUnfold3d(self, *args):
        scaleOn = cmds.checkBox(self.layoutScaleBox, q=True, value=True)
        rotateOn = cmds.checkBox(self.layoutRotateBox, q=True, value=True)
        startUdim = self.getUdim()
        if scaleOn and rotateOn:
            cmds.u3dLayout(res=256, spc=0.007, mar=0.01, scl=1, rst=90)
            #ps determines tile margin
            # cmds.polyMultiLayoutUV(prescale=2, layoutMethod=1, rotateForBestFit=1, 
            #                    flipReversed=True, percentageSpace=1, layout=2,
            #                    gridU=2, gridV=2, scale=1, sizeU=1,
            #                    sizeV=1, offsetU=0, offsetV=0)

        elif scaleOn and not rotateOn:
            # mar determines tile margin, spc is shell space
            cmds.u3dLayout(res=256, spc=0.007, mar=0.01, scl=1)

        elif rotateOn and not scaleOn:
            cmds.u3dLayout(res=256, spc=0.007, mar=0.01, scl=0, rst=90)
            # cmds.polyMultiLayoutUV(lm=1, sc=1, rbf=2, fr=1, ps=1, l=2, gu=1, gv=1, psc=0, su=1, sv=1, ou=0, ov=0)

        else:
            cmds.u3dLayout(res=256, spc=0.007, mar=0.01)

        cmds.polyEditUV(u=startUdim[0], v=startUdim[1])

    def unfoldUV(self, *args):
        cmds.u3dUnfold(ite=1, p=0, bi=1, tf=1, ms=128, rs=0)

    def unfoldU(self, *args):
        cmds.unfold(i=5000, ss=0.001, gb=0, gmb=0.5, pub=0, ps=0, oa=2, us=False)

    def unfoldV(self, *args):
        cmds.unfold(i=5000, ss=0.001, gb=0, gmb=0.5, pub=0, ps=0, oa=1, us=False)

    def straighten(self, *args):
        mel.eval('texStraightenUVs "UV" 30;')

    def straightenU(self, *args):
        mel.eval('texStraightenUVs "U" 30;')

    def straightenV(self, *args):
        mel.eval('texStraightenUVs "V" 30;')

    def cutsew3d(self, *args):
        mel.eval('SetCutSewUVTool;')

    def transUVTopo(self, *args):
        selection = cmds.ls(sl=True, o=True)
        reference = selection[-1]
        selection.remove(reference)
        for i in selection:
            cmds.transferAttributes(reference, i, 
                                    transferNormals=0, 
                                    transferUVs=2,
                                    sampleSpace=5, 
                                    searchMethod=0)

    def transUVWorld(self, *args):
        selection = cmds.ls(sl=True, o=True)
        reference = selection[-1]
        selection.remove(reference)
        for i in selection:
            cmds.transferAttributes(reference, i, 
                                    transferPositions=0, 
                                    transferNormals=0,
                                    transferUVs=2, 
                                    sourceUvSpace="map1",
                                    targetUvSpace="map1", 
                                    sampleSpace=0, 
                                    searchMethod=0)

    def uvToObj(self, *args):
        cmds.select(cmds.ls(sl=True, o=True))

    def distributeV(self, *args):
        startCenter = self.getCenter()
        mel.eval('texDistributeShells(0, 0.01, "up", {});')
        endCenter = self.getCenter()
        print startCenter, endCenter
        cmds.polyEditUV(u=(startCenter[0]-endCenter[0]), 
                        v=(startCenter[1]-endCenter[1]))
        mel.eval('texPivotCycle selection middle;')

    def distributeU(self, *args):
        startCenter = self.getCenter()
        mel.eval('texDistributeShells(0, 0.01, "right", {});')
        endCenter = self.getCenter()
        print startCenter, endCenter
        cmds.polyEditUV(u=(startCenter[0]-endCenter[0]), 
                        v=(startCenter[1]-endCenter[1]))
        mel.eval('texPivotCycle selection middle;')

    def autoSeams(self, *args):
        mel.eval('performPolyAutoSeamUV 0;')

    def getUdim(self):
        #tuple of two pairs in Python: ((xmin,xmax), (ymin,ymax))
        maxmin = cmds.polyEvaluate(bc2=True)
        uAvg = (maxmin[0][0] + maxmin[0][1])/2
        vAvg = (maxmin[1][0] + maxmin[1][1])/2
        uTile = math.floor(uAvg)
        vTile = math.floor(vAvg)
        udimTuple = (uTile, vTile)
        return udimTuple

    def getCenter(self):
        #tuple of two pairs in Python: ((xmin,xmax), (ymin,ymax))
        maxmin = cmds.polyEvaluate(bc2=True)
        uAvg = (maxmin[0][0] + maxmin[0][1])/2
        vAvg = (maxmin[1][0] + maxmin[1][1])/2
        centerTuple = (uAvg, vAvg)
        return centerTuple

    # def mirrorD is the exact same... ===========================================
    def mirror(self, *args):
        cmds.ConvertSelectionToContainedFaces()
        selection = cmds.ls(sl=True)  # starting UVs
        objs = cmds.ls(sl=True, o=True)

        cmds.select(selection)
        mel.eval('textureWindowSelectConvert 4;')
        mel.eval('polySelectBorderShell 1;')
        cmds.ConvertSelectionToContainedEdges()
        shellEdges = cmds.ls(sl=True, flatten=True)  # get border edge of UV shell

        cmds.select(selection)  # get selected faces
        mel.eval('PolySelectTraverse 1;')  # grow face selection
        cmds.ConvertSelectionToEdgePerimeter()  # grab selection perimeter
        # get border edge of user selection
        selPerimeter = cmds.ls(sl=True, flatten=True)

        sewEdges = []
        # get list of edges to sew, selection border edge that is NOT a shell edge
        sewEdges = [i for i in selPerimeter if i not in shellEdges]

        cmds.select(selection)  # select faces to run transfer Attributes
        mel.eval('textureWindowSelectConvert 4;')  # convert selection to UVs
        mel.eval('PolySelectTraverse 1;')  # grow selection without crossing UV borders
        cmds.ConvertSelectionToContainedFaces()

        startUdim = self.getUdim()
        cmds.transferAttributes(transferPositions=0, 
                                transferNormals=0, 
                                transferUVs=2, 
                                transferColors= 0,
                                sampleSpace= 0, 
                                searchMethod= 3,
                                searchScaleX =-1.0, 
                                flipUVs= 1, 
                                colorBorders=1)
        endUdim = self.getUdim()

        # clean history and move back to original UDIM, sew edges
        cmds.delete(objs[0],ch=True)
        cmds.polyEditUV(u=(startUdim[0]-endUdim[0]), v=0)

        for i in sewEdges:
            cmds.polyMapSew(i)

        cmds.select(selection)
        mel.eval('BakeNonDefHistory;')

    def mirrorD(self, *args):
        cmds.ConvertSelectionToContainedFaces()
        selection = cmds.ls(sl=True)  # starting UVs
        objs = cmds.ls(sl=True, o=True)
        print "obj:", objs

        cmds.select(selection)
        mel.eval('textureWindowSelectConvert 4;')
        mel.eval('polySelectBorderShell 1;')
        cmds.ConvertSelectionToContainedEdges()
        shellEdges = cmds.ls(sl=True, flatten=True)  # get border edge of UV shell
        print "shellEdges:\n %s" % shellEdges

        cmds.select(selection)  # get selected faces
        mel.eval('PolySelectTraverse 1;')  # grow face selection
        cmds.ConvertSelectionToEdgePerimeter()  # grab selection perimeter
        # get border edge of user selection
        selPerimeter = cmds.ls(sl=True, flatten=True)
        print"selectionPerimeter Edges:\n %s" % selPerimeter

        sewEdges = []
        # get list of edges to sew, selection border edge that is NOT a shell edge
        sewEdges = [i for i in selPerimeter if i not in shellEdges]
        print sewEdges


        cmds.select(selection)  # select faces to run transfer Attributes
        mel.eval('textureWindowSelectConvert 4;')  # convert selection to UVs
        mel.eval('PolySelectTraverse 1;')  # grow selection without crossing UV borders
        cmds.ConvertSelectionToContainedFaces()

        startUdim = self.getUdim()
        cmds.transferAttributes(transferPositions=0, 
                                transferNormals=0, 
                                transferUVs=2, 
                                transferColors= 0,
                                sampleSpace= 0, 
                                searchMethod= 3,
                                searchScaleX =-1.0, 
                                flipUVs= 1, 
                                colorBorders=1)
        endUdim = self.getUdim()

        # clean history and move back to original UDIM, sew edges
        cmds.delete(objs[0],ch=True)
        cmds.polyEditUV(u=(startUdim[0]-endUdim[0]), v=0)

        for i in sewEdges:
            cmds.polyMapSew(i)

        cmds.select(selection)
        mel.eval('BakeNonDefHistory;')

    def getFaceList(self):
        faceFilter= cmds.filterExpand(selectionMask=34)
        if not faceFilter:
            raise NameError('You must only Select Face Components!')
        return cmds.ls(sl=True, l=True)

    def getFaceLoc(self):
        # select list of uv's in first entry
        cmds.ConvertSelectionToUVs()
        uvList = cmds.ls(sl=True, l=True)
        uvLocs = cmds.polyEditUVShell(uvList, q=True)

        uLocs = uvLocs[0::2]
        vLocs = uvLocs[1::2]
        uAvgLoc = math.floor(sum(uLocs)/float(len(uLocs)))
        vAvgLoc = math.floor(sum(vLocs)/float(len(vLocs)))

        uvLocList = []
        uvLocList.append(uAvgLoc)
        uvLocList.append(vAvgLoc)

        return uvLocList

    def uv_transferMirror(self,*args):
        faceListBefore = self.getFaceList()
        oldLoc = self.getFaceLoc()
        cmds.ConvertSelectionToFaces()
        cmds.transferAttributes(transferPositions=0,
                                transferNormals=0, 
                                transferUVs=2, 
                                transferColors= 0, 
                                sampleSpace= 0, 
                                searchMethod= 3,
                                searchScaleX =-1.0, 
                                flipUVs= 1, 
                                colorBorders=1)
        faceListAfter = self.getFaceList()
        newLoc = self.getFaceLoc()
        cmds.ConvertSelectionToFaces()
        difPosU = oldLoc[0]- newLoc[0]
        difPosV = oldLoc[1]- newLoc[1]
        cmds.select(faceListAfter, r=True)
        cmds.polyEditUV(u=difPosU , v=difPosV)
        mesh = cmds.ls(sl=True, o=True)
        cmds.delete(mesh, ch=True)
