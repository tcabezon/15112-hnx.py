# #FUNCTIONS AND CLASSES
from hnXfunctions import *
from sphereClass import *
from bezier3DClass import *
from ringClass import *

#GRAPHICS
from cmu_112_graphics import *

#OTHER LIBRARIES
from matplotlib import pyplot
import numpy as np
from stl import mesh
import math
import stl

def calculateNormal(point0,point1,point2):
    vector1=point1-point0
    vector2=point2-point0
    normal=np.cross(vector1.transpose(),vector2)
    return normal 

sphere1=Sphere(20,stepU=3,stepV=3)

print('vertices',sphere1.vertices)
print('faces',sphere1.faces)

with open('tomas.stl','w') as output:
    sys.stdout=output
    print('solid tomas.stl')
    for face in sphere1.faces:
        normal=calculateNormal(sphere1.vertices[face[0]],sphere1.vertices[face[1]],sphere1.vertices[face[2]])
        print('facet normal ',normal[0],normal[1],normal[2])
        print('  outer loop')
        print('    vertex ',sphere1.vertices[face[0]][0],sphere1.vertices[face[0]][1],sphere1.vertices[face[0]][2])
        print('    vertex ',sphere1.vertices[face[1]][0],sphere1.vertices[face[1]][1],sphere1.vertices[face[1]][2])
        print('    vertex ',sphere1.vertices[face[2]][0],sphere1.vertices[face[2]][1],sphere1.vertices[face[2]][2])
        print('  endloop')        
        print('endfacet')   
    print('endsolid tomas.stl')     



