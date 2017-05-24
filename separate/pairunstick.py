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

def move_mindist_vers (xlist, ylist, zlist, atoms, s):

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
    
   mindist = numpy.min(dists)
   val =  numpy.where(dists==mindist)
   
   i = val[0][0]
   j = val[1][0]
   
   d = math.pow(xlist1[i] - xlist2[j], 2.0) + \
       math.pow(ylist1[i] - ylist2[j], 2.0) + \
       math.pow(zlist1[i] - zlist2[j], 2.0) 
   d = math.sqrt(d)
   
   print d, " == ", dists[i, j]
   
   u = ((xlist1[i] - xlist2[j])/d, \
           (ylist1[i] - ylist2[j])/d, \
           (zlist1[i] - zlist2[j])/d)
   
   print "Versor: " , u
   
   for i in range(len(xlist1)):
       xlist1[i] = xlist1[i] + u[0] * s
       ylist1[i] = ylist1[i] + u[1] * s
       zlist1[i] = zlist1[i] + u[2] * s
   
   xlist = xlist1 + xlist2
   ylist = ylist1 + ylist2
   zlist = zlist1 + zlist2
   atoms = atoms1 + atoms2
   
   coords1 = numpy.transpose(numpy.array((xlist1, ylist1, zlist1), dtype=float))
   
   dists = distance.cdist(coords1, coords2)
    
   mindist = numpy.min(dists)
   
   print "New mindist: ", mindist

   return xlist, ylist, zlist, atoms


###############################################################################

filename = ""
step = 4.0
nstep = 10 # se nstep == 1 unico spostamento 

if (len(sys.argv)) == 2:
  filename = sys.argv[1]
else:
  print "usage :", sys.argv[0] , " xyzfile"
  exit(1)

xlist, ylist, zlist, atoms = xyznanop.read_ncxyz (filename, False)

for i in range(nstep):
    s = step / float(nstep)
    
    xlist, ylist, zlist, atoms = \
            move_mindist_vers (xlist, ylist, zlist, atoms, s)

xyznanop.write_ncxyz ("out.xyz", xlist, ylist, zlist, atoms)
