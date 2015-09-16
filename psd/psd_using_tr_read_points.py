import sys
sys.path.append("../modules")

import util
import line
import point
import sphere
import circle
import square
import triangle

import util_for_tr

import random
import math
import sys
import vtk

###############################################################################

filename = "final_config.txt"

hw_many_planes = 100
hw_many_points = 1000

spheres = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    util.file_to_sphere_diffr_list(filename, spheres)

totr = 0.0
for s in spheres:
  totr += s.get_radius()
  
meanr = totr / float(len(spheres))
meand = 2.0 * meanr

#print "xmax: ", xmax, "xmin: ",xmin, "ymax: ", ymax, \
#    "ymin: ", ymin, "zmx: ", zmax, "zmin: ", zmin

file = open("points.txt", "r")

for line in file:
  sx, sy, sz = line.split(" ")  

  x = float(sx)
  y = float(sy)
  z = float(sz)  

  circles = util_for_tr.get_circle_in_plane (spheres, z)

  if not util_for_tr.is_inside_circles (x, y, circles):

    poly_data_points_initial = util_for_tr.get_circle_points_list(x, y, circles)

    poly_data_points = []
    for p in poly_data_points_initial:
      d = util_for_tr.point_distance(p, [x, y])
      if (d <= util_for_tr.MAXDISTANCEFORP):
        poly_data_points.append(p)

    print x, y, z, x, y, z, \
        2.0 * util_for_tr.get_radius([x, y], poly_data_points, z)

    sys.stdout.flush()

print >> sys.stderr, "100%"
sys.stderr.flush()

