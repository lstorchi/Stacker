import sys
import vtk
import re

import random
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
import util
import cube

# init 

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

filename = "nanoparticle_final_config.txt"
xyzfile = "test.xyz"

if (len(sys.argv)) == 3:
    filename = sys.argv[1]
    xyzfile = sys.argv[2]
else:
    print "usage: ", sys.argv[0], " nanofname.txt xyzfname.xyz"
    exit(1)

nanaparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanaparticles) 

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

minbox_x = 100000.0 
maxbox_x =-100000.0 
minbox_y = 100000.0
maxbox_y =-100000.0
minbox_z = 100000.0
maxbox_z =-100000.0

for nanop in nanaparticles: 
  x = nanop.get_edge_points()
