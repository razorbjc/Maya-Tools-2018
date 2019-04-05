#!/usr/bin/env python2.7

"""
TODO: Add script docstring here...

__author__: James Chan
"""

import maya.cmds as cmds
import maya.mel as mel
import math


class replaceTopo(object):
    windowName = "replaceTopo"

    def __init__(self):
        self.newMesh= "None"
        self.oldMesh = "None"
        self.oldTargets = "None"
        self.replaceFlag = False

    def launch(self):
        # checks if window is already open, closes and recreates if it is
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName, title="Replace By Topology", minimizeButton=False,
                    maximizeButton=False, sizeable=False, rtf=True, w=200, h=100)

        if cmds.windowPref(self.windowName, e=True):
            cmds.windowPref(self.windowName, remove=True)
        self.buildUI()
        cmds.showWindow()

    # builds layout and buttons, hooks up to commands
    def buildUI(self):
        widtha = 75
        widthb = 130
        widthc = 29
        white = [1,1,1]
        red = [.9,.5,.5]
        blue = [.5,.75,.9]
        green = [.4, .75, .4]
        yellow = [.9,.85,.45]
        orange = [.8,.3,.4]
        purple = [.6,.5,.8]

        columnMain = cmds.columnLayout(columnWidth=200, cal="center")

        cmds.rowLayout(numberOfColumns=3, columnAlign1="center", p=columnMain)
        cmds.button(label="New Mesh", width=widtha, command=self.setNewMesh)
        cmds.text(label="", w=1)
        self.newMeshDisplay=cmds.text(label=self.newMesh, width=widthb, align="left")

        cmds.rowLayout(numberOfColumns=3, columnAlign1="center", p=columnMain)
        cmds.button(label="Old Mesh", width=widtha, command=self.setOldMesh)
        cmds.text(label="", w=1)
        self.oldMeshDisplay=cmds.text(label=self.oldMesh, width=widthb, align="left")

        cmds.rowLayout(numberOfColumns=3, columnAlign1="center", p=columnMain)
        cmds.button(label="Old Targets", width=widtha, command=self.setOldTargets)
        cmds.text(label="", w=1)
        self.oldTargetsDisplay=cmds.text(label=self.oldTargets, width=widthb, 
                                         align="left")

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", p=columnMain, h=5)
        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", p=columnMain)
        cmds.radioCollection()
        cmds.radioButton( label='New Group', select=True, onc=self.replaceFlagOff)
        cmds.radioButton( label='Replace Targets', onc=self.replaceFlagOn )

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", p=columnMain, h=5)

        cmds.rowLayout(numberOfColumns=1, columnAlign1="center", p=columnMain)
        cmds.button(label="Run!", width=210, bgc=white, command=self.runWrapBlend)

    def setNewMesh(self, *args):
        selection = cmds.ls(sl=True, transforms=True, long=True)
        self.newMesh = selection[0]
        shortName = selection[0].split("|")[-1]
        print ("addNewSource = " + self.newMesh)
        cmds.text(self.newMeshDisplay, e=True, label=shortName)

    def setOldMesh(self, *args):
        selection = cmds.ls(sl=True, transforms=True, long=True)
        self.oldMesh = selection[0]
        shortName = selection[0].split("|")[-1]
        print ("oldSource = " + self.oldMesh)
        cmds.text(self.oldMeshDisplay, e=True, label=shortName)

    def setOldTargets(self, *args):
        selection = cmds.ls(sl=True, dag=True, transforms=True, 
                            objectsOnly=True, long=True)
        self.oldTargets = selection
        self.groupBank = []
        displayList = []
        finalString = ""

        # put all the oldTargets into displayList for GUI
        displayList = [i for i in self.oldTargets]

        # search for groups in oldTargets and add them to groupBank[]
        self.groupBank = [i for i in self.oldTargets if self.is_group(i)]
        # for i in self.oldTargets:
        #     if (self.is_group(i)):
        #         self.groupBank.append(i)

        # remove groups from oldTargets
        for i in self.groupBank:
            childTransforms = cmds.listRelatives(i, ad=True, type="transform", 
                                                 f=True, pa=True)
            for j in self.groupBank:
                if not childTransforms:
                    continue
                if j in childTransforms:
                    if j in displayList:
                        displayList.remove(j)

            self.oldTargets.remove(i)

        # if some groups are descendants of other groups, 
        # remove them from displayList
        for i in self.oldTargets:
            if (self.is_child(i)):
                displayList.remove(i)

        # convert displayList into string of short names to display in window
        for i in displayList:
            shortName = i.split("|")[-1]
            finalString = finalString + shortName + " "

        print "Final Display:"
        print displayList
        print "Final oldTargs:"
        print self.oldTargets
        cmds.text(self.oldTargetsDisplay, e=True, label=finalString)

    def runWrapBlend(self, *args):
        print ("addNewSource = %s " % self.newMesh)
        print ("oldSource = %s" % self.oldMesh)
        print ("oldTargets = %s" % str(self.oldTargets))
        self.newGroup = None
        self.errorCheck()
        self.cleanMeshes()

        print "Running WrapBS!"
        if not self.replaceFlag:
            self.newGroup = cmds.group(em=True, name="replaceTopo_GRP")

        # Create wrap deformer
        cmds.select(self.newMesh)
        cmds.select(self.oldMesh, add=True)
        self.wrapName = mel.eval('doWrapArgList "2" { "1","0","1" }')

        for target in self.oldTargets:
            if target == self.oldMesh:
                # if oldMesh is among targets, handle separately
                self.oldMeshIsTarget(target)
                continue
            #create blendshape, get blendshape name and target name
            blendName = cmds.blendShape(target, self.oldMesh, o='world')
            noGroupName = target.split("|")[-1] # get shortname
            shortName = noGroupName.split(":")[-1] # remove namepace from name
            blendString = (blendName[0].encode('ascii','ignore')).decode("utf-8")

            # blend to target, duplicate newshape, parent duplicate to new group, and
            # blend back to oldMesh position
            cmds.setAttr(blendString + "." + shortName, 1)
            created = cmds.duplicate(self.newMesh)

            if self.replaceFlag:
                currentParent = cmds.listRelatives(target, p=True, pa=True, f=True)
                print currentParent
                if currentParent is not None:
                    cmds.parent(created, currentParent[0])
                    print "parented to %s" % currentParent[0]
                cmds.delete(target)

            else:
                cmds.parent(created, self.newGroup)
            cmds.setAttr(blendString + "." + shortName, 0)

            relatives = cmds.listRelatives(created, c=True)
            # delete left-over wrapdeform shape node
            cmds.delete(relatives[-1])
            # rename newly created duplicate to old target's name
            newname = cmds.rename(created, noGroupName)
            cmds.select(newname)

        cmds.delete(self.wrapName)
        cmds.delete(self.oldMesh, all=True, constructionHistory=True)
        # cmds.delete(self.newMesh, all=True, constructionHistory=True)
        if (self.newGroup):
            cmds.select(self.newGroup)

    def is_group(self, node=None):
        print "entering is_group"
        print node
        children = cmds.listRelatives(node, c=True, pa=True, f=True)
        if children == None:
            return True
        for c in children:
            if cmds.nodeType(c) == 'mesh':
                return False
        else:
            return True

    def is_child(self, node=None):
        if node == None:
            node = cmds.ls(selection=True)[0]

        if cmds.nodeType(node) != "transform":
            return False

        parent = cmds.listRelatives(node, p=True)
        if (parent):
            print parent[0]
            i = 0
            while i < len(self.groupBank):
                if parent[0] in str(self.groupBank[i]):
                    return True
                i=i+1
        return False

    def cleanMeshes(self, *args):
        currentSelection = cmds.ls(sl=True)
        cmds.select(self.newMesh)
        # cmds.select(self.oldMesh, add=True)
        # cmds.select(self.oldTargets, add=True)
        mel.eval('FreezeTransformations;')
        mel.eval('ResetTransformations;')
        #mel.eval('DeleteHistory;')

    def errorCheck(self, *args):
        # check if meshes exist
        if (self.oldMesh == "None"):
            raise RuntimeError("You need to set the Old Mesh!")
        if (self.newMesh == "None"):
            raise RuntimeError("You need to set the New Mesh!")
        if (self.oldTargets == "None"):
            raise RuntimeError("You need to set Old Targets!")

        print "errorChecking"

        # check if all old targets have the same vertcount/topology 
        # as the selected old mesh
        vertcount = cmds.polyEvaluate(self.oldMesh, v=True)
        errorList = []
        for i in self.oldTargets:
            if cmds.polyEvaluate(i, v=True) != vertcount:
                errorList.append(i)
        if (errorList):
            cmds.select(errorList)
            raise RuntimeError("Selected Target does not match Old Mesh Topology!")


    def replaceFlagOn(self, *args):
        self.replaceFlag=True
        print "replaceON"

    def replaceFlagOff(self, *args):
        self.replaceFlag=False
        print "replaceOFF"

    def oldMeshIsTarget(self, target):
        # duplicate and continue to next target
        created = cmds.duplicate(self.newMesh)
        if self.replaceFlag==False:
            cmds.parent(created, self.newGroup)

        else:
            currentParent = cmds.listRelatives(target, p=True, pa=True, f=True)
            print currentParent
            if (currentParent):
                 cmds.parent(created, currentParent[0])
                 print "parented to %s" % currentParent[0]

        noGroupName = target.split("|")[-1]  # get shortname
        newname = cmds.rename(created, noGroupName)
