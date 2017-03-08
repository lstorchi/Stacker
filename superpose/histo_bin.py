import numpy
import sys
import re

filename = ""

bintouse = 100

if (len(sys.argv) == 2 ):
  filename = sys.argv[1]
elif (len(sys.argv) == 3 ):
  filename = sys.argv[1]
  bintouse = int(sys.argv[2])

file = open(filename, "r")

values = []
allpairs = []
idx = 0
for l in file:
  p = re.compile(r'\s+')
  line = p.sub(' ', l)
  line = line.lstrip()
  line = line.rstrip()
  linelist = line.split(" ")
  val = float(linelist[3])
  
  pair1 = linelist[0] + " " + linelist[1]
  pair2 = linelist[1] + " " + linelist[0]
  if (not ((pair1 in allpairs) or (pair2 in allpairs))):
    allpairs.append(pair1)
    values.append(val)

  idx  +=  1
  #print idx

y, x = numpy.histogram(values, bins=bintouse)

print >> sys.stderr, numpy.mean(values) , " +/- ", numpy.std(values)
print >> sys.stderr, "Num. ", len(values), " of ", idx

for i in range(0, len(y)):
  print (x[i]+x[i+1])/2.0, " " , y[i]
