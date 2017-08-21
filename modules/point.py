import vtk
import math

class point:
  
  def __init__ (self, x = 0.0, y = 0.0, z = 0.0, label = ""):
    self.x = x
    self.y = y
    self.z = z
    self.label = label

  def set_label (self, l):
    self.label = l

  def get_label(self):
    return self.label

  def set_coordinates (self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def get_coordinates (self):
    return self.x, self.y, self.z

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def get_z(self):
    return self.z

  def set_x(self, x):
    self.x = x

  def set_y(self, y):
    self.y = y

  def set_z(self, z):
    self.z = z

  def get_distance_from(self, point):

    dx = self.x - point.get_x()
    dy = self.y - point.get_y()
    dz = self.z - point.get_z()

    d = math.sqrt(dx*dx + dy*dy + dz*dz)

    return d

  def by_scalar (self, s):
    self.x = self.x * s
    self.y = self.y * s
    self.z = self.z * s

  def __sub__(self, other):
    return point(self.x-other.get_x(), self.y-other.get_y(), \
        self.z-other.get_z())

  def __add__(self, other):
    return point(self.x+other.get_x(), self.y+other.get_y(), \
        self.z+other.get_z())

  def __mul__(self, other):
    return point(self.x*other, self.y*other, \
        self.z*other)

  def __repr__(self):
    self.data = str(self.x) + " " + str(self.y) + " " + str(self.z)
    return repr(self.data)

  def get_actor(self, r = 0.01, rc = 1.0, gc = 1.0, bc = 1.0):
    source = vtk.vtkSphereSource()
    source.SetCenter(self.get_x(), self.get_y(), self.get_z())
    source.SetRadius(r)
    mapper = vtk.vtkPolyDataMapper()
    #mapper.SetInput(source.GetOutput())
    mapper.SetInputConnection(source.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(rc, gc, bc)

    return actor

def norm (point):
  f = 0.0
  
  f = point.get_x()*point.get_x() + \
      point.get_y()*point.get_y() + \
      point.get_z()*point.get_z()

  return math.sqrt(f)

def dot_prod (p1, p2):
    s = p1.get_x()*p2.get_x() + \
            p1.get_y()*p2.get_y() + \
            p1.get_z()*p2.get_z()

    return s

def cross_prod (p1, p2):

    ux = p1.get_x()
    uy = p1.get_y()
    uz = p1.get_z()

    vx = p2.get_x()
    vy = p2.get_y()
    vz = p2.get_z()

    x = uy * vz - uz * vy
    y = uz * vx - ux * vz
    z = ux * vy - uy * vx

    r = point(x, y, z)

    return r

