import copy

def inches(x):
    """converts inches to mm"""
    return 25.4 * x

def boolStr(abool):
    """retuns a lower case string of 'true' or 'false'"""
    if abool: #OSCad needs lower case
        return "true"
    else:
        return "false"

class Defaults(object):
    tab = " " * 3
    includeFiles = []
    preFiles = []
    postFiles = []
    fs = None
    fn = None
    fa = None
    autoColor = False
    augment = False
    diffColor = ["red", 0.25] #for augmentation of difference(){}
    colors = ["blue", "green", "orange", "yellow", "SpringGreen",
            "purple", "DarkOrchid", "MistyRose"]
##resistor color codes good for troubleshooting...?
##    colors=["black","brown","red","orange","yellow","green",
##            "blue","purple","grey","white"]

    colorCnt = 0
    augList = []

def Use(fileName):
    Defaults.includeFiles.append(fileName)


def PreInclude(fileName):
    Defaults.preFiles.append(fileName)

def PostInclude(fileName):
    Defaults.postFiles.append(fileName)

class SolidPyObj(object):

    def __init__(self):
        self._transformStack = []
        self.root = False
        self.disable = False
        self.parent = None
        self.background = False
        self.debug = False
        self.comment = ""
        self.tabLvl = 0
        if Defaults.autoColor:
            self.color(Defaults.colors[Defaults.colorCnt % len(Defaults.colors)])
            Defaults.colorCnt += 1

#ToDo add __str__ to Solid object model

    def __add__(self, solidObj1):
            """a=x+y calls x.__add__(y)->a"""
            if isinstance(self, Union):
                self.add(solidObj1)
                return self

            elif isinstance(solidObj1, Union):
                solidObj1.add(self)
                return solidObj1
            else:
                newUnion = Union(self, solidObj1)
                return newUnion

    def __sub__(self, solidObj1):
            if isinstance(self, Difference):
                self.add(solidObj1)
                return self
            else:
                newDifference = Difference(self, solidObj1)
                return newDifference

    def __mul__(self, solidObj1):
            if isinstance(self, Intersection):
                self.add(solidObj1)
                return self
            if isinstance(solidObj1, Intersection):
                solidObj1.add(self)
                return solidObj1
            else:
                newIntersection = Intersection(self, solidObj1)
                return newIntersection

    def copy(self):
        X = copy.deepcopy(self)

        if Defaults.autoColor == True:
            X.color(Defaults.colors[Defaults.colorCnt % len(Defaults.colors)])
            Defaults.colorCnt += 1
        return X

    def setTabLvl(self, lvl):
        self.tabLvl = lvl

    def rotate(self, x, y = None, z = None, v = None):
        """Puts a rotate transform on the transform stack"""
        rStr = ""
        if type(x) == list:
            loc = [str(getV(i)) for i in x]
        else:
            if y == None or z == None:
                vvx = str(getV(x))
                loc = [vvx, vvx, vvx]
            else:
                loc = [str(getV(x)), str(getV(y)), str(getV(z))]

        x, y, z = loc

        if v:
            q, r, s = v
            rStr = "rotate(a = [%s,%s,%s], v = [%.2f,%.2f,%.2f])" % (x, y, z, 1.0 * q, 1.0 * r, 1.0 * s)
        else:
            rStr = "rotate([%s, %s, %s])" % (x,y,z)
        self._transformStack.append(rStr)

    def release(self):

#        if isinstance(self.parent, Difference):
#            #No longer a candidate for augmentation
#            Defaults.augList.remove(self)
#            self.color("yellow", 1)


        if self.parent != None:
            self.parent.children.remove(self)
            self.parent = None
            self.tabLvl = 0

    def scale(self, x, y = None, z = None):
        """Puts a scale transform on the transform stack"""
        if type(x) == list:
            loc = [str(getV(i)) for i in x]
        else:
            if y == None or z == None:
                vvx = str(getV(x))
                loc = [vvx, vvx, vvx]
            else:
                loc = [str(getV(x)), str(getV(y)), str(getV(z))]

            x, y, z = loc

            rStr = "scale([%s,%s,%s])" % (x, y, z)
            self._transformStack.append(rStr)

    def translate(self, x, y = None, z = None):
        """
        Puts a translate transform on the transform stack
        translate( [x,y,z]) or translate(x,y,z)
        translate (1) -> [1,1,1]
    """

        if type(x) == list:
            loc = [str(getV(i)) for i in x]
        else:
            if  y == None or z == None:
                vvx = str(getV(x))
                loc = [vvx, vvx, vvx]
            else:
                loc = [str(getV(x)), str(getV(y)), str(getV(z))]

        x, y, z = loc

        rStr = "translate([%s,%s,%s])" % (x, y, z)
        self._transformStack.append(rStr)

    def mirror(self, x, y = None, z = None):
        """Puts a mirror transform on the transform stack
        mirror( [x,y,z]) or mirror(x,y,z)
        mirror (1) -> [1,1,1]
        """
        if type(x) == list:
            loc = [str(getV(i)) for i in x]
        else:
            if y == None or z == None:
                vvx = str(getV(x))
                loc = [vvx, vvx, vvx]
            else:
                loc = [str(getV(x)), str(getV(y)), str(getV(z))]

        x, y, z = loc

        rStr = "mirror([%s,%s,%s])" % (x, y, z)

        self._transformStack.append(rStr)

    def multmatrix(self, m):
        """Puts a multmatrix transform on the transform stack
        *** not tested ***"""
        rStr = "multmatrix(%s)" % str(m)
        self._transformStack.append(rStr)

    def color(self, color = "yellow", alpha = 1.0):
        if type(color) == str:
            rStr = 'color("%s", %s)' % (getV(color), str(getV(alpha)))

            if len(self._transformStack) > 0:
                if self._transformStack[0].startswith('color'):
                    self._transformStack.pop(0)
                    self._transformStack.insert(0, rStr)
            else:
                self._transformStack.append(rStr)

        if type(color) == list:
            r,g,b = [str(getV(i)) for i in color]
            rStr = 'color([%s,%s,%s], %s)' % (r, g, b, str(alpha))
            self._transformStack.append(rStr)

    def OSCString(self, protoStr):
        """Returns the OpenSCAD string to make the object"""
        #look for any modifiers
        OSCstr = ""

        for each in self._transformStack:
            OSCstr = each + " " + OSCstr

        modStr = ""
        if self.background:
            modStr += "%"
        if self.debug:
            modStr += "#"
        if self.disable:
            modStr += "!"
        if self.root:
            modStr += "*"
        OSCstr = +self.tabLvl * Defaults.tab + modStr + OSCstr

        OSCstr += protoStr

        if self.comment != "":
            OSCstr += " //%s\n" % self.comment
        else:
            OSCstr += "\n"

        return OSCstr


class Cube(SolidPyObj):
    """
    Cube( [x,y,z],center=True) or Cube( x,y,z,center)
    size = 1 -> [1,1,1]
    center: If True, object is centered at (0,0,0)
    """
##    def __init__(self, size = [1,1,1], center = False)
    def __init__(self, x, y = None, z = None, center = None):
        SolidPyObj.__init__(self)
        if type(x) == list:
            self.size = [getV(i) for i in x]
        else:
            if y == None:
                vvx = getV(x)
                self.size = [vvx, vvx, vvx]
            else:
                self.size = [getV(x), getV(y), getV(z)]

        self.center = center

    def renderOSC(self):
        x,y,z = self.size[0:3]
        protoStr = "cube(size=[%s,%s,%s], center=%s);" % (x, y, z, boolStr(self.center))
        return self.OSCString(protoStr)

class Sphere(SolidPyObj):
    """
    r=radius
    fa = Angle in degrees
    fs= Angle in mm
    """
    def __init__(self, r, fa = None, fs = None, fn = None):
        SolidPyObj.__init__(self)
        self.r = getV(r)
        self.fa = Defaults.fa
        self.fa = getV(fa)
        self.fs = getV(fs)
        self.fn = getV(fn)

    def renderOSC(self):
        protoStr = "sphere(r = %s" % str(self.r)
        if self.fa:
            protoStr += ", $fa = %s" % str(self.fa)
        if self.fs:
            protoStr += ", $fs = %s" % str(self.fs)
        if self.fn:
            protoStr += ", $fn = %s" % str(self.fn)
        protoStr += ");"
        return self.OSCString(protoStr)

class Cylinder(SolidPyObj):
    def __init__(self, h, r, r2 = None, fa = None, fs = None, fn = None, center = None):
        """
        h= height, r=radius note if r2 == None->r2=r
        fa = Angle in degrees
        fs= Angle in mm
        center: If True, object is centered at (0,0,0)
        """
        SolidPyObj.__init__(self)
        self.r = getV(r)
        self.h = getV(h)
        self.r2 = getV(r2)
        self.fa = getV(fa)
        self.fs = getV(fs)
        self.fn = getV(fn)
        self.center = center

    def renderOSC(self):
        if not self.r2:
            protoStr = "cylinder(h=%s, r=%s" % (str(self.h), str(self.r))
        else:
            protoStr = "cylinder(h=%s, r1=%s, r2=%s" % (str(self.h), str(self.r), str(self.r2))

        if self.fa:
            protoStr += ", $fa = %s" % str(self.fa)
        if self.fs:
            protoStr += ", $fs = %s" % str(self.fs)
        if self.fn:
            protoStr += ", $fn = %s" % str(self.fn)
        if self.center:
            protoStr += ", center = %s" % boolStr(self.center)
        protoStr += ");"
        return self.OSCString(protoStr)

class Polyhedron(SolidPyObj):
    def __init__(self, points, triangles):
        SolidPyObj.__init__(self)
        self.points = points
        self.triangles = triangles

    def renderOSC(self):
        protoStr = ""
        protoStr += "polyhedron(points = %s,\n triangles = %s);" % (str(self.points), str(self.triangles))
        return self.OSCString(protoStr)

class Linear_extrude(SolidPyObj):
    def __init__ (self, solidObj, height, center = None, convexity = None, twist = None):
        SolidPyObj.__init__(self)
        self.solidObj = solidObj
        self.height = getV(height)
        self.center = center
        self.convexity = getV(convexity)
        self.twist = getV(twist)

    def renderOSC(self):
        protoStr = "linear_extrude(height=%s" % self.height
        if self.center:
            protoStr += ", center = %s" % boolStr(self.center)
        if self.convexity:
            protoStr += ", convexity = %s" % self.convexity
        if self.twist:
            protoStr += ", twist = %s" % self.twist
        protoStr += ") "
        protoStr += self.solidObj.renderOSC()
        return self.OSCString(protoStr)


class Rotate_extrude(SolidPyObj):
    def __init__ (self, solidObj, convexity = None, fn = None):
        SolidPyObj.__init__(self)
        self.solidObj = solidObj
        self.convexity = getV(convexity)
        self.fn = getV(fn)


    def renderOSC(self):
        protoStr = "rotate_extrude("
        if self.convexity:
            protoStr += " convexity=%s" % self.convexity
        if self.fn:
            protoStr += ", fn = %s" % self.fn
        protoStr += ") "
        protoStr += self.solidObj.renderOSC()
        return self.OSCString(protoStr)

##projection(cut = true)
class Projection(SolidPyObj):
    def __init__ (self, solidObj, cut):

        SolidPyObj.__init__(self)
        self.solidObj = solidObj
        self.cut = cut

    def renderOSC(self):
        protoStr = "projection(cut=%s)" % self.cut
        protoStr += self.SolidPyObj.renderOSC()
        return self.OSCString(protoStr)

class Import(SolidPyObj):
    def __init__(self, filename):
        SolidPyObj.__init__(self)
        self.filename = filename

    def renderOSC(self):
        protoStr = ""
        protoStr += 'import("%s");' % self.filename
        return self.OSCString(protoStr)


class Circle(SolidPyObj):
    def __init__(self, r, fn = None):
        SolidPyObj.__init__(self)
        self.fn = getV(fn)
        self.r = getV(r)

    def renderOSC(self):
        protoStr = "" + self.tabLvl * Defaults.tab
        protoStr += "circle(r = %s" % self.r
        if self.fn:
            protoStr += ", $fn=%s" % self.fn
        protoStr += ");"
        return self.OSCString(protoStr)

class Square(SolidPyObj):
    def __init__(self, x , y = None, center = None):
        if type(x) == list:
            self.size = [getV(i) for i in x]
        else:
            if y == None:
                vvx = getV(x)
                self.size = [vvx, vvx]
            else:
                self.size = [getV(x), getV(y)]

        SolidPyObj.__init__(self)

        self.center = center

    def renderOSC(self):
        x,y = self.size[0:2]
        protoStr = ""
        protoStr += "square([%s,%s]" % (x,y)
        if self.center:
            protoStr += ", center = %s" % boolStr(self.center)
        protoStr += ");"
        return self.OSCString(protoStr)

class Polygon(SolidPyObj):
    def __init__(self, points, paths = None, convexity = None):
        SolidPyObj.__init__(self)
        self.points = points
        self.paths = paths
        self.convexity = getV(convexity)

    def renderOSC(self):
        protoStr = ""
        protoStr += "polygon(points=%s" % self.points
        if self.paths:
            protoStr += ", paths= %s" % self.paths
        if self.convexity:
            protoStr += ", convexity= %s" % self.convexity
        protoStr += ");"
        return self.OSCString(protoStr)



class Import_dxf(SolidPyObj):
    def __init__(self, filename, layer = None, origin = None, scale = None):
        SolidPyObj.__init__(self)
        self.filename = filename
        self.layer = layer
        self.origin = origin
        self.scale = scale

    def renderOSC(self):
        protoStr = ""
        protoStr += 'import_dxf(file="%s"' % self.filename
        if self.layer:
            protoStr += ", layername = %s" % self.layer
        if self.origin:
            protoStr += ", origin = %s" % self.origin
        if self.scale:
            protoStr += ", scale = %s" % self.scale
        protoStr += ");"
        return self.OSCString(protoStr)

##dxf_linear_extrude(file="finn.dxf", height=3, convexity=1, center=true);
class DXF_linear_extrude(SolidPyObj):
    def __init__(self, filename, height, convexity = None, center = None):
        SolidPyObj.__init__(self)
        self.filename = filename
        self.height = height
        self.convexity = convexity
        self.center = center

    def renderOSC(self):
        protoStr = ""
        protoStr += 'dxf_linear_extrude(file="%s"' % self.filename
        if self.height:
            protoStr += ", height=%s" % self.height
        if self.convexity:
            protoStr += ", convexity=%s" % self.convexity
        if self.center:
            protoStr += ", center=%s" % boolStr(self.center)
        protoStr += ");"
        return self.OSCString(protoStr)


## CGS Modeling ##

class CGS(SolidPyObj):
    """Generic class that other CGS classes inherit from. Will accept
    lists or individual solid objects."""
    def __init__(self, solidObj1, solidObj2):
        SolidPyObj.__init__(self)
        self.children = []

        if type(solidObj1) == list:
            for solid in solidObj1:
                self.add(solid)
        elif solidObj1:
            self.add(solidObj1)

        if type(solidObj2) == list:
            for solid in solidObj2:
                self.add(solid)
        elif solidObj2:
            self.add(solidObj2)

    def add(self, solidObj1):

        solidObj1.release()
        solidObj1.setTabLvl(self.tabLvl + 1)
        solidObj1.parent = self

#        if isinstance(self, Difference) and len(self.children) > 0:
#            color, alpha = Defaults.diffColor
#            solidObj1.color(color, alpha)
#            Defaults.augList.append(solidObj1)

        self.children.append(solidObj1)

    def setTabLvl(self, lvl):
        self.tabLvl = lvl
        for child in self.children:
            child.setTabLvl(lvl + 1)

    def renderOSC(self, protoStr):
        childrenStr = ""
        for child in self.children:
            childrenStr += child.renderOSC()
        childrenStr += self.tabLvl * Defaults.tab + "}\n"

        return self.OSCString(protoStr + childrenStr)

class Union(CGS):
    def __init__(self, solidObj1 = None, solidObj2 = None):

        CGS.__init__(self, solidObj1, solidObj2)

    def renderOSC(self):
        return CGS.renderOSC(self, "union() {\n")

class Difference(CGS):
    def __init__(self, solidObj1 = None, solidObj2 = None):
        CGS.__init__(self, solidObj1, solidObj2)

    def renderOSC(self):
        return CGS.renderOSC(self, "difference() {\n")

class Intersection(CGS):
    def __init__(self, solidObj1 = None, solidObj2 = None):

        CGS.__init__(self, solidObj1, solidObj2)

    def renderOSC(self):
        return CGS.renderOSC(self, "intersection() {\n")

class Minkowski(CGS):
    def __init__(self, solidObj1 = None, solidObj2 = None):

        CGS.__init__(self, solidObj1, solidObj2)

    def renderOSC(self):
        return CGS.renderOSC(self, "minkowski() {\n")

class Hull(CGS):
    def __init__(self, solidObj1 = None, solidObj2 = None):

        CGS.__init__(self, solidObj1, solidObj2)

    def renderOSC(self):
        return CGS.renderOSC(self, "hull() {\n")

class Module(CGS):
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs
        CGS.__init__(self, None, None)

    def renderOSC(self):
        #return CGS.renderOSC(self, "module " + self.name + "() {\n")

        protoStr = "" + self.tabLvl * Defaults.tab
        protoStr += "module " + self.name + "("
        cnt = 0
        for kws in self.kwargs:
            if cnt > 0: protoStr += ", " 
            if type(self.kwargs[kws]) == V:
                self.kwargs[kws] = self.kwargs[kws].renderOSC()
            protoStr += "%s=%s" % (kws, self.kwargs[kws])
            cnt += 1
        protoStr += ") {\n"
        return CGS.renderOSC(self, protoStr)

class OscModule(SolidPyObj):
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs
        SolidPyObj.__init__(self)

    def renderOSC(self):
        protoStr = ""
        protoStr += self.name + "("
        cnt = 0
        for kws in self.kwargs:
            if cnt > 0:
                protoStr += ", \n" + (1 + self.tabLvl) * Defaults.tab
            if type(self.kwargs[kws]) == V:
                self.kwargs[kws] = self.kwargs[kws].renderOSC()
            protoStr += "%s=%s" % (kws, self.kwargs[kws])
            cnt += 1
        protoStr += ");"
        return self.OSCString(protoStr)

class V(SolidPyObj):
    def __init__(self, name):
        self.name = name
        SolidPyObj.__init__(self)

    def renderOSC(self):
        return self.name

def getV(val):
    if type(val) == V: val = val.renderOSC()
    return val

def writeSCADfile(fileName, *args):
    """fileName = the SCAD file to save to. Include the '.scad' extension
    args can be SolidPyObj or lists of SolidPyObj"""

    theStr = ""

    for f in Defaults.includeFiles:
        theStr += "use<%s>;\n\n" % f

    for f in Defaults.preFiles:
        with open(f, 'r') as scad_file:
            theStr += scad_file.read()

    theStr += '\n'

    if Defaults.fa:
        theStr += '$fa=%s;\n' % Defaults.fa
    if Defaults.fn:
        theStr += '$fn=%s;\n' % Defaults.fn
    if Defaults.fs:
        theStr += '$fs=%s;\n' % Defaults.fs

    theStr += '\n'

    for obj in args:
        if type(obj) == list: # A list of SolidPyObj
            for item in obj:
                theStr += item.renderOSC() + "\n"
        else: # it must be a SolidPyObj here
            theStr += obj.renderOSC() + "\n"

    if Defaults.augment:
        for item in Defaults.augList:
            if item.tabLvl < 2:
                item.color("red", 0.25)
                item.comment += " (from Augmentation)"
                theStr += item.renderOSC() + "\n"

    theStr += '\n'

    for f in Defaults.postFiles:
        with open(f, 'r') as scad_file:
            theStr += scad_file.read()

    outF = open(fileName, 'w')
    outF.write(theStr)
    outF.close

def main():

    Use("ring.scad")

    g = OscModule("ring", 5, 5, 10)

    writeSCADfile('solidPy.scad', g)

    print g.renderOSC()


if __name__ == '__main__':
    main()
