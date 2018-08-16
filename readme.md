# SolidPy2 

[SP]:https://github.com/bjbsquared/SolidPy
This is a fork of [SolidPy][SP] which has been dormant since 2012.
 
## Overview
[OSC]:http://www.openscad.org
[OSCUM]:http://en.wikibooks.org/wiki/OpenSCAD_User_Manual

SolidPy2 is a Python module that allows generation of [OpenSCAD][OSC] code from Python code. Use of 
SolidPy2 is to meant to simplify and enhance the design experience of code-based, parametric, solid 
modeling. 

Python + SolidPy2 -> OpenSCAD code -> Solid Model

## Usage
Place SolidPy2.py within the PYTHONPATH or in the directory containing the Python module which imports it. 
Write Python code using SolidPy2 to define the solid model. Execute the SolidPy2 based model to 
generate an OpenSCAD version of the model. The OpenSCAD version of the model can be viewed and 
automatically updated by setting the 'Design -> Automatic Reload and Preview' option 
from the OpenSCAD IDE.

## Language Differences
 
 | SolidPy2 |OpenSCAD|Difference |
 |:------- | :-------- | :--------- |
 | a = Sphere(r=2)| sphere(r=2) | First letter Capitalized |
 | b = Cube(1,2,3) | cube([1,2,3]) | Square brackets are optional |
 | b.color("red",0.5)|color("red",0.5) cube([1,2,3]) | Objects are transformed using methods |
 | b = a.copy()| no equivalent| Shapes are objects |
 | c = a + b |union(){sphere(r=2) cube([1,2,3])}| Easy to read syntax|
 

## Features
* Simple, flexible syntax
* Use of a Python IDE and the Python language is powerful 
* Treat objects like objects (not text)
* Use existing [OpenSCAD][OSC] modules
* Grow the object tree and pick the fruit you want (instead of taking the whole tree)
* AutoColoring mode
* Reference another solids attributes
* Copy shapes
* SolidPy2 Class can be extended to suit 


## SolidPy2 Classes
The SolidPy2 classes were designed for maximum inheritance and flexibility. Each are named after the 
OpenSCAD solid they represent except the names are capitalized.

Shown below is the interface for each SolidPy2 class. Treat the arguments for each just as they are 
for OpenSCAD, although there will be differences in syntax. Some commands will allow a single object
or a list of objects to be used as an argument. For specific OpenSCAD information see the 
[OpenSCAD Users Manual][OSCUM].


## 3D Shapes

### Cube(self, x, y = None, z = None, center = None) or Cube(self, [x,y,z] center = None)
Returns a SolidPy2Obj which represents a cube. 

Examples: `myBox = Cube([3,4,5])` or `myBox = Cube(3,4,5)`


### Cylinder(h, r, r2 = None, fa = None, fs = None, fn = None, center = None)
Returns a SolidPy2Obj which represents a cylinder. 
       	 	
Example: `myTube = Cylinder(h = 5, r=10, center = True )`
 
 
### Sphere(r, fa = None, fs = None, fn = None)
Returns a SolidPy2Obj which represents a cylinder. 

Notice that OpenSCAD uses \\$fs and \\$fn while SolidPy2 drops the \\$.

Example: `myBall = Sphere(r=5, fn=64)`

### Linear_extrude(height,center,convexity,twist)
Extrudes 2D shapes to make 3D object. Returns a SolidPy2Obj object.

### Rotate_extrude(convexity = None, fn = None)
Returns a SolidPy2Obj object.

### ImportSTL(fileName)
Imports an STL surface geometry file for use in the current OpenSCAD model. Returns a SolidPy2Obj object.

### Module(moduleName,**kwargs) 
Calls a OpenSCAD module brought in by the **use(filename)** command. Arguments to the module must be given as keyworded values. Returns a SolidPy2Obj object.

Example:
```
use("Rachet Tooth.scad")
tooth = Module("rachetTooth", ht = 1, thk=8, ra = 16, ba = 80)
```
 
### Polyhedron(points,triangles) 
Returns a SolidPy2Obj object.


## 2D Shapes

### Circle(r)

### Square([x,y]) or Square(x, y)

### Polygon(pointsList, pathList, convexity)
Returns a SolidPy2Obj object.

### Projection(cut = true) 
Returns a SolidPy2Obj object.


## CGS Operations
CGS object hold other SolidPy2 objects as child objects. They perform the CGS operation on the child objects as described below.
 
### _Union_
1. Union()
   - creates an empty Union object that can be used to add SolidPy2 objects at a later time
1. Union([objectList])
   - creates a Union object containing the objects in [objectList]
1. Union ([objectList1], [objectList2]) 
   - creates a Union object containing the objects in both lists

The Union object represents a CSG shape made by adding all of the child objects together.

An alternate form of Union is the  **'+'** operator.

Example: `myUnion = a + b`
    
- If 'a' is a Union then 'b' is added to the 'a' Union.
- If 'b' is a Union then 'a' is added to the 'b' Union.
- If neither 'a' or 'b' is a Union then both are added to a new Union.

### _Difference_
1. Difference()
   - creates an empty Difference object that can be used to add SolidPy2 objects at a later time
1. Difference([objectList])
   - creates a Difference object based on the objects in [objectList]
1. Difference([objectList1], [objectList2])
   - creates a Difference object based on the objects in both lists

The Difference object represents a CSG shape made by taking the first child object and subtracting the remaining child objects. 

An alternate form of Difference is the  **'-'** operator.

Example: `myDiff = a - b`
    
- If 'a' is a Difference then 'b' is subtracted from  the 'a' Difference.
- If 'a' is not a Difference, a new Difference object is created with 'a' as its first child from which 'b' will be subtracted.


### _Intersection_
1. Intersection()
   - creates an empty Intersection object that can be used to add SolidPy2 objects at a later time
1. Intersection(solidObj1 = None, solidObj2 = None)
   - creates an Intersection object representing the intersection between solidObj1 and solidObj2
1. Intersection([objectList])
   - creates an Intersection object representing the intersection between all objects in objectList
1. Intersection([objectList1],[objectList2])
   - creates an Intersection object representing the intersection between all objects in objectList1
     and objectList2

An alternate form of Intersection is the  **'*'** operator.

Example: `myIntersect = a * b`
    
- If 'a' and 'b' are not  Intersection() objects, a new one is made.


### _Minkowski_
1.  Minkowski(solidObj1 = None,solidObj2 = None)
   - creates a Minkowski object representing the Minkowski sum of solidObj2 revolved around the
     perimeter of solidObj1

### _Hull_
1. Hull()
   - creates an empty Hull object that can be used to add SolidPy2 objects at a later time
1. Hull(solidObj1 = None, solidObj2 = None)
   - creates an Hull object representing the convext hull between solidObj1 and solidObj2
1. Hull([objectList])
   - creates an Hull object representing the convext hull between all objects in objectList
1. Hull([objectList1],[objectList2])
   - creates an Hull object representing the convext hull between all objects in objectList1
     and objectList2

## Transforms
Transforms are methods of SolidPy2 objects. Transforms are kept on the object's transform stack.

### translate(x,y,z) OR translate([x,y,z])
 | SolidPy2 |OpenSCAD
 |:------- | :-------- |
 | a = Sphere(r=2)|sphere(r=2)
 | a.translate(2,4,6)| translate([2,4,6]){sphere(r=2)} 
 
 
### mirror(x,y,z) OR mirror([x,y,z])
 | SolidPy2 |OpenSCAD
 |:------- | :-------- |
 | a = Sphere(r=2)|sphere(r=2)
 | a.translate(2,4,6)| translate([2,4,6]){sphere(r=2)} 

### multmatrix(m)
m is a 4x4 transformation matrix.

 | SolidPy2 |OpenSCAD
 |:------- | :-------- |
 | a = Sphere(r=2)|sphere(r=2)
 | a.multmatrix(m)| multmatrix(m){sphere(r=2)} 


### scale(x,y,z) OR scale([x,y,z])
 | SolidPy2 |OpenSCAD
 |:------- | :-------- |
 | a = Sphere(r=2)|sphere(r=2)
 | a.scale(2,4,6)| scale([2,4,6]){sphere(r=2)} 
 
### color("color",alpha) OR color([r,g,b],alpha)
 | SolidPy2 |OpenSCAD
 |:------- | :-------- |
 | a = Sphere(r=2)|sphere(r=2)
 | a.color("red", 0.5)| color("red", 0.5){sphere(r=2)} 

## Utility

### comment
Each object may have a comment applied which will be passed through into the OpenSCAD code. 

Example:
```
a=Cube(1,2,3)
a.comment = "Here is my Cube!"
```

### copy(SolidPy2Obj)
Copy creates a duplicate of the solid object except that the parent of the duplicate is set to 
`None` and children are duplicates of the original.

Example:
```
myBox = Cube(4,5,6)
myNewBox = myBox.copy()
```

### use('filename.scad')
This loads an OpenSCAD file in order to access modules within that file. 

### write_scad_file(fileName, \*args):
Will save the output in SCAD format to 'fileName' + '.scad'.  
\*args can be SolidPy2 objects or lists of SolidPy2 objects.

## Extras
### inches_to_mm(x)
Dimensions in OpenSCAD are generally assumed to be millimeters(mm). Converts from inches to mm.

## Object Modifiers
Each object has modifiers that are found in OpenSCAD. They are boolean attributes.

* **root** - ignore the rest of the design and use this as the root, invoked via '!' in OpenSCAD
* **disable** - ignore this object, invoked via '\*' in OpenSCAD
* **background** - ignore this object and draw transparently, invoked via '%' in OpenSCAD
* **debug** - highlight in transparent pink, invoked via '#' in OpenSCAD 

Example:
```
a = Cube(1,2,3)
a.disable = True
```
## Defaults
Object specifying defaults used for the SCAD code generation.

### Attributes

### _tab_
This sets the tab length in the OpenSCAD code written by write_scad_file().
By default, **Defaults.tab** = 4 (meaning 4 spaces).

### _useFiles_
This is a list of SCAD files that are imported into the generated SCAD file via 
OpenSCAD's _'use(filename)'_. 
This is updated by the use of SolidPy2's _'use(scad-file)'_, although it can also be modified directly.

### _numFragments_ (aka '$fn' in OpenSCAD)
Number (minimum of 3) of fragments approximating curves/curved surfaces.
Sets the OpenSCAD **$fn** variable at the beginning of the generated code.

### _minFragmentSize_ (aka '$fs' in OpenSCAD)
Minimum size (minimum of 0.01) for fragments approximating curves/curved surfaces.
Sets the OpenSCAD **$fs** variable at the beginning of the generated code.

### _minFragmentAngle_ (aka '$fa' in OpenSCAD)
Minimum angle (minimum of 0.01) constraining the number of fragments approximating curves/curved surfaces.
The number of fragments is the highest integer <= 360/**minAngle**.
Sets the OpenSCAD **$fa** variable at the beginning of the generated code.

### _autoColor_
Boolean controlling whether colors are automatically applied to SolidPy2 objects at creation.
The color order is set by the **Defaults.colors** list.

### _colors_
Ordered list of colors used by the **Defaults.autoColor** setting to automatically apply colors to a SolidPy2 objects.

Defaults.colors = ["blue", "green", "orange", "yellow", "SpringGreen", "purple", "DarkOrchid", "MistyRose"]

Colors can be added or changed as required. Colors can be found at [OpenSCAD Users Manual][OSCUM].

