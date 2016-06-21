import sys

import random
import math

sys.path.append("../modules")

import nanoparticle
import xyznanop
import sphere
import point
import util

# init 

nanoparticle.POINTINSIDEDIM = 0
nanoparticle.POINTINSURFACESTEP = float('inf')

filename = "final_config.txt"
xyznc = "NC.xyz"

if (len(sys.argv)) == 3:
  filename = sys.argv[1]
  xyznc = sys.argv[2]

spheres = []
zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0
R = -1.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    util.file_to_sphere_diffr_list(filename, spheres) 

scx, scy, scz, radius = util.sphere_to_arrays (spheres)

botx = min(scx)
boty = min(scy)
botz = min(scz)
topx = max(scx)
topy = max(scy)
topz = max(scz)

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

for i in range(len(scx)): 
  cx = scx[i] 
  cy = scy[i] 
  cz = scz[i]

  # ruota la nanoparticella random
  p1 = point.point(cx, cy, cz)

  p2x = random.uniform(botx, topx)
  p2y = random.uniform(boty, topy)
  p2z = random.uniform(botz, topz)

  tetha = random.uniform(0.0, 2.0*math.pi) 


