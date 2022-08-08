import maya.cmds as cmds
import maya.mel as mel


def polySet():
    selection = cmds.ls(sl=True)
    facecount_dict = {cmds.polyEvaluate(selection[0], f=True): [selection[0]]}
    del selection[0]
    for i in selection:
        current_facecount = cmds.polyEvaluate(i, f=True)
        if current_facecount not in facecount_dict.keys():
            facecount_dict[current_facecount] = [i]
        else:
            for j in facecount_dict.keys():
                if current_facecount == j:
                    facecount_dict[j].append(i)

    for i in facecount_dict.keys():
        cmds.select(facecount_dict[i])
        newSet = cmds.sets(n=("polycount_%s_faces" % i))

    cmds.select(newSet)

polySet()


