#!/usr/bin/env python2.7

"""
works with Maya 2018
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
        self.buildui()
        cmds.showWindow()

    # builds layout and buttons, hooks up to commands
    def buildui(self):
        columnmain = cmds.columnLayout(columnWidth=200)
        widthb = 61
        widtha = 40
        widthc = 29
        widthe = 124

        white = [1, 1, 1]
        red = [.9, .45, .45]
        blue = [.5, .75, .9]
        green = [.45, .8, .45]
        yellow = [.95, .85, .5]
        orange = [.9, .6, .2]
        purple = [.65, .5, .85]

        cmds.rowLayout(numberOfColumns=3, columnAlign1="center", p=columnmain)
        cmds.button(label="Rot. L", width=widtha, bgc=white, command=self.rotate_left)
        cmds.button(label="Orient", width=widtha, bgc=red, command=self.orient_shells)
        cmds.button(label="Rot. R", width=widtha, bgc=white, command=self.rotate_right)
        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", p=columnmain)
        cmds.button(label="Flip U", width=widthb, bgc=blue, command=self.udim_flip_u)
        cmds.button(label="Flip V", width=widthb, bgc=blue, command=self.udim_flip_v)

        cmds.rowLayout(numberOfColumns=1, p=columnmain, height=5)

        cmds.rowLayout(numberOfColumns=3, columnAlign1="center", p=columnmain)
        cmds.text(label="", width=widtha)
        cmds.button(label="/\\", width=widtha, bgc=white, command=self.translate_up)
        cmds.text(label="", width=widtha)

        cmds.rowLayout(numberOfColumns=3, p=columnmain)
        cmds.button(label="<", width=40, bgc=white, command=self.translate_left)
        self.transDistance = cmds.floatField(ed=True, v=1.0, precision=2, s=.25, w=40)
        cmds.button(label=">", width=40, bgc=white, command=self.translate_right)

        cmds.rowLayout(numberOfColumns=3, p=columnmain)
        cmds.text(label="", width=40)
        cmds.button(label="V", width=40, bgc=white, command=self.translate_down)
        cmds.text(label="", width=40)
        cmds.rowLayout(numberOfColumns=1, p=columnmain, height=5)

        # arrows button ends, Layout buttons begin
        ###############################################################
        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.button(label="Center", width=widthb, bgc=green, command=self.udim_center)
        cmds.button(label="Maximize", width=widthb, bgc=green, command=self.udim_max)

        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.button(label="Get TD", width=widthb, bgc=yellow, command=self.get_td)
        cmds.button(label="Set TD", width=widthb, bgc=yellow, command=self.set_td)

        cmds.rowLayout(numberOfColumns=3, p=columnmain)
        cmds.button(label="Stack", width=widthb, bgc=purple, command=self.stack_shells)
        cmds.button(label="U", width=widthc, bgc=purple, command=self.distribute_u)
        cmds.button(label="V", width=widthc, bgc=purple, command=self.distribute_v)

        cmds.rowLayout(numberOfColumns=1, p=columnmain)
        cmds.button(label="Layout", width=widthe, bgc=white,
                    command=self.layout_unfold3d)
        cmds.rowColumnLayout(numberOfColumns=2, p=columnmain)
        self.layoutScaleBox = cmds.checkBox(label="Scale", value=True)
        self.layoutRotateBox = cmds.checkBox(label="Rotate")

        # Layout button ends, UV edit buttons begin
        ###############################################################
        cmds.rowLayout(numberOfColumns=1, p=columnmain, height=6)

        cmds.rowLayout(numberOfColumns=3, p=columnmain)
        cmds.button(label="Unfold", width=widthb, bgc=blue, command=self.unfold_uv)
        cmds.button(label="U", width=widthc, bgc=blue, command=self.unfold_u)
        cmds.button(label="V", width=widthc, bgc=blue, command=self.unfold_v)

        cmds.rowLayout(numberOfColumns=3, p=columnmain)
        cmds.button(label="Straighten", width=widthb, bgc=red, command=self.straighten)
        cmds.button(label="U", width=widthc, bgc=red, command=self.straighten_u)
        cmds.button(label="V", width=widthc, bgc=red, command=self.straighten_v)

        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.button(label="Symmetry", width=widthb, bgc=yellow, command=self.symmetrize)
        cmds.button(label="Mirror", width=widthb, bgc=yellow, command=self.mirror)

        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.button(label="Grid", width=widthb, bgc=green, command=self.grid)
        cmds.button(label="CutSew", width=widthb, bgc=purple, command=self.cutsew3d)

        cmds.rowLayout(numberOfColumns=1, p=columnmain, height=4)

        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.text(label="Transfer UVs", width=90, align="left")
        cmds.rowLayout(numberOfColumns=2, p=columnmain)
        cmds.button(label="Topo", width=widthb, bgc=white, command=self.trans_uv_topo,
                    ann="Transfers UVs from the last selected object \
                        to the rest of your selected objects")
        cmds.button(label="World", width=widthb, bgc=white, command=self.trans_uv_world)
        # End
        ###############################################################

    def gather(self, *args):
        start_udim = self.get_udim()
        cmds.polyEditUV(u=-(start_udim[0]), v=-(start_udim[1]))
        self.udim_center()
        self.udim_max()

    def grid(self, *args):
        start_udim = self.get_udim()
        cmds.ConvertSelectionToFaces()
        sel = cmds.ls(sl=True)
        cmds.ConvertSelectionToUVs()
        mel.eval('polySelectBorderShell 0;')
        cmds.ShrinkPolygonSelectionRegion()
        if len(cmds.ls(sl=True))==0:
            cmds.error("Shell too simple. Use 'Unfold' instead")
        cmds.ConvertSelectionToEdges()
        cmds.InvertSelection()
        cutedges = cmds.ls(sl=True)
        cmds.polyForceUV(sel, uni=True)
        cmds.select(cutedges)
        cmds.InvertSelection()
        cmds.polyMapSewMove(cmds.ls(sl=True), nf=10, lps=0, ch=1)
        cmds.select(sel)
        mel.eval('polySelectBorderShell 0;')
        self.udim_center()
        self.udim_max()
        end_udim = self.get_udim()
        cmds.polyEditUV(u=(start_udim[0]-end_udim[0]), v=(start_udim[1]-end_udim[1]))
        mel.eval('texPivotCycle selection middle;')

    def rotate_left(self, *args):
        mel.eval('polyRotateUVs 45 1;')

    def rotate_right(self, *args):
        mel.eval('polyRotateUVs -45 1;')

    def translate_up(self, *args):
        cmds.polyEditUV(u=0, v=cmds.floatField(self.transDistance, q=True, v=True))
        mel.eval('texPivotCycle selection middle;')

    def translate_right(self, *args):
        cmds.polyEditUV(u=cmds.floatField(self.transDistance, q=True, v=True), v=0)
        mel.eval('texPivotCycle selection middle;')

    def translate_left(self, *args):
        cmds.polyEditUV(u=-(cmds.floatField(self.transDistance, q=True, v=True)), v=0)
        mel.eval('texPivotCycle selection middle;')

    def translate_down(self, *args):
        cmds.polyEditUV(u=0, v=-(cmds.floatField(self.transDistance, q=True, v=True)))
        mel.eval('texPivotCycle selection middle;')

    def stack_shells(self, *args):
        sel = cmds.ls(sl=True)
        mel.eval('texStackShells {};')
        cmds.select(sel)

    def orient_shells(self, *args):
        mel.eval('texOrientShells;')

    def get_td(self, *args):
        mel.eval('uvTkDoGetTexelDensity;')

    def set_td(self, *args):
        mel.eval('uvTkDoSetTexelDensity;')

    def udim_flip_u(self, *args):
        udim = self.get_udim()
        tilecenter = udim[0] + .5
        cmds.polyEditUV(pivotU=tilecenter, scaleU=-1)
        mel.eval('texPivotCycle selection middle;')

    def udim_flip_v(self, *args):
        udim = self.get_udim()
        tilecenter = udim[1] + .5
        cmds.polyEditUV(pivotV=tilecenter, scaleV=-1)
        mel.eval('texPivotCycle selection middle;')

    def udim_center(self, *args):
        center = self.get_center()
        udim = self.get_udim()
        utarget = udim[0] + .5  # find center of udim
        vtarget = udim[1] + .5
        cmds.polyEditUV(u=(utarget-center[0]), v=(vtarget-center[1]))
        mel.eval('texPivotCycle selection middle;')

    def udim_max(self, *args):
        center = self.get_center()
        uminmax, vminmax, = cmds.polyEvaluate(bc2=True)
        width = math.fabs(uminmax[0] - uminmax[1])
        height = math.fabs(vminmax[0] - vminmax[1])
        if width > height:
            factor = .98/width
        else:
            factor = .98/height
        cmds.polyEditUV(pivotU=center[0], pivotV=center[1], 
                        scaleV=factor, scaleU=factor)
        mel.eval('texPivotCycle selection middle;')

    def symmetrize(self, *args):
        udim = self.get_udim()
        cmds.setToolTo("texSymmetrizeUVContext")
        cmds.optionVar(fv=('polySymmetrizeUVAxisOffset', udim[0]+.5))

    def layout_unfold3d(self, *args):
        scale_on = cmds.checkBox(self.layoutScaleBox, q=True, value=True)
        rotate_on = cmds.checkBox(self.layoutRotateBox, q=True, value=True)
        start_udim = self.get_udim()
        if scale_on and rotate_on:
            cmds.u3dLayout(res=256, spc=0.007, mar=0.01, scl=1, rst=90)
            # ps determines tile margin

        elif scale_on and not rotate_on:
            # mar determines tile margin, spc is shell space
            cmds.u3dLayout(res=256, spc=0.007, mar=0.01, scl=1)

        elif rotate_on and not scale_on:
            cmds.u3dLayout(res=256, spc=0.007, mar=0.01, scl=0, rst=90)

        else:
            cmds.u3dLayout(res=256, spc=0.007, mar=0.01)

        cmds.polyEditUV(u=start_udim[0], v=start_udim[1])

    def unfold_uv(self, *args):
        cmds.u3dUnfold(ite=1, p=0, bi=1, tf=1, ms=128, rs=0)

    def unfold_u(self, *args):
        cmds.unfold(i=5000, ss=0.001, gb=0, gmb=0.5, pub=0, ps=0, oa=2, us=False)

    def unfold_v(self, *args):
        cmds.unfold(i=5000, ss=0.001, gb=0, gmb=0.5, pub=0, ps=0, oa=1, us=False)

    def straighten(self, *args):
        mel.eval('texStraightenUVs "UV" 30;')

    def straighten_u(self, *args):
        mel.eval('texStraightenUVs "U" 30;')

    def straighten_v(self, *args):
        mel.eval('texStraightenUVs "V" 30;')

    def cutsew3d(self, *args):
        mel.eval('SetCutSewUVTool;')

    def trans_uv_topo(self, *args):
        selection = cmds.ls(sl=True, o=True)
        reference = selection[0]
        selection.remove(reference)
        for i in selection:
            cmds.transferAttributes(reference, i, 
                                    transferNormals=0, 
                                    transferUVs=2,
                                    sampleSpace=5, 
                                    searchMethod=0)
            cmds.delete(i, ch=True)

    def trans_uv_world(self, *args):
        selection = cmds.ls(sl=True, o=True)
        reference = selection[0]
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
            cmds.delete(i, ch=True)

    def distribute_v(self, *args):
        startcenter = self.get_center()
        mel.eval('texDistributeShells(0, 0.01, "up", {});')
        end_center = self.get_center()
        print startcenter, end_center
        cmds.polyEditUV(u=(startcenter[0]-end_center[0]),
                        v=(startcenter[1]-end_center[1]))
        mel.eval('texPivotCycle selection middle;')

    def distribute_u(self, *args):
        start_center = self.get_center()
        mel.eval('texDistributeShells(0, 0.01, "right", {});')
        end_center = self.get_center()
        print start_center, end_center
        cmds.polyEditUV(u=(start_center[0]-end_center[0]),
                        v=(start_center[1]-end_center[1]))
        mel.eval('texPivotCycle selection middle;')

    def autoseams(self, *args):
        mel.eval('performPolyAutoSeamUV 0;')

    def get_udim(self):
        # tuple of two pairs in Python: ((xmin,xmax), (ymin,ymax))
        maxmin = cmds.polyEvaluate(bc2=True)
        u_avg = (maxmin[0][0] + maxmin[0][1])/2
        v_avg = (maxmin[1][0] + maxmin[1][1])/2
        u_tile = math.floor(u_avg)
        v_tile = math.floor(v_avg)
        udim_tuple = (u_tile, v_tile)
        return udim_tuple

    def get_center(self):
        # tuple of two pairs in Python: ((xmin,xmax), (ymin,ymax))
        maxmin = cmds.polyEvaluate(bc2=True)
        u_avg = (maxmin[0][0] + maxmin[0][1])/2
        v_avg = (maxmin[1][0] + maxmin[1][1])/2
        center_tuple = (u_avg, v_avg)
        return center_tuple

    def mirror(self, *args):
        cmds.ConvertSelectionToContainedFaces()
        selection = cmds.ls(sl=True)  # starting UVs
        objs = cmds.ls(sl=True, o=True)
        cmds.ConvertSelectionToContainedEdges()
        cmds.select(selection)
        mel.eval('textureWindowSelectConvert 4;')
        mel.eval('polySelectBorderShell 1;')
        cmds.ConvertSelectionToContainedEdges()
        shelledges = cmds.ls(sl=True, flatten=True)  # get border edge of UV shell

        cmds.select(selection)  # get selected faces
        mel.eval('PolySelectTraverse 1;')  # grow face selection
        cmds.ConvertSelectionToEdgePerimeter()  # grab selection perimeter
        # get border edge of user selection
        sel_perimeter = cmds.ls(sl=True, flatten=True)

        # get list of edges to sew, selection border edge that is NOT a shell edge
        sew_edges = [i for i in sel_perimeter if i not in shelledges]

        cmds.select(selection)  # select faces to run transfer Attributes
        mel.eval('textureWindowSelectConvert 4;')  # convert selection to UVs
        mel.eval('PolySelectTraverse 1;')  # grow selection without crossing UV borders
        cmds.ConvertSelectionToContainedFaces()

        start_udim = self.get_udim()
        cmds.transferAttributes(transferPositions=0, 
                                transferNormals=0, 
                                transferUVs=2, 
                                transferColors=0,
                                sampleSpace=0,
                                searchMethod=0,
                                searchScaleX=-1.0,
                                flipUVs=1,
                                colorBorders=1)
        end_udim = self.get_udim()

        # clean history and move back to original UDIM, sew edges
        cmds.delete(objs[0], ch=True)
        cmds.polyEditUV(u=(start_udim[0]-end_udim[0]), v=0)
        for i in sew_edges:
            cmds.polyMapSew(i)
        cmds.select(selection)
        mel.eval('BakeNonDefHistory;')
