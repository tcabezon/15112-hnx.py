from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

vertices = np.array([[ 5.00000000e+01,  0.00000000e+00 , 1.50000000e+02],
 [ 3.53553391e+01 , 0.00000000e+00 , 1.85355339e+02],
 [ 3.06161700e-15 , 0.00000000e+00  ,2.00000000e+02],
 [-3.53553391e+01 , 0.00000000e+00 , 1.85355339e+02],
 [-5.00000000e+01 , 0.00000000e+00 , 1.50000000e+02],
 [-3.53553391e+01 , 0.00000000e+00 , 1.14644661e+02],
 [-9.18485099e-15 , 0.00000000e+00 , 1.00000000e+02],
 [ 3.53553391e+01 , 0.00000000e+00 , 1.14644661e+02]])

def appStarted(app):
     pass

def redrawAll(app, canvas):
    displayPoints(app,canvas,vertices)
   



def displayPoints(app,canvas,points):
    for point in points:
        cx=app.width/2+point[0]
        cy=app.height/2+point[2]
        r=2
        canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill='red')
    pass

runApp(width=600, height=600)