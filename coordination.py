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

volume_of_sphere = 0.0
zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

for sp in file:
  x, y, z, r = sp.split(" ")
  center = point(float(x), float(y), float(z))
  s = sphere(center, float(r))
  spheres.append(s)

  volume_of_sphere += s.get_volume()

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

volume = (xmax-xmin) * (ymax-ymin) * (zmax-zmin)

print "TopX: ", xmax, "BotX: ", xmin
print "TopY: ", ymax, "BotY: ", ymin
print "TopZ: ", zmax, "BotZ: ", zmin

porosity = (volume-volume_of_sphere)/volume

print ""
print "Porosity : ", porosity

file.close()

coord_number_dist = {}

numof = 0
average_diff = 0.0
average_diff_2 = 0.0

print ""
print "Non-Touching spheres: "

for s1 in spheres:
  coordination = 0
  c1 = s1.get_center()
  r1 = s1.get_radius()
  for s2 in spheres:
    if (s2 != s1):
      c2 = s2.get_center()
      r2 = s2.get_radius()
      
      d = c1.get_distance_from (c2)
      
      if (d <= (r1+r2)):
        coordination += 1
      
        numof += 1
        average_diff += d
        average_diff_2 += d*d

  if coordination == 0:
    print c1, r1

  if coordination in coord_number_dist:
    coord_number_dist[coordination] += 1
  else:
    coord_number_dist[coordination] = 1

print ""
print "Average difference of touch sphere: ", average_diff/numof , \
    " +/- " , (1.0/numof) * math.sqrt((numof * average_diff_2) - \
    math.pow(average_diff,2.0))

print ""
print "Coordination: "
for coord in coord_number_dist.iterkeys():
  print coord, coord_number_dist[coord]
