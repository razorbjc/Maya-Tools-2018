import maya.cmds as cmds

def jc_namespaceRemover():
    cmds.namespace(setNamespace=':')
    namespacesAll = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    if namespacesAll != None:
        namespacesAll.remove("UI")
        namespacesAll.remove("shared")
    for i in namespacesAll:
        cmds.namespace(removeNamespace=i, mergeNamespaceWithRoot=True)

jc_namespaceRemover()
