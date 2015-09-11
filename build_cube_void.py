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

NUM_OF_STARTING_CUBE = 50
MAX_NUM_OF_CUBE = 200*NUM_OF_STARTING_CUBE

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

cubcenterx = numpy.empty(0)
cubcentery = numpy.empty(0)
cubcenterz = numpy.empty(0)
cubradius = numpy.empty(0)

centers = []
cubes = []

j = 0
while (j < (NUM_OF_STARTING_CUBE/2)):
  #x = random.uniform(xmin + 1.5*meand, xmax - 1.5*meand)
  #y = random.uniform(ymin + 1.5*meand, ymax - 1.5*meand)
  #z = random.uniform(zmin + 1.5*meand, zmax - 1.5*meand)

  x = random.uniform(xmin + 1.5*meand, xmin + 2.6*meand)
  y = random.uniform(ymin + 1.5*meand, ymin + 2.6*meand)
  z = random.uniform(zmin + 1.5*meand, zmin + 2.6*meand)

  #print x, y, z

  bools1 = numpy.sqrt((scx - x)**2 + (scy - y)**2 + (scz - z)**2) <= 2.0*radius
  interior_indices, = numpy.where(bools1)

  is_inside = False

  for idx in interior_indices:
    if (nanoparticles[idx].is_point_inside([x, y, z])):
      is_inside = True
      break

  if not is_inside:

    if (not ([x, y, z] in centers)): # se non lo faccio i punti su angolo non vengono 
                                     # visti come interni

      #for idx in interior_indices:
      #  actors.append(nanoparticles[idx].get_vtk_actor(color=True,opacity=1.0))

      cub = cube_fill.cube(x, y, z, CUBE_DIM)
      tetha = random.uniform(0.0, 2.0*math.pi)
      px = random.uniform(xmin + 1.5*meand, xmax - 1.5*meand)
      py = random.uniform(ymin + 1.5*meand, ymax - 1.5*meand)
      pz = random.uniform(zmin + 1.5*meand, zmax - 1.5*meand)

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

        #actors.append(cub.get_vtk_actor(0.5, 0.6, 0.1))

j = 0
while (j < (NUM_OF_STARTING_CUBE/2)):
  # questi vanno piazzati sulle superfici delle nanoparticelle

  x = random.uniform(xmin + 1.5*meand, xmin + 2.6*meand)
  y = random.uniform(ymin + 1.5*meand, ymin + 2.6*meand)
  z = random.uniform(zmin + 1.5*meand, zmin + 2.6*meand)

  bools1 = numpy.sqrt((scx - x)**2 + (scy - y)**2 + (scz - z)**2) <= 2.0*radius
  interior_indices, = numpy.where(bools1)

  is_inside = False

  for idx in interior_indices:
    if (nanoparticles[idx].is_point_inside([x, y, z])):
      is_inside = True
      break

  if not is_inside:

    if (not ([x, y, z] in centers)): # se non lo faccio i punti su angolo non vengono 
                                     # visti come interni

      # detrmina la nanoparticelle piu' vicina
      minval = min(numpy.sqrt((scx - x)**2 + (scy - y)**2 + (scz - z)**2))
      bools1 = numpy.sqrt((scx - x)**2 + (scy - y)**2 + (scz - z)**2) <= minval
      nearest_nanop, = numpy.where(bools1)

      if (len(nearest_nanop) == 1):
    
        p1, peqn = nanoparticles[nearest_nanop[0]].project_point_101(point.point(x, y, z))

        #actors.append(nanoparticles[nearest_nanop[0]].get_vtk_actor(color=True,opacity=1.0))
        #actors.append(p1.get_actor(0.1, 1.0, 0.0, 0.0))

        # genera il secondo punto uso i due vettori con cui posso definire il piano
        # http://stackoverflow.com/questions/18663755/how-to-convert-a-3d-point-on-a-plane-to-uv-coordinates
        a, b, c, d = peqn.get_plane_data()

        u1 = b
        u2 = -a
        u3 = 0.0

        if (a == 0.0 and b == 0.0):
          u1 = 0.0
          u2 = 0.0
          u3 = c

        norm = math.sqrt(u1*u1 + u2*u2 + u3*u3)

        if (norm != 0.0): # perche' succede devo definire meglio u

          u1 = u1 / norm
          u2 = u2 / norm
          u3 = u3 / norm
          p2x = p1.get_x() + CUBE_DIM * u1
          p2y = p1.get_y() + CUBE_DIM * u2
          p2z = p1.get_z() + CUBE_DIM * u3
                                         
          p2 = point.point(p2x, p2y, p2z)
         
          #actors.append(p2_pro.get_actor(0.2, 0.0, 1.0, 0.0))
          #actors.append(p2.get_actor(0.1, 0.0, 1.0, 0.0))
         
          #print "p1 to p2: ", p1.get_distance_from(p2)
          #print "p2 is in the plane: ", peqn.is_point_in(p2)
         
          # genera terzo punto
          # http://stackoverflow.com/questions/18663755/how-to-convert-a-3d-point-on-a-plane-to-uv-coordinates
          n1 = a
          n2 = b
          n3 = c
          norm = math.sqrt(n1*n1 + n2*n2 + n3*n3)
          n1 = n1 / norm
          n2 = n2 / norm
          n3 = n3 / norm
          v1 = n2*u3 - n3*u2
          v2 = n3*u1 - n1*u3
          v3 = n1*u2 - n2*u1
         
          p3x = p1.get_x() + CUBE_DIM * v1
          p3y = p1.get_y() + CUBE_DIM * v2
          p3z = p1.get_z() + CUBE_DIM * v3
                                         
          p3 = point.point(p3x, p3y, p3z)
         
          #actors.append(p3.get_actor(0.1, 0.0, 0.0, 1.0))
         
          #print "p1 to p3: ", p3.get_distance_from(p1)
          #print "p3 is in the plane: ", peqn.is_point_in(p3)
         
          # determina il quanto punto
          p4x = p3.get_x() + CUBE_DIM * u1
          p4y = p3.get_y() + CUBE_DIM * u2
          p4z = p3.get_z() + CUBE_DIM * u3
         
          p4 = point.point(p4x, p4y, p4z)
         
          #actors.append(p4.get_actor(0.1, 0.0, 0.0, 1.0))
         
          #print "p4 to p3: ", p3.get_distance_from(p4)
          #print "p4 is in the plane: ", peqn.is_point_in(p4)
         
         
          # linea perpendicolare al piane che passa per p1
          a, b, c, d = peqn.get_plane_data()
         
          norm = math.sqrt(a*a + b*b + c*c) 
         
          p5x = p1.get_x() + (a * (CUBE_DIM/norm))
          p5y = p1.get_y() + (b * (CUBE_DIM/norm))
          p5z = p1.get_z() + (c * (CUBE_DIM/norm))
         
          if (nanoparticles[nearest_nanop[0]].is_point_inside([p5x, p5y, p5z])):
            p5x = p1.get_x() - (a * (CUBE_DIM/norm))
            p5y = p1.get_y() - (b * (CUBE_DIM/norm))
            p5z = p1.get_z() - (c * (CUBE_DIM/norm))
         
          p5 = point.point(p5x, p5y, p5z)
         
          #actors.append(p5.get_actor(0.1, 0.0, 0.0, 1.0))
         
          #print "p1 to p5: ", p1.get_distance_from(p5)
         
          # linea perpendicolare al piane che passa per p2
          a, b, c, d = peqn.get_plane_data()
         
          norm = math.sqrt(a*a + b*b + c*c) 
         
          p6x = p2.get_x() + (a * (CUBE_DIM/norm))
          p6y = p2.get_y() + (b * (CUBE_DIM/norm))
          p6z = p2.get_z() + (c * (CUBE_DIM/norm))
         
          if (nanoparticles[nearest_nanop[0]].is_point_inside([p6x, p6y, p6z])):
            p6x = p2.get_x() - (a * (CUBE_DIM/norm))
            p6y = p2.get_y() - (b * (CUBE_DIM/norm))
            p6z = p2.get_z() - (c * (CUBE_DIM/norm))
         
          p6 = point.point(p6x, p6y, p6z)
         
          #actors.append(p6.get_actor(0.1, 0.0, 0.0, 1.0))
         
          #print "p2 to p6: ", p2.get_distance_from(p6)
         
          # linea perpendicolare al piane che passa per p3
          a, b, c, d = peqn.get_plane_data()
         
          norm = math.sqrt(a*a + b*b + c*c) 
         
          p7x = p3.get_x() + (a * (CUBE_DIM/norm))
          p7y = p3.get_y() + (b * (CUBE_DIM/norm))
          p7z = p3.get_z() + (c * (CUBE_DIM/norm))
         
          if (nanoparticles[nearest_nanop[0]].is_point_inside([p7x, p7y, p7z])):
            p7x = p3.get_x() - (a * (CUBE_DIM/norm))
            p7y = p3.get_y() - (b * (CUBE_DIM/norm))
            p7z = p3.get_z() - (c * (CUBE_DIM/norm))
         
          p7 = point.point(p7x, p7y, p7z)
         
          #actors.append(p7.get_actor(0.1, 0.0, 0.0, 1.0))
         
          #print "p3 to p7: ", p3.get_distance_from(p7)
         
          # linea perpendicolare al piane che passa per p4
          a, b, c, d = peqn.get_plane_data()
         
          norm = math.sqrt(a*a + b*b + c*c) 
         
          p8x = p4.get_x() + (a * (CUBE_DIM/norm))
          p8y = p4.get_y() + (b * (CUBE_DIM/norm))
          p8z = p4.get_z() + (c * (CUBE_DIM/norm))
         
          if (nanoparticles[nearest_nanop[0]].is_point_inside([p8x, p8y, p8z])):
            p8x = p4.get_x() - (a * (CUBE_DIM/norm))
            p8y = p4.get_y() - (b * (CUBE_DIM/norm))
            p8z = p4.get_z() - (c * (CUBE_DIM/norm))
         
          p8 = point.point(p8x, p8y, p8z)
         
          #actors.append(p8.get_actor(0.1, 0.0, 0.0, 1.0))
         
          #print "p4 to p8: ", p4.get_distance_from(p8)
         
          cub = cube_fill.cube(0.0, 0.0, 0.0, CUBE_DIM)
          if (cub.set_points ([p1.get_x(), p1.get_y(), p1.get_z()],
               [p2.get_x(), p2.get_y(), p2.get_z()],
               [p4.get_x(), p4.get_y(), p4.get_z()],
               [p3.get_x(), p3.get_y(), p3.get_z()],
               [p5.get_x(), p5.get_y(), p5.get_z()],
               [p6.get_x(), p6.get_y(), p6.get_z()],
               [p8.get_x(), p8.get_y(), p8.get_z()],
               [p7.get_x(), p7.get_y(), p7.get_z()])):

            x, y, z = cub.get_center()
   
            if (not inside_any_cubes (cub, cubes, cubcenterx, 
              cubcentery, cubcenterz, cubradius)):
              cubes.append(cub)
              centers.append([x, y, z])
              # append to centers array e radius using numpy.append(array, values)
              cubcenterx = numpy.append(cubcenterx, x)
              cubcentery = numpy.append(cubcentery, y)
              cubcenterz = numpy.append(cubcenterz, z)
              cubradius = numpy.append(cubradius, cub.get_radius()) 
            
              #actors.append(cub.get_vtk_actor(0.5, 0.6, 0.1))
            
              j = j + 1

i = len(cubes)
while (i < MAX_NUM_OF_CUBE):

  # seleziona le nanoparticelle 
  # usando le sfere per fare la selezione e' possibile io ottenga
  # dei falsi positivi

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

      # dovrebbe essere un modo semplice per vedere se il cubo si sovrappone
      if (not (newcenter in centers)):
      
        newcub = cube_fill.cube(newcenter[0], newcenter[1], newcenter[2], dim)
        newcub.set_iface (occupiediface)
        newcub.set_points (p1, p2, p3, p4, p5, p6, p7, p8)

        if (not cube_is_inside_nanoparticles(newcub, nanoparticles, \
          scx, scy, scz, radius)):
          if (not inside_any_cubes (newcub, cubes, cubcenterx, \
            cubcentery, cubcenterz, cubradius)):
            cubes.append(newcub)
            centers.append(newcenter)
            cubcenterx = numpy.append(cubcenterx, x)
            cubcentery = numpy.append(cubcentery, y)
            cubcenterz = numpy.append(cubcenterz, z)
            cubradius = numpy.append(cubradius, cub.get_radius()) 
            #actors.append(newcub.get_vtk_actor(0.5, 0.6, 0.1))
            i = i + 1

#visualize_nanop.visualize_actors (actors)

for cub in cubes:
  print cub.alldata_tostr()
