import sys
import math
import pybel
import openbabel

xyz1 = ""
xyz2 = ""

if (len(sys.argv)) == 3:
  xyz1 = sys.argv[1]
  xyz2 = sys.argv[2]
else:
  print "usage: ", sys.argv[0] , " file1.mol2 file2.mol2 "
  exit(1)

mol1 = pybel.readfile("mol2", xyz1).next()
mol2 = pybel.readfile("mol2", xyz2).next()

atomlist = []

if  mol1.OBMol.NumAtoms() == mol2.OBMol.NumAtoms() and \
    mol1.OBMol.NumBonds() == mol2.OBMol.NumBonds():

  for bond1 in openbabel.OBMolBondIter(mol1.OBMol):

    a1 = bond1.GetBeginAtomIdx()
    a2 = bond1.GetEndAtomIdx()
    bond2 = mol2.OBMol.GetBond(a1, a2)

    atom1 = mol2.OBMol.GetAtom(a1)
    atom2 = mol2.OBMol.GetAtom(a2)
    #print "  ", a1, " is ", atom1.GetAtomicNum() , " ", atom1.GetX(), " " , \
    #        atom1.GetY() , " ", atom1.GetZ()
    #print "  ", a2, " is ", atom2.GetAtomicNum() , " ", atom2.GetX(), " " , \
    #        atom2.GetY() , " ", atom2.GetZ()
    d1 = (atom1.GetX() - atom2.GetX())**2 + (atom1.GetY() - atom2.GetY())**2 + \
            (atom1.GetZ() - atom2.GetZ())**2 
    #print " distance: ", d1

    atom1 = mol1.OBMol.GetAtom(a1)
    atom2 = mol1.OBMol.GetAtom(a2)
    #print "  ", a1, " is ", atom1.GetAtomicNum() , " ", atom1.GetX(), " " , \
    #        atom1.GetY() , " ", atom1.GetZ()
    #print "  ", a2, " is ", atom2.GetAtomicNum() , " ", atom2.GetX(), " " , \
    #        atom2.GetY() , " ", atom2.GetZ()
    d2 = (atom1.GetX() - atom2.GetX())**2 + (atom1.GetY() - atom2.GetY())**2 + \
            (atom1.GetZ() - atom2.GetZ())**2 
    #print " distance: ", d2

    #if bond2 is None :
    #  print a1, " and ", a2 , " are not connected in molecule 2 ", math.fabs(d2-d1) 

    print d2

    #if math.fabs(d2-d1) > 0.5:
    if bond2 is None :
      atomlist.append(a1)
      atomlist.append(a2)
      #print " H   ", atom1.GetX() , " ", atom1.GetY(), " ", atom1.GetZ()
      #print " H   ", atom2.GetX() , " ", atom2.GetY(), " ", atom2.GetZ()
 

    #else:
    #  if bond1.GetBondOrder() == bond2.GetBondOrder():
    #    l1 = bond1.GetLength()
    #    l2 = bond2.GetLength()
    #    print l1 - l2
    #  else:
    #    print "bond order differ"

