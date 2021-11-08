import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def rangeNumberSteps(start,end,numberSteps):
    result=list()
    for i in range(numberSteps+1):
        result.append(start+(end-start)*i/numberSteps)
    #print(result)
    return result

def sphereMesh(center=[0.,0.,0.],stepU=10,stepV=6,r=1):
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
                '''
                if col==stepU-1:
                    facesSphere[indexInMatrix,1]= ((row-1)*(stepU)+col+1)-stepU
                else:
                    facesSphere[indexInMatrix,1]= ((row-1)*(stepU)+col+1)
                print(facesSphere[indexInMatrix,:])'''

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

    # Create the mesh
    sphere = mesh.Mesh(np.zeros(facesSphere.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(facesSphere):
        for j in range(3):
            #print(i,j,f,cube.vectors[i][j])
            sphere.vectors[i][j] = pointsSphere[f[j],:]
            #print(cube.vectors[i][j])

    print(facesSphere)
    return sphere

#####################################################
center=[0.,0.,0.]
stepU=100
stepV=60
r=1
sphere1= sphereMesh()
sphere2= sphereMesh(center=[0.,0.,1.])

combined = mesh.Mesh(np.concatenate([sphere1.data, sphere2.data]))
combined.save('combined.stl')

ring = mesh.Mesh.from_file('ring.stl')









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

'''
#plotting
# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
axes.plot3D(pointsSphere[:,0], pointsSphere[:,1], pointsSphere[:,2], 'grey')
axes.scatter(center[0],center[1],center[2])
# Show the plot to the screen
pyplot.show()'''