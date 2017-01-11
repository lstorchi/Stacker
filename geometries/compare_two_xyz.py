import sys
import math
import numpy

from scipy.spatial import distance

sys.path.append("../modules")

import xyznanop

xyz1 = ""
xyz2 = ""

if (len(sys.argv)) == 3:
  xyz1 = sys.argv[1]
  xyz2 = sys.argv[2]
else:
  print "usage: ", sys.argv[0] , " file1.xyz file2.xyz"
  exit(1)

x1, y1, z1, atoms1 = xyznanop.read_ncxyz(xyz1, trans = False)
x2, y2, z2, atoms2 = xyznanop.read_ncxyz(xyz2, trans = False)

if len(atoms1) != len(atoms2):
  print "Error different number of atoms"
  exit(1)

distances = []

for i in range(len(atoms1)):
  if atoms1[i] != atoms2[i]:
    print "Error different atom"
    exit(1)

  for j in range(len(atoms1)):
    if (j != i):
      if atoms1[j] != atoms2[j]:
        print "Error different atom"
        exit(1)
  
      
      d1 = (x1[i] - x1[j])**2 + (y1[i] - y1[j])**2 + (z1[i] - z1[j])**2
      d2 = (x2[i] - x2[j])**2 + (y2[i] - y2[j])**2 + (z2[i] - z2[j])**2 
      d1 = math.sqrt(d1)
      d2 = math.sqrt(d2)
  
      if (d1 <= 5.0) and (d2 <= 5.0):
        distances.append(math.fabs(d1 - d2))

import matplotlib.pyplot

matplotlib.pyplot.hist(distances)
matplotlib.pyplot.title("Istogramma")
matplotlib.pyplot.xlabel("Valore")
matplotlib.pyplot.ylabel("Freq.")
matplotlib.pyplot.show()

duesigma = 2.0 * numpy.std(distances)
print "Mean: ", numpy.mean(distances) 
print "2*stdev: ", 2.0 * numpy.std(distances)

indici = set()

for i in range(len(atoms1)):
  if atoms1[i] != atoms2[i]:
    print "Error different atom"
    exit(1)

  for j in range(len(atoms1)):
    if (j != i):
      if atoms1[j] != atoms2[j]:
        print "Error different atom"
        exit(1)
      
      d1 = (x1[i] - x1[j])**2 + (y1[i] - y1[j])**2 + (z1[i] - z1[j])**2
      d2 = (x2[i] - x2[j])**2 + (y2[i] - y2[j])**2 + (z2[i] - z2[j])**2 
      d1 = math.sqrt(d1)
      d2 = math.sqrt(d2)
     
      if (d1 <= 5.0) and (d2 <= 5.0):
        if (math.fabs(d2-d1) > 0.7):
          if (i not in indici) or (j not in indici):
            indici.add(i)
            indici.add(j)
            print "H ", x1[i], " ", y1[i], " ", z1[i]
            print "H ", x1[j], " ", y1[j], " ", z1[j]

