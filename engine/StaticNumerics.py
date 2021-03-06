# Done

# This is the non-reactive version of the numeric classes.  To get the overloading right,
# we have to go through contortions using radd, rsub, and rmul so that an ordinary
# number doesn't screw up overloading in 1 + signal, 1 - signal, and 1 * signal.
# Not sure why rdiv isn't here.

import g
import math
import random
from Types import *
from panda3d.core import Quat, VBase3

# This is a where we park signal functions.

pi       = math.pi
twopi    = 2*pi
sCeiling = math.ceil
sFloor = math.floor

def sFraction(x):
    return x - sFloor(x)

def staticLerp(t, x, y):
    return (1-t)*x + t*y

# This class is the 0 element in an arbitrary numeric
# class.  It is used as the initial result of an integrator.


# Note that the destination is never changed.

def staticLerpA(t, x, y):
    x1 = x/twopi
    y1 = y/twopi
    x2 = twopi * (x1 - math.floor(x1))
    y2 = twopi * (y1 - math.floor(y1))
    if x2 < y2:
        if y2 - x2 > pi:
            return staticLerp(t, x2+twopi, y2)
        return staticLerp(t, x2, y2)
    else:
        if x2 - y2 > pi:
            return staticLerp(t, x2-2*pi, y2)
        return staticLerp(t, x2, y2)

# Normalize an angle to the -pi to pi range
def sNormA(a):
    a1 = a/twopi
    a2 = twopi * (a1 - math.floor(a1))
    return a2 if a2 <= pi else a2 - twopi

# The P2 class (2-d point)
# Note that P2 x Scalar works.  Probably not P2 / scalar though.

class SP2:
      def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = P2Type
      def __str__(self):
          return "P2(%7.2f, %7.2f)" % (self.x, self.y)
      def __add__(self, y):
          return g.add(self, y)
      def __radd__(self, y):
          return g.add(y, self)
      def __sub__(self, y):
          return g.sub(self, y)
      def __rsub__(self, y):
          return g.sub(y, self)
      def __mul__(self, y):
          return g.mul (self, y)
      def __rmul__(self, y):
          return g.mul (y, self)
      def __abs__(self):
          return g.abs(self)
      def __neg__(self):
          return scaleP2(-1, self)
      def interp(self, t, p2):
          return SP2(staticLerp(t, self.x, p2.x),
                     staticLerp(t, self.y, p2.y))
      def interpA(self, t, p2):
          return SP2(staticLerpA(t, self.x, p2.x),
                     staticLerpA(t, self.y, p2.y))

# Used for integration

P2Type.encode = lambda p:str(p.x)+","+str(p.y)
def readP2(str):
    nums = parseNumbers(str)
    return SP2(nums[0],nums[1])
P2Type.decode = readP2

P2Type.zero = SP2(0,0)

# non-overloaded methods for P2 arithmentic

def addP2(a,b):
    return SP2(a.x+b.x, a.y+b.y)

def subP2(a,b):
    return SP2(a.x-b.x, a.y-b.y)

def scaleP2(s,a):
    return SP2(s*a.x, s*a.y)

def absP2(a):
    return math.sqrt(a.x*a.x+a.y*a.y)

def dotP2(a,b):
    return SP2(a.x*b.x,a.y*b.y)


# The P3 class, similar to P2

class SP3:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.type = P3Type
  def __str__(self):
      return "P3(%7.2f, %7.2f, %7.2f)" % (self.x, self.y, self.z)
  def __add__(self, y):
          return g.add(self, y)
  def __radd__(self, y):
          return g.add(y, self)
  def __sub__(self, y):
          return g.sub(self, y)
  def __rsub__(self, y):
          return g.sub(y, self)
  def __mul__(self, y):
          return g.mul(self, y)
  def __rmul__(self, y):
          return g.mul(y, self)
  def __abs__(self):
          return g.abs(self)
  def __neg__(self):
          return scaleP3(-1, self)
  def interp(self, t, p2):
          return SP3(staticLerp(t, self.x, p2.x),
                     staticLerp(t, self.y, p2.y),
                     staticLerp(t, self.z, p2.z))

P3Type.encode = lambda p:str(p.x)+","+str(p.y)+","+str(p.z)
def readP3(str):
    nums = parseNumbers(str)
    return SP3(nums[0],nums[1], nums[2])
P3Type.decode = readP3

def crossProduct(a, b):
    return SP3(a.y * b.z - a.z * b.y,
               a.z * b.x - a.x * b.z,
               a.x * b.y - a.y * b.x)

def normP3(p):
    a = absP3(p)
    if a < 0.0000001:  # Avoid divide by 0
        return SP3(0,0,0)
    else:
        return scaleP3(1/a, p)
def addP3(a, p):
    return SP3(a.x + p.x, a.y + p.y, a.z + p.z)
def subP3(a, p):
    return SP3(a.x - p.x, a.y - p.y, a.z - p.z)
def scaleP3(s, a):
    return SP3(a.x * s, a.y * s, a.z * s);
def absP3(a):
    return math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
def dotP3(a,b):
    return SP3(a.x*b.x, a.y*b.y, a.z*b.z)

# Construct a polar 2-D point
def SP2Polar(r, theta):
    return SP2(r*math.cos(theta), r*math.sin(theta))

def SP3C(r, theta, z):
    p = SP2Polar(r, theta)
    return SP3(p.x, p.y, z)

# Conversions from tuple type.

def toP3(x):
    t = getPType(x)
    if t == P3Type:
        return x
    if type(x) == TupleType and len(x) == 3:
        for v in x:
            if getPType(v) != numType:
                return None
        return SP3(x[0], x[1], x[2])
    return None

def toP2(x):
    t = getPType(x)
    if t == P2Type:
        return x
    if type(x) == TupleType and len(x) == 2:
        for v in x:
            if getPType(v) != numType:
                return None
        return SP2(x[0], x[1])
    return None

def gendot(x,y):
    t = getPType(x)
    if t == numType:
        return x*y
    if t == P2Type:
        return dotP2(x,y)
    return dotP3(x,y)

class Pair:
      def __init__(self, first, second):
          self.first = first
          self.second = second
          self.type = pairType(getPType(first), getPType(second))

def sPair(x,y):
    Pair(x, y)

def sFirst(p):
    p.first

def sSecond(p):
    p.second
    
def sHPRtoP3(p):
    return SP3(math.sin(p.h)* math.cos(p.p),
        -math.cos(p.h)* math.cos(p.p), 
        -math.sin(p.p))
    
def sP3toHPR(p):
    return SHPR(math.atan2(p.y, p.x) + pi/2,
              math.atan2(p.z, abs(SP2(p.x, p.y))),
              0)

# The P3 class, similar to P2

class SHPR:
  def __init__(self, h, p, r):
    self.h = h
    self.p = p
    self.r = r
    self.type = HPRType
  def __add__(self, y):
      return g.add(self, y)
  def __sub__(self, y):
      return g.sub(self, y)
  def __rsub__(self, y):
          return g.sub(y, self)
  def __mul__(self, y):
          return g.mul(self, y)
  def __rmul__(self, s):
      return g.mul(s, self)
  def __str__(self):
      return "HPR(%7.2f, %7.2f, %7.2f)" % ( self.h, self.p, self.r)
  def __neg__(self):
          return g.mul(self, -1)
  def interp(self, t, p2):
          return SHPR(staticLerpA(t, self.h, p2.h),
                      staticLerpA(t, self.p, p2.p),
                      staticLerpA(t, self.r, p2.r))

def addHPR(a,b):
    return SHPR(a.h+b.h, a.p+b.p, a.r+b.r)

def subHPR(a,b):
    return SHPR(a.h-b.h, a.p-b.p, a.r-b.r)

def scaleHPR(s,a):
    return SHPR(a.h*s, a.p*s, a.r*s)

def getUpHPR(hpr):
    q = Quat()
    q.setHpr(VBase3(math.degrees(hpr.h), math.degrees(hpr.p), math.degrees(hpr.r)))
    v = q.getUp()
    return SP3(v.x, v.y, v.z)

HPRType.encode = lambda p:str(p.h)+","+str(p.p)+","+str(p.r)
def readHPR(str):
    nums = parseNumbers(str)
    return SHPR(nums[0],nums[1], nums[2])

HPRType.decode = readHPR

P2Type.zero = SP2(0,0)
P3Type.zero = SP3(0,0,0)
HPRType.zero = SHPR(0,0,0)
P2Type.zero = SP2(0,0)

# Random number stuff - static only!

def randomChoice(choices):
    return random.choice(choices)

def random01():
    return random.random()

def random11():
    return 2*random.random()-1

def randomRange(low, high = None):
    if high is None:
        return low * random01()
    return low + random01()*(high-low)

def randomInt(low, high = None):
    if high is None:
        return random.randint(0, low)
    return random.randint(low, high)

def shuffle(choices):
    c = list(choices)
    random.shuffle(c)
    return c

def sStep(x):
    if (x < 0):
        return 0
    else:
        return 1
    

def sSmoothStep(x):
    if (x < 0):
        return 0
    if (x > 1):
        return 1
    return x*x*(-2*x + 3)

random.seed()

