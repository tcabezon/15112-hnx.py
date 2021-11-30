from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math
from hnXfunctions import *


class Bezier3D(object):
    def __init__(self,controlPointList,numberOfPoints,cx=0,cy=0,cz=0,stepU=5):
        #center of the resulting bezier3D object
        self.cx=cx
        self.cy=cy
        self.cz=cz
        self.center=[cx,cy,cz]
        #self.stepU xy plane divisions
        self.stepU=stepU 
        #list of the control points that generate the bezier curve
        self.controlPointList=controlPointList
        #number of points in the bezier curve
        self.numberOfPoints=numberOfPoints

        self.bezierCurvePoints=self.bezierCurvePointList()
        self.bezierMeshPoints,self.bezierMeshFaces=self.bezierPointsAndFaces()
        self.faces=self.bezierMeshFaces
        self.vertices=self.bezierMeshPoints
        # stepV z axisdivisions, it is given by the number of divisions we have in the bezier curve
        self.stepV=len(self.bezierCurvePoints)-1
        self.points2D=threeDtotwoD(self.bezierMeshPoints)


    def bezierPointsAndFaces(self):
        #self.stepU xy plane divisions
        # stepV z axisdivisions

        stepV=len(self.bezierCurvePoints)-1

        #generate 'body'
        pointsMesh=np.zeros((((stepV-1)*(self.stepU)),3))
        facesMesh=np.zeros((((stepV-2)*(self.stepU))*2,3), dtype=int)
        #print(self.bezierCurvePoints[1:-2])

        for row, v in enumerate(self.bezierCurvePoints[1:-1]):
            for col, u in enumerate(rangeNumberSteps(0,2*math.pi-(2*math.pi/self.stepU)
                                                            ,self.stepU-1)):
                
                #add points to the pointsMesh matrix
                #everytime we access a point we have to add 1 to the index
                indexInMatrix= row*(self.stepU)+col
                pointsMesh[indexInMatrix,0]=self.cx+self.bezierCurvePoints[row+1][0]*math.cos(u)
                pointsMesh[indexInMatrix,1]=self.cy+self.bezierCurvePoints[row+1][0]*math.sin(u)
                #the height is equal for all the points in the given xy plane when rotating
                pointsMesh[indexInMatrix,2]=self.cz+self.bezierCurvePoints[row+1][1]
                
                #add faces to the facesMesh matrix
                if row!=0:
                    #top triangle
                    facesIndexTop= (row-1)*(2*self.stepU)+self.stepU+col
                    facesMesh[facesIndexTop,0]= (row*(self.stepU)+col)
                    facesMesh[facesIndexTop,1]= ((row-1)*(self.stepU)+(col+1)%self.stepU)
                    facesMesh[facesIndexTop,2]= ((row-1)*(self.stepU)+col)
                    

                    #bottom triangle
                    facesIndexBottom= (row-1)*(2*self.stepU)+col
                    facesMesh[facesIndexBottom,0]= (row*(self.stepU)+col)
                    facesMesh[facesIndexBottom,1]= ((row)*(self.stepU)+(col+1)%self.stepU)
                    facesMesh[facesIndexBottom,2]= ((row-1)*(self.stepU)+(col+1)%self.stepU)

        #generate top and bottom vertex of the mesh
        topVertexMesh=np.array([[0,self.cy,self.cz+self.bezierCurvePoints[0][1]]])
        bottomVertexMesh=np.array([[0,self.cy,self.cz+self.bezierCurvePoints[-1][1]]])
        #generate top and bottom faces of the mesh
        topfacesMesh=np.zeros((self.stepU,3), dtype=int)
        bottomfacesMesh=np.zeros((self.stepU,3), dtype=int)
        bottomVertexIndex=((stepV-1)*(self.stepU)+1)
        topVertexIndex=0
        for i in range(self.stepU):
            #top faces
            topfacesMesh[i,0]=topVertexIndex
            topfacesMesh[i,1]=i+1
            topfacesMesh[i,2]=(i+1)%self.stepU+1
            #bottom faces
            bottomfacesMesh[i,0]=bottomVertexIndex
            bottomfacesMesh[i,1]=((stepV-1)*(self.stepU)+1)+(i+1)%self.stepU-self.stepU
            bottomfacesMesh[i,2]=bottomVertexIndex-self.stepU+i


        #result

        #CONCATENATE THE POINTS
        pointsMesh= np.concatenate((topVertexMesh, pointsMesh,bottomVertexMesh), axis=0)

        #CONCATENATE THE FACES
        #we add 1 to all the elements in the facesMesh matrix because the first 
        #element in the result matrix will be the top vertex
        facesMesh=facesMesh+1

        facesMesh= np.concatenate((topfacesMesh, facesMesh,bottomfacesMesh), axis=0)
        return pointsMesh,facesMesh  
    
    def bezierMesh(self):
        pointsMesh,facesMesh=self.bezierPointsAndFaces()
        # Create the mesh
        #this function uses the numpy stl library mesh function (from stl import mesh)
        bMesh = mesh.Mesh(np.zeros(facesMesh.shape[0], dtype=mesh.Mesh.dtype))

        for i, f in enumerate(facesMesh):
            for j in range(3):
                #print(i,j,f,cube.vectors[i][j])
                bMesh.vectors[i][j] = pointsMesh[f[j],:]
                #print(cube.vectors[i][j])

        #print(facesMesh)
        return bMesh

    def saveMesh(self):
        
        bMesh = self.bezierMesh()
        # SAVE THE MODEL
        bMesh.save('bezierMesh.stl')
        print('mesh saved')

    def displayMesh(self):
        # generate the mesh
        bMesh = self.bezierMesh()
        # PLOTTING
        # Create a new plot
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)
        # Add the vectors to the plot
        #using matplot library to plot the 3D mesh
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(bMesh.vectors, facecolors='b',edgecolors='k', linewidths=1, alpha=0.75))
        # Auto scale to the mesh size
        scale = bMesh.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        pyplot.show()


    def bezierCurvePointList(self):
        if self.controlPointList==[]: return []
        bezierCurve=[]
        controlPointList=self.controlPointList
        for i in range(self.numberOfPoints):
            t=i/(self.numberOfPoints-1)
            bezierCurve.append(self.deCasteljau(controlPointList, t))
        #print(bezierCurve)
        return bezierCurve

    def deCasteljau(self,pointList, t):
        #recursive definition of the de casteljau algorithm
        #inspired from https://es.wikipedia.org/wiki/Algoritmo_de_De_Casteljau

        if len(pointList)==1:
            #if we finally found b_0,n
            return pointList[0]
        else:
            newList=[]
            #calculate b_i,n given b_i-1,n
            for i in range(len(pointList)-1):
                newPoint=[]
                for j in range(len(pointList[i])):
                    newPoint_j=(1-t)*pointList[i][j]+(t)*pointList[i+1][j]
                    newPoint.append(newPoint_j)
                #print('newPoint', newPoint)
                newList.append(newPoint)
            return self.deCasteljau(newList, t)

    

