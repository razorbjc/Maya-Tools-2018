'''
Template class for docking a Qt widget to maya 2017+.
Author: Lior ben horin
12-1-2017
'''

import weakref
import os
import maya.cmds as cmds
import maya.OpenMayaUI as omui
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

        buth = 24
        butw = 140
        mainColumn=cmds.columnLayout( adjustableColumn=True)
        cmds.rowLayout(numberOfColumns=2, parent = mainColumn)
        cmds.text(label="", width=65)
        cmds.symbolButton( image=os.path.join(USERAPPDIR, "\icons\jtools_icon.png"),
                           w=48,
                           h=48)

#######################################################################

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="uvui_icon.png", command=self.uvui)
        cmds.button(label="UV UI", w=butw, h=buth, ann="fuck you", command=self.uvui)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="facecut_icon.png", command=self.facecut)
        cmds.button(label="FaceCut", w=butw, h=buth, ann="fuck you", command=self.facecut)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="combine_icon.png", command=self.smartcombine)
        cmds.button(label="Smart Combine", w=butw, h=buth, ann="fuck you", command=self.smartcombine)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="duplicate_icon.png", command=self.smartduplicate)
        cmds.button(label="Smart Duplicate", w=butw, h=buth, ann="fuck you", command=self.smartduplicate)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="extract_icon.png", command=self.smartextract)
        cmds.button(label="Smart Extract", w=butw, h=buth, ann="fuck you", command=self.smartextract)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="curvetube_icon.png", command=self.curvetube)
        cmds.button(label="CurveTube", w=butw, h=buth, ann="fuck you", command=self.curvetube)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="unsmooth_icon.png", command=self.unsmooth)
        cmds.button(label="Unsmooth", w=butw, h=buth, ann="fuck you", command=self.unsmooth)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="replace_icon.png", command=self.replacetopo)
        cmds.button(label="Replace Topology", w=butw, h=buth, ann="fuck you", command=self.replacetopo)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="nameSpace_icon.png", command=self.remove_namespaces)
        cmds.button(label="Remove Namespaces", w=butw, h=buth, ann="fuck you", command=self.remove_namespaces)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="dualTog_icon.png", command=self.dualtoggle)
        cmds.button(label="Dual Toggle", w=butw, h=buth, ann="fuck you", command=self.dualtoggle)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="camTog_icon.png", command=self.imageplanetoggle)
        cmds.button(label="Imageplane Toggle", w=butw, h=buth, ann="fuck you", command=self.imageplanetoggle)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", parent = mainColumn)
        cmds.shelfButton(image="clipToggle_icon.png", command=self.imageplanetoggle)
        cmds.button(label="CamClip Toggle", w=butw, h=buth, ann="fuck you", command=self.imageplanetoggle)

#######################################################################

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
