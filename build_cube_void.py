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

def is_inside_nanoparticles (x, y, z, nanoparticles, scx, scy, scz, radius):

  bools1 = numpy.sqrt((scx - x)**2 + (scy - y)**2 + (scz - z)**2) <= 2.0*radius
  interior_indices, = numpy.where(bools1)

  is_inside = False

  for idx in interior_indices:
    if (nanoparticles[idx].is_point_inside([x, y, z])):
      is_inside = True
      break

  return is_inside

###############################################################################

def cube_is_inside_nanoparticles (cube, nanoparticles, scx, scy, scz, radius):

  x, y, z = cube.get_center()

  bools1 = numpy.sqrt((scx - x)**2 + (scy - y)**2 + (scz - z)**2) <= 2.0*radius
  interior_indices, = numpy.where(bools1)

  is_inside = False

  for p in cube.get_cube_coordintes():
    for idx in interior_indices:
      if (nanoparticles[idx].is_point_inside(p)):
        is_inside = True
        break

    if is_inside:
      break

  return is_inside


###############################################################################

# non mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

MAX_NUM_OF_CUBE = 50000
POINT_TODO = 10
CUBE_DIM = 1.0

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

print >> sys.stderr, "Mean r: ", meanr
print >> sys.stderr, "Box limits: ", xmin, xmax, ymin, ymax, zmin, zmax

# voglio fermarmi a circa 2 D dalla vetta visto che in cima avro' sempre una
# densita' minore(ricorda la prima sfera che supera zmax ferma la procedura.


#actors = []

centers = []
cubes = []
j = 0
while (j < POINT_TODO):
  x = random.uniform(xmin + 1.5*meand, xmax - 1.5*meand)
  y = random.uniform(ymin + 1.5*meand, ymax - 1.5*meand)
  z = random.uniform(zmin + 1.5*meand, zmax - 1.5*meand)

  #print x, y, z

  bools1 = numpy.sqrt((scx - x)**2 + (scy - y)**2 + (scz - z)**2) <= 2.0*radius
  interior_indices, = numpy.where(bools1)

  is_inside = False

  for idx in interior_indices:
    if (nanoparticles[idx].is_point_inside([x, y, z])):
      is_inside = True
      break

  if not is_inside:

    if (not ([x, y, z] in centers)):

      #for idx in interior_indices:
      #  actors.append(nanoparticles[idx].get_vtk_actor(color=True,opacity=1.0))
   
      centers.append([x, y, z])
      j = j + 1
      cub = cube_fill.cube(x, y, z, CUBE_DIM)
      cubes.append(cub)
      #actors.append(cub.get_actor(0.5, 0.6, 0.1))

i = 0
while (i < MAX_NUM_OF_CUBE):

  # seleziona le nanoparticelle 
  # usando le sfere per fare la selezione e' possibile io ottenga
  # dei falsi positivi

  addedcubes = []
  for cub in cubes:
    if (cub.has_free_face ()):

      iface = random.randint(1, 6)
      while (not cub.is_face_free(iface)):
        iface = random.randint(1, 6)

      cx, cy, cz = cub.get_center ()
      cub.set_iface (iface)
      dim = cub.get_dim()
      
      # la faccia del nuovo cubo che verra' occupata 
      occupiediface = 0
      if (iface == 1):
        cz = cz - dim/2.0
        occupiediface = 2
      elif (iface == 2):
        cz = cz + dim/2.0
        occupiediface = 1
      elif (iface == 3):
        cx = cx - dim/2.0
        occupiediface = 5
      elif (iface == 4):
        cy = cy + dim/2.0
        occupiediface = 6
      elif (iface == 5):
        cx = cx + dim/2.0
        occupiediface = 3
      elif (iface == 6):
        cy = cy - dim/2.0
        occupiediface = 4

      # dovrebbe essere un modo semplice per vedere se il cubo si sovrappone
      if (not ([cx, cy, cz] in centers)):
      
        centers.append([cx, cy, cz])
        newcub = cube_fill.cube(cx, cy, cz, dim)
        newcub.set_iface (occupiediface)

        if (not cube_is_inside_nanoparticles(newcub, nanoparticles, \
          scx, scy, scz, radius)):
          addedcubes.append(newcub)
          #actors.append(newcub.get_actor(0.5, 0.6, 0.1))
          print cx, cy, cz, CUBE_DIM
          i = i + 1

  cubes.extend(addedcubes)

#visualize_nanop.visualize_actors (actors)
