from sphere import *
from common import *

import triangle
import circle
import point
import line

import math
import sys

import random

from math import cos, sin, sqrt

import numpy

TWOPI = 6.283185307179586476925287

#######################################################

def is_a_float (val):

    try:
        float(val)
    except ValueError:
        return False

    return True

#######################################################

def generate_random_spheres (spheres = []):

  # suddivido in box dove posizionare le sfere
  # ogni box e' grande 2 di spigolo
  boxdim = 2.0
  for boxix in range(int((topx-botx)/boxdim)):
    for boxiy in range(int((topx-botx)/boxdim)):
      for boxiz in range(int((topx-botx)/boxdim)):
        cx = random.uniform(R,boxdim-R)
        cy = random.uniform(R,boxdim-R)
        cz = random.uniform(R,boxdim-R)
        
        cx += boxix*boxdim
        cy += boxiy*boxdim
        cz += boxiz*boxdim
        
        c = point.point(cx, cy, cz)
        s = sphere(c, R)

        spheres.append(s)

#######################################################

def move_spheres (spheres = []):
  for s in spheres:
    p = s.get_center()

    x, y, z = p.get_coordinates()
    z = z + 0.001 
    p.set_coordinates(x, y, z)

    s.set_center (p)

#######################################################

def point_rotate(p1, p2, p0, theta):
#   Modified by Loriano
#   Return a point rotated about an arbitrary axis in 3D.
#   Positive angles are counter-clockwise looking down the axis toward the origin.
#   The coordinate system is assumed to be right-hand.
#   Arguments: 'axis point 1', 'axis point 2', 'point to be rotated', 'angle of rotation (in radians)' >> 'new point'
#   Revision History:
#       Version 1.01 (11/11/06) - Revised function code
#       Version 1.02 (11/16/06) - Rewrote PointRotate3D function
#
#   Reference 'Rotate A Point About An Arbitrary Axis (3D)' - Paul Bourke        
#   http://paulbourke.net/geometry/rotate/
#   http://paulbourke.net/geometry/rotate/PointRotate.py

    # Translate so axis is at origin    
    p = p0 - p1
    # Initialize point q
    q = point.point(0.0,0.0,0.0)
    Np = p2 - p1
    Nm = sqrt(Np.get_x()**2 + Np.get_y()**2 + Np.get_z()**2)

    # i due punti coincidono, non faccio nulla e ritorno
    if Nm == 0:
      return p0
    
    # Rotation axis unit vector
    n = point.point(Np.get_x()/Nm, Np.get_y()/Nm, Np.get_z()/Nm)

    # Matrix common factors     
    c = cos(theta)
    t = (1 - cos(theta))
    s = sin(theta)
    X = n.x
    Y = n.y
    Z = n.z

    # Matrix 'M'
    d11 = t*X**2 + c
    d12 = t*X*Y - s*Z
    d13 = t*X*Z + s*Y
    d21 = t*X*Y + s*Z
    d22 = t*Y**2 + c
    d23 = t*Y*Z - s*X
    d31 = t*X*Z - s*Y
    d32 = t*Y*Z + s*X
    d33 = t*Z**2 + c

    #            |p.x|
    # Matrix 'M'*|p.y|
    #            |p.z|
    q.x = d11*p.x + d12*p.y + d13*p.z
    q.y = d21*p.x + d22*p.y + d23*p.z
    q.z = d31*p.x + d32*p.y + d33*p.z

    # Translate axis and rotated point back to original location    
    return q + p1

#######################################################

def is_in_the_void(scx, scy, scz, R, px, py, pz) :

  #distx = numpy.power((scx - px), 2)
  #disty = numpy.power((scy - py), 2)
  #distz = numpy.power((scz - pz), 2)

  distx = (scx - px) * (scx - px)
  disty = (scy - py) * (scy - py)
  distz = (scz - pz) * (scz - pz)

  dist = distx + disty + distz

  d = numpy.sqrt(dist)

  bools = d <= R

  interior_indices, = numpy.where(bools)
 
  return (len(interior_indices) == 0)

#######################################################

def nearest_to_point (scx, scy, scz, px, py, pz) :

  distx = (scx - px) * (scx - px)
  disty = (scy - py) * (scy - py)
  distz = (scz - pz) * (scz - pz)

  dist = distx + disty + distz

  d = numpy.sqrt(dist)

  if len(d) == 0:
    return -1.0

  return min(d)

  """

  #dist = numpy.linspace( 0.0, 0.0, len(scx))
 
  dist = 0.0
  minr2 = 100000000.0

  for i in range(len(scx)):
    distx = scx[i] - px
    distx2 = distx * distx 
    disty = scy[i] - py
    disty2 = disty * disty 
    distz = scz[i] - pz
    distz2 = distz * distz 

    dist = math.sqrt(distx2 + disty2 + distz2)

    if (dist < minr2):
      minr2 = dist

  return minr2

  """


#######################################################

def get_near_point (scx, scy, scz, px, py, pz, distance) :

  #distx = numpy.power((scx - px), 2)
  #disty = numpy.power((scy - py), 2)
  #distz = numpy.power((scz - pz), 2)

  distx = (scx - px)
  disty = (scy - py)
  distz = (scz - pz)

  distx2 = distx * distx
  disty2 = disty * disty
  distz2 = distz * distz

  dist = distx2 + disty2 + distz2

  d = numpy.sqrt(dist)

  #print "d: " , len(indices)

  bools1 = d <= distance
  #bools2 = d != 0.0

  #print "bools1: " , len(bools1)

  indices, = numpy.where(bools1)

  #print len(indices)

  toretx = numpy.linspace( 0.0, 0.0, len(indices))
  torety = numpy.linspace( 0.0, 0.0, len(indices))
  toretz = numpy.linspace( 0.0, 0.0, len(indices)) 
  toretdst = numpy.linspace( 0.0, 0.0, len(indices))

  for i in range(len(indices)):
    toretx[i] = scx[indices[i]]
    torety[i] = scy[indices[i]]
    toretz[i] = scz[indices[i]]
    toretdst[i] = d[indices[i]]

  #print toretdst

  return toretx, torety, toretz, toretdst

#######################################################

def file_to_sphere_list(filename, spheres):

  file = open(filename, "r")

  R = - 1.0
  zmax = xmax = ymax = -10000.0
  zmin = xmin = ymin =  10000.0
  
  for sp in file:
    x, y, z, r = sp.split(" ")
    center = point.point(float(x), float(y), float(z))
    s = sphere(center, float(r))
    spheres.append(s)
  
    if (R < 0.0):
      R = s.get_radius()
    else:
      if (R != s.get_radius()):
        print("Error R differ")
        exit()
  
    if (zmax < (float(z) + float(r))):
      zmax = (float(z) + float(r))
    if (xmax < (float(x) + float(r))):
      xmax = (float(x) + float(r))
    if (ymax < (float(y) + float(r))):
      ymax = (float(y) + float(r))
  
    if (zmin > (float(z) - float(r))):
      zmin = (float(z) - float(r))
    if (xmin > (float(x) - float(r))):
      xmin = (float(x) - float(r))
    if (ymin > (float(y) - float(r))):
      ymin = (float(y) - float(r))
  
  file.close()

  return xmin, xmax, ymin, ymax, zmin, zmax, R

#######################################################

def get_near_sphere (scx, scy, scz, px, py, pz, distance) :

  distx = (scx - px)
  disty = (scy - py)
  distz = (scz - pz)

  distx2 = distx * distx
  disty2 = disty * disty
  distz2 = distz * distz

  dist = distx2 + disty2 + distz2

  d = numpy.sqrt(dist)

  bools1 = d <= distance

  indices, = numpy.where(bools1)

  toretx = numpy.linspace( 0.0, 0.0, len(indices))
  torety = numpy.linspace( 0.0, 0.0, len(indices))
  toretz = numpy.linspace( 0.0, 0.0, len(indices)) 
  toretdst = numpy.linspace( 0.0, 0.0, len(indices))

  for i in range(len(indices)):
    toretx[i] = scx[indices[i]]
    torety[i] = scy[indices[i]]
    toretz[i] = scz[indices[i]]
    toretdst[i] = d[indices[i]]
    #print d[indices[i]] , toretx[i], torety[i], toretz[i]

  return toretx, torety, toretz, toretdst

#######################################################

def file_to_sphere_diffr_list(filename, spheres):

  file = open(filename, "r")

  zmax = xmax = ymax = -10000.0
  zmin = xmin = ymin =  10000.0
  
  for sp in file:
    x, y, z, r = sp.split(" ")
    center = point.point(float(x), float(y), float(z))
    s = sphere(center, float(r))
    spheres.append(s)
  
    if (zmax < (float(z) + float(r))):
      zmax = (float(z) + float(r))
    if (xmax < (float(x) + float(r))):
      xmax = (float(x) + float(r))
    if (ymax < (float(y) + float(r))):
      ymax = (float(y) + float(r))
  
    if (zmin > (float(z) - float(r))):
      zmin = (float(z) - float(r))
    if (xmin > (float(x) - float(r))):
      xmin = (float(x) - float(r))
    if (ymin > (float(y) - float(r))):
      ymin = (float(y) - float(r))
  
  file.close()

  return xmin, xmax, ymin, ymax, zmin, zmax

###############################################################################

def get_rgb (value, min, max):

  r = 0
  g = 0
  b = 0

  middle = (float(max) - float(min)) / 2.0
  
  # red 
  if value >= middle:
    r = 0
  else:
    q = 0.0 
    a = 0.0
    if (middle == 0.0):
      q = 0.0
      a = 255.0 / min
    else:
      q = (255.0 * middle) / (middle - min)
      a = -1.0 * q / middle
    r = (a * value) + q

  # green 
  if value < middle:
    q = 0.0
    a = 0.0
    if (min == 0.0):
      q = 0.0
      a = 255.0 / middle
    else:
      q = (255.0 * min) / (min - middle)
      a = -1.0 * q / min
    g = (a * value) + q
  elif value == middle:
    g = 255
  else:
    q = 0.0
    a = 0.0
    if (max == 0.0):
      q = 0.0
      a = 255.0 / mid
    else:
      q = (255.0 * max) / (max - middle)
      a = -1.0 * q / max
    g = (a * value) + q

  # blue 
  if (value <= middle):
    b = 0
  else:
    a = 0.0
    q = 0.0
    if (middle == 0.0):
      q = 0.0
      a = 255.0 / max
    else:
      q = (255.0 * middle) / (middle - max)
      a = -1.0 * q / middle
    b = (a * value) + q

  return int(r), int(g), int(b)

###############################################################################

def angle_sum_poly (polypoint, q):

  EPSILON = 0.0000001
  RTOD = 57.2957795

  p1 = point.point()
  p2 = point.point()

  anglesum = 0.0
  n = len(polypoint)
  for i in range(n):

    p1.set_x(polypoint[i].get_x() - q.get_x())
    p1.set_y(polypoint[i].get_y() - q.get_y())
    p1.set_z(polypoint[i].get_z() - q.get_z())
    p2.set_x(polypoint[(i+1)%n].get_x() - q.get_x())
    p2.set_y(polypoint[(i+1)%n].get_y() - q.get_y())
    p2.set_z(polypoint[(i+1)%n].get_z() - q.get_z())

    #print polypoint[i].get_x() - q.get_x()
    #print polypoint[i].get_y() - q.get_y()
    #print polypoint[i].get_z() - q.get_z()
    #print polypoint[(i+1)%n].get_x() - q.get_x()
    #print polypoint[(i+1)%n].get_y() - q.get_y()
    #print polypoint[(i+1)%n].get_z() - q.get_z()
    #print " "
    
    m1 = point.norm(p1)
    m2 = point.norm(p2)

    costheta = 0.0
    if ((m1*m2) <= EPSILON):
      return(TWOPI)
    else:
      costheta = (p1.get_x()*p2.get_x() + p1.get_y()*p2.get_y() + \
          p1.get_z()*p2.get_z()) / (m1*m2)
    
    if costheta > 1.0:
      costheta =  1.0
    elif costheta < -1.0:
      costheta = -1.0

    anglesum += math.acos(costheta)

  return anglesum 

###############################################################################

def get_dist_point_segment (a, b, c):

  ab = b - a
  ac = c - a 
  bc = c - b
  
  e = triangle.dot(ac, ab)
  
  if (e <= 0.0):
    return triangle.dot(ac, ac)
  
  f = triangle.dot(ab, ab)
  if (e >= f): 
    return triangle.dot(bc, bc)
  
  return math.sqrt(triangle.dot(ac, ac) - e * e / f)

###############################################################################

def closest_point_point_segment(a, b, c):

  ab = b - a;
  
  t = triangle.dot(c - a, ab) / triangle.dot(ab, ab)
  
  if (t < 0.0): 
    t = 0.0
  
  if (t > 1.0):
    t = 1.0
  
  d = a + triangle.sxv(t, ab)
  
  return d

###############################################################################

def generate_point_inside_poly(p1, p2, p3, p4, step, psurface_list, label):

  polypoint = []
  polypoint.append(p1)
  polypoint.append(p2)
  polypoint.append(p3)
  polypoint.append(p4)

  # i 4 punti devono essere ordinati oraio o antiorario e' indifferente 
  # calcolo il lato piu' lungo 

  d = []

  d.append(p1.get_distance_from(p2))
  d.append(p2.get_distance_from(p3))
  d.append(p3.get_distance_from(p4))
  d.append(p4.get_distance_from(p1))
  
  idx = 0
  for i in range(1,4):
    if (d[i] > d[i-1]):
      idx = i

  #print "Max: ", d[idx]
  
  # forse meglio indicare lo step cosi' da avere uniformita' di punti
  numofp = int(d[idx] / step)
  if (numofp == 0):
    print("Step too big ", d[idx] , " and ", step, file=sys.stderr)
    return

  B = point.point()
  C = point.point()

  l = line.line3d()
  if idx == 0:
    l.set_two_point(p1, p2)
    B.set_coordinates(p2.get_x(), p2.get_y(), p2.get_z())
    C.set_coordinates(p3.get_x(), p3.get_y(), p3.get_z())
  elif idx == 1:
    l.set_two_point(p2, p3)
    B.set_coordinates(p3.get_x(), p3.get_y(), p3.get_z())
    C.set_coordinates(p4.get_x(), p4.get_y(), p4.get_z())
  elif idx == 2:
    l.set_two_point(p3, p4)
    B.set_coordinates(p4.get_x(), p4.get_y(), p4.get_z())
    C.set_coordinates(p1.get_x(), p1.get_y(), p1.get_z())
  elif idx == 3:
    l.set_two_point(p4, p1)
    B.set_coordinates(p1.get_x(), p1.get_y(), p1.get_z())
    C.set_coordinates(p2.get_x(), p2.get_y(), p2.get_z())

  # questi punti li genero lungo il lato piu' lungo 
  plist = l.generate_equi_point(numofp)
  """ provo a non aggiungere i punti del lato che comunque non 
      sono bene indetificabili come apparteneti ad una superficie o all'altra
  """
  for p in plist: 
    p.set_label(label)      
    psurface_list.append(p)
    #print psurface_list[-1].get_label()

  # http://www.youtube.com/watch?v=HmMJGcHV9Oc
  # equazione vettoriale del piano
  #
  # --   --       --       --  
  # OP = OA + a * AB + b * BC
  #
  # dove O origine P punto che voglio e A B C li definisco
  # a seconda del segmento che ho preso sopra
  #
  #  A---------------------B
  #                        |
  #                        |
  #                        |
  #                        C
  # mi muovo lungo BC step by step
  # posso usare sempre le rette cambio nella line3d il valore di a
  # e di b quindi A diventa ogni volta il punto in plist, e b diventa
  # il vettore paralleloa BC, dovrebbe bastare appunto BC.

  lBC = line.line3d()
  lBC.set_b(C-B)
  for p in plist:
    lBC.set_a(p)
    plistBC = lBC.generate_equi_point(numofp)
    for pBC in plistBC:
      diff = math.fabs(angle_sum_poly(polypoint, pBC) - TWOPI)
      if (diff < 1e-10):
        pBC.set_label(label)
        psurface_list.append(pBC)
        #print psurface_list[-1].get_label()

  return 

###############################################################################

# V = an array of n+2 vertices in a plane
#     with V[n]=V[0] and V[n+1]=V[1]
# N = unit normal vector of the polygon's plane

def area3D_polygon (n, V, N):
# http://softsurfer.com/Archive/algorithm_0101/algorithm_0101.htm#area3D_Polygon%28%29

  print("FIX IT")

  return -1.0

  area = 0.0

  print(N)
  
  # select largest abs coordinate to ignore for projection
  ax = math.fabs(N.get_x())
  ay = math.fabs(N.get_y())
  az = math.fabs(N.get_z())

  if ax == 0.0:
    j = 2
    k = 0
    for i in range(1,n+1):
      area += V[i].get_x() * (V[j].get_y() - V[k].get_y())
    return (area / 2.0)
  elif ay == 0.0:
    j = 2
    k = 0
    for i in range(1,n+1):
      area += V[i].get_y() * (V[j].get_z() - V[k].get_z())
    return area / 2.0
  elif az == 0.0:
    j = 2
    k = 0
    for i in range(1,n+1):
      area += V[i].get_x() * (V[j].get_z() - V[k].get_z())
    return area / 2.0

  coord = 3 # ignore z-coord
  if ax > ay:
    if ax > az: 
      coord = 1 # ignore x-coord
  elif ay > az: 
    coord = 2 # ignore y-coord

  # compute area of the 2D projection
  j = 2 
  k = 0
  for i in range(1,n+1):
    if coord == 1:
      area += (V[i].get_y() * (V[j].get_z() - V[k].get_z()))
    elif coord == 2:
      print(V[j].get_z(), V[k].get_z())
      area += (V[i].get_x() * (V[j].get_z() - V[k].get_z()))
    elif coord == 3:
      area += (V[i].get_x() * (V[j].get_y() - V[k].get_y()))

    j += 1
    k += 1

  # scale to get area before projection
  an = math.sqrt( ax*ax + ay*ay + az*az) # length of normal vector
  if coord == 1:
    area *= (an / (2*ax))
  elif coord == 2:
    area *= (an / (2*ay))
  elif coord == 3:
    area *= (an / (2*az))
   
  return area
