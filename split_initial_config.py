import re
import sys
import time

sys.path.append("./modules")

import util
import point
import sphere
import nanoparticle

import math
import numpy
import random

###############################################################################

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

NUMOFBOX = 64

#box_xdim = 135.0
#box_ydim = 135.0
#box_zdim = 135.0

box_xdim = 205.0
box_ydim = 205.0
box_zdim = 205.0

filenamenanop = "final_config_nanoparticle.txt"

if (len(sys.argv)) == 2:
  filenamenanop = sys.argv[1]

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filenamenanop, nanoparticles) 

nanopscx, nanopscy, nanopscz = \
    nanoparticle.nanoparticle_to_arrays (nanoparticles)

r = 0.0
for nanop in nanoparticles:
  r += nanop.get_max_sphere()

mead_d = 2.0 * (r/float(len(nanoparticles)))

print mead_d

if (box_xdim < (5.0 * mead_d)):
  print "Maybe the box is to small"
  exit(1)

if (box_ydim < (5.0 * mead_d)):
  print "Maybe the box is to small"
  exit(1)

if (box_zdim < (5.0 * mead_d)):
  print "Maybe the box is to small"
  exit(1)

for i in range(NUMOFBOX):
  px = random.uniform(botx+mead_d, topx - box_xdim)
  py = random.uniform(boty+mead_d, topy - box_ydim)
  pz = random.uniform(botz+mead_d, topz - box_zdim)
  
  # seleziono solo le nanoparticelle con il centro detro la box visto che poi 
  # dal calcolo della psd escludo comunque i punti ai bordi della box

  box_botx = px
  box_topx = px + box_xdim
  box_boty = py
  box_topy = py + box_ydim
  box_botz = pz
  box_topz = pz + box_zdim

  bools1 = (nanopscx >= box_botx)
  bools2 = (nanopscy >= box_boty)
  bools3 = (nanopscz >= box_botz)

  bools4 = (nanopscx <= box_topx)
  bools5 = (nanopscy <= box_topy)
  bools6 = (nanopscz <= box_topz)

  interior_indices, = numpy.where(bools1*bools2*bools3*bools4*bools5*bools6)

  filetoprint = open(filenamenanop + "_" + str(i), "w")
  for id in interior_indices:
    cx, cy, cz, A, B, H, p2x, p2y, p2z, tetha = \
        nanoparticles[id].get_to_print()

    data = str(cx) + " " + \
           str(cy) + " " + \
           str(cz) + " " + \
           str(A) + " " + \
           str(B) + " " + \
           str(H) + " " + \
           str(p2x) + " " + \
           str(p2y) + " " + \
           str(p2z) + " " + \
           str(tetha) + "\n"

    filetoprint.write(data)

  filetoprint.close()
