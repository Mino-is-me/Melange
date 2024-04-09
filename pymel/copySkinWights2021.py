import maya.cmds as cmds

def copySkin():
    objects=cmds.ls(sl=True)
    findSkinCluster=cmds.listHistory(objects[0],pdo=1,il=2)
    oldSkincluster=cmds.ls(findSkinCluster,typ='skinCluster')
    

    for e in objects:
        if e == objects[0]:
            pass
        else:
            shapeHistory = cmds.listHistory(e, lv = 2)
            oldSkc=cmds.ls(shapeHistory,typ='skinCluster') # test if there is a skincluster on new geo already
            if oldSkc:
                cmds.delete(oldSkc)
                #print 'deleted existing skincluster on '+ e
            jnt=cmds.skinCluster(oldSkincluster,weightedInfluence=True,q=True)
            cmds.select(jnt)
            #newSkc=cmds.skinCluster(jnt, e, tsb=True)[0]
            newSkc=cmds.skinCluster(jnt, e, tsb=True, mi = 40, omi = True)[0] # max influences
            cmds.copySkinWeights( ss=oldSkincluster[0], ds=newSkc, nm=True,surfaceAssociation='closestPoint')
            cmds.rename(newSkc,oldSkincluster[0])

copySkin()