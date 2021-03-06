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

import cubes_utility

CUBE_DIM = 0.633
CUBERADIUSLIMIT = CUBE_DIM*math.sqrt(3.0)
#CUBERADIUSLIMIT = CUBE_DIM

###############################################################################

def inside_any_cubes (cub, cubes, cubcenterx, cubcentery, cubcenterz, 
    cubradius):

  cx, cy, cz = cub.get_center()

  bools1 = numpy.sqrt((cubcenterx - cx)**2 + (cubcentery - cy)**2 +  \
      (cubcenterz - cz)**2) <= 2.0*CUBERADIUSLIMIT
  interior_indices, = numpy.where(bools1)

  #print numpy.sqrt((cubcenterx - cx)**2 + (cubcentery - cy)**2 +\
  #    (cubcenterz - cz)**2)

  #for i in range(len(cubcenterx)):
  #  d = math.sqrt((cubcenterx[i] - cx)**2 + (cubcentery[i] - cy)**2 + \
  #      (cubcenterz[i] - cz)**2)
  #  if (d <= 2.0*CUBE_DIM*math.sqrt(3.0)):
  #     if (cubes[i].get_tagnumber() != \
  #         cub.get_tagnumber()):
  #       return True

  #print interior_indices, len(interior_indices)

  if (len(interior_indices) > 0):
    for idx in interior_indices:
      #print cubes[idx].get_tagnumber(), " vs ", cub.get_tagnumber()
      if (cubes[idx].get_tagnumber() != \
          cub.get_tagnumber()):
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

import os, errno

def silentremove(filename):
  try:
    os.remove(filename)
  except OSError as e: # this would be "except OSError, e:" before Python 2.6
    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
      raise # re-raise exception if a different error occured

###############################################################################

def is_very_close (newcenter, cubcenterx, cubcentery, cubcenterz):

  cx = newcenter[0]
  cy = newcenter[1]
  cz = newcenter[2]

  bools1 = numpy.sqrt((cubcenterx - cx)**2 + (cubcentery - cy)**2 +  \
      (cubcenterz - cz)**2) <= CUBE_DIM/2.0

  interior_indices, = numpy.where(bools1)

  return (len(interior_indices) != 0)

###############################################################################

NUM_OF_STARTING_CUBE = 20
MAX_NUM_OF_CUBE = 10*NUM_OF_STARTING_CUBE

cubesets = []

zmax = xmax = ymax = 30*CUBE_DIM
zmin = xmin = ymin = 0.0

# questo potrebbe essere un buon modo per trovare un massimo di numeri
NXN = int ((xmax-xmin)/CUBE_DIM) + 1
NYN = int ((ymax-ymin)/CUBE_DIM) + 1
NZN = int ((zmax-zmin)/CUBE_DIM) + 1

MAX_NUM_OF_CUBE = NXN * NYN * NZN

#MAX_NUM_OF_CUBE = 10*NUM_OF_STARTING_CUBE

print "MAX_NUM_OF_CUBE: ", MAX_NUM_OF_CUBE

print >> sys.stderr, "Box limits: ", xmin, xmax, ymin, ymax, zmin, zmax

# voglio fermarmi a circa 2 D dalla vetta visto che in cima avro' sempre una
# densita' minore(ricorda la prima sfera che supera zmax ferma la procedura.

visactors = False
actors = []

if (visactors):
  actors.extend(cube.cube_to_actors (xmin, ymin, zmin, \
      xmax, ymax, zmax))

cubcenterx = numpy.empty(0)
cubcentery = numpy.empty(0)
cubcenterz = numpy.empty(0)
cubradius = numpy.empty(0)

centers = []
cubes = []

globalindex = 0


print "First step... ", globalindex, " ", len(cubesets)

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

    cub.set_tagnumber (globalindex)

    if (not inside_any_cubes (cub, cubes, cubcenterx, 
      cubcentery, cubcenterz, cubradius)):

      cubes.append(cub)
      cubesets.append([globalindex])
      centers.append([x, y, z])
      # append to centers array e radius using numpy.append(array, values)
      cubcenterx = numpy.append(cubcenterx, x)
      cubcentery = numpy.append(cubcentery, y)
      cubcenterz = numpy.append(cubcenterz, z)
      cubradius = numpy.append(cubradius, cub.get_radius()) 

      j = j + 1
      globalindex = globalindex + 1

      if (visactors):
        actors.append(cub.get_vtk_actor(0.5, 0.6, 0.1))

print "Second step... ", globalindex, " ", len(cubesets)

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

    cub.set_tagnumber (globalindex)

    if (not inside_any_cubes (cub, cubes, cubcenterx, 
      cubcentery, cubcenterz, cubradius)):

      cubes.append(cub)
      cubesets.append([globalindex])
      centers.append([x, y, z])
      # append to centers array e radius using numpy.append(array, values)
      cubcenterx = numpy.append(cubcenterx, x)
      cubcentery = numpy.append(cubcentery, y)
      cubcenterz = numpy.append(cubcenterz, z)
      cubradius = numpy.append(cubradius, cub.get_radius()) 

      j = j + 1
      globalindex = globalindex + 1

      if (visactors):
        actors.append(cub.get_vtk_actor(0.5, 0.6, 0.1))

print "Third step... ", globalindex, " ", len(cubesets)

numofloop = 0
i = len(cubes)
while ((i < MAX_NUM_OF_CUBE) and (numofloop < 4 * MAX_NUM_OF_CUBE)) :

  print "  ", i , " of " , MAX_NUM_OF_CUBE
  print "    ", numofloop, " of " , 4 * MAX_NUM_OF_CUBE

  oldnumof = len(cubes)

  for cubi in range(oldnumof):
    #print "      ", cubi , " of ", oldnumof

    if (cubes[cubi].has_free_face ()):

      added = False 
      maxnumoftry = 0

      while (added == False): 

        maxnumoftry = maxnumoftry + 1

        #print "         ", maxnumoftry, " of 7"

        # se dopo 7 tentativi non risco a posizionare mi blocco
        if (maxnumoftry == 7):
          added = True

        numofloop = numofloop + 1

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
              # faccio il check tra quelli dello stesso seme cosi' in pratica
              # cosi' posso poi fare un check con sfere per gli altri semi.
              if (not (is_very_close (newcenter, cubcenterx, cubcentery, cubcenterz))):

                newcub = cube_fill.cube(newcenter[0], newcenter[1], newcenter[2], dim)
                newcub.set_iface (occupiediface)
                newcub.set_points (p1, p2, p3, p4, p5, p6, p7, p8)
                # devo settare il tag prima
                newcub.set_tagnumber(cubes[cubi].get_tagnumber())
                
                if (not inside_any_cubes (newcub, cubes, cubcenterx, \
                  cubcentery, cubcenterz, cubradius)):
                
                  cubesets[cubes[cubi].get_tagnumber()].append(i)
                  
                  i = i + 1
                  
                  cubes.append(newcub)
                  centers.append(newcenter)
                  cubcenterx = numpy.append(cubcenterx, newcenter[0])
                  cubcentery = numpy.append(cubcentery, newcenter[1])
                  cubcenterz = numpy.append(cubcenterz, newcenter[2])
                  cubradius = numpy.append(cubradius, cub.get_radius()) 
                  
                  added = True
                  
                  if (visactors):
                    actors.append(newcub.get_vtk_actor(0.5, 0.6, 0.1))

print "Total num of cubes: " , len(cubes)



silentremove("full.xyz")
cubes_utility.cubes_to_xyzfile(cubes, "full.xyz")

print "Num of seeds : ", len(cubesets)
for i in range(len(cubesets)):
  cubs_to_print = []
  for idx in cubesets[i]:
    cubs_to_print.append(cubes[idx])
  silentremove(str(i)+".xyz")
  cubes_utility.cubes_to_xyzfile(cubs_to_print, str(i)+".xyz")

if (visactors):
  visualize_nanop.visualize_actors (actors)
