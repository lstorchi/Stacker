import re
import sys 
import math
import scipy 
import numpy

from scipy.spatial import distance
from scipy import cluster

sys.path.append("../modules")

import nanoparticle
import xyznanop
import common
import sphere
import point
import util
import line

filename = ""
nanoparticle.POINTINSIDEDIM = 0

if (len(sys.argv)) == 2:
  filename = sys.argv[1]
else:
  print "usage :", sys.argv[0] , " xyzfile"
  exit(1)

xlist, ylist, zlist, atoms = xyznanop.read_ncxyz (filename)

atoms1 = []
xlist1 = []
ylist1 = []
zlist1 = []

atoms2 = []
xlist2 = []
ylist2 = []
zlist2 = []

half = len(atoms)/2
for i in range(len(atoms)):
  if (i<half):
    xlist1.append(xlist[i])
    ylist1.append(ylist[i])
    zlist1.append(zlist[i])
    atoms1.append(atoms[i])
  else:
    xlist2.append(xlist[i])
    ylist2.append(ylist[i])
    zlist2.append(zlist[i])
    atoms2.append(atoms[i])

vdwradius = {'O':0.60, 'Ti':1.40}
sumofvdw = numpy.zeros((len(atoms1),len(atoms1)))
for i in range(0,len(atoms1)):
  for j in range(0,len(atoms1)):
    sumofvdw[i][j] = vdwradius[atoms1[i]] + vdwradius[atoms1[j]]

n1 = numpy.column_stack((xlist1, ylist1, zlist1))
n2 = numpy.column_stack((xlist2, ylist2, zlist2))
 
dists = scipy.spatial.distance.cdist(n1, n2)
md = numpy.min(dists)

print "Min. Dist: ", md

dists = dists - sumofvdw
md = numpy.min(dists)

print "Min. Dist: ", md
