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

if (len(sys.argv)) == 2:
  filename = sys.argv[1]
else:
  print "usage :", sys.argv[0] , " listacoppie nanopfile.txt"
  exit(1)


fp = open(filename)
for l in fp:
    tokens = l.split()
    if len(tokens) > 2:
        print "Error ", tokens
        exit(1)
    clusterid = int(tokens[0])


    print "scp banquoch:/home/redo/Paper_Stacker/stacker/superpose/Orig/"+\
            str(clusterid)+"_near/"+tokens[1]+" ."

fp.close()
