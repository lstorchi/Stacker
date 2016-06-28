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

vdwradius = {'O':0.60, 'Ti':1.40}
sumofvdw = numpy.zeros((len(atoms),len(atoms)))
for i in range(0,len(atoms)):
  for j in range(0,len(atoms)):
    sumofvdw[i][j] = vdwradius[atoms[i]] + vdwradius[atoms[j]]

pairs = []
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

      if (md > 2.0 and md < 5.0):
        plist1 = nanop1.get_corners ()
        plist2 = nanop2.get_corners ()

        p1top, p1bottom = nanop1.get_ptop_and_bottom ()
        p2top, p2bottom = nanop2.get_ptop_and_bottom ()

        plist1.append(p1top)
        plist1.append(p1bottom)

        plist2.append(p2top)
        plist2.append(p2bottom)

        l3d = line.line3d()
        angle = l3d.get_angle_two_line(p1top, p1bottom, p2top, p2bottom)

        print md

        #le distanze per il clustering direi sono le distanze tra tutti i vertici 
        #appure posso usare g_cluster 
 
print "Num. of Pairs: ", len(pairs)
