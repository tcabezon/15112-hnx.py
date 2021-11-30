from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def ring_displayPoints(app,canvas,points,r=2,color='green'):
    transformMatrix=np.array([[1,0],[0,-1]])
    originalCoordinates=np.copy(points)
    originalCoordinates3D=np.copy(app.vertices)
    #originalCoordinates3D=originalCoordinates3D.astype(int)
    new_points=np.matmul(points,transformMatrix)
    new_points=new_points*app.scale
    for i in range(new_points.shape[0]):
        point=new_points[i]
        cx=app.width/2+point[0]
        cy=app.height/2+point[1]
        canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill=color)
        canvas.create_text(cx,cy,text='({:.0f},{:.0f})'.format(originalCoordinates[i][0],originalCoordinates[i][1]),font='Arial 10 bold',anchor='sw')
        canvas.create_text(cx+10,cy+10,text='({:.0f},{:.0f},{:.0f})'.format(originalCoordinates3D[i][0],originalCoordinates3D[i][1],originalCoordinates3D[i][2]),fill='blue',font='Arial 10 bold',anchor='sw')
