from point import *

import numpy
import math

class sphere:

  def __init__(self, center = point(0.0, 0.0, 0.0), radius = 0.0):
    self.center = center
    self.radius = radius

  def set_center (self, center):
    self.center = center

  def set_radius (self, radius):
    self.radius = radius

  def get_center (self):
    return self.center

  def get_radius (self):
    return self.radius

  def get_volume (self):
    V = (4.0 / 3.0) * math.pi * math.pow(self.radius, 3)

    return V

  def is_point_inside (self, x, y, z):
    p = point(x, y, z)

    d = self.center.get_distance_from(p)

    return (d < self.radius)

  def generate_surface_points (self, n):

    point_list = []
    
    d = (2.0 * math.pi) / float(n-1)

    alpha = 0.0
    for i in range(n):
      beta = 0.0
      for j in range(n):
        x = self.radius * math.sin(alpha) * math.cos(beta) + \
            self.center.get_x()
        y = self.radius * math.sin(alpha) * math.sin(beta) + \
            self.center.get_y()
        z = self.radius * math.cos(alpha) + self.center.get_z()

        point_list.append(point(x, y,  z))

        beta += d
      alpha += d

    return point_list

###############################################################################
# free functions
###############################################################################

def sphere_to_arrays (spheres = []):

  scx = numpy.linspace( 0.0, 0.0, len(spheres)) 
  scy = numpy.linspace( 0.0, 0.0, len(spheres))
  scz = numpy.linspace( 0.0, 0.0, len(spheres))
  radius = numpy.linspace( 0.0, 0.0, len(spheres))

  i = 0
  for s in spheres:
    c = s.get_center()
    scx[i] = c.get_x()
    scy[i] = c.get_y()
    scz[i] = c.get_z()
    radius[i] = s.get_radius()
    i += 1

  return scx, scy, scz, radius
