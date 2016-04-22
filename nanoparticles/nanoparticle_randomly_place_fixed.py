import sys

import random
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
import util

# init 

nanoparticle.POINTINSIDEDIM = 0
nanoparticle.POINTINSURFACESTEP = float('inf')

filename = "final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

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

#if (botx >= topx) or (boty >= topy) or \
#   (boty >= topy):
#  print "Error Invalid BOX"
#  exit()

for i in range(len(scx)): 
  cx = scx[i] 
  cy = scy[i] 
  cz = scz[i]
  H = 28.99
  B = 23.56
  A = 14.44

  # ruota la nanoparticella random
  p1 = point.point(cx, cy, cz)

  p2x = random.uniform(botx, topx)
  p2y = random.uniform(boty, topy)
  p2z = random.uniform(botz, topz)

  tetha = random.uniform(0.0, 2.0*math.pi) 

  n = nanoparticle.nanotio2(cx, cy, cz, A, B, H)

  print >> sys.stderr, "Ratio: ", (H/2.0)/B
  print >> sys.stderr, "Sphere volume: ", spheres[i].get_volume(), \
      "Nanoparticle: ", n.get_volume(), " [", \
          math.fabs(spheres[i].get_volume() - n.get_volume()), "] "
  
  print cx, cy, cz, A, B, H, p2x, \
      p2y, p2z, tetha
