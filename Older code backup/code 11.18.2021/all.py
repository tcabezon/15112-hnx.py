from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *

#####################################################
#parameters
#####################################################
center=[0.,0.,0.] 
stepU=10
stepV=10
r=100
pointsSphere,facesSphere= spherePointsAndFaces(center,stepU,stepV,r)
theta_x=210
theta_y=330
pointsSphere2D=threeDtotwoD(pointsSphere,theta_x,theta_y)


def appStarted(app):
    app.draw=False
  
def keyPressed(app, event):
    app.draw=not app.draw

def redrawAll(app, canvas):
    if app.draw:
        displayFaces(app,canvas,pointsSphere2D,facesSphere)
        displayPoints(app,canvas,pointsSphere2D)
    canvas.create_text(app.width/2, app.height-30,
                       text=f'press any key to stop or start drawing\napp.draw = {app.draw}', font='Arial 10 bold')
    

runApp(width=400, height=400)
