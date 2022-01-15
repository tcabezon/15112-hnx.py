#################################################
# hnX.py
#
# Your name: Tomas Cabezon Pedroso
# Your andrew id: tcabezon
#################################################

• PROGRAM DESCRIPTION • 

This project will be a ring generator. The output of his program will be a .stl file of the 3D model that the user created using the program.
The user will interact with the program so an aesthetic shape is achieved. To do so, this program will be a simple 3d modelling software. The program will display the current shape of the ring to the user, who will be able to make changes to it. This includes adding new elements to the mesh or editing it.

• RUNING THE PROGRAM • 

Open the hnX.py file and run it.

Files that are needed to use hnX.py:
- hnXfunctions.py
- ringClass.py
- sphereClass.py
- bezier3DClass.py
- toSTL.py
- cmu_112_graphics.py

Libraries needed:
- Numpy: https://numpy.org/


• USING THE PROGRAM • 

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
'Arrow Down': rotating down
'Arrow Right': rotating right
'Arrow Left':rotatinf left

- ZOOM OPTIONS
'.' or '+': zooming in
',' or '-' or '_': zooming out

• PARAMETERS OF THE PROGRAM • 

The following parameters in the hnX.py are important to define the mesh quality or ring size:
- When loading the Ring object:
   -> Ring(innerDiameter,ringRadious,stepCircunferenc,stepRing):
	stepCircunference: number of the subdivisions along the ring, number of subdivisions on the rotation process
	stepRing: number of subdivisions of the section circumference that is rotated to generate the ring
   -> Sphere(r,stepU,stepV):
	stepU: sphere xy plane divisions
	stepV: sphere z axis divisions
   -> Bezier3D(controlPointList, numberOfPoints, stepU):
	numberOfpoints: number of divisions on each bezier curve
	stepU: number of subdivisions in the rotation process of the bezier curve to generate the 3D element
   


