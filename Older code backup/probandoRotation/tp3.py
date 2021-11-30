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
from bezierFunctions import *



#####################
# DISPLAY
#####################

#####################
# AppStarted
#####################

def meshView(canvas,app):
    canvas.create_rectangle(app.meshViewStart*app.width*app.doubleView,0,app.width,app.height,fill='#f2f2f2')
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,app.faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)
    

def appStarted(app):
    app.mode='mainMode'
    app.doubleView=True
    app.meshViewStart=(1/3) #percentage of the app.width
    app.ring=Ring(200,5,stepRing=5,stepCircunference=3)
    app.draw=True
    app.mousePosition=(0,0)
    app.editMode=False
    app.modeDictionary={'m':'moveMode',
                        'r':'rotateMode',
                        'z':'moveZMode',
                        'a':'mainMode',
                        'e':'editMode',
                        'p':'zoomMode',
                        'x':'moveBezierMode',
                        'b':'bezier',
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
    app.pointList=[[app.width/2,app.height/4],[app.width/2,3*app.height/4]]
    app.numberOfBezierPoints=20
    app.bezierCurvePoints=None
    app.stepBezier=10
    app.movingPoint=None
    app.slider='2'
    app.sliderDictionary={'1':5,
                        '2':10,
                        '3':15,
                        '4':20,
                        '5':25,
                        '6':30}

    # app.vertices=np.copy(vertices)
    # app.points2D=np.copy(ring1.points2D)

    app.vertices=np.copy(app.ring.vertices)
    app.points2D=np.copy(app.ring.points2D)
    app.faces=np.copy(app.ring.faces)
    

################
#MAIN MODE
################
  
def mainMode_keyPressed(app, event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
    

def mainMode_redrawAll(app, canvas):

    meshView(canvas,app)
    

#####################
# moveMode
#####################


def moveMode_redrawAll(app,canvas):
    meshView(canvas,app)
    

def moveMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        

def moveMode_mouseDragged(app,event):
    mousePosition=(event.x ,event.y)
    #convert the point from the isometric view to global 2D
    mousePosition=isometricToTwoD(app,mousePosition)
    if app.movingPoint==None:
        tolerance=40
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
    displayFaces(app,canvas,app.points2D,app.faces)
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
    displayFaces(app,canvas,app.points2D,app.faces)
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
    print('mouse dragged at',mousePosition)
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
    displayFaces(app,canvas,app.points2D,app.faces)
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
                       text="Press 's' AGAIN to save the current mesh as currentMesh.stl", font='Arial 10 bold', anchor='se')
    margin=30
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,app.faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)
    

def saveMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
    if event.key=='s':
        print('saving mesh')
        saveCurrentMesh(app)

        
##################### 
# editMode
#####################

def editMode_redrawAll(app,canvas):
    resultString='Press the following keys to change\nthe different radious:\n'
    for elem in app.sliderDictionary:
        resultString+=elem+': '+str(app.sliderDictionary[elem])+'\n'
    canvas.create_text(app.width-app.margin, app.margin,
                       text=resultString, font='Arial 10 bold', anchor='ne')
    printModeDictionary(app,canvas)
    displayFaces2D(app,canvas)
    displayPoints2D(app,canvas)
    printCenter(app,canvas)

def editMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
    if event.key in app.sliderDictionary:
        app.slider=event.key
    

def editMode_mousePressed(app, event):
    mousePosition=(event.x ,event.y)
    print('mousePosition1',mousePosition)
    mousePosition=isometricToTwoD_noScale(app,mousePosition)
    print('mousePosition2',mousePosition)
    print('mouse at',mousePosition)
    if mousePressedInsideRing(app,mousePosition):
        r=app.sliderDictionary[app.slider]
        print('addingElement at', mousePosition,'with radious',r)
        newSphere=Sphere(r,cx=0,cy=mousePosition[0],cz=mousePosition[1],stepU=5,stepV=5)
        print(newSphere)
        app.ring.addElement(newSphere)
    app.faces=np.copy(app.ring.faces)
    app.vertices=np.copy(app.ring.vertices)
    app.points2D=np.copy(app.ring.points2D)


###############
#BEZIER MODE
###############


def bezier_mousePressed(app, event):
    newPoint =  [event.x, event.y]
    app.pointList.insert(len(app.pointList)-1,newPoint)
    
    

def bezier_redrawAll(app, canvas):
    printBezierOptions(app,canvas)
    printModeDictionary(app, canvas)
    canvas.create_line(app.width/2,app.margin,app.width/2,app.height-app.margin)
    drawPoints(canvas,app.pointList,color='gray')
    drawBezierCurve(canvas,app)


def bezier_keyPressed(app, event):
    if event.key=='d':
        displayMesh(app)
    if event.key=='g':
        saveMesh(app) 
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]

###############
#MOVE BEZIER MODE
###############

def moveBezierMode_redrawAll(app,canvas):
    printModeDictionary(app, canvas)
    printBezierOptions(app,canvas)
    canvas.create_line(app.width/2,app.margin,app.width/2,app.height-app.margin)
    drawPoints(canvas,app.pointList,color='gray')
    drawBezierCurve(canvas,app)
    
   
def moveBezierMode_mouseDragged(app,event):
    mousePosition=(event.x ,event.y)
    if app.movingPoint==None: 
        tolerance=20
        pointToMoveIndex=findClickedPoint(mousePosition,app.pointList,tolerance)
        if pointToMoveIndex!=None:
            app.movingPoint=pointToMoveIndex
        
    elif app.movingPoint!=None:
        #if first or last point in the list are clicke, we only update the y position, so they stay on the axis
        if app.movingPoint==0 or app.movingPoint==len(app.pointList)-1:
            app.pointList[app.movingPoint][1]=mousePosition[1]
        else:
            app.pointList[app.movingPoint]=mousePosition
        
  
def moveBezierMode_mouseReleased(app,event):
    mouseReleasedPosition=(event.x ,event.y)
    print('mouse released at:', mouseReleasedPosition)
    if app.movingPoint!=None:
        app.movingPoint=None

        
def moveBezierMode_keyPressed(app,event):
    print(event.key)
    if event.key=='d':
        displayMesh(app)
    if event.key=='g':
        saveMesh(app) 
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]        

    
runApp(width=1200, height=600)



