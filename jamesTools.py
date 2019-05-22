'''
for Maya 2018
Custom tools by James
'''
import weakref
import os
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel
from shiboken2 import wrapInstance

import smartCombine
import uvui
import smartExtract
import faceCut
import unsmooth
import curveTube
import replaceTopo
import removeNamespaces
import imagePlaneToggle
import dualToggle
import camClipToggle

from Qt import QtGui, QtWidgets, QtCore  # https://github.com/mottosso/Qt.py by Marcus Ottosson


def dock_window(dialog_class):
    try:
        cmds.deleteUI(dialog_class.CONTROL_NAME)
        logger.info('removed workspace {}'.format(dialog_class.CONTROL_NAME))

    except:
        pass

    # building the workspace control with maya.cmds
    main_control = cmds.workspaceControl(dialog_class.CONTROL_NAME,
                                         ttc=["AttributeEditor", -1],
                                         iw=190,
                                         mw=190,
                                         ih=530,
                                         wp='fixed',
                                         label=dialog_class.DOCK_LABEL_NAME)

    # now lets get a C++ pointer to it using OpenMaya
    control_widget = omui.MQtUtil.findControl(dialog_class.CONTROL_NAME)
    # conver the C++ pointer to Qt object we can use
    control_wrap = wrapInstance(long(control_widget), QtWidgets.QWidget)

    # control_wrap is the widget of the docking window and now we can start working with it:
    control_wrap.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    win = dialog_class(control_wrap)

    # after maya is ready we should restore the window since it may not be visible
    cmds.evalDeferred(lambda *args: cmds.workspaceControl(main_control, e=True, rs=True))

    # will return the class of the dock content.
    return win.run()


class MyDockingUI(QtWidgets.QWidget):

    instances = list()
    CONTROL_NAME = "James Tools"
    DOCK_LABEL_NAME = "James Tools"

    def __init__(self, parent=None):
        super(MyDockingUI, self).__init__(parent)

        # let's keep track of our docks so we only have one at a time.
        MyDockingUI.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))
        self.window_name = self.CONTROL_NAME
        self.ui = parent
        self.layout = parent.layout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.build_ui()

    def build_ui(self):
        USERAPPDIR = cmds.internalVar(userPrefDir=True)
        #  logopath = os.path.join(USERAPPDIR, "\icons\iconTest1.png")
        top_column = cmds.columnLayout(adjustableColumn=True)
        cmds.rowLayout(numberOfColumns=2, parent=top_column)
        cmds.text(label="", width=65)
        cmds.symbolButton(image="jtools_icon.png", w=48, h=48)
        cmds.setParent('..')

        form = cmds.formLayout()
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        cmds.formLayout(form, edit=True, attachForm=((tabs, 'top', 0),
                                                     (tabs, 'left', 0),
                                                     (tabs, 'bottom', 0),
                                                     (tabs, 'right', 0)))
        bh = 24
        bw = 140

#######################################################################
        main_column = cmds.columnLayout(adjustableColumn=True)
        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="uvui_icon.png", c="import uvui\nuvui.uvui().launch()")
        cmds.button(label="UV UI", w=bw, h=bh, c=self.uvui)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="facecut_icon.png", c="import faceCut\nfaceCut.faceCut()")
        cmds.button(label="FaceCut", w=bw, h=bh, c=self.facecut)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="combine_icon.png", c="import smartCombine\nsmartCombine.smartCombine()")
        cmds.button(label="Smart Combine", w=bw, h=bh, c=self.smartcombine)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="duplicate_icon.png", c="import smartExtract\nsmartExtract.smartDuplicate()")
        cmds.button(label="Smart Duplicate", w=bw, h=bh, c=self.smartduplicate)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="extract_icon.png", c="import smartExtract\nsmartExtract.smartExtract()")
        cmds.button(label="Smart Extract", w=bw, h=bh, c=self.smartextract)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="curvetube_icon.png", c="import curveTube\ncurveTube.curveTube()")
        cmds.button(label="CurveTube", w=bw, h=bh, c=self.curvetube)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="unsmooth_icon.png", c="import unsmooth\nunsmooth.unsmooth()")
        cmds.button(label="Unsmooth", w=bw, h=bh, c=self.unsmooth)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="replace_icon.png", c="import replaceTopo\nreplaceTopo.replaceTopo().launch()")
        cmds.button(label="Replace Topology", w=bw, h=bh, c=self.replacetopo)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="nameSpace_icon.png",
                         c="import removeNamespaces\nremoveNamespaces.removeNamespaces()")
        cmds.button(label="Remove Namespaces", w=bw, h=bh, c=self.remove_namespaces)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="dualTog_icon.png", c=self.dualtoggle,
                         doubleClickCommand="import dualToggle\ndualToggle.dualToggle_off()")
        cmds.button(label="Dual Toggle", w=bw, h=bh, c=self.dualtoggle)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="camTog_icon.png",
                         c="import imagePlaneToggle\nimagePlaneToggle.imagePlaneToggle()")
        cmds.button(label="Imageplane Toggle", w=bw, h=bh, command=self.imageplanetoggle)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="clipToggle_icon.png",
                         c="import camClipToggle\ncamClipToggle.camClipToggle()")
        cmds.button(label="Cam Clip Toggle", w=bw, h=bh, command=self.camcliptoggle)
        cmds.setParent('..')
        cmds.setParent('..')

#######################################################################
        maya_column = cmds.columnLayout(adjustableColumn=True)
        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=maya_column)
        cmds.shelfButton(i="commandButton.png", iol="selNth", stp='mel',
                         c='polySelectEdgesEveryN "edgeRing" 2;')
        cmds.button(label="Select Nth Edge", w=bw, h=bh, command=self.polysel_every_n)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=maya_column)
        cmds.shelfButton(i="commandButton.png", iol="mirCut", stp='mel',
                         c="polyMirrorCut 1 1 0.001;")
        cmds.button(label="polyMirrorCut", w=bw, h=bh, command=self.polymirrorcut)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=maya_column)
        cmds.shelfButton(i="commandButton.png", iol="remesh", stp='python',
                         c="cmds.polyRemesh()")
        cmds.button(label="polyRemesh", w=bw, h=bh, command=self.polyremesh)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=maya_column)
        cmds.shelfButton(i="commandButton.png", iol="retopo", stp='python',
                         c="cmds.polyRetopo()")
        cmds.button(label="polyRetopo", w=bw, h=bh, command=self.polyretopo)
        cmds.setParent('..')
        cmds.setParent('..')

#######################################################################
        cmds.tabLayout(tabs, edit=True, tabLabel=((main_column, 'Custom'), (maya_column, 'Maya')))

    def smartcombine(self, *args):
        smartCombine.smartCombine()

    def smartextract(self, *args):
        smartExtract.smartExtract()

    def smartduplicate(self, *args):
        smartExtract.smartDuplicate()

    def facecut(self, *args):
        faceCut.faceCut()

    def uvui(self, *args):
        uvui.uvui().launch()

    def unsmooth(self, *args):
        unsmooth.unsmooth()

    def curvetube(self, *args):
        curveTube.curveTube()

    def replacetopo(self, *args):
        replaceTopo.replaceTopo().launch()

    def remove_namespaces(self, *args):
        removeNamespaces.removeNamespaces()

    def imageplanetoggle(self, *args):
        imagePlaneToggle.imagePlaneToggle()

    def dualtoggle(self, *args):
        dualToggle.dualToggle_on()

    def camcliptoggle(self, *args):
        camClipToggle.camClipToggle()

    def polyretopo(self, *args):
        cmds.polyRetopo()

    def polyremesh(self, *args):
        cmds.polyRemesh()

    def polymirrorcut(self, *args):
        mel.eval('polyMirrorCut 1 1 0.001;')

    def polysel_every_n(self, *args):
        mel.eval('polySelectEdgesEveryN "edgeRing" 2;')

    @staticmethod
    def delete_instances():
        for ins in MyDockingUI.instances:
            logger.info('Delete {}'.format(ins))
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass

            MyDockingUI.instances.remove(ins)
            del ins

    def run(self):
        return self

# this is where we call the window
my_dock = dock_window(MyDockingUI)
