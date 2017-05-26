import re
import sys 
import math
import scipy 
import numpy

from scipy.spatial import distance

sys.path.append("../modules")

import nanoparticle
import xyznanop
import common
import sphere
import point
import util
import line

###############################################################################

filename = ""

if (len(sys.argv)) == 2:
  filename = sys.argv[1]
else:
  print "usage :", sys.argv[0] , " xyzfile"
  exit(1)

xlist, ylist, zlist, atoms = xyznanop.read_ncxyz (filename, False)

xlist1 = xlist[:len(xlist)/2]
ylist1 = ylist[:len(ylist)/2]
zlist1 = zlist[:len(zlist)/2]
atoms1 = atoms[:len(atoms)/2]

xlist2 = xlist[len(xlist)/2:]
ylist2 = ylist[len(ylist)/2:]
zlist2 = zlist[len(zlist)/2:]
atoms2 = atoms[len(atoms)/2:]

coords1 = numpy.transpose(numpy.array((xlist1, ylist1, zlist1), dtype=float))
coords2 = numpy.transpose(numpy.array((xlist2, ylist2, zlist2), dtype=float))

dists = distance.cdist(coords1, coords2)
 
val = numpy.where(dists <= 4.0)

xout = []
yout = []
zout = []
aout = []

for i in val[0]:
    xout.append(xlist1[i])
    yout.append(ylist1[i])
    zout.append(zlist1[i])
    aout.append(atoms1[i])
    
for j in val[1]:
    xout.append(xlist2[j])
    yout.append(ylist2[j])
    zout.append(zlist2[j])
    aout.append(atoms2[j])
 
xyznanop.write_ncxyz ("out.xyz", xout, yout, zout, aout)
