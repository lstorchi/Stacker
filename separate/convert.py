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

filename = ""

if (len(sys.argv)) == 2:
  filename = sys.argv[1]
else:
  print "usage :", sys.argv[0] , " xyzfile"
  exit(1)

xlist, ylist, zlist, atoms = xyznanop.read_ncxyz (filename, False)

for i in range(len(xlist)):
    xlist[i] = DELTA * xlist[i]
    ylist[i] = DELTA * ylist[i]
    zlist[i] = DELTA * zlist[i]
 
xyznanop.write_ncxyz ("out.xyz", xlist, ylist, zlist, atoms)
