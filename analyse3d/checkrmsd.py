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

from operator import itemgetter

sys.path.append("../modules")
import kabsch_minima
import xyznanop

###############################################################################

def compare (filename1, filename2, verbose, dumpalsoobmol):

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
    
      if (verbose):
        print "RMSD: ", kabsch_minima.rmsd(mol1list, mol2list)
    
      rmatrix, translate2, translate1 = \
              kabsch_minima.return_rotation_matrix(mol2list, mol1list, verbose)
    
      if verbose:
        print "Translate: ", filename1
      for i in range(0, len(atoms1)):
        xlist1[i] -= translate1[0]
        ylist1[i] -= translate1[1]
        zlist1[i] -= translate1[2]
      if verbose:
        print "Done"
    
      if verbose:
        xyznanop.write_ncxyz("out1.xyz", xlist1, ylist1, zlist1, atoms1)
    
      if verbose:
        print "Translate: ", filename2
      for i in range(0, len(atoms1)):
        xlist2[i] -= translate2[0]
        ylist2[i] -= translate2[1]
        zlist2[i] -= translate2[2]
    
      d11 = rmatrix[0, 0]
      d12 = rmatrix[0, 1]
      d13 = rmatrix[0, 2]
    
      d21 = rmatrix[1, 0]
      d22 = rmatrix[1, 1]
      d23 = rmatrix[1, 2]
    
      d31 = rmatrix[2, 0]
      d32 = rmatrix[2, 1]
      d33 = rmatrix[2, 2]
    
      qx = []
      qy = []
      qz = []
      
      if verbose:
        print "Rotate: ", filename2
      for i in range(0,len(atoms2)):
        qx.append(d11*xlist2[i] + d12*ylist2[i] + d13*zlist2[i])
        qy.append(d21*xlist2[i] + d22*ylist2[i] + d23*zlist2[i]) 
        qz.append(d31*xlist2[i] + d32*ylist2[i] + d33*zlist2[i]) 
      if verbose:
        print "Done"
    
      if verbose:
        xyznanop.write_ncxyz("out2.xyz", qx, qy, qz, atoms2)
    
      for i in range(0, len(atoms1)):
        mol1list[i, 0] = xlist1[i]
        mol1list[i, 1] = ylist1[i]
        mol1list[i, 2] = zlist1[i]
    
      for i in range(0, len(atoms2)):
        mol2list[i, 0] = qx[i]
        mol2list[i, 1] = qy[i]
        mol2list[i, 2] = qz[i]
    
      rmsdfinal = kabsch_minima.rmsd(mol1list, mol2list)

      if verbose:
        print filename1, " ", filename2, " ", "RMSD: ", \
                rmsdfinal
   
      if dumpalsoobmol:
        ormatrix = pybel.ob.matrix3x3()
        for i in range(3):
          for j in range(3):
            ormatrix.Set(i, j, rmatrix[i,j]) 
            myrm = pybel.ob.doubleArray(9)
            ormatrix.GetArray(myrm)
        
        print "Translate: ", filename1
        mol1 = pybel.readfile("xyz", filename1).next()
        print "  read file"
        mol1.OBMol.Translate(pybel.ob.vector3(-translate1[0], -translate1[1], -translate1[2]));
        print "  translate"
        output = pybel.Outputfile("xyz", "pout1.xyz", overwrite=True)
        output.write(mol1)
        output.close()
        print "Done"
        
        print "Rotate and Translate: ", filename1
        mol2 = pybel.readfile("xyz", filename2).next()
        print "  read file"
        mol2.OBMol.Translate(pybel.ob.vector3(-translate2[0], -translate2[1], -translate2[2]));
        print "  translate"
        mol2.OBMol.Rotate(myrm)
        print "  rotate"
        output = pybel.Outputfile("xyz", "pout2.xyz", overwrite=True)
        output.write(mol2)
        output.close()
        print "Done"
    
      return rmsdfinal
    else:
      print "Wrong dim"
      print len(atoms1) , len(atoms2)

    return None

###############################################################################

filename1 = ""
filename2 = ""
verbose = False
dumpalsoobmol = False

file1 = ""
file2 = ""
if (len(sys.argv) == 3 ):
  file1 = sys.argv[1]
  file2 = sys.argv[2]
else:
  exit(1)

rmsd = compare (file1, file2, False, False)
if rmsd < 1e-3:
    rmsd = 0.0
print  file1, " ", file2, " ", rmsd
