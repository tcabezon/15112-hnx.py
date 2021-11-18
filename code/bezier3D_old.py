import numpy as np
from stl import mesh
import math
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from functions import *
from bezierFunctions import *


#####################################################
# PARAMETERS
#####################################################
center=[0.,0.,0.]
stepU=10
stepV=10
r=100

bezierCurvePoints=np.array([[608.0, 88.0], [673.7143728090227, 75.27853138918522], [720.4910836762689, 86.32528916662434], [748.3209876543212, 113.47325102880662], [757.9448254839201, 149.73008857050925], [750.8898033836306, 189.31670307710544], [729.5061728395062, 228.2057613168724], [697.003810394757, 264.66023133329946], [657.4887974394146, 299.771918237396], [608.0, 338.0]])
minY=np.min(bezierCurvePoints[:,1])
print(minY)
bezierCurvePoints[:,1]-=75.27853138918522
bezierCurvePoints[:,0]-=608. 
print(bezierCurvePoints)
# generate the mesh
bMesh = bezierMesh(bezierCurvePoints,stepU)


# SAVE THE MODEL
bMesh.save('correct.stl')


# PLOTTING
# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Add the vectors to the plot
#using matplot library to plot the 3D mesh
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(bMesh.vectors, facecolors='b',edgecolors='k', linewidths=1, alpha=0.75))


# Auto scale to the mesh size
scale = bMesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
axes.scatter(0,bezierCurvePoints[:,0], bezierCurvePoints[:,1])

# Show the plot to the screen
pyplot.show()



#vertices=np.array([[608.0, 88.0], [673.7143728090227, 75.27853138918522], [720.4910836762689, 86.32528916662434], [748.3209876543212, 113.47325102880662], [757.9448254839201, 149.73008857050925], [750.8898033836306, 189.31670307710544], [729.5061728395062, 228.2057613168724], [697.003810394757, 264.66023133329946], [657.4887974394146, 299.771918237396], [608.0, 338.0]])
