sel = cmds.ls(sl=True,fl=True)
obj = cmds.ls(sl=True,o=True)
name = cmds.listRelatives(obj,p=True)
dup = cmds.duplicate(obj)[0]
targetbb = cmds.xform(sel,q=True,bb=True)
chipoff = cmds.polyChipOff(ch=1, kft=1, dup=0)
separate = cmds.polySeparate(obj, rs=1, ch=1)
separate.pop()

print "chipoff:", chipoff
print "separate:", separate
print "bb:", targetbb

for i in separate:
    tempbb = cmds.xform(i,q=True,bb=True)
    print "tempbb:",tempbb
    if tempbb[0] == targetbb[0]:
        print "head is", i
        head = i
    else:
        print "body is", i
        body = i
print "head:", head
print "body:", body 
print "name:", name
print "dup:",dup

result = cmds.polyUnite(head, body, ch=True)[0]
mergenode = cmds.polyMergeVertex(result, d=0.001, am=1, ch=True)
print "result:", result
print "final:", mergenode

cmds.transferAttributes(dup, result, transferPositions=0, transferNormals=0, transferUVs=2, sourceUvSpace="map1", targetUvSpace="map1", sampleSpace=0, searchMethod=0)
cmds.delete(dup)
cmds.delete(result, ch=True)
cmds.rename(result, name)
