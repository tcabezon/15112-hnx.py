from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math
from functions import *



class Ring(object):
    def __init__(self,innerDiameter,ringRadious,cx=0,cy=0,cz=0,stepU=8,stepV=8,stepCircunference=8,stepRing=8):
        self.innerDiameter=innerDiameter
        self.innerRadious=innerDiameter/2
        self.ringRadious=ringRadious
        self.ringStepRadious=stepU 
        self.stepV=stepV
        self.center=[cx,cy,cz]
        self.stepCircunference=stepCircunference
        self.stepRing=stepRing
        self.elements=[]
        self.vertices,self.faces=self.generateRing()
        self.points2D=threeDtotwoD(self.vertices)
        self.mesh=self.ringMesh()

    def generateRing(self):
        #circunference that will be rotated
        circunference=self.generateCircunference()
        stepV=self.stepCircunference
        stepU=self.stepRing
        
        verticesRing=np.zeros((((stepV)*(stepU)),3))
        facesRing=np.zeros((((stepV)*(stepU))*2,3), dtype=int)

        for v in range(len(circunference)):
            for u in range(stepU):
                #add points to the verticesRing matrix
                indexInMatrix= v*(stepU)+u
                angle=2*math.pi/stepU*u
                r=circunference[v][2]
                verticesRing[indexInMatrix,0]=circunference[v][0]
                verticesRing[indexInMatrix,1]=r*math.cos(angle)
                verticesRing[indexInMatrix,2]=r*math.sin(angle)
                
                #add faces to the facesRing matrix
                if v!=0:
                    #top triangle
                    facesIndexTop= (v-1)*(2*stepU)+stepU+u
                    facesRing[facesIndexTop,0]= (v*(stepU)+u)
                    facesRing[facesIndexTop,1]= ((v-1)*(stepU)+(u+1)%stepU)
                    facesRing[facesIndexTop,2]= ((v-1)*(stepU)+u)
                    

                    #bottom triangle
                    facesIndexBottom= (v-1)*(2*stepU)+u
                    facesRing[facesIndexBottom,0]= (v*(stepU)+u)
                    facesRing[facesIndexBottom,1]= ((v)*(stepU)+(u+1)%stepU)
                    facesRing[facesIndexBottom,2]= ((v-1)*(stepU)+(u+1)%stepU)

                else:
                    facesIndexTop= (v-1)*(2*stepU)+stepU+u
                    facesRing[facesIndexTop,0]= (v*(stepU)+u)
                    facesRing[facesIndexTop,1]= ((v-1)*(stepU)+(u+1)%stepU)
                    facesRing[facesIndexTop,2]= ((v-1)*(stepU)+u)
                    

                    #bottom triangle
                    facesIndexBottom= (v-1)*(2*stepU)+u
                    facesRing[facesIndexBottom,0]= (v*(stepU)+u)
                    facesRing[facesIndexBottom,1]= ((v)*(stepU)+(u+1)%stepU)
                    facesRing[facesIndexBottom,2]= ((v-1)*(stepU)+(u+1)%stepU)

        #some of the faces use negative indexing, the faces that connect the first points of the rotation with the last. We have to use the positive notation so there are no problems afterwards,when merging elements
        for faceIndex in range(len(facesRing)):
            for i in range(len(facesRing[faceIndex])):
                if  facesRing[faceIndex][i]<0: facesRing[faceIndex][i]+=len(verticesRing)

        return verticesRing,facesRing

        
        

    def generateCircunference(self):
        circunferencePoints=np.zeros((self.stepCircunference,3))

        for i in range(self.stepCircunference):
            beta=2*math.pi/self.stepCircunference*i
            circunferencePoints[i][0]=self.center[0]+self.ringRadious*math.cos(beta)
            circunferencePoints[i][1]=self.center[1]
            circunferencePoints[i][2]=self.center[2]+self.innerDiameter/2+self.ringRadious+self.ringRadious*math.sin(beta)

        print(circunferencePoints)
        return circunferencePoints


    def ringMesh(self):
        verticesRing=self.vertices
        facesRing=self.faces
        # Create the mesh
        #this function uses the numpy stl library mesh function (from stl import mesh)
        RingMesh = mesh.Mesh(np.zeros(facesRing.shape[0], dtype=mesh.Mesh.dtype))

        for i, f in enumerate(facesRing):
            for j in range(3):
                #print(i,j,f,cube.vectors[i][j])
                RingMesh.vectors[i][j] = verticesRing[f[j],:]
                #print(cube.vectors[i][j])

        #print(facesRing)
        return RingMesh

    def addElement(self,other):
        # the indexes of the faces in the second element must be updated
        addingFaces=other.faces+self.vertices.shape[0]
        self.vertices=np.concatenate((self.vertices, other.vertices), axis=0)
        self.faces=np.concatenate((self.faces, addingFaces), axis=0)
        self.points2D=threeDtotwoD(self.vertices)
        self.mesh=self.ringMesh()
        







