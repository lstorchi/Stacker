###############################################################################

def append_if_not_in (fulllist, toadd):

  for i in toadd:
    if i not in fulllist:
      fulllist.append(i)

###############################################################################

def cubes_to_list_of_atoms(cubes, allpbc, allic, allcsc):

  for cub in cubes:
    pbc = []
    cub.get_perovskite_xyz_Pb(pbc)
    ic = []
    cub.get_perovskite_xyz_I(ic)
    csc = []
    cub.get_perovskite_xyz_Cs(csc)
    
    append_if_not_in (allpbc, pbc)
    append_if_not_in (allic, ic)
    append_if_not_in (allcsc, csc)

###############################################################################

def list_of_atoms_to_file (filename, allpbc, allic, allcsc):

  opf = open(filename, "w")

  numof = len(allpbc) + len(allic) + len(allcsc)

  opf.write(" "+str(numof)+"\n")
  opf.write(" \n")
  for i in allpbc:
    opf.write("Pb "+str(10.0*i[0])+" "+str(10.0*i[1])+" "+str(10.0*i[2])+"\n")
  for i in allic:
    opf.write(" I "+str(10.0*i[0])+" "+str(10.0*i[1])+" "+str(10.0*i[2])+"\n")
  for i in allcsc:
    opf.write("Cs "+str(10.0*i[0])+" "+str(10.0*i[1])+" "+str(10.0*i[2])+"\n")

  opf.close()

###############################################################################

def cubes_to_xyzfile (cubes, filename):

  allpbc = [] 
  allic = [] 
  allcsc = []

  cubes_to_list_of_atoms(cubes, allpbc, allic, allcsc)

  list_of_atoms_to_file (filename, allpbc, allic, allcsc)

###############################################################################
