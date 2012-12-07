import sys
sys.path.append("./modules")

import util
import point
import sphere

import math

filename = "final_config.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

spheres = []

zmax = xmax = ymax = -10000000.0
zmin = xmin = ymin =  10000000.0

xmin, xmax, ymin, ymax, zmin, zmax = \
     util.file_to_sphere_diffr_list(filename, spheres)

print "TopX: ", xmax, "BotX: ", xmin
print "TopY: ", ymax, "BotY: ", ymin
print "TopZ: ", zmax, "BotZ: ", zmin
print ""

# radial distribution function
dr = 0.5
tuple_box = (xmax-xmin, ymax-ymin, zmax-zmin)

from paircorrelation import *
from numpy import *

x = linspace( 0.0, 0.0, len(spheres)) 
y = linspace( 0.0, 0.0, len(spheres))
z = linspace( 0.0, 0.0, len(spheres))

R = 0.0
i = 0
for s in spheres:
  c = s.get_center()
  x[i] = c.get_x()
  y[i] = c.get_y()
  z[i] = c.get_z()
  i += 1
  R += s.get_radius()

R = R / float(len(spheres))

R_max = min(min(tuple_box)/2.0, 6.0*R)

g_average, radii, x_int, y_int, z_int, indxs = \
    pair_correlation_function(x, y, z, \
        max(tuple_box)+(R),R_max,dr)

spheres_inner = []
for i in indxs:
  s = spheres[i]

  spheres_inner.append(s)

coord_number_dist = {}

numof = 0
average_diff = average_diff_2 = 0.0

for s1 in spheres_inner:
  coordination = 0
  c1 = s1.get_center()
  r1 = s1.get_radius()
  for s2 in spheres:
    c2 = s2.get_center()
    r2 = s2.get_radius()

    if ((c1.get_x() != c2.get_x()) and \
        (c1.get_y() != c2.get_y()) and \
        (c1.get_z() != c2.get_z())) :
      
      d = c1.get_distance_from (c2)
      
      if (d <= ((r1+r2)+( ((r1+r2)/100.0) * 10.0 )) ):
      #if (d <= (r1+r2)):
        coordination += 1
      
        numof += 1
        average_diff += d
        average_diff_2 += d*d

  if coordination in coord_number_dist:
    coord_number_dist[coordination] += 1
  else:
    coord_number_dist[coordination] = 1

print ""
print "Average difference of touch sphere: ", average_diff/numof , \
    " +/- " , (1.0/numof) * math.sqrt((numof * average_diff_2) - \
    math.pow(average_diff,2.0))

tot = 0.0
print ""
print "Coordination: "
for coord in coord_number_dist.iterkeys():
  print coord, float(coord_number_dist[coord])/float(len(spheres_inner))
  tot += coord * float(coord_number_dist[coord])

print " Average coordination number: ", tot/len(spheres_inner)
