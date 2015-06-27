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

###############################################################################

# non mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

MAX_NUM_OF_POINT = 2000
POINT_TODO = 1

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

nanoparticles = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles)

scx, scy, scz, radius = nanoparticle.nanoparticle_list_to_arrays(nanoparticles)

meanr = radius.mean()
meand = 2.0 * meanr

print "Mean r: ", meanr
print "Box limits: ", xmin, xmax, ymin, ymax, zmin, zmax

# voglio fermarmi a circa 2 D dalla vetta visto che in cima avro' sempre una
# densita' minore(ricorda la prima sfera che supera zmax ferma la procedura.

for i in range(MAX_NUM_OF_POINT/POINT_TODO):

  # seleziona le nanoparticelle 
  # usando le sfere per fare la selezione e' possibile io ottenga
  # dei falsi positivi

  for j in range(POINT_TODO):
    x = random.uniform(xmin + 1.5*meand, xmax - 1.5*meand)
    y = random.uniform(ymin + 1.5*meand, ymax - 1.5*meand)
    z = random.uniform(zmin + 1.5*meand, zmax - 1.5*meand)

    print x, y, z

    bools1 = numpy.sqrt((scx - x)**2 + (scy - y)**2 + (scz - z)**2) <= 2.0*radius
    interior_indices, = numpy.where(bools1)

    is_inside = False

    nanoparticles_tovis = []

    for idx in interior_indices:
      nanoparticles_tovis.append(nanoparticles[idx])
      if (nanoparticles[idx].is_point_inside([x, y, z])):
        is_inside = True
        break

    if not is_inside:
      cub = cube_fill.cube(x, y, z, 1.0)
      #visualize_nanop.visualize_nanoparticle_and_point(nanoparticles_tovis, x, y, z)
      visualize_nanop.visualize_nanoparticle_and_actor(nanoparticles_tovis, \
          cub.get_actor(0.5, 0.6, 0.1))
      
      exit()
     
