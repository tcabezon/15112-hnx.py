import numpy as np
from stl import mesh
import math
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from functions import *

'''
def rangeNumberSteps(start,end,numberSteps):
    result=list()
    for i in range(numberSteps+1):
        result.append(start+(end-start)*i/numberSteps)
    #print(result)
    return result

def spherePointsAndFaces(center=[0.,0.,0.],stepU=10,stepV=6,r=1):
    #stepU xy plane divisions
    # stepV z axisdivisions

    #generate 'body'
    pointsSphere=np.zeros((((stepV-1)*(stepU)),3))
    facesSphere=np.zeros((((stepV-2)*(stepU))*2,3), dtype=int)

    for row, v in enumerate(rangeNumberSteps(math.pi/stepV,
                                                math.pi-(math.pi/stepV),stepV-2)):
        for col, u in enumerate(rangeNumberSteps(0,2*math.pi-(2*math.pi/stepU)
                                                        ,stepU-1)):
            
            #add points to the pointsSphere matrix
            indexInMatrix= row*(stepU)+col
            pointsSphere[indexInMatrix,0]=center[0]+r*math.sin(v)*math.cos(u)
            pointsSphere[indexInMatrix,1]=center[1]+r*math.sin(v)*math.sin(u)
            pointsSphere[indexInMatrix,2]=center[2]+r*math.cos(v)
            
            #add faces to the facesSphere matrix
            if row!=0:
                #top triangle
                facesIndexTop= (row-1)*(2*stepU)+stepU+col
                facesSphere[facesIndexTop,0]= (row*(stepU)+col)
                facesSphere[facesIndexTop,1]= ((row-1)*(stepU)+(col+1)%stepU)
                facesSphere[facesIndexTop,2]= ((row-1)*(stepU)+col)
                
                #bottom triangle
                facesIndexBottom= (row-1)*(2*stepU)+col
                facesSphere[facesIndexBottom,0]= (row*(stepU)+col)
                facesSphere[facesIndexBottom,1]= ((row)*(stepU)+(col+1)%stepU)
                facesSphere[facesIndexBottom,2]= ((row-1)*(stepU)+(col+1)%stepU)

    #generate top and bottom vertex of the sphere
    topVertexSphere=np.array([[center[0],center[1],center[2]+r]])
    bottomVertexSphere=np.array([[center[0],center[1],center[2]-r]])
    #generate top and bottom faces of the sphere
    topFacesSphere=np.zeros((stepU,3), dtype=int)
    bottomFacesSphere=np.zeros((stepU,3), dtype=int)
    bottomVertexIndex=((stepV-1)*(stepU)+1)
    topVertexIndex=0
    for i in range(stepU):
        #top faces
        topFacesSphere[i,0]=topVertexIndex
        topFacesSphere[i,1]=i+1
        topFacesSphere[i,2]=(i+1)%stepU+1
        #bottom faces
        bottomFacesSphere[i,0]=bottomVertexIndex
        bottomFacesSphere[i,1]=((stepV-1)*(stepU)+1)+(i+1)%stepU-stepU
        bottomFacesSphere[i,2]=bottomVertexIndex-stepU+i


    #result

    #CONCATENATE THE POINTS
    pointsSphere= np.concatenate((topVertexSphere, pointsSphere,bottomVertexSphere), axis=0)

    #CONCATENATE THE FACES
    #we add 1 to all the elements in the facesSphere matrix because the first 
    #element in the result matrix will be the top vertex
    facesSphere=facesSphere+1

    facesSphere= np.concatenate((topFacesSphere, facesSphere,bottomFacesSphere), axis=0)
    return pointsSphere,facesSphere

def sphereMesh(center=[0.,0.,0.],stepU=10,stepV=6,r=1):
    pointsSphere,facesSphere=spherePointsAndFaces(center,stepU,stepV,r)
    # Create the mesh
    sphere = mesh.Mesh(np.zeros(facesSphere.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(facesSphere):
        for j in range(3):
            #print(i,j,f,cube.vectors[i][j])
            sphere.vectors[i][j] = pointsSphere[f[j],:]
            #print(cube.vectors[i][j])

    print(facesSphere)
    return sphere

'''
#####################################################
# PARAMETERS
#####################################################
center=[0.,0.,0.]
stepU=10
stepV=10
r=100

# generate the mesh
sphere= sphereMesh(center,stepU,stepV,r)

'''
# SAVE THE MODEL
sphere.save('sphere.stl')
'''

# PLOTTING
# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Add the vectors to the plot
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(sphere.vectors, facecolors='b',edgecolors='k', linewidths=1, alpha=0.75))


# Auto scale to the mesh size
scale = sphere.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
#axes.scatter3D(vertices[:,0], vertices[:,1], vertices[:,2])

# Show the plot to the screen
pyplot.show()
