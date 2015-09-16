import sys

import random
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
import util

###############################################################################

def compute_superfract (nanop, nearnanop):

  points_surface = nanop.get_surface_points()

  insidepoint = 0
  for other_particle in nearnanop:
    for p in points_surface:
      if other_particle.is_point_inside([p.get_x(), \
          p.get_y(), p.get_z()]):
        insidepoint += 1
        
  superfract = (float(insidepoint)/(float(len(points_surface))))
                                                        
  return superfract

###############################################################################

def rotate_nanop (nanop, tetha, p2):

  pcx, pcy, pcz = nanop.get_center()
  A, B, H = nanop.get_dimensions()
  p1 = point.point(pcx, pcy, pcz)

  nanoparticle.POINTINSURFACESTEP = 1.0

  newnanop = nanoparticle.nanotio2(pcx, pcy, pcz, A, B, H)
  newnanop.rotate_nanoparticle(p1, p2, tetha)

  nanoparticle.POINTINSURFACESTEP = float('inf')

  return newnanop

###############################################################################

# init 

nanoparticle.POINTINSIDEDIM = 0
nanoparticle.POINTINSURFACESTEP = float('inf')

filename = "nanoparticle_randomly_place.out"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles) 

print "Read ", len(nanoparticles) , " nanoparticles "

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

new_nanoparticles_list = []
for selectedid in range(len(nanoparticles)):

  print "Doing ", selectedid+1, " of ", len(nanoparticles)

  nanop_selected = nanoparticles[selectedid]

  pcx, pcy, pcz = nanop_selected.get_center()
  A, B, H = nanop_selected.get_dimensions()
  dm = max(B, A, H)/2.0

  # devo generare per questa nanoparticella punti in superficie e dentro
  nanoparticle.POINTINSURFACESTEP = 1.0

  p1, p2, tetha = nanop_selected.get_rotation_info()

  nanop = nanoparticle.nanotio2(pcx, pcy, pcz, A, B, H)
  nanop.rotate_nanoparticle(p1, p2, tetha)

  nanoparticle.POINTINSURFACESTEP = float('inf')

  nearnanop, neardst = nanoparticle.get_near_nanoparticle (new_nanoparticles_list, \
      pcx, pcy, pcz, (2.0 * nanop.get_max_sphere()))

  print "Selected " , len(neardst), " nanoparticles "

  max_numt = 1000
  min_nanop = nanop
  superfract = compute_superfract (nanop, nearnanop)
  tetha = nanop.get_theta()
  p2 = nanop.get_p2()
  min_superfract = superfract
  i = 0
  while superfract > 0.01:
    p2x = random.uniform(botx, topx)
    p2y = random.uniform(boty, topy)
    p2z = random.uniform(botz, topz)
    p2 = point.point(float(p2x), float(p2y), float(p2z))
    tetha = random.uniform(0.0, 2.0*math.pi) 

    nanop = rotate_nanop (nanop, tetha, p2)
    superfract = compute_superfract (nanop, nearnanop)

    if (superfract < min_superfract):
      min_nanop = nanop
      min_superfract = superfract

    i = i + 1

    if (i > max_numt):
      break;

  if i > max_numt:
    print "Min superfract :", min_superfract

  new_nanoparticles_list.append(min_nanop)

  print >> sys.stderr, pcx, pcy, pcz, A, B, H, p2.get_x(), p2.get_y(), p2.get_z(), tetha
