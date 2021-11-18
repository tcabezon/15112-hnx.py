from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *
from bezierFunctions import *

def displayMesh(app):
    # generate the mesh
    bezierCurve=bezierCurvePointList(app.pointList,app.numberOfBezierPoints)
    bezierCurve=np.array(bezierCurve)
    bezierCurve[:,0]-=(app.width/2)
    bMesh = bezierMesh(bezierCurve,app.stepU)


    # SAVE THE MODEL
    bMesh.save('sphere.stl')


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

def bezier_appStarted(app):
    app.label = 'animation'
    app.pointList=[[app.width/2,app.height/4],[app.width/2,3*app.height/4]]
    app.numberOfBezierPoints=10
    app.bezierCurvePoints=None
    app.stepU=10


def bezier_mousePressed(app, event):
    newPoint =  [event.x, event.y]
    app.pointList.insert(len(app.pointList)-1,newPoint)
    
    

def bezier_redrawAll(app, canvas):
    drawPoints(canvas,app.pointList,color='gray')
    drawBezierCurve(canvas,app)


def bezier_keyPressed(app, event):
    if event.key=='s':
        displayMesh(app)

    
        


runApp(width=400, height=400, fnPrefix='bezier_')