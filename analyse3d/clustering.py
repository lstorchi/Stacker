import numpy
import sys
import re

from sklearn.cluster import KMeans

filename = ""

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print "usage: ", sys.argv[0] , " filename "
    exit(1)

fp = open(filename, "r")

fp.readline()

names = []
allxv = []
for line in fp:
    p = re.compile(r'\s+')
    line = p.sub(' ', line)
    line = line.lstrip()
    line = line.rstrip()
   
    plist =  line.split(" ")

    if len(plist) == 7:
        names.append(plist[0])
        allxv.append([float(plist[1]), float(plist[2]), float(plist[3]), \
            float(plist[4]), float(plist[5]), float(plist[6])])
 

fp.close()

X = numpy.asarray(allxv)
numofclust = 7

est = KMeans(n_clusters=numofclust)
est.fit(X)
labels = est.labels_

for l in labels:
    print l
