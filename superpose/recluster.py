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

pairsandvalues = {}
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


m = numpy.mean(values)
print m , " +/- ", numpy.std(values)
print "Num. of pairs  ", len(values)
print "Num. of single ", len(single)

lowervalue = []
lowerpairs = []
for i in range(len(values)):
    if (values[i] < m):
        lowerpairs.append(allpairs[i]) 
        lowervalue.append(values[i])

idx = 0
inserted = []
for l in single:
    if not (l in inserted):
        idx += 1
        fp = open(filename+"_set_"+str(idx)+".txt", "w")
        for i in range(len(lowerpairs)):
          lv = lowerpairs[i].split(" ")
          if lv[0] == l or lv[1] == l:
              fp.write("%s %f\n"%(lowerpairs[i], lowervalue[i]))
              inserted.append(l)
        fp.close()
