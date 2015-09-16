import re
import sys
import time
import numpy

sys.path.append("../modules")

import sphere
import util

filename = "final_config.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

spheres = []
zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    util.file_to_sphere_diffr_list(filename, spheres) 

scx, scy, scz, radius = util.sphere_to_arrays (spheres)

botx = min(scx)
boty = min(scy)
botz = min(scz)
topx = max(scx)
topy = max(scy)
topz = max(scz)

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

rm = numpy.mean(radius)
print "Mean radius: ", rm


"""
y, x = numpy.histogram(radius, bins=100)

for i in range(min(len(x), len(y))):
  print x[i], y[i]
"""
