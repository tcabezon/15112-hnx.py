
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# Define the 8 vertices of the cube
vertices = np.array([\
    [0.5,0.5,0.5],
    [0,0,0],
    [1,0,0],
    [1,1,0],
    [0,1,0],
    [0.5,0.5,-0.5]])
# Define the 12 triangles composing the cube
faces = np.array([\
                [0,1,2],
                [0,2,3],
                [0,3,4],
                [0,4,1],
                [5,2,1],
                [5,3,2],
                [5,4,3],
                [5,1,4]])
    

# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
print(cube)
for i, f in enumerate(faces):
    for j in range(3):
        #print(i,j,f,cube.vectors[i][j])
        cube.vectors[i][j] = vertices[f[j],:]
        #print(cube.vectors[i][j])

# Write the mesh to file "cube.stl"
cube.save('cube.stl')


#plotting
# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube.vectors, facecolors='r',edgecolors='k', linewidths=1, alpha=0.75))
#axes.plot3D(vertices[:,0], vertices[:,1], vertices[:,2], 'gray')

# Auto scale to the mesh size
scale = cube.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
#axes.scatter3D(vertices[:,0], vertices[:,1], vertices[:,2])

# Show the plot to the screen
pyplot.show()