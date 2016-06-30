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

vdwradius = {'O':0.60, 'Ti':1.40}
sumofvdw = numpy.zeros((len(atoms),len(atoms)))
for i in range(0,len(atoms)):
  for j in range(0,len(atoms)):
    sumofvdw[i][j] = vdwradius[atoms[i]] + vdwradius[atoms[j]]

#print sumofvdw

xlistall = []
ylistall = []
zlistall = []
atomsall = []

lplacedcx = []
lplacedcy = []
lplacedcz = []

maxloopnumber = 10000
totnumofatom = 0

H = 28.99
B = 23.56
A = 14.44

for i in range(len(scx)): 
  
  cx = scx[i] 
  cy = scy[i] 
  cz = scz[i]
  r = radius[i]

  todo = True

  dx = numpy.square(lplacedcx - cx)
  dy = numpy.square(lplacedcy - cy)
  dz = numpy.square(lplacedcz - cz)
  
  dists = numpy.sqrt( dx + dy + dz)
  selectedidx = numpy.argwhere(dists <= 3*r)

  lplacedcx.append(cx)
  lplacedcy.append(cy)
  lplacedcz.append(cz)

  counter = 0
  mintetha = 0.0
  minp2 = point.point(0.0, 0.0, 0.0)
  mindval = 10000.0

  p1 = point.point(cx, cy, cz)

  while todo:
    counter = counter + 1

    # ruota la nanoparticella random
    p2x = random.uniform(botx, topx)
    p2y = random.uniform(boty, topy)
    p2z = random.uniform(botz, topz)
  
    p2 = point.point(p2x, p2y, p2z)
  
    tetha = random.uniform(0.0, 2.0*math.pi) 
  
    xlist, ylist, zlist = xyznanop.return_rototransl_xyz(p1, p2, tetha, \
            xlistin, ylistin, zlistin)
  
    mindist = 10000.0
    for j in selectedidx:
      n1 = numpy.column_stack((xlist, ylist, zlist))
      n2 = numpy.column_stack((xlistall[j], ylistall[j], zlistall[j]))
      dists = scipy.spatial.distance.cdist(n1, n2)
      dists = dists - sumofvdw

      md = numpy.min(dists)

      if (mindist > md):
        mindist = md
      
      #la distanza minima deve essere suoperiore alla somma dei raggi di van der wall 
      #se cosi' csarto e riprovo altrimenti todo e false ed aggiungo la nanoparticella 

    print >> sys.stderr, "  idx: ", i, " ", counter ," of ", maxloopnumber, " ", mindist
    sys.stderr.flush()

    if (mindval > mindist):
      mindval = mindist
      mintetha = tetha
      minp2 = p2
   
    # se mindist > 6 nemmeno ci provo a riposizionare
    if ((mindist > 0.0) and (mindist < 2.0)) or (mindist > 6.0):
      todo = False
      xlistall.append(xlist)
      ylistall.append(ylist)
      zlistall.append(zlist)
      atomsall.append(atoms)

      totnumofatom = totnumofatom + len(xlist)

      print >> sys.stderr, i ," of ", len(scx), " " , mindist 
      sys.stderr.flush()

      print cx, cy, cz, A, B, H, p2.get_x(), p2.get_y(), p2.get_z(), tetha

    if counter >= maxloopnumber:
      xlist, ylist, zlist = xyznanop.return_rototransl_xyz(p1, minp2, tetha, \
            xlistin, ylistin, zlistin)

      todo = False
      xlistall.append(xlist)
      ylistall.append(ylist)
      zlistall.append(zlist)
      atomsall.append(atoms)

      totnumofatom = totnumofatom + len(xlist)

      print cx, cy, cz, A, B, H, minp2.get_x(), minp2.get_y(), \
              minp2.get_z(), tetha

      print >> sys.stderr, i ," of ", len(scx), " " , mindval
      sys.stderr.flush()

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
