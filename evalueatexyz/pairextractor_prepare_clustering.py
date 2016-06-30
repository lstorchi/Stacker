import re
import sys 
import math
import scipy 
import numpy

from scipy.spatial import distance
from scipy import cluster

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

print "Read done"

vdwradius = {'O':0.60, 'Ti':1.40}
sumofvdw = numpy.zeros((len(atoms),len(atoms)))
for i in range(0,len(atoms)):
  for j in range(0,len(atoms)):
    sumofvdw[i][j] = vdwradius[atoms[i]] + vdwradius[atoms[j]]

pairs = []
clusterpair = []
print "Start pair selection ..."

for id1 in range(len(nanoparticles)):
  nanop1 = nanoparticles[id1]
  p1cx, p1cy, p1cz = nanop1.get_center()
  sumr = 2.25 * nanop1.get_max_sphere()

  indices, d = nanoparticle.get_near_nanoparticle_indexs(nanoparticles, \
          p1cx, p1cy, p1cz, sumr)

  theta = nanop1.get_theta()
  p2 = nanop1.get_p2()
  p1 = point.point(p1cx, p1cy, p1cz)

  xlist1, ylist1, zlist1 = xyznanop.return_rototransl_xyz(p1, p2, theta, \
          xlist, ylist, zlist)
  
  n1 = numpy.column_stack((xlist1, ylist1, zlist1))
  
  for i in range(len(indices)):
    id2 = indices[i]
 
    pair = str(id1) + "_" + str(id2)
    if (id1 != id2) and (pair not in pairs):
      pairs.append(str(id1) + "_" + str(id2))
      pairs.append(str(id2) + "_" + str(id1))
    
      nanop2 = nanoparticles[id2]

      p2cx, p2cy, p2cz = nanop2.get_center()
 
      theta = nanop2.get_theta()
      p2 = nanop2.get_p2()
      p1 = point.point(p2cx, p2cy, p2cz)

      xlist2, ylist2, zlist2 = xyznanop.return_rototransl_xyz(p1, p2, theta, \
              xlist, ylist, zlist)

      n2 = numpy.column_stack((xlist2, ylist2, zlist2))
 
      dists = scipy.spatial.distance.cdist(n1, n2)
      dists = dists - sumofvdw

      md = numpy.min(dists)

      if (md > 0.0 and md < 3.0):
        clusterpair.append(str(id1) + "_" + str(id2))

        #le distanze per il clustering direi sono le distanze tra tutti i vertici 
        #appure posso usare g_cluster 
 
print "Num. of Pairs: ", len(pairs), " after second check " , len(clusterpair)

print "Start preparing PDB..." 

for i in range(len(clusterpair)):
  pair = clusterpair[i]

  idxs = pair.split("_")

  if (len(idxs) > 2):
    print "Orrore 1"
    exit(1)

  idx1 = int(idxs[0])
  idx2 = int(idxs[1])

  nanop1 = nanoparticles[idx1]
  nanop2 = nanoparticles[idx2]

  p1cx, p1cy, p1cz = nanop1.get_center()
  p2cx, p2cy, p2cz = nanop2.get_center()
 
  theta = nanop1.get_theta()
  p2 = nanop1.get_p2()
  p1 = point.point(p1cx, p1cy, p1cz)

  xlist1, ylist1, zlist1 = xyznanop.return_rototransl_xyz(p1, p2, theta, \
          xlist, ylist, zlist)

  xlistall = xlist1.tolist()
  ylistall = ylist1.tolist()
  zlistall = zlist1.tolist()

  theta = nanop2.get_theta()
  p2 = nanop2.get_p2()
  p1 = point.point(p2cx, p2cy, p2cz)

  xlist2, ylist2, zlist2 = xyznanop.return_rototransl_xyz(p1, p2, theta, \
          xlist, ylist, zlist)

  xlistall.extend(xlist2.tolist())
  ylistall.extend(ylist2.tolist())
  zlistall.extend(zlist2.tolist())

  filename = "pair_" + \
          str(idx1) + "_" + str(idx2) + ".xyz"

  molname = "pair_"+ str(idx1) + "_" + str(idx2)
  dim = len(xlist1)+len(xlist2)
  target = open(filename, 'w')
  target.write("%d\n%s\n" % (dim, molname))

  # direi che devo ritraslare tutto su zero credo 
  xc = numpy.mean(xlistall)
  yc = numpy.mean(ylistall)
  zc = numpy.mean(zlistall)

  xlist1 = xlist1 - xc
  ylist1 = ylist1 - yc
  zlist1 = zlist1 - zc

  xlist2 = xlist2 - xc
  ylist2 = ylist2 - yc
  zlist2 = zlist2 - zc

  for i in range(len(xlist1)):
    target.write("%3s %10.5g %10.5g %10.5g\n" % \
            (atoms[i], xlist1[i], ylist1[i], zlist1[i]))
  
  for i in range(len(xlist2)):
    target.write("%3s %10.5g %10.5g %10.5g\n" % \
            (atoms[i], xlist2[i], ylist2[i], zlist2[i]))
 
  target.close()
