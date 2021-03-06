import sys
sys.path.append("../modules")

import util
import line
import cube
import math
import point
import sphere
import circle
import square
import triangle
import cube_fill
import util_for_tr
import nanoparticle
import visualize_nanop

import random
import numpy
import math
import sys
import vtk

# non mi interessano le intersezioni

filename = "cubes.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

cubes = []

file = open(filename, "r")

for sp in file:
  cx, cy, cz, dim, \
      p1x, p1y, p1z, p2x, p2y, p2z, \
      p3x, p3y, p3z, p4x, p4y, p4z, \
      p5x, p5y, p5z, p6x, p6y, p6z, \
      p7x, p7y, p7z, p8x, p8y, p8z, \
      = sp.split(" ")

  cub = cube_fill.cube(float(cx), float(cy), \
      float(cz), float(dim))
  p1 = [float(p1x), float(p1y), float(p1z)]
  p2 = [float(p2x), float(p2y), float(p2z)]
  p3 = [float(p3x), float(p3y), float(p3z)]
  p4 = [float(p4x), float(p4y), float(p4z)]
  p5 = [float(p5x), float(p5y), float(p5z)]
  p6 = [float(p6x), float(p6y), float(p6z)]
  p7 = [float(p7x), float(p7y), float(p7z)]
  p8 = [float(p8x), float(p8y), float(p8z)]

  # setta i punti solo se tutti compatibili con la distanza
  cub.set_points (p1, p2, p3, p4, p5, p6, p7, p8)

  cubes.append(cub)

file.close()

actors = []

#p = [97.8826536512+0.4, 111.442677785+0.46, 111.202123474+0.49]
#ptc = point.point(p[0], p[1], p[2])
#actors.append(ptc.get_actor())

for cub in cubes:
  #print "is inside: ", cub.is_point_inside(p)
  actors.append(cub.get_vtk_actor(0.5, 0.6, 0.1, 1.0))

visualize_nanop.visualize_actors (actors)
