import math
from functions import *

np.set_printoptions(precision=1)
x=-3
y=5
print(math.degrees(math.atan(y/x)))

def printPoints(app,canvas):
    r=2
    for i in range(len(app.vertices)):
        point=app.vertices[i]
        cx=app.width/2+point[0]
        cy=app.height/2-point[1]
        canvas.create_oval(cx+r,cy+r,cx-r,cy-r,fill='blue')
        canvas.create_text(cx+10,cy+10,text=f'{i}: ({app.vertices[i][0]},{app.vertices[i][1]},{app.vertices[i][2]})',fill='blue',font='Arial 10 bold',anchor='sw')

verticesStart = np.array([\
    [(1/math.sqrt(2))*100,(-1/math.sqrt(2))*100,(-1/math.sqrt(2)*(-1/math.sqrt(2)))],
    [100,0,0],
    [100,100,0],
    [0,100,0]])

verticessStart=verticesStart.astype(float)

unit_vector=np.array([[1/math.sqrt(2),1/math.sqrt(2)]])
print(unit_vector)
print(unit_vector.shape)

points=np.array([\
    [0,0,0],
    [100,0,0],
    [100,100,0],
    [0,100,0]])
points=points.astype(float)
print(points)

for i in range(len(points)):
    point=points[i][0:2]
    print(point)
    distance=np.matmul(point,unit_vector.transpose())
    print(distance)

from cmu_112_graphics import *

def appStarted(app):
    app.counter = 0
    app.vertices=np.copy(verticesStart)

def keyPressed(app, event):
    angle=45
    if event.key=='Up':
        print('rotatin 1dregree right')
        rotatePointsAngleV(app,angle)
    if event.key=='Down':
        print('rotatin 1dregree right')
        rotatePointsAngleV(app,-angle)

def redrawAll(app, canvas):
    canvas.create_line(0,0,math.sqrt(2)*10,math.sqrt(2)*10,fill='red',width=3)
    cx=app.width/2
    cy=app.height/2
    r=100
    canvas.create_oval(cx+r,cy+r,cx-r,cy-r)
    r=math.sqrt(100**2+100**2)
    canvas.create_oval(cx+r,cy+r,cx-r,cy-r)
    printPoints(app,canvas)


runApp(width=600, height=600)

