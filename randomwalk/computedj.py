import sys
import math
import time
import numpy
import random

from operator import attrgetter

import sys
sys.path.append("../modules")

###############################################################################

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

###############################################################################

def get_distance(x0, y0, z0, x1, y1, z1):

    dist = math.sqrt((x0-x1)**2 + (y0-y1)**2 + (z0-z1)**2 )

    return dist

###############################################################################

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filenamelist", help="Electron filename list \"file1:file2:file3:....:fileN\"", \
        type=str, required=True, dest="filenamelist")
parser.add_argument("-t","--time", help="Total time", \
        type=numpy.float64, required=True)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()
filenames = args.filenamelist.split(":")
N = numpy.float64(len(filenames))
CONV = numpy.float64(1.0e9)

total = numpy.float64(0.0)

for filename in filenames:

   file = open(filename, "r")
   
   line = file.readline()
   mergedline = ' '.join(line.split())
   sx, sy, sz, snpnum, stpidx = mergedline.split(" ")
   
   x0 = numpy.float64(sx)
   y0 = numpy.float64(sy)
   z0 = numpy.float64(sz)
   
   xpred = x0
   ypred = y0
   zpred = z0

   for line in file:
     mergedline = ' '.join(line.split())
     sx, sy, sz, snpnum, stpidx = mergedline.split(" ")
   
     x = numpy.float64(sx)
     y = numpy.float64(sy)
     z = numpy.float64(sz)
   
     distopred = get_distance(xpred, ypred, zpred, x, y, z)
   
     if distopred > 200.0:
        print "Maybe a problem: ", distopred, " in file ", filename
        print "        at line: ", mergedline

     xpred = x
     ypred = y
     zpred = z

   total += ((xpred-x0)/CONV)**2 + ((ypred-y0)/CONV)**2 + ((zpred-z0)/CONV)**2 
   
   file.close()

print numpy.log(((1.0/N) * total) / (6.0 * args.time)), ((1.0/N) * total) / (6.0 * args.time)
