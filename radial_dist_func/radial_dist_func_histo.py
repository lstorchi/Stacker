import sys
sys.path.append("../modules")

from point import *
from sphere import *

import math

filename = "final_config.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

file = open(filename, "r")

spheres = []

zmax = xmax = ymax = -10000000.0
zmin = xmin = ymin =  10000000.0

R_average = 0.0

for sp in file:
  x, y, z, r = sp.split(" ")
  center = point(float(x), float(y), float(z))
  s = sphere(center, float(r))
  spheres.append(s)

  R_average += float(r)

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

R_average = R_average / len(spheres)

print "TopX: ", xmax, "BotX: ", xmin
print "TopY: ", ymax, "BotY: ", ymin
print "TopZ: ", zmax, "BotZ: ", zmin
print ""
print "R_average: " , R_average

file.close()

values = []

volume = (zmax - zmin) * (xmax - xmin) * (ymax - ymin)
ndens = len(spheres) / volume

dr = 0.4
bintouse = int ((zmax - zmin) / dr)

print "volume: ", volume
print "ndens: ", ndens
print "bin: ", bintouse

for s1 in spheres:
  c1 = s1.get_center()
  x1 = c1.get_x()
  y1 = c1.get_y()
  z1 = c1.get_z()
  for s2 in spheres:
    c2 = s2.get_center()
    dx = c2.get_x() - x1
    dy = c2.get_y() - y1
    dz = c2.get_z() - z1
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)

    values.append(dist)

y, x = numpy.histogram(values, bins=bintouse)

for i in range(0, len(y)):
  r = (x[i]+x[i+1])/2.0
  norm = ndens * 4.0 * numpy.pi * r * r * dr
  print (r, " " , y[i]*norm)

  print (x[i]+x[i+1])/2.0, " " , y[i]

