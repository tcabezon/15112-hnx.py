
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



