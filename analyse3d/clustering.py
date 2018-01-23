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
        x1 = float(plist[1])
        if x1 > 10:
            x1 = 0
        x2 = float(plist[2])
        if x2 > 10:
            x2 = 0
        x3 = float(plist[3])
        if x3 > 10:
            x3 = 0
        x4 = float(plist[4])
        if x4 > 10:
            x4 = 0
        x5 = float(plist[5])
        if x5 > 10:
            x5 = 0
        x6 = float(plist[6])
        if x6 > 10:
            x6 = 0
        allxv.append([x1, x2, x3, x4, x5, x6])

fp.close()

X = numpy.asarray(allxv)
numofclust = 7

est = KMeans(n_clusters=numofclust)
est.fit(X)
labels = est.labels_

for l in labels:
    print l
