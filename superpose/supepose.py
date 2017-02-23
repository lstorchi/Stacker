import re
import os
import sys
import sets
import math
import glob
import numpy
import pybel
import scipy
import subprocess

sys.path.append("../modules")
import kabsch_minima

filename1 = ""
filename2 = ""

if (len(sys.argv)) == 3: 
  filename1 = sys.argv[1]
  filename2 = sys.argv[2]
else:
  print "usage :", sys.argv[0] , " filename1.mol2 filename2.mol2"
  exit(1)

xlist1, ylist1, zlist1, atoms1 = xyznanop.read_ncxyz (filename1)
xlist2, ylist2, zlist2, atoms2 = xyznanop.read_ncxyz (filename2)

if len(atoms1) == len(atoms2):
  mol1list = numpy.zeros((len(atoms1), 3))
  mol2list = numpy.zeros((len(atoms2), 3))

  for i in range(0, len(atoms1)):
    mol1list[i, 0] = xlist1[i]
    mol1list[i, 1] = ylist1[i]
    mol1list[i, 2] = zlist1[i]

  for i in range(0, len(atoms2)):
    mol2list[i, 0] = xlist2[i]
    mol2list[i, 1] = ylist2[i]
    mol2list[i, 2] = zlist2[i]

  print "RMSD: ", kabsch_minima.rmsd(mol1list, mol2list)
else:
  print "Wrong dims"
