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
import util_for_tr
import nanoparticle

import random
import numpy
import math
import sys
import vtk

###############################################################################

# non mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0
util_for_tr.NUMOFCIRCLEPOINTS = 180

MAX_POINT_TODO = 2000

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

hw_many_planes = 35
hw_many_points = 400

nanoparticles = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles)

Dz = (zmax-zmin)
Dy = (ymax-ymin)
Dx = (xmax-xmin)

scx, scy, scz, radius = nanoparticle.nanoparticle_list_to_arrays(nanoparticles)

meanr = radius.mean()
meand = 2.0 * meanr

# voglio fermarmi a circa 2 D dalla vetta visto che in cima avro' sempre una
# densita' minore(ricorda la prima sfera che supera zmax ferma la procedura.
dz = ((zmax - zmin) - (3.0 * meand)) / float(hw_many_planes+1)

print >> sys.stderr, xmin, xmax, ymin, ymax, zmin, zmax, dz
print >> sys.stderr, xmin + 1.5*meand, xmax - 1.5*meand
print >> sys.stderr, ymin + 1.5*meand, ymax - 1.5*meand
print >> sys.stderr, meand, nanoparticles[0].get_dimensions()

count_point_not_inside = 0

refperc = 5.0

for iplane in range(hw_many_planes):

  perc = 100.0 * (float(iplane) / float(hw_many_planes))
  if perc >= refperc:
    print >> sys.stderr, refperc , "%"
    refperc += 5.0
    sys.stderr.flush()

  zplane = zmin + 1.5 * meand + (iplane+1)*dz

  # seleziona le nanoparticelle che dovrebbero passare per il piano
  # usando le sfere per fare la selezione e' possibile io ottenga
  # dei falsi positivi

  bools1 = numpy.fabs(scz - zplane) < radius
  interior_indices, = numpy.where(bools1)

  for i in range(hw_many_points):

    x = random.uniform(xmin + 1.5*meand, xmax - 1.5*meand)
    y = random.uniform(ymin + 1.5*meand, ymax - 1.5*meand)

    is_inside = False

    for idx in interior_indices:
      cx, cy, cz = nanoparticles[idx].get_center()
      dist = util_for_tr.point_distance([x, y], [cx, cy])

      if (dist <= radius[idx]):
        if (nanoparticles[idx].is_point_inside([x, y, zplane])):
          is_inside = True
          break

    if not is_inside:
      count_point_not_inside += 1

      if (count_point_not_inside >= MAX_POINT_TODO) :
        print >> sys.stderr, "Max point reached " 
        sys.stdout.flush()
        sys.stderr.flush()
        exit(1)

      p = point.point(x, y, zplane)

      # q lo genero fuori dalla box perche' cosi' sono certo attraversera 
      # tutte le nanoparticelle
      point_circle = circle.circle(x, y, 2.0 * max(Dx, Dy, Dz))
      second_points = point_circle.generate_circle_points(\
          util_for_tr.NUMOFCIRCLEPOINTS)

      for sp in second_points:
        q = point.point(sp[0], sp[1], zplane)  

        selected_point = []
        min_d = float("inf")
        for idx in interior_indices:
          intersect_points = nanoparticles[idx].intersect_line(p, q)

          d = 0.0
          if (len(intersect_points) == 2):
            d = util_for_tr.point_distance([intersect_points[0][0], 
              intersect_points[0][1]], \
                [intersect_points[1][0], \
                  intersect_points[1][1]])

            print len(intersect_points), " " , d
            sys.stdout.flush()
          else:
            print >> sys.stderr, x, " ", y, " ", zplane, " NO INTESECT"

print >> sys.stderr, "100%"
sys.stderr.flush()
