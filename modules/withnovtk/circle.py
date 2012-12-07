import numpy
import math

import line

class circle:

  def __init__(self, cx = 0.0, cy = 0.0, radius = 0.0):
    self.cx = cx
    self.cy = cy
    self.radius = radius

  def set_center (self, cx = 0.0, cy = 0.0):
    self.cx = cx
    self.cy = cy

  def set_radius (self, radius):
    self.radius = radius

  def get_center (self):
    return self.cx, self.cy

  def get_radius (self):
    return self.radius

  def is_point_inside (self, x, y):

    return ((x - self.cx)**2 + (y - self.cy)**2 - self.radius**2) <= 0

  def generate_half_circle_points (self, n):

    point_list = []
    
    d = (math.pi) / float(n-1)

    alpha = 0.0
    for i in range(n):
      if (alpha <= math.pi):
        x = self.cx + self.radius * math.cos(alpha)
        y = self.cy + self.radius * math.sin(alpha)

        point_list.append([x, y])

        alpha += d

    return point_list

  def generate_circle_points (self, n):

    point_list = []
    
    d = (2.0 * math.pi) / float(n-1)

    alpha = 0.0
    for i in range(n):
      if (alpha < (2.0 * math.pi)):
        x = self.cx + self.radius * math.cos(alpha)
        y = self.cy + self.radius * math.sin(alpha)

        point_list.append([x, y])

        alpha += d

    return point_list


###############################################################################

def line_circle_intersection (cir, l):

  points = []

  m = l.get_m()
  q = l.get_q()
  p1 = l.get_p1()
  x1 = p1[0]
  y1 = p1[1]

  #print x1, y1

  h, k = cir.get_center()

  #print h, k

  R = cir.get_radius()
  h2 = h**2.0
  k2 = k**2.0
  R2 = R**2.0
  m2 = m**2.0
  x12 = x1**2.0
  y12 = y1**2.0

  b = -2.0 * (h + (m2 * x1) - (m * y1) + (m * k))

  a = 1.0 + m2
  c = h2 + k2 + y12 + (m2 * x12) - R2 - \
      (2.0 * m * x1 * y1) + (2.0 * k * m * x1) - \
      (2.0 * k * y1)

  delta = (b**2.0) - (4.0 * a * c)

  #print delta

  if delta == 0.0:
    x = -1.0 * b / (2.0 * a) 
    y = m*x + q 
    points.append([x, y])
  elif delta > 0.0:
    x = (-1.0 * b + math.sqrt(delta))/ (2.0 * a)
    y = m*x + q
    points.append([x, y])

    x = (-1.0 * b - math.sqrt(delta))/ (2.0 * a)
    y = m*x + q
    points.append([x, y])

  return points

###############################################################################

def get_radius_given_area(area):

  return math.sqrt(area / math.pi) 

###############################################################################
