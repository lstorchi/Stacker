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

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

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

# voglio fermarmi a circa 2 D dalla vetta visto che in cima avro' sempre una
# densita' minore(ricorda la prima sfera che supera zmax ferma la procedura.
dz = ((zmax - zmin) - (2.0 * meand)) / float(hw_many_planes+1)

#print "xmax: ", xmax, "xmin: ",xmin, "ymax: ", ymax, \
#    "ymin: ", ymin, "zmx: ", zmax, "zmin: ", zmin

refperc = 5.0

for iplane in range(hw_many_planes):

  zplane = zmin + meand + (iplane+1)*dz
  circles = util_for_tr.get_circle_in_plane (spheres, zplane)

  perc = 100.0 * (float(iplane) / float(hw_many_planes))
  if perc >= refperc:
    print >> sys.stderr, refperc , "%"
    refperc += 5.0
    sys.stderr.flush()

  for i in range(hw_many_points):

    x = random.uniform(xmin + meand, xmax - meand)
    y = random.uniform(ymin + meand, ymax - meand)

    if not util_for_tr.is_inside_circles (x, y, circles):

      poly_data_points_initial = util_for_tr.get_circle_points_list(x, y, circles)

      poly_data_points = []
      for p in poly_data_points_initial:
        d = util_for_tr.point_distance(p, [x, y])
        if (d <= util_for_tr.MAXDISTANCEFORP):
          poly_data_points.append(p)

      """
      poly_data_points = util_for_tr.get_circle_points_list(x, y, circles)
      """

      print x, y, zplane, x, y, zplane, \
          2.0 * util_for_tr.get_radius([x, y], poly_data_points, zplane)

      sys.stdout.flush()

print >> sys.stderr, "100%"
sys.stderr.flush()

