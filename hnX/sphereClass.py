from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math
from hnXfunctions import *


class Sphere(object):
    def __init__(self,r,cx=0,cy=0,cz=0,stepU=8,stepV=8):
        self.r=r
        self.cx=cx
        self.cy=cy
        self.cz=cz
        self.center=[cx,cy,cz]
        self.stepU=stepU 
        self.stepV=stepV
        self.vertices,self.faces=self.sphereVerticesAndFaces()
        self.points2D=threeDtotwoD(self.vertices)


    def sphereVerticesAndFaces(self):
        r=self.r
        stepV=self.stepV
        stepU=self.stepU
        center=self.center
        #stepU xy plane divisions
        # stepV z axisdivisions

        #generate 'body'
        pointsSphere=np.zeros((((stepV-1)*(stepU)),3))
        facesSphere=np.zeros((((stepV-2)*(stepU))*2,3), dtype=int)

        for row, v in enumerate(rangeNumberSteps(math.pi/stepV,
                                                    math.pi-(math.pi/stepV),stepV-2)):
            for col, u in enumerate(rangeNumberSteps(0,2*math.pi-(2*math.pi/stepU)
                                                            ,stepU-1)):
                
                #add points to the pointsSphere matrix
                indexInMatrix= row*(stepU)+col
                pointsSphere[indexInMatrix,0]=center[0]+r*math.sin(v)*math.cos(u)
                pointsSphere[indexInMatrix,1]=center[1]+r*math.sin(v)*math.sin(u)
                pointsSphere[indexInMatrix,2]=center[2]+r*math.cos(v)
                
                #add faces to the facesSphere matrix
                if row!=0:
                    #top triangle
                    facesIndexTop= (row-1)*(2*stepU)+stepU+col
                    facesSphere[facesIndexTop,0]= (row*(stepU)+col)
                    facesSphere[facesIndexTop,1]= ((row-1)*(stepU)+(col+1)%stepU)
                    facesSphere[facesIndexTop,2]= ((row-1)*(stepU)+col)
                    

                    #bottom triangle
                    facesIndexBottom= (row-1)*(2*stepU)+col
                    facesSphere[facesIndexBottom,0]= (row*(stepU)+col)
                    facesSphere[facesIndexBottom,1]= ((row)*(stepU)+(col+1)%stepU)
                    facesSphere[facesIndexBottom,2]= ((row-1)*(stepU)+(col+1)%stepU)

        #generate top and bottom vertex of the sphere
        topVertexSphere=np.array([[center[0],center[1],center[2]+r]])
        bottomVertexSphere=np.array([[center[0],center[1],center[2]-r]])
        #generate top and bottom faces of the sphere
        topFacesSphere=np.zeros((stepU,3), dtype=int)
        bottomFacesSphere=np.zeros((stepU,3), dtype=int)
        bottomVertexIndex=((stepV-1)*(stepU)+1)
        topVertexIndex=0
        for i in range(stepU):
            #top faces
            topFacesSphere[i,0]=topVertexIndex
            topFacesSphere[i,1]=i+1
            topFacesSphere[i,2]=(i+1)%stepU+1
            #bottom faces
            bottomFacesSphere[i,0]=bottomVertexIndex
            bottomFacesSphere[i,1]=((stepV-1)*(stepU)+1)+(i+1)%stepU-stepU
            bottomFacesSphere[i,2]=bottomVertexIndex-stepU+i


        #result

        #CONCATENATE THE POINTS
        pointsSphere= np.concatenate((topVertexSphere, pointsSphere,bottomVertexSphere), axis=0)

        #CONCATENATE THE FACES
        #we add 1 to all the elements in the facesSphere matrix because the first 
        #element in the result matrix will be the top vertex
        facesSphere=facesSphere+1

        facesSphere= np.concatenate((topFacesSphere, facesSphere,bottomFacesSphere), axis=0)
        return pointsSphere,facesSphere

    def sphereMesh(self):
        verticesSphere,facesSphere=self.sphereVerticesAndFaces()
        # Create the mesh
        #this function uses the numpy stl library mesh function (from stl import mesh)
        sphereMesh = mesh.Mesh(np.zeros(facesSphere.shape[0], dtype=mesh.Mesh.dtype))

        for i, f in enumerate(facesSphere):
            for j in range(3):
                #print(i,j,f,cube.vectors[i][j])
                sphereMesh.vectors[i][j] = verticesSphere[f[j],:]
                #print(cube.vectors[i][j])

        #print(facesSphere)
        return sphereMesh

    def rangeNumberSteps(start,end,numberSteps):
        result=list()
        for i in range(numberSteps+1):
            result.append(start+(end-start)*i/numberSteps)
        #print(result)
        return result