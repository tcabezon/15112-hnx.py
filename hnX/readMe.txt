#################################################
# hnX.py
#
# Your name: Tomas Cabezon Pedroso
# Your andrew id: tcabezon
#################################################

• PROGRAM DESCRIPTION:

This project will be a ring generator. The output of his program will be a .stl file of the 3D model that the user created using the program.
The user will interact with the program so an aesthetic shape is achieved. To do so, this program will be a simple 3d modelling software. The program will display the current shape of the ring to the user, who will be able to make changes to it. This includes adding new elements to the mesh or editing it.

• RUNING THE PROGRAM:

Open the hnX.py file and run it.

Files that are needed to use heX.py:
- hnXfunctions.py
- ringClass.py
- sphereClass.py
- bezier3DClass.py
- cmu_112_graphics.py

Libraries needed:
- Numpy: https://numpy.org/
- Numpy stl: https://pypi.org/project/numpy-stl/
- MatplotLib: https://matplotlib.org/

• USING THE PROGRAM:

The program has the following commands to the different App Modes:
- a: main mode 
- b: bezier mode
- x: move bezier mode
- q: restart app

For advanced editing options:
- m: move mode
- r: rotate mode
- z: move Z mode
- p: rotate mode

While in main Mode there are some useful shortcuts:

- DRAWING BEZIER/SPHERE
'0': add Sphere element
'9': add Bezier3D element

- ELEMENT SIZE OPTIONS
'1'-'5': change element size

- ROTATION OPTIONS
'Arrow Up': rotating up
'Arrow Down':
        print('rotating down')
        rotatePointsAngleV(app,-angle)
    if event.key=='Right':
        print('rotatin right')
        rotatePointsAngleH(app,angle)
    if event.key=='Left':
        print('rotatin left')
        rotatePointsAngleH(app,-angle)

    #ZOOM OPTIONS
    if event.key in ['.','+']:
        print('zooming in')
        zoomIn(app,1.1)
    if event.key in [',','-','_']:
        print('zooming out')
        zoomOut(app,0.9)



