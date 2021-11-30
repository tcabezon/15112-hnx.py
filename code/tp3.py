#GRAPHICS
from cmu_112_graphics import *

#FUNCTIONS AND CLASSES
from functions import *
from sphereClass import *
from bezier3DClass import *
from ringClass import *

#OTHER LIBRARIES
from matplotlib import pyplot
import numpy as np
from stl import mesh
import math
from stl import mesh


#####################
# AppStarted
#####################

def appStarted(app):
    #allow double window display
    app.doubleView=True
    app.meshViewStart=(1/2.75) #percentage of the app.width
    app.drawElement='Sphere'
    app.bezierPointsScale=1
    app.numberOfButtons=5
    app.widthEachElement=(app.width*app.meshViewStart-(app.numberOfButtons+1)*5)/app.numberOfButtons
    app.mode='mainMode'
    app.ring=Ring(200,5,stepRing=12,stepCircunference=3)
    app.draw=True
    app.mousePosition=(0,0)
    app.editMode=False
    app.modeDictionary={'a':'mainMode',
                        'b':'bezier',
                        'x':'moveBezierMode'}
    app.advancedModeDictionary={'m':'moveMode',
                        'r':'rotateMode',
                        'z':'moveZMode',
                        'p':'zoomMode'}
    app.movingPoint=None 
    app.rotatingInitialPosition=None
    app.zPressed=False
    app.initialYCoordinate=None
    app.margin=30
    app.maxX=None
    app.maxY=None
    app.scale=1
    app.zoomInitialPosition=None
    #initialize the BezierCurve control point List
    controlPointList=[[0,0.3],[0,-0.3]]
    app.numberOfBezierPoints=8
    app.bezier=Bezier3D(controlPointList,app.numberOfBezierPoints)
    #copy of the 2D points for the rotation option on the bezier mode
    app.bezier.points2Dcopy=np.copy(app.bezier.points2D)
    app.movingPoint=None
    app.slider='2'
    app.sliderDictionary={'1':5,
                        '2':10,
                        '3':15,
                        '4':20,
                        '5':25}

    # app.vertices=np.copy(vertices)
    # app.points2D=np.copy(ring1.points2D)

    app.vertices=np.copy(app.ring.vertices)
    app.points2D=np.copy(app.ring.points2D)
    app.faces=np.copy(app.ring.faces)
    app.beziertheta_x=210
    app.beziertheta_y=330
    app.printMessage=False
    

################
#MAIN MODE
################
  
def mainMode_keyPressed(app, event):
    print(event.key)
    if event.key in app.advancedModeDictionary:
        app.mode=app.advancedModeDictionary[event.key]
        app.doubleView=False
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        app.doubleView=True

    #GET RING INFO
    if event.key=='i':
        print(app.ring.elements)

    #RESTART THE APP
    if event.key=='q':
        print('restarting app')
        appStarted(app)

    #DRAWING BEZIER/SPHERE
    if event.key == '0':
        app.drawElement='Sphere'
    if event.key == '9':
        app.drawElement='Bezier'
    

    #ELEMENT SIZE OPTIONS
    if event.key in app.sliderDictionary:
        app.slider=event.key

    #ROTATION OPTIONS
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

    #ZOOM OPTIONS
    if event.key in ['.','+']:
        print('zooming in')
        zoomIn(app,1.1)
    if event.key in [',','-','_']:
        print('zooming out')
        zoomOut(app,0.9)

    #SAVE OPTIONS
    if event.key=='s':
        print('saving mesh')
        saveCurrentMesh(app)
    
def mainMode_mousePressed(app,event):
    mousePosition=(event.x ,event.y)
    if ((mousePosition[0])<app.width*app.meshViewStart and (mousePosition[1])<app.width*app.meshViewStart ):
        mousePosition=isometricToTwoD_noScale(app,mousePosition)
        if mousePressedInsideRing(app,mousePosition):
            if app.drawElement=='Sphere':
                r=app.sliderDictionary[app.slider]
                print('adding Sphere at', mousePosition,'with radious',r)
                newSphere=Sphere(r,cx=0,cy=mousePosition[0],cz=mousePosition[1],stepU=5,stepV=6)
                print(newSphere)
                app.ring.addElement(newSphere)
                app.faces=np.copy(app.ring.faces)
                app.vertices=np.copy(app.ring.vertices)
                app.points2D=np.copy(app.ring.points2D)
            elif app.drawElement=='Bezier':
                bezierPointsScale=int(app.slider)*app.widthEachElement/app.numberOfButtons
                #generate the list of control points that will be used to generate the bezier3D object
                scaledControlPoints=scaleControlPoints(app.bezier.bezierCurvePoints,bezierPointsScale)
                print('adding Bezier3D at', mousePosition,'with radious',bezierPointsScale)
                newBezier=Bezier3D(scaledControlPoints,app.numberOfBezierPoints,cx=0,cy=mousePosition[0],cz=mousePosition[1],stepU=6)
                print(newBezier)
                app.ring.addElement(newBezier)
                app.faces=np.copy(app.ring.faces)
                app.vertices=np.copy(app.ring.vertices)
                app.points2D=np.copy(app.ring.points2D)
    #if mouse clicked over the sphere icons
    elif (mousePosition[1]<(app.width*app.meshViewStart+app.widthEachElement+5) and mousePosition[0]<app.width*app.meshViewStart):
        print('Object selected: Sphere')
        app.drawElement='Sphere'
        #get the size clicked
        index=(mousePosition[0]//(app.widthEachElement+5))+1
        print('Size index',index)
        app.slider=str(int(index))

    #if mouse clicked over the bezier icons
    elif (mousePosition[1]<(app.width*app.meshViewStart+2*app.widthEachElement+2*5) and mousePosition[0]<app.width*app.meshViewStart):
        if len(app.bezier.controlPointList)>2:
            app.printMessage=False
            print('Object selected: Bezier')
            app.drawElement='Bezier'
            #get the size clicked
            index=(mousePosition[0]//(app.widthEachElement+5))+1
            print('Size index',index)
            app.slider=str(int(index))
        else:
            app.printMessage=True

    
    


def mainMode_redrawAll(app, canvas):
    if app.printMessage:
        start=[5,2*app.widthEachElement+10+app.width*app.meshViewStart]
        canvas.create_text(start,text="You need to press 'b' to edit bezier curve before.", font='Arial 12 bold', anchor='nw')
    meshView(canvas,app)
    editionWindow(canvas,app)
    printButtonsSpheres(canvas,app)
    printButtonsBezier(canvas,app)


    
##############################################################################################################################
# ADVANCE EDITING OPTIONS#################
##########################################


#####################
# moveMode
#####################


def moveMode_redrawAll(app,canvas):
    meshView(canvas,app)
    

def moveMode_keyPressed(app,event):
    print(event.key)
    if event.key in app.advancedModeDictionary:
        app.mode=app.advancedModeDictionary[event.key]
        app.doubleView=False
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        app.doubleView=True
    #RESTART THE APP
    if event.key=='q':
        print('restarting app')
        appStarted(app)
    #SAVE OPTIONS
    if event.key=='s':
        print('saving mesh')
        saveCurrentMesh(app)
        

def moveMode_mouseDragged(app,event):
    mousePosition=(event.x ,event.y)
    #convert the point from the isometric view to global 2D
    mousePosition=isometricToTwoD(app,mousePosition)
    if app.movingPoint==None:
        tolerance=10
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
    if event.key in app.advancedModeDictionary:
        app.mode=app.advancedModeDictionary[event.key]
        app.doubleView=False
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        app.doubleView=True
    #RESTART THE APP
    if event.key=='q':
        print('restarting app')
        appStarted(app)
    #SAVE OPTIONS
    if event.key=='s':
        print('saving mesh')
        saveCurrentMesh(app)



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
    if event.key in app.advancedModeDictionary:
        app.mode=app.advancedModeDictionary[event.key]
        app.doubleView=False
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        app.doubleView=True
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
    #RESTART THE APP
    if event.key=='q':
        print('restarting app')
        appStarted(app)
    #SAVE OPTIONS
    if event.key=='s':
        print('saving mesh')
        saveCurrentMesh(app)
        
  
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
    if event.key in app.advancedModeDictionary:
        app.mode=app.advancedModeDictionary[event.key]
        app.doubleView=False
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        app.doubleView=True
    if event.key in ['Up','+']:
        print('zooming in')
        zoomIn(app,1.1)
    if event.key in ['Down','-']:
        print('zooming out')
        zoomOut(app,0.9)
    #RESTART THE APP
    if event.key=='q':
        print('restarting app')
        appStarted(app)
    #SAVE OPTIONS
    if event.key=='s':
        print('saving mesh')
        saveCurrentMesh(app)
        
  
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


###############
#BEZIER MODE
###############


def bezier_mousePressed(app, event):
    newPoint =  [event.x, event.y]
    newPoint=convertEditViewToBezierPoints(app,newPoint)
    if (abs(newPoint[0]>0.5 or newPoint[1]>0.5 )): 
        print('point outside box')
    else:
        #print('app.bezier.controlPointList',app.bezier.controlPointList)
        #print('app.bezier.bezierCurvePoints',app.bezier.bezierCurvePoints)
        #print('newPoint',newPoint)
        app.bezier.controlPointList.insert(len(app.bezier.controlPointList)-1,newPoint)
        #update the other variables of the app.bezier object
        app.bezier.bezierCurvePoints=app.bezier.bezierCurvePointList()
        app.bezier.bezierMeshPoints,app.bezier.bezierMeshFaces=app.bezier.bezierPointsAndFaces()
        app.bezier.stepV=(len(app.bezier.bezierCurvePoints)-1)
        app.bezier.points2D=threeDtotwoD(app.bezier.bezierMeshPoints,app.beziertheta_x,app.beziertheta_y)
        app.bezier.points2Dcopy=app.bezier.points2D

    

def bezier_redrawAll(app, canvas):
    #2D view
    margin=10
    canvas.create_rectangle(margin,margin,(app.meshViewStart*app.width*app.doubleView)-margin,(app.meshViewStart*app.width*app.doubleView)-margin,fill='#f2f2f2')
    canvas.create_text(app.margin, app.height-app.margin,
                       text='The first and last point in the curve are automatically placed. If you want them in a different position, you can move them', font='Arial 10 bold', anchor='sw')
    printBezierOptions(app,canvas)
    printModeDictionary(app, canvas)
    canvas.create_line(app.width*app.meshViewStart/2,app.margin,app.width*app.meshViewStart/2,app.width*app.meshViewStart-app.margin)
    drawPoints(app,canvas,app.bezier.controlPointList,color='gray')
    drawBezierCurve(canvas,app)
    #3D view
    displayFaces(app,canvas,app.bezier.points2Dcopy*300,app.bezier.bezierMeshFaces)
    displayPoints(app,canvas,app.bezier.points2Dcopy*300)
    printCenter(app,canvas)

def bezier_keyPressed(app, event):
    if event.key=='Up' or event.key=='Right':
        app.beziertheta_x+=10
        app.beziertheta_y+=10
        print('changing theta x,y: ',app.beziertheta_x,app.beziertheta_y)
        app.bezier.points2Dcopy=threeDtotwoD(app.bezier.bezierMeshPoints,app.beziertheta_x,app.beziertheta_y)
    if event.key=='Down' or event.key=='Left':
        app.beziertheta_x-=10
        app.beziertheta_y-=10
        print('changing theta x,y: ',app.beziertheta_x,app.beziertheta_y)
        app.bezier.points2Dcopy=threeDtotwoD(app.bezier.bezierMeshPoints,app.beziertheta_x,app.beziertheta_y)
    if event.key=='d':
        app.bezier.displayMesh()
    if event.key=='g':
        app.bezier.saveMesh() 
    if event.key in app.advancedModeDictionary:
        app.mode=app.advancedModeDictionary[event.key]
        app.doubleView=False
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        app.doubleView=True
    #RESTART THE APP
    if event.key=='q':
        print('restarting app')
        appStarted(app)
    #SAVE OPTIONS
    if event.key=='s':
        print('saving mesh')
        saveCurrentMesh(app)

###############
#MOVE BEZIER MODE
###############

def moveBezierMode_redrawAll(app,canvas):
    #2D view
    margin=10
    canvas.create_rectangle(margin,margin,(app.meshViewStart*app.width*app.doubleView)-margin,(app.meshViewStart*app.width*app.doubleView)-margin,fill='#f2f2f2')
    canvas.create_text(app.margin, app.height-app.margin,
                       text='The first and last point in the curve are automatically placed. If you want them in a different position, you can move them', font='Arial 10 bold', anchor='sw')
    printBezierOptions(app,canvas)
    printModeDictionary(app, canvas)
    canvas.create_line(app.width*app.meshViewStart/2,app.margin,app.width*app.meshViewStart/2,app.width*app.meshViewStart-app.margin)
    drawPoints(app,canvas,app.bezier.controlPointList,color='gray')
    drawBezierCurve(canvas,app)
    #3D view
    displayFaces(app,canvas,app.bezier.points2Dcopy*300,app.bezier.bezierMeshFaces)
    displayPoints(app,canvas,app.bezier.points2Dcopy*300)
    printCenter(app,canvas)
    
   
def moveBezierMode_mouseDragged(app,event):
    mousePosition=(event.x ,event.y)
    mousePosition=convertEditViewToBezierPoints(app,mousePosition)
    if app.movingPoint==None: 
        tolerance=20
        pointToMoveIndex=findClickedPoint(mousePosition,app.bezier.controlPointList,tolerance)
        if pointToMoveIndex!=None:
            app.movingPoint=pointToMoveIndex
        
    elif app.movingPoint!=None:
        #if first or last point in the list are clicke, we only update the y position, so they stay on the axis
        if app.movingPoint==0 or app.movingPoint==len(app.bezier.controlPointList)-1:
            app.bezier.controlPointList[app.movingPoint][1]=mousePosition[1]
        else:
            app.bezier.controlPointList[app.movingPoint]=mousePosition
        #####
        #update the other variables of the app.bezier object
        app.bezier.bezierCurvePoints=app.bezier.bezierCurvePointList()
        app.bezier.bezierMeshPoints,app.bezier.bezierMeshFaces=app.bezier.bezierPointsAndFaces()
        app.bezier.stepV=(len(app.bezier.bezierCurvePoints)-1)
        app.bezier.points2D=threeDtotwoD(app.bezier.bezierMeshPoints,app.beziertheta_x,app.beziertheta_y)
        app.bezier.points2Dcopy=app.bezier.points2D
        
  
def moveBezierMode_mouseReleased(app,event):
    mouseReleasedPosition=(event.x ,event.y)
    print('mouse released at:', mouseReleasedPosition)
    if app.movingPoint!=None:
        app.movingPoint=None

        
def moveBezierMode_keyPressed(app,event):
    print(event.key)
    if event.key=='Up' or event.key=='Right':
        app.beziertheta_x+=10
        app.beziertheta_y+=10
        print('changing theta x,y: ',app.beziertheta_x,app.beziertheta_y)
        app.bezier.points2Dcopy=threeDtotwoD(app.bezier.bezierMeshPoints,app.beziertheta_x,app.beziertheta_y)
    if event.key=='Down' or event.key=='Left':
        app.beziertheta_x-=10
        app.beziertheta_y-=10
        print('changing theta x,y: ',app.beziertheta_x,app.beziertheta_y)
        app.bezier.points2Dcopy=threeDtotwoD(app.bezier.bezierMeshPoints,app.beziertheta_x,app.beziertheta_y)
    if event.key=='d':
        app.bezier.displayMesh()
    if event.key=='g':
        app.bezier.saveMesh() 
    if event.key in app.advancedModeDictionary:
        app.mode=app.advancedModeDictionary[event.key]  
        app.doubleView=False  
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]
        app.doubleView=True
    #RESTART THE APP
    if event.key=='q':
        print('restarting app')
        appStarted(app)
    #SAVE OPTIONS
    if event.key=='s':
        print('saving mesh')
        saveCurrentMesh(app)

    
runApp(width=900, height=600)



