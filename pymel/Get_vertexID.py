import maya.cmds as cmds
import maya.api.OpenMaya as om
import operator

def getClosestVertex(mesh, pos=(0,0,0)):
    pos = om.MPoint(pos)
    sel = om.MSelectionList()
    sel.add(mesh)
    fn_mesh = om.MFnMesh(sel.getDagPath(0))
     
    index = fn_mesh.getClosestPoint(pos, space=om.MSpace.kWorld)[1]  # closest polygon index    
    face_vertices = fn_mesh.getPolygonVertices(index)  # get polygon vertices
        
    vertex_distances = ((vertex, fn_mesh.getPoint(vertex, om.MSpace.kWorld).distanceTo(pos)) 
                       for vertex in face_vertices)
    return min(vertex_distances, key=operator.itemgetter(1))


class ReJoint:
    def __init__(self):
        self.myWindow = cmds.window(title='가까운 버텍스ID 찾기')
    
        cmds.frameLayout (l="Mesh",w=400 )
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(20, 20))
        
        cmds.button(label='Select Object',h=40,w=200,c=self.object_point)
        name = cmds.textField("nameOfTexFld", tx="none",w=200)    
        
       
          
        cmds.setParent('..') 
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(20, 20))
            
        cmds.button(label='Mesh',h=40,w=200,c=self.mesh)
        name3 = cmds.textField("nameOfTexFld2", tx="none",w=200)    


            
        cmds.setParent('..')
        
        
                
        cmds.button(label='!!!select vertexID!!!',h=40,w=200,c=self.ReTarget)
        cmds.showWindow(self.myWindow)
   
    
  
    
    def ReTarget(self,args):
        cmds.select( clear=True )


       
        for i in range(0,len(self.name1)):
            
            cmds.pointConstraint( self.name1[i] , "cpConstraintIn")
            cmds.delete("cpConstraintIn_pointConstraint1")
    
            xformPos = cmds.xform("cpConstraintIn",q=True, objectSpace=True, t=True)
        
            a=getClosestVertex(self.name2,pos=[xformPos[0],xformPos[1],xformPos[2]])
            
            b = str(a[0])

            
            cmds.select(self.name2 + '.vtx['+b+']',add=True)
            print(self.name2 + '.vtx['+b+']')


        


    def object_point(self,args):
        a = cmds.ls( sl=True)
        cmds.textField("nameOfTexFld", edit=True, tx=str(a))
        self.name1 =a

        
    def mesh(self,args):
        b = cmds.ls( sl=True)
        cmds.textField("nameOfTexFld2", edit=True, tx=b[0])
        self.name2 =b[0]
        

        
    

                

ReJoint()