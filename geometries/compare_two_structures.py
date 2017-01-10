import sys
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

if  mol1.OBMol.NumAtoms() == mol2.OBMol.NumAtoms() and \
    mol1.OBMol.NumBonds() == mol2.OBMol.NumBonds():

  for bond1 in openbabel.OBMolBondIter(mol1.OBMol):

    a1 = bond1.GetBeginAtomIdx()
    a2 = bond1.GetEndAtomIdx()
    bond2 = mol2.OBMol.GetBond(a1, a2)
