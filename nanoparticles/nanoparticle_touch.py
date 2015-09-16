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

# init 

selected_index = 0

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

nanaparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanaparticles) 

print "Using ", len(nanaparticles) , " nanoparticles "

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

scx, scy, scz, radius = \
    nanoparticle.nanoparticle_list_to_arrays(nanaparticles)

print "Start counting " 

for selected_index in range(len(nanaparticles)):
  nanop = nanaparticles[selected_index]
  
  tot = 0
  for i in nanoparticle.get_near_nanoparticles_index_to (0, \
      scx, scy, scz, radius):
    if (i != selected_index):
      if (nanop.nanoparticle_touch_me(nanaparticles[i])):
        tot += 1

  print "Nanoparticle ", selected_index + 1 , " touches ", tot , \
      " particles "
