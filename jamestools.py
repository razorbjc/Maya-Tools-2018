'''
Template class for docking a Qt widget to maya 2017+.
Author: Lior ben horin
12-1-2017
'''
import weakref
import os
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel
from shiboken2 import wrapInstance

import jc_smartcombine
import jc_uvui
import jc_smartextract
import jc_facecut
import jc_unsmooth
import jc_curvetube
import jc_replacetopo
import jc_remove_namespaces
import jc_imageplanetoggle
import jc_dualtoggle
import jc_camcliptoggle

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
        cmds.shelfButton(i="uvui_icon.png", c="import jc_uvui\njc_uvui.uvui().launch()")
        cmds.button(label="UV UI", w=bw, h=bh, c=self.uvui)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="facecut_icon.png", c="import jc_facecut\njc_facecut.facecut()")
        cmds.button(label="FaceCut", w=bw, h=bh, c=self.facecut)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="combine_icon.png", c="import jc_smartcombine\njc_smartcombine.smartcombine()")
        cmds.button(label="Smart Combine", w=bw, h=bh, c=self.smartcombine)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="duplicate_icon.png", c="import jc_smartextract\njc_smartextract.smartduplicate()")
        cmds.button(label="Smart Duplicate", w=bw, h=bh, c=self.smartduplicate)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="extract_icon.png", c="import jc_smartextract\njc_smartextract.smartextract()")
        cmds.button(label="Smart Extract", w=bw, h=bh, c=self.smartextract)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="curvetube_icon.png", c="import jc_curvetube\njc_curvetube.curvetube()")
        cmds.button(label="CurveTube", w=bw, h=bh, c=self.curvetube)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="unsmooth_icon.png", c="import jc_unsmooth\njc_unsmooth.unsmooth()")
        cmds.button(label="Unsmooth", w=bw, h=bh, c=self.unsmooth)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="replace_icon.png", c="import jc_replacetopo\njc_replacetopo.replacetopo().launch()")
        cmds.button(label="Replace Topology", w=bw, h=bh, c=self.replacetopo)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="nameSpace_icon.png",
                         c="import jc_remove_namespaces\njc_remove_namespaces.remove_namespaces()")
        cmds.button(label="Remove Namespaces", w=bw, h=bh, c=self.remove_namespaces)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="dualTog_icon.png", c=self.dualtoggle,
                         doubleClickCommand="import jc_dualtoggle\njc_dualtoggle.jc_dualtoggle_off()")
        cmds.button(label="Dual Toggle", w=bw, h=bh, c=self.dualtoggle)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="camTog_icon.png",
                         c="import jc_imageplanetoggle\njc_imageplanetoggle.imageplanetoggle()")
        cmds.button(label="Imageplane Toggle", w=bw, h=bh, command=self.imageplanetoggle)
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent=main_column)
        cmds.shelfButton(i="clipToggle_icon.png",
                         c="import jc_camcliptoggle\njc_camcliptoggle.camcliptoggle()")
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
        jc_smartcombine.smartcombine()

    def smartextract(self, *args):
        jc_smartextract.smartextract()

    def smartduplicate(self, *args):
        jc_smartextract.smartduplicate()

    def facecut(self, *args):
        jc_facecut.facecut()

    def uvui(self, *args):
        jc_uvui.uvui().launch()

    def unsmooth(self, *args):
        jc_unsmooth.unsmooth()

    def curvetube(self, *args):
        jc_curvetube.curvetube()

    def replacetopo(self, *args):
        jc_replacetopo.replacetopo().launch()

    def remove_namespaces(self, *args):
        jc_remove_namespaces.remove_namespaces()

    def imageplanetoggle(self, *args):
        jc_imageplanetoggle.imageplanetoggle()

    def dualtoggle(self, *args):
        jc_dualtoggle.dualtoggle_on()

    def camcliptoggle(self, *args):
        jc_camcliptoggle.camcliptoggle()

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
