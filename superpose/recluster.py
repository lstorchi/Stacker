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

allpairs = []
values = []
single = []
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

  if not (linelist[0] in single):
      single.append(linelist[0])

  if not (linelist[1] in single):
      single.append(linelist[1])


print >> sys.stderr, numpy.mean(values) , " +/- ", numpy.std(values)
print >> sys.stderr, "Num. of pairs  ", len(values)
print >> sys.stderr, "Num. of single ", len(single)

