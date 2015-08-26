import math
import point

class plane:
  
  def __init__ (self, a = point.point (), b = point.point(), c = point.point()):

    self.set_points (a, b, c)

  def set_points (self, p1, p2, p3):

    self.A = p1.get_y()*(p2.get_z() - p3.get_z()) + \
        p2.get_y()*(p3.get_z() - p1.get_z()) + \
        p3.get_y()*(p1.get_z() - p2.get_z())
    self.B = p1.get_z()*(p2.get_x() - p3.get_x()) + \
        p2.get_z()*(p3.get_x() - p1.get_x()) + \
        p3.get_z()*(p1.get_x() - p2.get_x())
    self.C = p1.get_x()*(p2.get_y() - p3.get_y()) + \
        p2.get_x()*(p3.get_y() - p1.get_y()) + \
        p3.get_x()*(p1.get_y() - p2.get_y())
    self.D = -1.0 * (p1.get_x()*(p2.get_y()*p3.get_z() - \
        p3.get_y()*p2.get_z()) + p2.get_x()*(p3.get_y()*p1.get_z() - \
        p1.get_y()*p3.get_z()) + p3.get_x()*(p1.get_y()*p2.get_z() - \
        p2.get_y()*p1.get_z()))

    return 

  def get_normal_vector (self):

    norm = math.sqrt(self.A * self.A + \
        self.B * self.B + \
        self.C * self.C)

    n = point.point (self.A/norm, self.B/norm, self.C/norm)

    return n

  def get_plane_data(self):

    return self.A, self.B, self.C, self.D

  def return_angle(self, p2):
    A, B, C, D = p2.get_plane_data()

    p = self.A * A + self.B * B + self.C * C 
    pa = math.sqrt(self.A * self.A + self.B * self.B + self.C * self.C)
    pb = math.sqrt(A * A + B * B + C * C)

    return math.acos(p / (pa*pb))

  def get_distance (self, p):

    denum = math.sqrt(self.A*self.A + 
        self.B*self.B + self.C*self.C)

    D = self.A * p.get_x() + \
        self.B * p.get_y() + \
        self.C * p.get_z() + \
        self.D

    return D/denum

  def is_point_outside_of_plane(self, p):

    return self.A * p.get_x() + \
        self.B * p.get_y() + \
        self.C * p.get_z() + \
        self.D != 0.0

  def is_point_in(self, p):
    return self.A * p.get_x() + \
        self.B * p.get_y() + \
        self.C * p.get_z() + \
        self.D == 0.0

  def check_point_side (self, p):
    v = self.A * p.get_x() + \
        self.B * p.get_y() + \
        self.C * p.get_z() + \
        self.D

    if (v > 0.0):
      return 1
    elif (v < 0.0):
      return -1
      
    return 0


  def project_point (self, p):

    a2 = self.A * self.A
    b2 = self.B * self.B
    c2 = self.C * self.C

    t0 = -1.0 * ((self.A * p.get_x() + \
                  self.B * p.get_y() + \
                  self.C * p.get_z() +
                  self.D) / (a2 + b2 + c2))

    x0 = p.get_x() + self.A * t0
    y0 = p.get_y() + self.B * t0
    z0 = p.get_z() + self.C * t0

    return point.point(x0, y0, z0)
