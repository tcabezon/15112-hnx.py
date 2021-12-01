from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# Functions used for the hnX.py main program,
# this includes functions to display, 
# to edit the mesh or 
# to convert point from 3D view, to 2D view or viceversa


def rangeNumberSteps(start,end,numberSteps):
    result=list()
    for i in range(numberSteps+1):
        result.append(start+(end-start)*i/numberSteps)
    #print(result)
    return result

def drawArrow(canvas,start, end, fill="red", width=3):

    canvas.create_line(start[0],start[1],end[0],end[1], fill=fill, width=width)


def threeDtotwoD(treeDPoints,theta_x=210,theta_y=330):
#def threeDtotwoD(treeDPoints,theta_x=100,theta_y=330):
    #inspired by 15-112 3D graphics mini lecture
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
    transformMatrix=np.array([[1,0],[0,-1]])
    originalCoordinates=np.copy(points)
    originalCoordinates3D=np.copy(app.vertices)
    originalCoordinates3D=originalCoordinates3D.astype(int)
    new_points=np.matmul(points,transformMatrix)
    new_points=new_points*app.scale
    for i in range(new_points.shape[0]):
        point=new_points[i]
        center=[(app.doubleView*app.width*app.meshViewStart)+((1-app.meshViewStart)*app.width)/2,app.height/2]
        cx=center[0]+point[0]
        cy=center[1]+point[1]
        canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill=color)
        
def twoDToIsometric(app,points):
    #inspired by 15-112 3D graphics mini lecture
    transformMatrix=np.array([[1,0],[0,-1]])
    points=np.matmul(points,transformMatrix)
    center=[(app.doubleView*app.width*app.meshViewStart)+((1-app.meshViewStart)*app.width)/2,app.height/2]
    points[0]+=center[0]
    points[1]+=center[1]
    return points

def isometricToTwoD(app,point):
    center=[(app.doubleView*app.width*app.meshViewStart)+((1-app.meshViewStart)*app.width)/2,app.height/2]
    x=-center[0]+point[0]
    y=-point[1]+center[1]
    x=x*(1/app.scale)
    y=y*(1/app.scale)
    return (x,y)

def isometricToTwoD_noScale(app,point):
    center=[(app.doubleView*app.width*app.meshViewStart)/2,(app.doubleView*app.width*app.meshViewStart)/2]
    x=-center[0]+point[0]
    y=-point[1]+center[1]
    return (x,y)



def displayFaces(app,canvas,vertices,faces):
    transformMatrix=np.array([[1,0],[0,-1]])
    vertices=np.matmul(vertices,transformMatrix)
    vertices=vertices*app.scale
    for i in range(faces.shape[0]):
        faceIndexes=faces[i]
        center=[(app.doubleView*app.width*app.meshViewStart)+((1-app.meshViewStart)*app.width)/2,app.height/2]
        point1=center+vertices[faceIndexes[0]]
        point2=center+vertices[faceIndexes[1]]
        point3=center+vertices[faceIndexes[2]]
        canvas.create_line(point1[0],point1[1],point2[0],point2[1])
        canvas.create_line(point1[0],point1[1],point3[0],point3[1])
        canvas.create_line(point2[0],point2[1],point3[0],point3[1])



def printCenter(app,canvas):
    [cx,cy]=[(app.doubleView*app.width*app.meshViewStart)+((1-app.meshViewStart)*app.width)/2,app.height/2]
    r=2
    canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill='red')
     
def findClickedPoint(mousePosition,points2D,tolerance=20):
    #find the closest point to the mouse position with a distance smaller than the tolerance
    closestPoint=None
    closestDistance=None
    for p in range(len(points2D)):
        point=points2D[p]
        currentDistance= distance(point, mousePosition)
        if currentDistance<tolerance:
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
    resultString='Press the following keys to enter\nthe different App Modes:\n'
    for elem in app.modeDictionary:
        resultString+='・ '+elem+': '+app.modeDictionary[elem]+'\n'
    resultString+="・ q: to restart\n"
    resultString+="\nFor advanced editing options, press:\n"
    for elem in app.advancedModeDictionary:
        resultString+='・ '+elem+': '+app.advancedModeDictionary[elem]+'\n'
    
    if app.doubleView==False:
        resultString+="\nYOUR ARE IN ADVANCE EDITING MODE,\nSOME FEATURES WILL BE SLOWER.\n\nRemember that if you add more elements \nto the mesh these changes will be deleted.\nPress 's' to save the current mesh."
        canvas.create_rectangle((app.meshViewStart*app.width)+(app.meshViewStart-0.1)*app.width*( not app.doubleView),0,app.width,app.height,fill='#f2f2f2')
        moveText=(app.meshViewStart*app.width*app.doubleView)
    canvas.create_text(app.margin+(app.meshViewStart*app.width)+(app.meshViewStart-0.1)*app.width*( not app.doubleView), app.margin,
                        text=resultString, font='Arial 12 bold', anchor='nw')
    
    canvas.create_text(app.width-app.margin, app.height-app.margin,
                       text=f'{app.mode}', font='Arial 12 bold', anchor='se')

def rotatePointsAngleH(app,alpha):
    #alpha is in degrees so we convert it to radians
    alpha=math.radians(alpha)
    for i in range(len(app.vertices)):
        point=app.vertices[i]
        module=math.sqrt(point[0]**2+point[1]**2)
        ########################################
        #getting the value of the angle for all the four cuadrants
        if point[0]==0:
            if point[1]>0:
                tetha=math.radians(90)
            else:
                tetha=math.radians(270)
        else:
            tetha=math.atan(point[1]/point[0])
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
        app.vertices[i][0]=newX
        app.vertices[i][1]=newY
        app.points2D=threeDtotwoD(app.vertices)

def rotatePointsAngleV(app,alpha):
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
    return maxX

def findMaxY(app):
    points2D=np.copy(app.points2D)
    # initialize to the first point
    maxX=abs(points2D[0][1])
    for i in range(len(points2D)):
        currentX=abs(points2D[i][1])
        if currentX>maxX:
            maxX=currentX
    return maxX

def zoomIn(app,scale):
    app.scale*=scale

def zoomOut(app,scale):
    app.scale*=scale

def zoom(app,scale):
    app.scale*=scale

def displayRing(app,canvas):
    cx=app.width/2
    cy=app.height/2
    diameter1=200
    diameter2=190
    canvas.create_oval(cx+diameter1/2,cy+diameter1/2,cx-diameter1/2,cy-diameter1/2,fill='gray')
    canvas.create_oval(cx+diameter2/2,cy+diameter2/2,cx-diameter2/2,cy-diameter2/2,fill='white')

def plotMesh(myMesh):
    # PLOTTING
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    # Add the vectors to the plot
    #using matplot library to plot the 3D mesh
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(myMesh.vectors, facecolors='b',edgecolors='k', linewidths=1, alpha=0.75))
    # Auto scale to the mesh size
    scale = myMesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    # Show the plot to the screen
    pyplot.show()

def displayPoints2D(app,canvas,r=2,color='green'):
    #we will only display the YZ plane 
    originalCoordinates3D=np.copy(app.ring.vertices[:,1:])
    new_points=originalCoordinates3D
    center=[(app.doubleView*app.width*app.meshViewStart)/2,(app.doubleView*app.width*app.meshViewStart)/2]
    for i in range(new_points.shape[0]):
        point=new_points[i]
        cx=center[0]+point[0]
        cy=center[1]-point[1]
        canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill=color)

def displayFaces2D(app,canvas):
    transformMatrix=np.array([[1,0],[0,-1]])
    points=np.copy(app.ring.vertices[:,1:])
    new_vertices=np.matmul(points,transformMatrix)
    for i in range(app.ring.faces.shape[0]):
        faceIndexes=app.ring.faces[i]
        center=[(app.doubleView*app.width*app.meshViewStart)/2,(app.doubleView*app.width*app.meshViewStart)/2]
        point1=center+new_vertices[faceIndexes[0]]
        point2=center+new_vertices[faceIndexes[1]]
        point3=center+new_vertices[faceIndexes[2]]
        canvas.create_line(point1[0],point1[1],point2[0],point2[1])
        canvas.create_line(point1[0],point1[1],point3[0],point3[1])
        canvas.create_line(point2[0],point2[1],point3[0],point3[1])


def mousePressedInsideRing(app,mousePosition):
    distanceToCenter=distance((0,0),mousePosition)
    if (distanceToCenter<(app.ring.innerRadious+2*app.ring.ringRadious)
        and distanceToCenter>(app.ring.innerRadious)):
        return True
    else: return False


def saveCurrentMesh(app):
    # Create the mesh
    #this function uses the numpy stl library mesh function (from stl import mesh)
    myMesh = mesh.Mesh(np.zeros(app.faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(app.faces):
        for j in range(3):
            myMesh.vectors[i][j] = app.vertices[f[j],:]
    print('Current mesh saved as currentMesh.stl')
    myMesh.save('currentMesh.stl')


def convertEditViewToBezierPoints(app,point):
    newPointY=((app.meshViewStart*app.width*app.doubleView)/2-point[1])/(app.meshViewStart*app.width*app.doubleView)
    newPointX=(point[0]-(app.meshViewStart*app.width*app.doubleView)/2)/(app.meshViewStart*app.width*app.doubleView)
    return [newPointX,newPointY]

def meshView(canvas,app):
    printModeDictionary(app, canvas)
    displayFaces(app,canvas,app.points2D,app.faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)

def editionWindow(canvas,app):
    margin=5
    canvas.create_rectangle(margin,margin,(app.meshViewStart*app.width*app.doubleView)-margin,(app.meshViewStart*app.width*app.doubleView)-margin,fill='#f2f2f2')
    displayFaces2D(app,canvas)
    displayPoints2D(app,canvas)
    printCenter(app,canvas)
    
def printSizesDictionary(app,canvas):
    resultString='Press the following keys to change\nthe different radious:\n'
    for elem in app.sliderDictionary:
        resultString+=elem+': '+str(app.sliderDictionary[elem])+'\n'
    canvas.create_text(app.width-app.margin, app.margin,
                       text=resultString, font='Arial 12 bold', anchor='ne')
    
def printButtonsSpheres(canvas,app,color='#f2f2f2'):
    margin=5 #same as meshView, buttonsBezier
    numberOfButtons=app.numberOfButtons
    widthEachElement=(app.width*app.meshViewStart-(numberOfButtons+1)*margin)/numberOfButtons
    for i in range(numberOfButtons):
        start=[margin+(i*(widthEachElement+margin)),app.width*app.meshViewStart]
        end=[margin+(i*(widthEachElement+margin))+widthEachElement,app.width*app.meshViewStart+widthEachElement]
        if (i+1==int(app.slider) and app.drawElement=='Sphere'):
            canvas.create_rectangle(start,end,fill='black')
            (cx,cy)=((end[0]-start[0])/2+start[0],(end[1]-start[1])/2+start[1])
            r=i*5+5
            canvas.create_oval(cx+r,cy+r,cx-r,cy-r,outline='#f2f2f2')
        else:
            canvas.create_rectangle(start,end,fill='#f2f2f2')
            (cx,cy)=((end[0]-start[0])/2+start[0],(end[1]-start[1])/2+start[1])
            r=(i+1)*5
            canvas.create_oval(cx+r,cy+r,cx-r,cy-r)

def printButtonsBezier(canvas,app,color='#f2f2f2'):
    margin=5 #same as meshView, buttonsSpher
    numberOfButtons=app.numberOfButtons
    widthEachElement=(app.width*app.meshViewStart-(numberOfButtons+1)*margin)/numberOfButtons
    for i in range(numberOfButtons):
        start=[margin+(i*(widthEachElement+margin)),widthEachElement+margin+app.width*app.meshViewStart]
        end=[margin+(i*(widthEachElement+margin))+widthEachElement,widthEachElement+margin+app.width*app.meshViewStart+widthEachElement]
        if len(app.bezier.controlPointList)==2:
            canvas.create_rectangle(start,end,fill='#f2f2f2')
            (cx,cy)=((end[0]-start[0])/2+start[0],(end[1]-start[1])/2+start[1])
            canvas.create_text(cx,cy,text='bezier\ncurve', font='Arial 10')
        else:    
            if (i+1==int(app.slider) and app.drawElement=='Bezier'):
                canvas.create_rectangle(start,end,fill='black')
                (cx,cy)=((end[0]-start[0])/2+start[0],(end[1]-start[1])/2+start[1])
                r=(i+1)/numberOfButtons
                bezierCurvePoints1DList=pointsRespectToCenter(app.bezier.bezierCurvePoints,cx,cy,widthEachElement*r)
                canvas.create_polygon(bezierCurvePoints1DList,outline='#f2f2f2')
            else:
                canvas.create_rectangle(start,end,fill='#f2f2f2')
                (cx,cy)=((end[0]-start[0])/2+start[0],(end[1]-start[1])/2+start[1])
                r=(i+1)/numberOfButtons
                bezierCurvePoints1DList=pointsRespectToCenter(app.bezier.bezierCurvePoints,cx,cy,widthEachElement*r)
                canvas.create_polygon(bezierCurvePoints1DList,outline='black',fill='#f2f2f2')

def convertListTo1D(list2D):
    list1D=[]
    for row in range(len(list2D)):
        for col in range(len(list2D[row])):
            num=list2D[row][col]*500 +300
            list1D.append(num)
    return list1D

def pointsRespectToCenter(bezierCurvePoints,cx,cy,scale):
    #this function draws the polygon thar shows the 3D bezier object in 2D
    newList=[]
    for point in bezierCurvePoints:
        pointX=point[0]*scale+cx
        newList.append(pointX)
        pointY=-point[1]*scale+cy
        newList.append(pointY)
    #backwards to mirror the curve points
    for i in range(len(bezierCurvePoints)):
        backwardsIndex=len(bezierCurvePoints)-1-i
        pointX=-bezierCurvePoints[backwardsIndex][0]*scale+cx
        newList.append(pointX)
        pointY=-bezierCurvePoints[backwardsIndex][1]*scale+cy
        newList.append(pointY)   
    return newList

def scaleControlPoints(pointList,scale):
    scaledPoints=[]
    for point in pointList:
        px=point[0]*scale
        py=point[1]*scale
        scaledPoints.append([px,py])
    return scaledPoints

###############################
# BEZIER FUNCTIONS


def drawBezierCurve(canvas,app):
    bezierCurve=app.bezier.bezierCurvePoints
    drawPoints(app,canvas,bezierCurve,'blue')
    
#draw a list of points in 2D
def drawPoints(app,canvas,pointList,color='black'):
    r=2
    for i in range(len(pointList)):
        (cx, cy) = np.array(pointList[i])*(app.width*app.meshViewStart)
        (cx,cy) = ((app.width*app.meshViewStart)/2+cx,(app.width*app.meshViewStart)/2-cy)
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color)
        if i!=0:
            canvas.create_line((cx, cy),previousPoint,fill=color)
        previousPoint= (cx,cy)
  
def printBezierOptions(app,canvas):
    canvas.create_text(app.margin, app.width*app.meshViewStart,
                       text=f'Press:\nd, to display the mesh\ng, to save the .stl file', font='Arial 10 bold', anchor='nw')
def displayMesh(app):
    # generate the mesh
    bezierCurve=bezierCurvePointList(app.pointList,app.numberOfBezierPoints)
    bezierCurve=np.array(bezierCurve)
    bezierCurve[:,0]-=(app.width/2)
    bMesh = bezierMesh(bezierCurve,app.stepBezier)

    # PLOTTING
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    # Add the vectors to the plot
    #using matplot library to plot the 3D mesh
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(-bMesh.vectors, facecolors='b',edgecolors='k', linewidths=1, alpha=0.75))


    # Auto scale to the mesh size
    scale = bMesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    
    axes.scatter(0,-bezierCurve[:,0], -bezierCurve[:,1])

    # Show the plot to the screen
    pyplot.show()