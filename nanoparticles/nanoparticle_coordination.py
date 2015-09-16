import sys
import vtk
import numpy

import random
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
import util
import cube

import common

###############################################################################

def get_near_nanoparticle (nanopscx, nanopscy, nanopscz, px, py, pz, distance):

  distx = (nanopscx - px)
  disty = (nanopscy - py)
  distz = (nanopscz - pz)

  distx2 = distx * distx
  disty2 = disty * disty
  distz2 = distz * distz

  dist = distx2 + disty2 + distz2

  d = numpy.sqrt(dist)

  bools1 = d <= distance

  indices, = numpy.where(bools1)

  return indices

###############################################################################

nanoparticle.POINTINSIDEDIM = 0
nanoparticle.POINTINSURFACESTEP = float('inf')

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

nanoparticles_init = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles_init) 

print "Read ", len(nanoparticles_init) , " nanoparticles "

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

nanopscx, nanopscy, nanopscz, nanopradius = \
    nanoparticle.nanoparticle_list_to_arrays(nanoparticles_init)

nanoparticles = []
for selectedid in range(len(nanoparticles_init)):
  nanop = nanoparticles_init[selectedid]
  pcx, pcy, pcz = nanop.get_center()

  A, B, H = nanop.get_dimensions()
  dm = max(B, A, H)/2.0

  # seleziona solo particelle interne
  distx = min(math.fabs(pcx-botx), math.fabs(pcx-topx))
  disty = min(math.fabs(pcy-boty), math.fabs(pcy-topy))
  distz = min(math.fabs(pcz-botz), math.fabs(pcz-topz))

  #print min(distx, disty, distz), 2.0 * dm

  if (min(distx, disty, distz) > (2.0 * dm)):
    nanoparticles.append(nanop)

print "Using ", len(nanoparticles) , " nanoparticles "

print "Start counting " 

totrapavg = 0.0 
totrap = 0.0
count = 0.0

listofsovrapperc = []

for selectedid in range(len(nanoparticles)):
  nanop_selected = nanoparticles[selectedid]

  pcx, pcy, pcz = nanop_selected.get_center()
  A, B, H = nanop_selected.get_dimensions()
  dm = max(B, A, H)/2.0

  # devo generare per questa nanoparticella punti in superficie e dentro
  nanoparticle.POINTINSIDEDIM = 30
  nanoparticle.POINTINSURFACESTEP = 0.25

  p1, p2, tetha = nanop_selected.get_rotation_info()

  nanop = nanoparticle.nanotio2(pcx, pcy, pcz, A, B, H)
  nanop.rotate_nanoparticle(p1, p2, tetha)

  nanoparticle.POINTINSIDEDIM = 0
  nanoparticle.POINTINSURFACESTEP = float('inf')

  maxbox_x = pcx + dm
  minbox_x = pcx - dm
  maxbox_y = pcy + dm
  minbox_y = pcy - dm
  maxbox_z = pcz + dm
  minbox_z = pcz - dm

  nearnanop, neardst = nanoparticle.get_near_nanoparticle (nanoparticles, \
      pcx, pcy, pcz, (2.0 * nanop.get_max_sphere()))

  selected_index = -1
  for i in range(len(neardst)):
    if neardst[i] == 0.0:
      selected_index = i

  #print selected_index 
  print "Selected ", len(nearnanop) , " nanoparticles "

  surface_insidepoint = 0
  surface_touchinanop = []
  surface_type = {}

  # calcolo superficie di interesezione
  sf001add = False
  sf101add = False
  points_surface = nanop.get_surface_points()
  for p in points_surface:
    for a in range(len(nearnanop)):
      if (a != selected_index):
        other_particle = nearnanop[a]
        if other_particle.is_point_inside([p.get_x(), 
          p.get_y(), p.get_z()]):
    
          surface_insidepoint += 1
          surface_touchinanop.append(a)

          label = p.get_label()

          if label == "001":
            sf001add = True
          elif label == "101":
            sf101add = True

          if label in surface_type:
            surface_type[label] += 1
          else:
            surface_type[label] = 1
 
  SurfaceTOT, SurfaceP1, SurfaceP2, SurfaceP3, \
      SurfaceP4, SurfaceP5, SurfaceP6, SurfaceP7, \
      SurfaceP8, SurfaceP9, SurfaceP10 = nanop.get_surface()

  for l, v in surface_type.iteritems():
    SFrt = float(v)/float(len(points_surface))
    print "Surface: ", l, " fract: ", SFrt
    print "Surface: ", l, " surface: ", SFrt*SurfaceTOT

  if not sf001add:
    print "Surface: "+ " 001 " + " fract: ", 0.0
    print "Surface: "+ " 001 " + " surface: ", 0.0

  if not sf101add:
    print "Surface: "+ " 101 " + " fract: ", 0.0
    print "Surface: "+ " 101 " + " surface: ", 0.0

  print "Surface inside point: ", surface_insidepoint, " of ", len(points_surface)
  SFrt = float(surface_insidepoint)/float(len(points_surface))
  print "Surface inter fract: ", SFrt
  print "Surface inter surface: ", SFrt*SurfaceTOT
  print "Nanoparticle surfaces TOT: ", SurfaceTOT
  print "                      P1 : ", SurfaceP1
  print "                      P2 : ", SurfaceP2
  print "                      P3 : ", SurfaceP3
  print "                      P4 : ", SurfaceP4
  print "                      P5 : ", SurfaceP5
  print "                      P6 : ", SurfaceP6
  print "                      P7 : ", SurfaceP7
  print "                      P8 : ", SurfaceP8
  print "                      P9 : ", SurfaceP9
  print "                      P10: ", SurfaceP10

  touchinanop = []
  pointpernanoparticle = {} # dictionary to collect all point inside 
                            # a specific nanaparticle

  insidepoint = 0

  box_V = 0.0
  points_inside = []
  totpoint = 0

  # se uso ogni volta punti nel paralleloepipedo 
  # uso punti direttamente dentro il nanocristallo
  points_inside = nanop.inside_point_grid()
  for p in points_inside:
    for a in range(len(nearnanop)):
      if (a != selected_index):
        other_particle = nearnanop[a]
        if other_particle.is_point_inside([p.get_x(), 
          p.get_y(), p.get_z()]):
  
          insidepoint += 1
          touchinanop.append(a)
  
          if a in pointpernanoparticle:
            pointpernanoparticle[a] += 1
          else:
            pointpernanoparticle[a] = 1
  
  print selectedid+1 , " of ", len(nanoparticles)
  print "Insidepoint: ", insidepoint, " of ", len(points_inside)
  print "Number of touching nanoparticles: ", len(set(touchinanop))
  print "Volume fract: ", float(insidepoint)/float(len(points_inside))
  V = nanop.get_volume() * (float(insidepoint)/float(len(points_inside)))
  print "Volume sovrapposto: ", V
  print "Volume nanoparticle: ", nanop.get_volume()

  if (len(set(touchinanop)) > 0):
    rap = V/nanop.get_volume()
    print "Rapporto: ", rap
    avgrap = rap/float(len(set(touchinanop)))
    print "Rapporto medio: ", (V/nanop.get_volume())/float(len(set(touchinanop)))
    totrap = totrap + rap
    totrapavg = totrapavg + avgrap

  for a, v in pointpernanoparticle.iteritems():
    sovrvol = nanop.get_volume() * (float(v)/float(len(points_inside)))

    print "With particle ", a, " ", sovrvol/nanop.get_volume()
    listofsovrapperc.append(sovrvol/nanop.get_volume())

  # nel computo aggiungo anche i punti di superficie
  totpointinside = (float(insidepoint)+float(surface_insidepoint))
  totamountpoint = float(len(points_inside))+float(len(points_surface))
  print "Volume fract with surface: ", totpointinside/totamountpoint
  V = nanop.get_volume() * totpointinside/totamountpoint
  print "Volume sovrapposto with surface: ", V

  print ""

  count = count + 1.0

  del nanop

print "Media rapporto: ", totrap/count
print "Media rapporto a coppia: ", totrapavg/count

print "Media rapporto di coppia calcolato : ", numpy.average(listofsovrapperc)
print "Deviazione standard: ", numpy.std(listofsovrapperc)

hist, bin_ed = numpy.histogram(listofsovrapperc, bins=100)

for i in range(len(hist)):
  print (bin_ed[i]+bin_ed[i+1])/2.0 , " ", hist[i]
