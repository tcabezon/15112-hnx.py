
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

vertices=vertices.astype(float)
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

print(len(faces))
np.set_printoptions(precision=1)

points2Dstart=threeDtotwoD(vertices)
for point in points2Dstart:
    print(point)
points2Dstart=points2Dstart.astype(float)
print(points2Dstart)


#####################
# DISPLAY
#####################

#####################
# AppStarted
#####################

def appStarted(app):
    app.mode='rotateMode'
    app.draw=True
    app.mousePosition=(0,0)
    app.editMode=False
    app.modeDictionary={'m':'moveMode',
                        'r':'rotateMode',
                        'z':'moveZMode',
                        'e':'mainMode'}
    app.movingPoint=None 
    app.rotatingInitialPosition=None
    app.vertices=np.copy(vertices)
    print(app.vertices)
    app.points2D=points2Dstart
    app.zPressed=False
    app.initialYCoordinate=None
    app.margin=30
    app.maxX=None
    

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
    if app.movingPoint[0]!=None:
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
# rotateMode
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
    angle=45
    if event.key=='Up':
        print('rotatin 1dregree right')
        rotatePointsAngle(app,angle)
    if event.key=='Down':
        print('rotatin 1dregree right')
        rotatePointsAngle(app,-angle)
        
'''       
def rotateMode_mousePressed(app,event):
    mousePosition=(event.x ,event.y)
    if app.rotatingInitialPosition==None:
        #tolerance=20
        app.maxX=findMaxX(app)      
        app.rotatingInitialPosition=mousePosition
        print('Rotating parameters found, started at',app.rotatingInitialPosition[0])

def rotateMode_mouseDragged(app,event):
    mousePosition=(event.x ,event.y)
    if app.rotatingInitialPosition!=None:
        rotatedXDistance=mousePosition[0]-app.rotatingInitialPosition[0]
        print('entered rotation, rotated distance',rotatedXDistance)
        angle=45*rotatedXDistance/app.maxX
        rotatePointsAngle(app,angle)
'''   
def rotateMode_mouseDragged(app,event):
    #find the maxX value of the points to know the rotating angle value
    if app.maxX==None:
        app.maxX=findMaxX(app) 
    #get the mouse position
    mousePosition=(event.x ,event.y)
    #if is the first time that we enter the function, this is, is we are starting rotating, save the initial position
    if app.rotatingInitialPosition==None:
       app.rotatingInitialPosition=mousePosition
    #if we are the mouse position is different to the initial position:
    # we have dragged a distance so we have to rotate the object proportional to that
    if mousePosition!=app.rotatingInitialPosition:
        #we calculate the dragged distances
        rotatedXDistance=mousePosition[0]-app.rotatingInitialPosition[0]
        #the rotated angel is proportional to the dragged distance
        #To get this angle and distance relationship i have supposed that
        # dragging a distance equal to the max(x_distance) of all the points should rotate 45 degrees
        angle=45*rotatedXDistance/app.maxX
        rotatePointsAngle(app,angle)  
    app.rotatingInitialPosition=mousePosition    

        
def rotateMode_mouseReleased(app,event):
    #when the mouse is released after we are rotating a point, we reset the None values of 
    #the variables app.rotatingInitialPosition and app.maxX=None
    if app.rotatingInitialPosition!=None:
        app.rotatingInitialPosition=None
        app.maxX=None


runApp(width=600, height=600)



