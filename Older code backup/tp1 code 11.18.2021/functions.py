from cmu_112_graphics import *
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
    #this function uses the numpy stl library mesh function (from stl import mesh)
    sphere = mesh.Mesh(np.zeros(facesSphere.shape[0], dtype=mesh.Mesh.dtype))

    for i, f in enumerate(facesSphere):
        for j in range(3):
            #print(i,j,f,cube.vectors[i][j])
            sphere.vectors[i][j] = pointsSphere[f[j],:]
            #print(cube.vectors[i][j])

    #print(facesSphere)
    return sphere

def drawArrow(canvas,start, end, fill="red", width=3):
    canvas.create_line(start[0],start[1],end[0],end[1], fill=fill, width=width)


def threeDtotwoD(treeDPoints,theta_x=210,theta_y=330):

    transformationMatrix=[\
                        [ math.cos(math.radians(theta_x)),math.sin(math.radians(theta_x))],
                        [ math.cos(math.radians(theta_y)),math.sin(math.radians(theta_y))],
                        [ 0, 1]]
    twoDPoints=np.matmul(treeDPoints,transformationMatrix)
    return twoDPoints


def newtwoDToThreeD_NoZChange(twoDPoints,treeDPoints,theta_x=210,theta_y=330):
    getZ=np.array([[0,0,0],[0,0,1]])
    #print(treeDPoints)
    onlyZ=np.matmul(getZ,treeDPoints.transpose())
    xY=twoDPoints-onlyZ.transpose()
    #print(xY)
    matrix=np.array([[ math.cos(math.radians(theta_x)),math.sin(math.radians(theta_x))],
                        [ math.cos(math.radians(theta_y)),math.sin(math.radians(theta_y))]])
    inverse = np.linalg.inv(matrix)
    mult=np.matmul(xY,inverse)
    getXY=np.array([[1,0,0],[0,1,0]])
    getZ=np.array([[0,0,0],[0,0,0],[0,0,1]])
    z=np.matmul(treeDPoints,getZ)
    x_y=np.matmul(mult,getXY)
    return (x_y+z)

def newtwoDToThreeD_zChange(twoDPoints,treeDPoints,theta_x=210,theta_y=330):
    getZ=twoDPoints[1]-treeDPoints[1]*math.sin(math.radians(theta_y))-treeDPoints[0]*math.sin(math.radians(theta_x))
    treeDPoints[2]=getZ
    return treeDPoints

def displayPoints(app,canvas,points,r=2,color='green'):
    np.set_printoptions(precision=1)
    transformMatrix=np.array([[1,0],[0,-1]])
    originalCoordinates=np.copy(points)
    originalCoordinates3D=np.copy(app.vertices)

    #originalCoordinates3D=originalCoordinates3D.astype(int)
    points=np.matmul(points,transformMatrix)
    for i in range(points.shape[0]):
        point=points[i]
        cx=app.width/2+point[0]
        cy=app.height/2+point[1]
        canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill=color)
        canvas.create_text(cx,cy,text='({:.0f},{:.0f})'.format(originalCoordinates[i][0],originalCoordinates[i][1]),font='Arial 10 bold',anchor='sw')
        canvas.create_text(cx+10,cy+10,text='({:.0f},{:.0f},{:.0f})'.format(originalCoordinates3D[i][0],originalCoordinates3D[i][1],originalCoordinates3D[i][2]),fill='blue',font='Arial 10 bold',anchor='sw')

def twoDToIsometric(app,points):
    transformMatrix=np.array([[1,0],[0,-1]])
    points=np.matmul(points,transformMatrix)
    points[0]+=app.width/2
    points[1]+=app.height/2
    return points

def isometricToTwoD(app,point):
    x=-app.width/2+point[0]
    y=-point[1]+app.height/2
    return (x,y)



def displayFaces(app,canvas,vertices,faces):
    transformMatrix=np.array([[1,0],[0,-1]])
    vertices=np.matmul(vertices,transformMatrix)
    for i in range(faces.shape[0]):
        faceIndexes=faces[i]
        #print(f'face {i}: ',faceIndexes)
        center=[app.width/2,app.height/2]
        point1=center+vertices[faceIndexes[0]]
        point2=center+vertices[faceIndexes[1]]
        point3=center+vertices[faceIndexes[2]]
        #print(point1, point2, point3)
        canvas.create_line(point1[0],point1[1],point2[0],point2[1])
        canvas.create_line(point1[0],point1[1],point3[0],point3[1])
        canvas.create_line(point2[0],point2[1],point3[0],point3[1])



def printCenter(app,canvas):
    cx=app.width/2
    cy=app.height/2
    r=2
    canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill='red')
     
def findClickedPoint(mousePosition,points2D,tolerance=20):
    #print('findingClosestPoint')
    #find the closest point to the mouse position with a distance smaller than the tolerance
    closestPoint=None
    closestDistance=None
    for p in range(len(points2D)):
        point=points2D[p]
        #print(p,point)
        currentDistance= distance(point, mousePosition)
        if currentDistance<tolerance:
            #print('found!')
            if closestDistance==None:
                closestPoint=p
                closestDistance=currentDistance
            else:
                if currentDistance<closestDistance:
                    closestPoint=p
                    closestDistance=currentDistance
    print(f'closest point: {closestPoint}')
    return closestPoint

            
def distance(point1,point2):
    distance=math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    return distance

def printModeDictionary(app, canvas):
    
    #canvas.create_text(app.margin, app.margin,text="printing dictionary", font='Arial 10 bold', anchor='nw')
    resultString='Press the following keys to enter\nthe different App Modes:\n'
    for elem in app.modeDictionary:
        resultString+=elem+': '+app.modeDictionary[elem]+'\n'
    canvas.create_text(app.margin, app.margin,
                       text=resultString, font='Arial 10 bold', anchor='nw')
    
    canvas.create_text(app.margin, app.height-app.margin,
                       text=f'{app.mode}', font='Arial 10 bold', anchor='sw')

def rotatePointsAngleH(app,alpha):
    #alpha is in degrees so we convert it to radians
    alpha=math.radians(alpha)
    #print(alpha)
    
    for i in range(len(app.vertices)):
        #print('rotating point ',i,' from ',len(app.vertices))
        point=app.vertices[i]
        #print(point)
        module=math.sqrt(point[0]**2+point[1]**2)
        ############################
        if point[0]==0:
            if point[1]>0:
                tetha=math.radians(90)
            else:
                tetha=math.radians(270)
        else:
            tetha=math.atan(point[1]/point[0])
            #print('tetha',math.degrees(tetha))
            if point[0]>0: #x>0
                if point[1]>0: #y>0
                    tetha=tetha #no changes
                else: #y<0
                    tetha=math.radians(360)+tetha       
            else: #x<0
                if point[1]>0: #y>0
                    tetha=math.radians(180)+tetha 
                else: #y<0
                    tetha=math.radians(180)+tetha 
        #print('tetha=',math.degrees(tetha))
        ########################################
        
        newX=module*math.cos(tetha+alpha)
        newY=module*math.sin(tetha+alpha)
        #print('new point:', newX,newY)
        app.vertices[i][0]=newX
        app.vertices[i][1]=newY
        app.points2D=threeDtotwoD(app.vertices)
'''
def rotatePointsAngleV(app,alpha):
    print(alpha)
    #alpha is in degrees so we convert it to radians
    alpha=math.radians(alpha)
    print(alpha)
    #rotating matrix, math from the rotation matrix in wikipedia
    #https://en.wikipedia.org/wiki/Rotation_matrix
    rotation_matrix=np.array([[math.cos(alpha)+0.5*(1-math.cos(alpha)),-0.5*(1-math.cos(alpha)),(-1/math.sqrt(2))*math.sin(alpha)],
                              [-0.5*(1-math.cos(alpha)),math.cos(alpha)+0.5*(1-math.cos(alpha)),(-1/math.sqrt(2))*math.sin(alpha)],
                              [(1/math.sqrt(2))*math.sin(alpha),(1/math.sqrt(2))*math.sin(alpha),math.cos(alpha)]])
    
    result=np.matmul(app.vertices,rotation_matrix)
    app.vertices=np.copy(result)
'''
def rotatePointsAngleV(app,alpha):
    #print(alpha)
    #alpha is in degrees so we convert it to radians
    alpha=math.radians(alpha)
    #rotating matrix, math from the rotation matrix and quaternions in wikipedia
    # https://en.wikipedia.org/wiki/Rotation_matrix
    # https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
    # https://stackoverflow.com/questions/6721544/circular-rotation-around-an-arbitrary-axis answer by user1205577
    
    
    #rotation_vector
    (a,b,c)=(1/math.sqrt(2),-1/math.sqrt(2),0)
    #rotating angle
    r=alpha
    q0 = math.cos(r/2)
    q1 = math.sin(r/2)*a
    q2 = math.sin(r/2)*b
    q3 = math.sin(r/2)*c
    rotation_matrix=np.array([[q0**2+q1**2-q2**2-q3**2,2*(q1*q2 - q0*q3), 2*(q1*q3 + q0*q2)],
                       [2*(q2*q1 + q0*q3),     q0**2-q1**2+q2**2-q3**2 ,     2*(q2*q3 - q0*q1)],
                       [2*(q3*q1 - q0*q2),          2*(q3*q2 + q0*q1),     q0**2-q1**2-q2**2+q3**2]])
    '''
    #simpler version if the rotation axis is (1/math.sqrt(2),-1/math.sqrt(2),0)
    rotation_matrix=np.array([[math.cos(alpha)+0.5*(1-math.cos(alpha)),-0.5*(1-math.cos(alpha)),(-1/math.sqrt(2))*math.sin(alpha)],
                              [-0.5*(1-math.cos(alpha)),math.cos(alpha)+0.5*(1-math.cos(alpha)),(-1/math.sqrt(2))*math.sin(alpha)],
                              [(1/math.sqrt(2))*math.sin(alpha),(1/math.sqrt(2))*math.sin(alpha),math.cos(alpha)]])
    '''
    result=np.matmul(rotation_matrix,app.vertices.transpose())
    app.vertices=result.transpose()
    app.points2D=threeDtotwoD(app.vertices)
    

def findMaxX(app):
    points2D=np.copy(app.points2D)
    # initialize to the first point
    maxX=abs(points2D[0][0])
    for i in range(len(points2D)):
        currentX=abs(points2D[i][0])
        if currentX>maxX:
            maxX=currentX
    #print('maxX2D',maxX)
    #maxX=maxX*math.cos(math.radians(30))
    #print('maxXisometric',maxX)
    return maxX

def findMaxY(app):
    points2D=np.copy(app.points2D)
    # initialize to the first point
    maxX=abs(points2D[0][1])
    for i in range(len(points2D)):
        currentX=abs(points2D[i][1])
        if currentX>maxX:
            maxX=currentX
    #print('maxX2D',maxX)
    #maxX=maxX*math.cos(math.radians(30))
    #print('maxXisometric',maxX)
    return maxX






    
