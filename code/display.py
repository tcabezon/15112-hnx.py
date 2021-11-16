
from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *
    

# Define the 8 vertices of the octahedron
vertices = np.array([\
    [0,0,0],
    [100,0,0],
    [100,100,0],
    [0,100,0],
    [50,50,200]])
'''
2D
[[   0    0]
 [ -86  -50]
 [   0 -100]
 [  86  -50]
 [   0  149]]'''

# Define the 12 triangles composing the octahedron
faces = np.array([\
                 [0,2,1],
                 [0,3,2],
                 [4,0,1],
                 [4,1,2],
                 [4,2,3],
                 [4,3,0]])



points2Dstart=threeDtotwoD(vertices)
for point in points2Dstart:
    print(point)
points2Dstart=points2Dstart.astype(int)
#print(points2D)


#####################
# DISPLAY
#####################
print(faces.shape[0])

def appStarted(app):
    app.mode='mainMode'
    app.draw=True
    app.mousePosition=(0,0)
    app.editMode=False
    app.modeDictionary={'m':'moveMode',
                        'r':'rotateMode',
                        'z':'moveZMode',
                        'e':'mainMode'}
    app.movingPoint=None 
    app.vertices=vertices
    app.points2D=points2Dstart
    app.zPressed=False
    app.initialYCoordinate=None
    app.margin=30
    

################
#MAIN MODE
################
  
def mainMode_keyPressed(app, event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
    

def mainMode_redrawAll(app, canvas):
    printModeDictionary(app, canvas)
    margin=30
    displayFaces(app,canvas,app.points2D,faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)
    

#####################
# moveMode
#####################

def moveMode_redrawAll(app,canvas):
    margin=30
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)
    

def moveMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        

def moveMode_mouseDragged(app,event):
    mousePosition=(event.x ,event.y)
    #convert the point from the isometric view to global 2D
    mousePosition=isometricToTwoD(app,mousePosition)
    if app.movingPoint==None:
        tolerance=20
        pointToMoveIndex=findClickedPoint(mousePosition,app.points2D,tolerance) 
        if pointToMoveIndex!=None:
            app.movingPoint=pointToMoveIndex
            print('dragging point',pointToMoveIndex)
    if app.movingPoint!=None:
        app.points2D[app.movingPoint]=mousePosition
        #convert the 2D coordinates to 3D and update the point
        app.vertices[app.movingPoint]=newtwoDToThreeD_NoZChange(mousePosition,app.vertices[app.movingPoint],theta_x=210,theta_y=330)
         
        
def moveMode_mouseReleased(app,event):
    mouseReleasedPosition=(event.x ,event.y)
    mouseReleasedPosition=isometricToTwoD(app,mouseReleasedPosition)
    print('mouse released at:', mouseReleasedPosition)
    if app.movingPoint!=None:
        app.movingPoint=None

#####################
# moveZMode
#####################

def moveZMode_redrawAll(app,canvas):
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,faces)
    displayPoints(app,canvas,app.points2D)
    if app.movingPoint!=None:
        arrow=twoDToIsometric(app,app.points2D[app.movingPoint])
        drawArrow(canvas,arrow, (arrow[0],(arrow[1]-app.width*0.1)), "red", 3)
    printCenter(app,canvas)
   
def moveZMode_mouseDragged(app,event):
    mousePosition=(event.x ,event.y)
    #convert the point from the isometric view to global 2D
    mousePosition=isometricToTwoD(app,mousePosition)
    if app.movingPoint==None: 
        tolerance=20
        pointToMoveIndex=findClickedPoint(mousePosition,app.points2D,tolerance)
        if pointToMoveIndex!=None:
            print(app.points2D)
            app.initialYCoordinate=app.points2D[pointToMoveIndex][1]
            app.movingPoint=pointToMoveIndex
        #print('dragging point',pointToMoveIndex)
    elif app.movingPoint!=None:
        app.points2D[app.movingPoint][1]=mousePosition[1]
        #convert the 2D coordinates to 3D and update the point
        app.vertices[app.movingPoint]=newtwoDToThreeD_zChange(mousePosition,app.vertices[app.movingPoint],theta_x=210,theta_y=330)
  
def moveZMode_mouseReleased(app,event):
    mouseReleasedPosition=(event.x ,event.y)
    mouseReleasedPosition=isometricToTwoD(app,mouseReleasedPosition)
    print('mouse released at:', mouseReleasedPosition)
    if app.movingPoint!=None:
        #zChange=mouseReleasedPosition[1]-app.initialYCoordinate
        #app.vertices[app.movingPoint][2]=app.initialYCoordinate
        #zChange=mouseReleasedPosition[1]-app.initialYCoordinate
        #app.vertices[app.movingPoint][2]+=zChange
        app.movingPoint=None

        
def moveZMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]



#####################
# moveMode
#####################

def rotateMode_redrawAll(app,canvas):
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)
    

def rotateMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        

def rotateMode_mouseDragged(app,event):
    mousePosition=(event.x ,event.y)
    #convert the point from the isometric view to global 2D
    mousePosition=isometricToTwoD(app,mousePosition)
    if app.movingPoint==None:
        tolerance=20
        pointToMoveIndex=findClickedPoint(mousePosition,app.points2D,tolerance) 
        app.movingPoint=pointToMoveIndex
        print('dragging point',pointToMoveIndex)
    if app.movingPoint!=None:
        app.points2D[app.movingPoint]=mousePosition
        #convert the 2D coordinates to 3D and update the point
        app.vertices[app.movingPoint]=newtwoDToThreeD_NoZChange(mousePosition,app.vertices[app.movingPoint],theta_x=210,theta_y=330)
         
        
def rotateMode_mouseReleased(app,event):
    mouseReleasedPosition=(event.x ,event.y)
    mouseReleasedPosition=isometricToTwoD(app,mouseReleasedPosition)
    print('mouse released at:', mouseReleasedPosition)
    if app.movingPoint!=None:
        app.movingPoint=None


runApp(width=600, height=600)



