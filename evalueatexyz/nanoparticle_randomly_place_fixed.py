import sys

import random
import scipy
import numpy
import math

from scipy.spatial import distance

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

xlistin, ylistin, zlistin, atoms = xyznanop.read_ncxyz(xyznc)

xlistall = []
ylistall = []
zlistall = []
atomsall = []
totnumofatom = 0

lplacedcx = []
lplacedcy = []
lplacedcz = []

for i in range(len(scx)): 
  cx = scx[i] 
  cy = scy[i] 
  cz = scz[i]

  # ruota la nanoparticella random
  p1 = point.point(cx, cy, cz)

  p2x = random.uniform(botx, topx)
  p2y = random.uniform(boty, topy)
  p2z = random.uniform(botz, topz)

  p2 = point.point(p2x, p2y, p2z)

  tetha = random.uniform(0.0, 2.0*math.pi) 

  xlist, ylist, zlist = xyznanop.return_rototransl_xyz(p1, p2, tetha, \
          xlistin, ylistin, zlistin)

  totnumofatom = totnumofatom + len(xlist)

  xlistall.append(xlist)
  ylistall.append(ylist)
  zlistall.append(zlist)
  atomsall.append(atoms)

  lplacedcx.append(cx)
  lplacedcy.append(cy)
  lplacedcz.append(cz)

  dx = numpy.square(lplacedcx - cx)
  dy = numpy.square(lplacedcy - cy)
  dz = numpy.square(lplacedcz - cz)

  #print numpy.sqrt( dx + dy + dz)
  #print " "

filename = "test.xyz"
target = open(filename, 'w')
target.write(str(totnumofatom)+"\n")
target.write("\n")

for i in range(len(xlistall)):
  for j in range(len(xlistall[i])):
    target.write(str(atomsall[i][j]) + " " + \
              str(xlistall[i][j]) + " " + \
              str(ylistall[i][j]) + " " + \
              str(zlistall[i][j]))
    target.write("\n")

target.close()
