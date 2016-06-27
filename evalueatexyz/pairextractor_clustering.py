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
 
for selectedid in range(len(nanoparticles)):
  nanop = nanoparticles[selectedid]
  pcx, pcy, pcz = nanop.get_center()

  nearnanop, neardst = nanoparticle.get_near_nanoparticle (nanoparticles, \
      pcx, pcy, pcz, (2.0 * nanop.get_max_sphere()))
