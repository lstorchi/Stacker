import sys
sys.path.append("./modules")

import util
import line
import cube
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
  cubes.append(cub)

file.close()

actors = []

for cube in cubes:
  actors.append(cub.get_actor(0.5, 0.6, 0.1))

visualize_nanop.visualize_actors (actors)
