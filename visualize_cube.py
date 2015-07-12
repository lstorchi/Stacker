import sys
sys.path.append("./modules")

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
  cx, cy, cz, dim = sp.split(" ")
  cub = cube_fill.cube(float(cx), float(cy), \
      float(cz), float(dim))
  cub2 = cube_fill.cube(float(cx), float(cy), \
      float(cz), float(dim))
 
  # test rotate  
  tetha = random.uniform(0.0, 2.0*math.pi)
  x = random.uniform(0.0, 300.0)
  y = random.uniform(0.0, 300.0)
  z = random.uniform(0.0, 300.0)
  #p = point.point(float(cx), float(cy), float(cz) + 10.0)
  p = point.point(x, y, z)
  # 
  cub2.rotate(p, tetha)
  cubes.append(cub)
  cubes.append(cub2)

file.close()

actors = []

p = [97.8826536512+0.4, 111.442677785+0.46, 111.202123474+0.49]
ptc = point.point(p[0], p[1], p[2])
actors.append(ptc.get_actor())

for cub in cubes:
  print "is inside: ", cub.is_point_inside(p)
  actors.append(cub.get_vtk_actor(0.5, 0.6, 0.1, 1.0))

visualize_nanop.visualize_actors (actors)
