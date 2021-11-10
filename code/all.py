from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *

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
'''
combined = mesh.Mesh(np.concatenate([sphere1.data, sphere2.data]))
combined.save('combined.stl')
'''


'''
# Write the mesh to file "cube.stl"
#sphere1.save('sphere1.stl')
#sphere2.save('sphere2.stl')

#plotting
# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(ring.vectors, facecolors='r',edgecolors='k', linewidths=1, alpha=0.75))
#axes.add_collection3d(mplot3d.art3d.Poly3DCollection(sphere2.vectors, facecolors='b',edgecolors='k', linewidths=1, alpha=0.75))
#axes.plot3D(vertices[:,0], vertices[:,1], vertices[:,2], 'gray')

# Auto scale to the mesh size
scale = ring.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
#axes.scatter3D(vertices[:,0], vertices[:,1], vertices[:,2])

# Show the plot to the screen
pyplot.show()

#plotting
# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
axes.plot3D(pointsSphere[:,0], pointsSphere[:,1], pointsSphere[:,2], 'grey')
axes.scatter(center[0],center[1],center[2])
# Show the plot to the screen
pyplot.show()'''