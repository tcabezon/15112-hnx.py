from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *
from bezierFunctions import *
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
'''
def appStarted(app):
    app.mode='bezier'
    app.modeDictionary={'m':'moveBezierMode',
                        'b':'bezier'}
    app.margin=10
    app.pointList=[[app.width/2,app.height/4],[app.width/2,3*app.height/4]]
    app.numberOfBezierPoints=20
    app.bezierCurvePoints=None
    app.stepBezier=10
    app.movingPoint=None

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
    if event.key=='s':
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
    if event.key=='s':
        saveMesh(app) 
    if event.key in app.modeDictionary:
        app.mode=app.modeDictionary[event.key]

    
runApp(width=600, height=600)

'''
Things that could be improved:
Adding the points to the bezier curve control points not in order but depending 
on the rest of the points. This is, if the user clicks betweeen points with index 2 and 3, 
the new point should be added to the list with index 3, not at the end
'''