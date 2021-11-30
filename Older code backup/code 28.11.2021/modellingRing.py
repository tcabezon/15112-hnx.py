
from cmu_112_graphics import *
import numpy as np
from stl import mesh
import math

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from functions import *
from ringClass import* 
from modellingRingDisplayFunctions import *


#####################
# DISPLAY
#####################

#####################
# AppStarted
#####################

def appStarted(app):
    app.mode='mainMode'
    app.modeDictionary={'m':'moveMode',
                        'r':'rotateMode',
                        'z':'moveZMode',
                        'a':'mainMode',
                        'e':'editMode',
                        'p':'zoomMode'}
    
    app.margin=30
    app.scale=1
    app.ring=Ring(200,50,stepRing=4)
    app.points2D=app.ring.points2D
    app.vertices=app.ring.vertices
    print(app.ring.vertices)
    print(app.ring.f)
    

    

################
#MAIN MODE
################
  
def mainMode_keyPressed(app, event):
    print(event.key)
    #if event.key in app.modeDictionary:
        #app.mode=app.modeDictionary[event.key]
    

def mainMode_redrawAll(app, canvas):
    #canvas.create_line(0,0,200,200, fill='black')
    #printModeDictionary(app, canvas)
    
    displayFaces(app,canvas,app.points2D,app.ring.faces)
    displayPoints(app,canvas,app.points2D)
    printCenter(app,canvas)
   

runApp(width=600, height=600)