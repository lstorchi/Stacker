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

def norm (point):
  f = 0.0
  
  f = point.get_x()*point.get_x() + \
      point.get_y()*point.get_y() + \
      point.get_z()*point.get_z()

  return math.sqrt(f)
