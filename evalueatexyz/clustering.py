import re
import sys 
import math
import scipy 
import numpy

from scipy.spatial import distance
from scipy import cluster

from os import listdir
from os.path import isfile, join

sys.path.append("../modules")

import nanoparticle
import xyznanop
import common
import sphere
import point
import util
import line

mypath = "./XYZ/"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


alldists = []
for file in onlyfiles:
  if file.endswith('.xyz'):
    print mypath+file
    xlist, ylist, zlist, atoms = xyznanop.read_ncxyz (mypath+file)

    xlist1 = xlist[0:(len(xlist)/2)-1]
    ylist1 = ylist[0:(len(ylist)/2)-1]
    zlist1 = zlist[0:(len(zlist)/2)-1]

    xlist2 = xlist[len(xlist)/2:len(xlist)-1]
    ylist2 = ylist[len(ylist)/2:len(ylist)-1]
    zlist2 = zlist[len(zlist)/2:len(zlist)-1]

    dists = []
    for i in range(0,len(xlist1)):
      dx = (xlist1[i] - xlist2[i])**2 
      dy = (ylist1[i] - ylist2[i])**2
      dz = (zlist1[i] - zlist2[i])**2

      d = math.sqrt(dx+dy+dz)

      dists.append(d)

    alldists.append(dists)


print "Start Clustering..." 
pointstocluster = numpy.zeros((len(alldists), len(alldists[0])))
for i in range(0,len(alldists)):
  for j in range(0,len(alldists[i])):
    pointstocluster[i,j] = alldists[i][j]

for NUMOFCLUST in range(10, 500, 10):
  print "using: ", NUMOFCLUST 
  centroids, selected = cluster.vq.kmeans2 (pointstocluster, NUMOFCLUST)

