#!/usr/bin/env python2.7
import maya.cmds as mc
import maya.mel as mel


def launchQuadPatch(arg=None):
    import quadPatch2018 as quadPatcher
    quadPatcher.quadPatchUI()


def launchMuscleTools(arg=None):
    import muscleTools as muscleTools
    reload(muscleTools)


def launchPerfectRib(arg=None):
    import perfectRib as perfectRib
    reload(perfectRib)


def launchMuscleTransfer(arg=None):
    import transferMuscle as transferMuscle
    reload(transferMuscle)


def launchUnCollide(arg=None):
    import collisionByBool as collisionByBool
    reload(collisionByBool)


def launchSnapVertices(arg=None):
    import snapToClosestMesh as snapToClosestMesh
    reload(snapToClosestMesh)


def launchFilterBySel(arg=None):
    import filterBySelection as filterBySelection
    reload(filterBySelection)


def launchMultiReplacer(arg=None):
    import multiReplaceObjects as multiReplacer
    multiReplacer.multiReplaceUI()


def launchCustomLattice(arg=None):
    import customLattice
    customLattice.customLatticeUI()


def exeSetOrientToComponent(arg=None):
    import setOrientToComponent as exOtc
    reload(exOtc)


def exeStraightenVertices(arg=None):
    import straightenVertices as exSV
    reload(exSV)


def exeDistributeVertices(arg=None):
    import distributeVertices
    distributeVertices.checkSelection()


def exeCheckUDIMS(arg=None):
    import checkUVcrossingUDIM
    checkUVcrossingUDIM.checkMayaVersion()


def QstraightenVertices(arg=None):
    mc.confirmDialog(m='Select continuous edges or vertices and run Script to make them into straight line evenly spaced out.  Order of selection matters.  This tool needs reordering script in case selection was not in order.', b='Close')


def QsetOrientToComponent(arg=None):
    mc.confirmDialog(m="Select a face, edge, or vertex and run script to fix the object's orientation to selected component normal", b='Close')


def QDistributeVertices(arg=None):
    mc.confirmDialog(m='Select either an Edge Loop or an Edge Ring and then run script to distribute verticies evenly', b='Close')


def QCheckUDIMS(arg=None):
    mc.confirmDialog(m='Check UVs that are crossing UDIM borders.\nSelect objects then run script or select none to check all objects.', b='Close')


def assetToolsGUI():

    if mc.dockControl("asset_tools_Collection_dock",exists=True):
        mc.deleteUI("asset_tools_Collection_dock")

    dock_ui = mc.window ("toshi_tools_gui",widthHeight=(200,150),
                              title="Asset Tools Collections",iconName="Asset Tools Collections",
                              resizeToFitChildren=True,minimizeButton=True)
    form = mc.formLayout()
    tabs = mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    mc.formLayout( form, edit=True, attachForm=( (tabs, 'top', 0), (tabs, 'left', 0),
                                                 (tabs, 'bottom', 0), (tabs, 'right', 0) ) )
    allowedAreas = ['right','left'];
    mc.dockControl("asset_tools_Collection_dock",area='left',content=dock_ui,allowedArea=allowedAreas,label='ASSET TOOLS COLLECTION',visible=True)
    assets_tab_1 = mc.rowColumnLayout(numberOfColumns=1, rs=(10, 10))
    mc.button(label="Quad Patch", h=30, command=launchQuadPatch)
    mc.button(l='Muscle Tools', h=30, c=launchMuscleTools)
    mc.button(l='Muscle Transfer', h=30, c=launchMuscleTransfer)
    mc.button(l='Uncollide', h=30, c=launchUnCollide)
    mc.button(l='Snap Vertices', h=30, c=launchSnapVertices)
    mc.button(l='Filter By Selection', h=30, c=launchFilterBySel)
    mc.button(l='Multi Replacer', h=30, c=launchMultiReplacer)
    mc.button(l='Custom Lattice', h=30, c=launchCustomLattice)
    mc.setParent('..')

    assets_tab_2 = mc.rowColumnLayout(numberOfColumns=3)
    mc.button(l='Set Orient To Component', h=30, c=exeSetOrientToComponent)
    mc.text('  ')
    mc.button(l=' ? ', c=QsetOrientToComponent)
    
    mc.button(l='Straighten Vertices', h=30, c=exeStraightenVertices)
    mc.text('  ')
    mc.button(l=' ? ', c=QstraightenVertices)

    mc.button(l='Distribute Vertices', h=30, c=exeDistributeVertices)
    mc.text('  ')
    mc.button(l=' ? ', c=QDistributeVertices)

    mc.button(l='Check UDIM Borders', h=30, c=exeCheckUDIMS)
    mc.text('  ')
    mc.button(l=' ? ', c=QCheckUDIMS)
    mc.setParent('..')

    # assets_tab_3 = mc.rowColumnLayout(numberOfColumns=1)
    # mc.setParent('..')

    # mc.tabLayout(tabs, edit=True, tabLabel=((assets_tab_1, 'Model Tools'), (assets_tab_2, 'Simple Scripts'), (assets_tab_3, 'Beta Testing')))
    mc.tabLayout(tabs, edit=True, tabLabel=((assets_tab_1, 'Model Tools'), (assets_tab_2, 'Simple Scripts')))


if __name__ == '__main__':
    assetToolsGUI()
