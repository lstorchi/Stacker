import sys

import random
import math

sys.path.append("./modules")

import nanoparticle
import sphere
import point
import util

###############################################################################

def compute_superfract_ratio (nanop, nearnanop):

  area, areaUP_top, areaUP_right, areaUP_left, areaUP_back, areaUP_front, \
      areaDOWN_bottom, areaDOWN_right, areaDOWN_left, areaDOWN_back, \
      areaDOWN_front = nanop.get_surface()
  
  trueratio = (8.0*areaUP_right)/(2.0*areaUP_top)

  surface_insidepoint = 0
  surface_type = {}

  # calcolo superficie di interesezione
  points_surface = nanop.get_surface_points()
  for p in points_surface:
    for a in range(len(nearnanop)):
      if (a != selected_index):
        other_particle = nearnanop[a]
        if other_particle.is_point_inside([p.get_x(), 
          p.get_y(), p.get_z()]):
    
          label = p.get_label()

          if label in surface_type:
            surface_type[label] += 1
          else:
            surface_type[label] = 1

  for l, v in surface_type.iteritems():
    print l, v
  

  comptration = 0.0
  if ("001" in surface_type) and ("101" in  surface_type):
    comptration = surface_type["001"] / surface_type["101"]
 
  print comptration, trueratio, math.fabs(comptration-trueratio)

  return math.fabs(comptration-trueratio)

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
  superfract_ratio = compute_superfract_ratio (nanop, nearnanop)
  tetha = nanop.get_theta()
  p2 = nanop.get_p2()
  min_superfract_ratio = superfract_ratio
  i = 0
  while superfract_ratio > 1.0:
    p2x = random.uniform(botx, topx)
    p2y = random.uniform(boty, topy)
    p2z = random.uniform(botz, topz)
    p2 = point.point(float(p2x), float(p2y), float(p2z))
    tetha = random.uniform(0.0, 2.0*math.pi) 

    nanop = rotate_nanop (nanop, tetha, p2)
    superfract_ratio = compute_superfract_ratio (nanop, nearnanop)

    if (superfract_ratio < min_superfract_ratio):
      min_nanop = nanop

    i = i + 1

    if (i > max_numt):
      break;

  if i > max_numt:
    print "Min superfract_raio difference :", superfract_ratio

  new_nanoparticles_list.append(min_nanop)

  print >> sys.stderr, pcx, pcy, pcz, A, B, H, p2.get_x(), p2.get_y(), p2.get_z(), tetha
