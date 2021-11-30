import numpy as np
from stl import mesh
import math
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from functions import *


#####################################################
# PARAMETERS
#####################################################
center=[0.,0.,0.]
stepU=17
stepV=35
r=100

# generate the mesh
sphere= sphereMesh(center,stepU,stepV,r)


# SAVE THE MODEL
sphere.save('sphere.stl')


# PLOTTING
# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Add the vectors to the plot
#using matplot library to plot the 3D mesh
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(sphere.vectors, facecolors='b',edgecolors='k', linewidths=1, alpha=0.75))


# Auto scale to the mesh size
scale = sphere.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
#axes.scatter3D(vertices[:,0], vertices[:,1], vertices[:,2])

# Show the plot to the screen
pyplot.show()


