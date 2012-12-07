import re
import sys
import vtk
import time

sys.path.append("./modules")

import util
import point
import sphere
import nanoparticle

import math
import numpy
import random

###############################################################################

def get_near_nanoparticle (nanopscx, nanopscy, nanopscz, px, py, pz, distance):

  distx = (nanopscx - px)
  disty = (nanopscy - py)
  distz = (nanopscz - pz)

  distx2 = distx * distx
  disty2 = disty * disty
  distz2 = distz * distz

  dist = distx2 + disty2 + distz2

  d = numpy.sqrt(dist)

  bools1 = d <= distance

  indices, = numpy.where(bools1)

  return indices

###############################################################################

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

filename = "pore_radius_list_nano.txt"
filenamenanop = "final_config_nanoparticle.txt"

if (len(sys.argv)) == 3:
  filename = sys.argv[1]
  filenamenanop = sys.argv[2]

file = open(filename, "r")

pores = []

for sp in file:
  x, y, z, cx, cy, cz, r = sp.split(" ")

  center = point.point(float(cx), float(cy), float(cz))
  s = sphere.sphere(center, float(r))
  pores.append(s)

file.close()

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filenamenanop, nanoparticles) 

nanopscx, nanopscy, nanopscz = \
    nanoparticle.nanoparticle_to_arrays (nanoparticles)

for pore in pores:
  pcenter = pore.get_center()
  pradius = pore.get_radius()
  distance = 3.0 * pradius
  cx = pcenter.get_x()
  cy = pcenter.get_y()
  cz = pcenter.get_z()

  psurface_points = pore.generate_surface_points(20)

  indexes = get_near_nanoparticle (nanopscx, nanopscy, \
      nanopscz, cx, cy, cz, distance)

  touch_nanoparticle = False
  for i in indexes:
    if (nanoparticles[i].sphere_touch_me_surface_points(pradius, pcenter,
        psurface_points)):
      touch_nanoparticle = True 
      break;

  if touch_nanoparticle:
    print >> sys.stderr, "Touch nanoparticle"
  else:
    print cx, cy, cz, cx, cy, cz, pradius

