import maya.cmds as cmds
import maya.mel as mel
import math


class wrapBlend(object):
    windowName = "jc_wrapBlend_window"

    def __init__(self):
        self.newMesh= "None"
        self.oldMesh = "None"
        self.oldTargets = "None"
        self.oldTargetsString = "None"

    def buildWindow(self):
        # checks if window is already open, closes and recreates if it is
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName, title="jc_wrapBlend", minimizeButton=False,
                    maximizeButton=False, sizeable=True, rtf=True, w=200, h=100)

        if cmds.windowPref(self.windowName, e=True):
            cmds.windowPref(self.windowName, remove=True)
        self.buildUI()
        cmds.showWindow()

    # builds layout and buttons, hooks up to commands
    def buildUI(self):
        widtha = 65
        widthb = 135
        widthc = 29
        white = [1,1,1]
        red = [.9,.5,.5]
        blue = [.5,.75,.9]
        green = [.4, .75, .4]
        yellow = [.9,.85,.45]
        orange = [.8,.3,.4]
        purple = [.6,.5,.8]

        columnMain = cmds.columnLayout(columnWidth=200)

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", p=columnMain)
        cmds.button(label="New Mesh", width=widtha, command=self.setNewMesh)
        self.newMeshDisplay=cmds.text(label=self.newMesh, width=widthb, align="left")

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", p=columnMain)
        cmds.button(label="Old Mesh", width=widtha, command=self.setOldMesh)
        self.oldMeshDisplay=cmds.text(label=self.oldMesh, width=widthb, align="left")

        cmds.rowLayout(numberOfColumns=2, columnAlign1="center", p=columnMain)
        cmds.button(label="Old Targets", width=widtha, command=self.setOldTargets)
        self.oldTargetsDisplay=cmds.text(label=self.oldTargets, width=widthb, align="left")

        cmds.rowLayout(numberOfColumns=1, columnAlign1="center", p=columnMain)
        cmds.button(label="Run!", width=205, bgc=white, command=self.runWrapBlend)

    def setNewMesh(self, *args):
        selection = cmds.ls(sl=True)
        self.newMesh = selection[0]
        print ("addNewSource = " + self.newMesh)
        cmds.text(self.newMeshDisplay, e=True, label=self.newMesh)

    def setOldMesh(self, *args):
        selection = cmds.ls(sl=True)
        self.oldMesh = selection[0]
        print ("oldSource = " + self.oldMesh)
        cmds.text(self.oldMeshDisplay, e=True, label=self.oldMesh)

    def setOldTargets(self, *args):
        selection = cmds.ls(sl=True, dag=True, transforms=True, objectsOnly=True, long=True)
        self.oldTargets = selection
        print self.oldTargets
        stringDisplay=""
        # detect groups


        for i in self.oldTargets:
            if (self.is_group(i)):
                print "detected that %s is a group" % (i)
                print "removing from oldTargets..."
                self.oldTargets.remove(i)
                continue
            else:
                shortName = str(i.split("|")[-1])
                stringDisplay = stringDisplay + shortName +", "

        print "real oldTargs:"
        print self.oldTargets
        cmds.text(self.oldTargetsDisplay, e=True, label=stringDisplay)

    def runWrapBlend(self, *args):
        print ("addNewSource = " + self.newMesh)
        print ("oldSource = " + self.oldMesh)
        print ("oldTargets = " + str(self.oldTargets))
        target = None
        self.newGroup = cmds.group(em=True, name="wrapBlend_GRP")
        blendName = None

        self.cleanMeshes()
        print "runWrapBlend self.TargetVertices: "+ str(self.targetVertices)
        print "Running WrapBS!"

        cmds.select(self.newMesh)
        cmds.select(self.oldMesh, add=True)
        selected = cmds.ls(sl=True)
        print selected
        self.wrapName = mel.eval('doWrapArgList "2" { "1","0","1" }')
        print "name of wrap node: " + self.wrapName[0]
        print "loop begins"
        for target in self.oldTargets:
            cmds.select(target)
            cmds.select(self.oldMesh, add=True)
            print "selected: "+str(target)+" and "+str(self.oldMesh)
            blendName = mel.eval('blendShape;')
            print blendName[0]
            shortName = target.split("|")[-1]
            print blendName[0] + "." + shortName
            newString = (blendName[0].encode('ascii','ignore')).decode("utf-8")
            print newString
            cmds.setAttr(newString + "." + shortName, 1)
            created = cmds.duplicate(self.newMesh)
            cmds.parent(created, self.newGroup)
            cmds.setAttr(newString + "." + shortName, 0)
            newname = cmds.rename(created, shortName)
            garbageString = str((newname)+"ShapeOrig")
            cmds.delete(garbageString.split("|")[-1])
            print (garbageString.split("|")[-1])
            # print "new name: "
            # print created
            # print "will be renamed to "
            # print shortName

            # print newname
            # print newString + "." + shortName


        cmds.delete(self.wrapName)
        cmds.delete(self.oldMesh, all=True, constructionHistory=True)
        cmds.delete(self.newMesh, all=True, constructionHistory=True)


    def is_group(self, node=None):
        print "entering is_group"
        print node
        if node == None:
            node = cmds.ls(selection=True)[0]
        if cmds.nodeType(node) != "transform":
            return False

        children = cmds.listRelatives(node, c=True)

        if children == None:
            return True

        for c in children:
            if cmds.nodeType(c) != 'transform':
                return False
        else:
            return True


    def cleanMeshes(self, *args):
        ## "Checking for same vertCount on all of Old Targets"
        ## Freeze/Reset Tranforms + Delete History"
        self.targetVertices = cmds.polyEvaluate(self.oldMesh, vertex=True)
        print self.targetVertices







