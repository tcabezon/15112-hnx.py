from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *
from sphereClass import *
from ringClass import *
    
#ring1=Ring(200,50,stepRing=3,stepCircunference=3)
#vertices = ring1.vertices
#faces=ring1.faces





#####################
# DISPLAY
#####################

#####################
# AppStarted
#####################

def appStarted(app):
    app.mode='mainMode'
    app.ring=Sphere(10,cx=0,cy=100,cz=20)
    app.draw=True
    app.mousePosition=(0,0)
    app.editMode=False
    app.modeDictionary={'m':'moveMode',
                        'r':'rotateMode',
                        'z':'moveZMode',
                        'a':'mainMode',
                        'e':'editMode',
                        'p':'zoomMode',
                        's':'saveMode'}
    app.movingPoint=None 
    app.rotatingInitialPosition=None
    app.zPressed=False
    app.initialYCoordinate=None
    app.margin=30
    app.maxX=None
    app.maxY=None
    app.scale=1
    app.zoomInitialPosition=None

    # app.vertices=np.copy(vertices)
    # app.points2D=np.copy(ring1.points2D)

    app.vertices=app.ring.vertices
    app.points2D=app.ring.points2D
    

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
    displayFaces(app,canvas,app.points2D,app.ring.faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)

#####################
# moveMode
#####################

def moveMode_redrawAll(app,canvas):
    margin=30
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,app.ring.faces)
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
    displayFaces(app,canvas,app.points2D,app.ring.faces)
    displayPoints(app,canvas,app.points2D)
    if app.movingPoint!=None:
        print('arrow in point')
        arrow=twoDToIsometric(app,app.scale*app.points2D[app.movingPoint])
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
# rotateMode
#####################

def rotateMode_redrawAll(app,canvas):
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,app.ring.faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)
    
    

def rotateMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
    angle=10
    if event.key=='Up':
        print('rotating up')
        rotatePointsAngleV(app,angle)
    if event.key=='Down':
        print('rotating down')
        rotatePointsAngleV(app,-angle)
    if event.key=='Right':
        print('rotatin right')
        rotatePointsAngleH(app,angle)
    if event.key=='Left':
        print('rotatin left')
        rotatePointsAngleH(app,-angle)
        
  
def rotateMode_mouseDragged(app,event):
    #find the maxX value of the points to know the rotating angle value
    '''if app.maxX==None:
        app.maxX=findMaxX(app) 
        app.maxY=findMaxY(app) '''
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
        rotatedYDistance=-mousePosition[1]+app.rotatingInitialPosition[1]
        #the rotated angel is proportional to the dragged distance
        #To get this angle and distance relationship i have supposed that
        # dragging a distance equal to the max(x_distance) of all the points should rotate 45 degrees
        '''
        angleX=45*rotatedXDistance/app.maxX
        angleY=45*rotatedYDistance/app.maxY
        '''
        angleX=45*rotatedXDistance/(app.width/2)
        angleY=45*rotatedYDistance/(app.height/2)
        rotatePointsAngleH(app,angleX)  
        rotatePointsAngleV(app,angleY)  
    app.rotatingInitialPosition=mousePosition    

        
def rotateMode_mouseReleased(app,event):
    #when the mouse is released after we are rotating a point, we reset the None values of 
    #the variables app.rotatingInitialPosition and app.maxX=None
    if app.rotatingInitialPosition!=None:
        app.rotatingInitialPosition=None
        app.maxX=None

#####################
# zoomMode
#####################

def zoomMode_redrawAll(app,canvas):
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,app.ring.faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)
    
    

def zoomMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
    angle=10
    if event.key in ['Up','+']:
        print('zooming in')
        zoomIn(app,1.1)
    if event.key in ['Down','-']:
        print('zooming out')
        zoomOut(app,0.9)
        
  
def zoomMode_mouseDragged(app,event):
    #get the mouse position
    mousePosition=(event.x ,event.y)
    #if is the first time that we enter the function, this is, is we are starting rotating, save the initial position
    if app.zoomInitialPosition==None:
       app.zoomInitialPosition=mousePosition
    #if we are the mouse position is different to the initial position:
    # we have dragged a distance so we have to rotate the object proportional to that
    if mousePosition!=app.zoomInitialPosition:
        #we calculate the dragged distances
        zoomedYDistance=-mousePosition[1]+app.zoomInitialPosition[1]
        print(' zoomedYDistance', zoomedYDistance)
        #the zoomed scale is proportional to the dragged distance
        #we shouldn't do zoom if the distance is 0
        if zoomedYDistance>0: 
            scale=1+zoomedYDistance/app.height
            print('zoom in:',scale)
            zoom(app,scale) 
        elif zoomedYDistance<0: 
            scale=1+(zoomedYDistance/app.height)
            print('zoom out:',scale)
            zoom(app,scale)  
        
    app.zoomInitialPosition=mousePosition    

        
def zoomMode_mouseReleased(app,event):
    #when the mouse is released after we are rotating a point, we reset the None values of 
    #the variables app.rotatingInitialPosition and app.maxX=None
    if app.zoomInitialPosition!=None:
        app.zoomInitialPosition=None
        app.maxX=None

#####################
# saveMode
#####################

def saveMode_redrawAll(app,canvas):
    canvas.create_text(app.width-app.margin, app.height-app.margin,
                       text="Press 's' to save the mesh\nPress 'd' to display de mesh in matplotlib", font='Arial 10 bold', anchor='se')
    margin=30
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,app.ring.faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)
    

def saveMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
    if event.key=='s':
        print('saving mesh')
        app.ring.mesh.save('ring.stl')
    if event.key=='d':
        print('diplaying mesh')
        plotMesh(app.ring.mesh)
        
#####################
# editMode
#####################

def editMode_redrawAll(app,canvas):
    printModeDictionary(app, canvas)
    displayFaces2D(app,canvas,app.points2D,app.ring.faces)
    displayPoints2D(app,canvas,app.points2D)
    printCenter(app,canvas)

def editMode_mousePressed(app, event):
    mousePosition=(event.x ,event.y)
    mousePosition=isometricToTwoD(app,mousePosition)
    print('mouse at',mousePosition)
    if mousePressedInsideRing(app,mousePosition):
        print('addingElement')
        r=5
        newSphere=Sphere(r,cx=0,cy=mousePosition[0],cz=mousePosition[1])
        print(newSphere)
        app.ring.addElement(newSphere)

def editMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
    
runApp(width=600, height=600)