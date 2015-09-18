import sys
sys.path.append("../modules")

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

def inside_any_cubes (cub, cubes, cubcenterx, cubcentery, cubcenterz, 
    cubradius):

  cx, cy, cz = cub.get_center()

  bools1 = numpy.sqrt((cubcenterx - cx)**2 + (cubcentery - cy)**2 +  \
      (cubcenterz - cz)**2) <= 2.0*cubradius
  interior_indices, = numpy.where(bools1)

  for idx in interior_indices:
    if (cubes[idx].is_point_inside([cx, cy, cz])):
      return True

  for idx in interior_indices:
    for p in cub.get_cube_coordintes():
      if (cubes[idx].is_point_inside(p)):
        return True

  for idx in interior_indices:
    for p in cubes[idx].get_cube_coordintes():
      if (cub.is_point_inside(p)):
        return True

  return False

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

def get_occopied_face (iface):

  if (iface == 1):
    occupiediface = 2
  elif (iface == 2):
    occupiediface = 1
  elif (iface == 3):
    occupiediface = 5
  elif (iface == 4):
    occupiediface = 6
  elif (iface == 5):
    occupiediface = 3
  elif (iface == 6):
    occupiediface = 4

  return occupiediface

###############################################################################

# non mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

NUM_OF_STARTING_CUBE = 20
MAX_NUM_OF_CUBE = 50*NUM_OF_STARTING_CUBE

CUBE_DIM = 0.633

zmax = xmax = ymax = 20.0
zmin = xmin = ymin = 0.0

print >> sys.stderr, "Box limits: ", xmin, xmax, ymin, ymax, zmin, zmax

# voglio fermarmi a circa 2 D dalla vetta visto che in cima avro' sempre una
# densita' minore(ricorda la prima sfera che supera zmax ferma la procedura.

actors = []

actors.extend(cube.cube_to_actors (xmin, ymin, zmin, \
    xmax, ymax, zmax))

cubcenterx = numpy.empty(0)
cubcentery = numpy.empty(0)
cubcenterz = numpy.empty(0)
cubradius = numpy.empty(0)

centers = []
cubes = []

j = 0
while (j < (NUM_OF_STARTING_CUBE/2)):

  x = random.uniform(xmin + CUBE_DIM*math.sqrt(3.0), xmax - CUBE_DIM*math.sqrt(3.0))
  y = random.uniform(ymin + CUBE_DIM*math.sqrt(3.0), ymax - CUBE_DIM*math.sqrt(3.0))
  z = random.uniform(zmin + CUBE_DIM*math.sqrt(3.0), zmax - CUBE_DIM*math.sqrt(3.0))

  if (not ([x, y, z] in centers)): # se non lo faccio i punti su angolo non vengono 
                                   # visti come interni

    cub = cube_fill.cube(x, y, z, CUBE_DIM)
    tetha = random.uniform(0.0, 2.0*math.pi)
    px = random.uniform(xmin, xmax)
    py = random.uniform(ymin, ymax)
    pz = random.uniform(zmin, zmax)

    p = point.point(px, py, pz)

    cub.rotate(p, tetha)

    # check if any point of the cubes is inside not perfect but good enough

    if (not inside_any_cubes (cub, cubes, cubcenterx, 
      cubcentery, cubcenterz, cubradius)):
      cubes.append(cub)
      centers.append([x, y, z])
      # append to centers array e radius using numpy.append(array, values)
      cubcenterx = numpy.append(cubcenterx, x)
      cubcentery = numpy.append(cubcentery, y)
      cubcenterz = numpy.append(cubcenterz, z)
      cubradius = numpy.append(cubradius, cub.get_radius()) 

      j = j + 1

      actors.append(cub.get_vtk_actor(0.5, 0.6, 0.1))


j = 0
while (j < (NUM_OF_STARTING_CUBE/2)):
  # questi vanno piazzati sulle superficie 

  x = random.uniform(xmin + CUBE_DIM*math.sqrt(3.0), xmax - CUBE_DIM*math.sqrt(3.0))
  y = random.uniform(ymin + CUBE_DIM*math.sqrt(3.0), ymax - CUBE_DIM*math.sqrt(3.0))
  z = zmin + CUBE_DIM/2.0

  if (not ([x, y, z] in centers)): # se non lo faccio i punti su angolo non vengono 
                                   # visti come interni

    cub = cube_fill.cube(x, y, z, CUBE_DIM)

    # check if any point of the cubes is inside not perfect but good enough

    if (not inside_any_cubes (cub, cubes, cubcenterx, 
      cubcentery, cubcenterz, cubradius)):
      cubes.append(cub)
      centers.append([x, y, z])
      # append to centers array e radius using numpy.append(array, values)
      cubcenterx = numpy.append(cubcenterx, x)
      cubcentery = numpy.append(cubcentery, y)
      cubcenterz = numpy.append(cubcenterz, z)
      cubradius = numpy.append(cubradius, cub.get_radius()) 

      j = j + 1

      actors.append(cub.get_vtk_actor(0.5, 0.6, 0.1))

i = len(cubes)
while (i < MAX_NUM_OF_CUBE):

  oldnumof = len(cubes)

  for cubi in range(oldnumof):
    if (cubes[cubi].has_free_face ()):
      
      iface = random.randint(1, 6)
      while (not cubes[cubi].is_face_free(iface)):
        iface = random.randint(1, 6)

      newcenter, p1, p2, p3, p4, \
      p5, p6, p7, p8 = cubes[cubi].set_iface (iface)
      dim = cubes[cubi].get_dim()
      # la faccia del nuovo cubo che verra' occupata 
      occupiediface = get_occopied_face (iface)

      if ((newcenter[0] < xmax) and (newcenter[0] > xmin) and \
          (newcenter[1] < ymax) and (newcenter[1] > ymin) and \
          (newcenter[2] < zmax) and (newcenter[2] > zmin)):

        # dovrebbe essere un modo semplice per vedere se il cubo si sovrappone
        if (not (newcenter in centers)):
        
          newcub = cube_fill.cube(newcenter[0], newcenter[1], newcenter[2], dim)
          newcub.set_iface (occupiediface)
          newcub.set_points (p1, p2, p3, p4, p5, p6, p7, p8)
       
          if (not inside_any_cubes (newcub, cubes, cubcenterx, \
            cubcentery, cubcenterz, cubradius)):
            cubes.append(newcub)
            centers.append(newcenter)
            cubcenterx = numpy.append(cubcenterx, x)
            cubcentery = numpy.append(cubcentery, y)
            cubcenterz = numpy.append(cubcenterz, z)
            cubradius = numpy.append(cubradius, cub.get_radius()) 
            i = i + 1
       
            actors.append(newcub.get_vtk_actor(0.5, 0.6, 0.1))

visualize_nanop.visualize_actors (actors)
