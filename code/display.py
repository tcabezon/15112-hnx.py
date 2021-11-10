
from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *
'''
def threeDtotwoD(treeDPoints,theta_x=210,theta_y=330):

    transformationMatrix=[\
                        [ math.cos(math.radians(theta_x)),math.sin(math.radians(theta_x))],
                        [ math.cos(math.radians(theta_y)),math.sin(math.radians(theta_y))],
                        [ 0, 1]]
    twoDPoints=np.matmul(treeDPoints,transformationMatrix)
    return twoDPoints

def displayPoints(app,canvas,points,r=2,color='green'):
    transformMatrix=np.array([[1,0],[0,-1]])
    points=np.matmul(points,transformMatrix)
    for point in points:
        cx=app.width/2+point[0]
        cy=app.height/2+point[1]
        canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill=color)

def displayFaces(app,canvas,vertices,faces):
    transformMatrix=np.array([[1,0],[0,-1]])
    vertices=np.matmul(vertices,transformMatrix)
    for i in range(faces.shape[0]):
        faceIndexes=faces[i]
        print(f'face {i}: ',faceIndexes)
        center=[app.width/2,app.height/2]
        point1=center+vertices[faceIndexes[0]]
        point2=center+vertices[faceIndexes[1]]
        point3=center+vertices[faceIndexes[2]]
        print(point1, point2, point3)
        canvas.create_line(point1[0],point1[1],point2[0],point2[1])
        canvas.create_line(point1[0],point1[1],point3[0],point3[1])
        canvas.create_line(point2[0],point2[1],point3[0],point3[1])

def printCenter(app,canvas):
    cx=app.width/2
    cy=app.height/2
    r=2
    canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill='red')
        
'''     

# Define the 8 vertices of the octahedron
vertices = np.array([\
    [0,0,0],
    [1,0,0],
    [1,1,0],
    [0,1,0],
    [0.5,0.5,2]])

# Define the 12 triangles composing the octahedron
faces = np.array([\
                 [0,2,1],
                 [0,3,2],
                 [4,0,1],
                 [4,1,2],
                 [4,2,3],
                 [4,3,0]])



points2D=threeDtotwoD(vertices)
points2D=np.multiply(100,points2D)
points2D=points2D.astype(int)
print(points2D)


#####################
# DISPLAY
#####################
print(faces.shape[0])

def appStarted(app):
    app.draw=False
  
def keyPressed(app, event):
    app.draw=not app.draw

def redrawAll(app, canvas):
    if app.draw:
        displayFaces(app,canvas,points2D,faces)
        displayPoints(app,canvas,points2D)
        printCenter(app,canvas)
    canvas.create_text(app.width/2, app.height-30,
                       text=f'press any key to stop or start drawing\napp.draw = {app.draw}', font='Arial 10 bold')
    

runApp(width=400, height=400)

