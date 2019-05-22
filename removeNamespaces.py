#!/usr/bin/env python2.7

"""
for Maya 2016/2018
Removes all namespaces. May need to be run multiple times for stacked namespaces

__author__: James Chan
"""

import maya.cmds as cmds


def removeNamespaces():
    cmds.namespace(setNamespace=':')
    namespaces_all = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    if namespaces_all:
        namespaces_all.remove("UI")
        namespaces_all.remove("shared")
    for i in namespaces_all:
        cmds.namespace(removeNamespace=i, mergeNamespaceWithRoot=True)
