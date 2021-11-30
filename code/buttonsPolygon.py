from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *
from sphereClass import *
from bezier3DClass import *
from ringClass import *
from bezierFunctions import *

numberOfBezierPoints=20
bezierCurvePoints=[[0.0, 0.3], [0.05574759945130314, 0.2982990397805212], [0.0975582990397805, 0.28035665294924556], [0.12543209876543207, 0.24617283950617286], [0.13936899862825786, 0.19574759945130316], [0.13936899862825786, 0.1290809327846365], [0.12543209876543207, 0.046172839506172875], [0.0975582990397805, -0.052976680384087815], [0.05574759945130317, -0.16836762688614537], [0.0, -0.3]]
bezierCurvePoints1DList=convertListTo1D(bezierCurvePoints)
print(bezierCurvePoints1DList)

pointList=[100.,30,200,50.,300,30,200,10]

#bezierCurvePoints=[0.,30,200,50.,300,30,200,10]



def appStarted(app):
    app.mode='bezier'

def bezier_redrawAll(app, canvas):
    #2D view
    margin=10
    canvas.create_rectangle(0,0,300,300)
    canvas.create_polygon(pointList, fill="green")
    canvas.create_polygon(bezierCurvePoints1DList, fill="red") 

runApp(width=900, height=600)