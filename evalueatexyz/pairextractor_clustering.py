import sys 
import re
import numpy
import math

sys.path.append("../modules")

import nanoparticle
import xyznanop
import common
import sphere
import point
import util
import line

filename = ""
nanopfile = ""
nanoparticle.POINTINSIDEDIM = 0

if (len(sys.argv)) == 3:
  filename = sys.argv[1]
  nanopfile = sys.argv[2]
else:
  print "usage :", sys.argv[0] , " xyzfile nanopfile.txt"
  exit(1)

xlist, ylist, zlist, atoms = xyznanop.read_ncxyz (filename)

xc = numpy.mean(xlist)
yc = numpy.mean(ylist)
zc = numpy.mean(zlist)

xlist = xlist - xc
ylist = ylist - yc
zlist = zlist - zc

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
        nanoparticle.file_to_nanoparticle_list(nanopfile, nanoparticles)

print >> sys.stderr, "Read done"

radius = {'O':0.60, 'Ti':1.40}

pairs = []
for id1 in range(len(nanoparticles)):
  nanop1 = nanoparticles[id1]
  p1cx, p1cy, p1cz = nanop1.get_center()
  sumr = 2.25 * nanop1.get_max_sphere()

  indices, d = nanoparticle.get_near_nanoparticle_indexs(nanoparticles, \
          p1cx, p1cy, p1cz, sumr)

  for i in range(len(indices)):
    id2 = indices[i]
 
    pair = str(id1) + "_" + str(id2)
    if (id1 != id2) and (pair not in pairs):
      pairs.append(str(id1) + "_" + str(id2))
      pairs.append(str(id2) + "_" + str(id1))
    
      nanop2 = nanoparticles[id2]
    

print "Num. of Pairs: ", len(pairs)
