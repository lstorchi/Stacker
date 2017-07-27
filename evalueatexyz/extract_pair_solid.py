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
  print "usage :", sys.argv[0] , " listacoppie nanopfile.txt"
  exit(1)

fp = open(nanopfile)
allstring = fp.readlines()
fp.close()


fp = open(filename)
for l in fp:
    tokens = l.split()
    if len(tokens) > 2:
        print "Error ", tokens
        exit(1)
    clusterid = int(tokens[0])

    subtokens = tokens[1].split("_")
    if len(subtokens) != 4:
        print "Error ", subtokens
        exit(1)

    id1 = int(subtokens[2])
    id2 = int(re.sub('\.xyz$', '', subtokens[-1]))
     
    fpwrt = open(str(clusterid) + ".txt", "w")
    fpwrt.write(allstring[id1])
    fpwrt.write(allstring[id2])
    fpwrt.close() 

fp.close()
