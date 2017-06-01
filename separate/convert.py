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

DELTA = 0.529177249

xyzfname = ""
dftboutf = ""

if (len(sys.argv)) == 3:
  xyzfname = sys.argv[1]
  dftboutf = sys.argv[2]
else:
  print "usage :", sys.argv[0] , " xyzfile dftb+detailed.out "
  exit(1)

xlist, ylist, zlist, atoms = xyznanop.read_ncxyz (xyzfname, False)

fp = open(dftboutf, "r")

coords = []
start = False
for l in fp:

    if (l.find("Net atomic charges (e)") != -1 ):
        start = False

    if start:
        coords.append(l)

    if (l.find("Coordinates of moved atoms (au):") != -1 ):
        start = True

fp.close()

atomslist = []

for l in coords:
    p = re.compile(r'\s+')
    line = p.sub(' ', l)
    line = line.lstrip()
    line = line.rstrip()
                     
    plist = line.split(" ")

    if len(plist) == 4:
        atomslist.append((int(plist[0])-1, \
                float(plist[1])*DELTA, float(plist[2])*DELTA, \
                float(plist[3])*DELTA))

for a in atomslist:
    idx = a[0]

    xlist[idx] = a[1]
    ylist[idx] = a[2]
    zlist[idx] = a[3]

xyznanop.write_ncxyz ("out.xyz", xlist, ylist, zlist, atoms)
