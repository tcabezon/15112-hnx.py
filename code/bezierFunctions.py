from cmu_112_graphics import *
import numpy as np
from stl import mesh
from stl import mesh
import math
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *
'''
def deCasteljau(pointList, t):
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
        return deCasteljau(newList, t)
'''
'''
Things that could be improved:
Using numpy to calculate the points newPoint_j instead of a for loop.
'''
'''
def bezierCurvePointList(pointList,numberOfPoints):
    if pointList==[]: return []
    bezierCurve=[]
    for i in range(numberOfPoints):
        t=i/(numberOfPoints-1)
        bezierCurve.append(deCasteljau(pointList, t))
    #print(bezierCurve)
    return bezierCurve
'''

def drawBezierCurve(canvas,app):
    bezierCurve=app.bezier.bezierCurvePoints
    drawPoints(app,canvas,bezierCurve,'blue')
    
#draw a list of points in 2D
def drawPoints(app,canvas,pointList,color='black'):
    r=2
    for i in range(len(pointList)):
        (cx, cy) = np.array(pointList[i])*(app.width*app.meshViewStart)
        (cx,cy) = ((app.width*app.meshViewStart)/2+cx,(app.width*app.meshViewStart)/2-cy)
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color)
        if i!=0:
            canvas.create_line((cx, cy),previousPoint,fill=color)
        previousPoint= (cx,cy)
        
'''
def bezierPointsAndFacer(bezierCurvePoints,stepU=10):
    #stepU xy plane divisions
    # stepV z axisdivisions

    stepV=len(bezierCurvePoints)-1

    #generate 'body'
    pointsMesh=np.zeros((((stepV-1)*(stepU)),3))
    facesMesh=np.zeros((((stepV-2)*(stepU))*2,3), dtype=int)
    print(bezierCurvePoints[1:-2])

    for row, v in enumerate(bezierCurvePoints[1:-1]):
        for col, u in enumerate(rangeNumberSteps(0,2*math.pi-(2*math.pi/stepU)
                                                        ,stepU-1)):
            
            #add points to the pointsMesh matrix
            #everytime we access a point we have to add 1 to the index
            indexInMatrix= row*(stepU)+col
            pointsMesh[indexInMatrix,0]=bezierCurvePoints[row+1][0]*math.cos(u)
            pointsMesh[indexInMatrix,1]=bezierCurvePoints[row+1][0]*math.sin(u)
            #the height is equal for all the points in the given xy plane when rotating
            pointsMesh[indexInMatrix,2]=bezierCurvePoints[row+1][1]
            
            #add faces to the facesMesh matrix
            if row!=0:
                #top triangle
                facesIndexTop= (row-1)*(2*stepU)+stepU+col
                facesMesh[facesIndexTop,0]= (row*(stepU)+col)
                facesMesh[facesIndexTop,1]= ((row-1)*(stepU)+(col+1)%stepU)
                facesMesh[facesIndexTop,2]= ((row-1)*(stepU)+col)
                

                #bottom triangle
                facesIndexBottom= (row-1)*(2*stepU)+col
                facesMesh[facesIndexBottom,0]= (row*(stepU)+col)
                facesMesh[facesIndexBottom,1]= ((row)*(stepU)+(col+1)%stepU)
                facesMesh[facesIndexBottom,2]= ((row-1)*(stepU)+(col+1)%stepU)

    #generate top and bottom vertex of the mesh
    topVertexMesh=np.array([[0,0,bezierCurvePoints[0][1]]])
    bottomVertexMesh=np.array([[0,0,bezierCurvePoints[-1][1]]])
    #generate top and bottom faces of the mesh
    topfacesMesh=np.zeros((stepU,3), dtype=int)
    bottomfacesMesh=np.zeros((stepU,3), dtype=int)
    bottomVertexIndex=((stepV-1)*(stepU)+1)
    topVertexIndex=0
    for i in range(stepU):
        #top faces
        topfacesMesh[i,0]=topVertexIndex
        topfacesMesh[i,1]=i+1
        topfacesMesh[i,2]=(i+1)%stepU+1
        #bottom faces
        bottomfacesMesh[i,0]=bottomVertexIndex
        bottomfacesMesh[i,1]=((stepV-1)*(stepU)+1)+(i+1)%stepU-stepU
        bottomfacesMesh[i,2]=bottomVertexIndex-stepU+i


    #result

    #CONCATENATE THE POINTS
    pointsMesh= np.concatenate((topVertexMesh, pointsMesh,bottomVertexMesh), axis=0)

    #CONCATENATE THE FACES
    #we add 1 to all the elements in the facesMesh matrix because the first 
    #element in the result matrix will be the top vertex
    facesMesh=facesMesh+1

    facesMesh= np.concatenate((topfacesMesh, facesMesh,bottomfacesMesh), axis=0)
    return pointsMesh,facesMesh
'''
'''
def bezierMesh(bezierCurvePoints,stepU=10):
    pointsMesh,facesMesh=bezierPointsAndFacer(bezierCurvePoints,stepU)
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
'''

def printBezierOptions(app,canvas):
    canvas.create_text(app.margin, app.width*app.meshViewStart,
                       text=f'Press:\nd, to display the mesh\ng, to save the .stl file', font='Arial 10 bold', anchor='nw')
'''
def saveMesh(app):
    # generate the mesh
    bezierCurve=bezierCurvePointList(app.pointList,app.numberOfBezierPoints)
    bezierCurve=np.array(bezierCurve)
    bezierCurve[:,0]-=(app.width/2)
    bMesh = bezierMesh(bezierCurve,app.stepBezier)


    # SAVE THE MODEL
    bMesh.save('bezierMesh.stl')
    print('mesh saved')
'''
def displayMesh(app):
    # generate the mesh
    bezierCurve=bezierCurvePointList(app.pointList,app.numberOfBezierPoints)
    bezierCurve=np.array(bezierCurve)
    bezierCurve[:,0]-=(app.width/2)
    bMesh = bezierMesh(bezierCurve,app.stepBezier)

    # PLOTTING
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    # Add the vectors to the plot
    #using matplot library to plot the 3D mesh
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(-bMesh.vectors, facecolors='b',edgecolors='k', linewidths=1, alpha=0.75))


    # Auto scale to the mesh size
    scale = bMesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    
    axes.scatter(0,-bezierCurve[:,0], -bezierCurve[:,1])

    # Show the plot to the screen
    pyplot.show()