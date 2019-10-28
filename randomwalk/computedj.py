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

parser.add_argument("-f","--filename", help="Electron filename", \
        type=str, required=True, dest="filename")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()
filename = args.filename

file = open(filename, "r")

i = 0
lineinfile = file_len(filename)
title = file.readline()
#start posizion
line = file.readline()
mergedline = ' '.join(line.split())
sx, sy, sz, snpnum, stpidx = mergedline.split(" ")

x0 = float(sx)
y0 = float(sy)
z0 = float(sz)

xpred = x0
ypred = y0
zpred = z0

for line in file:
  mergedline = ' '.join(line.split())
  sx, sy, sz, snpnum, stpidx = mergedline.split(" ")

  x = float(sx)
  y = float(sy)
  z = float(sz)

  distopred = get_distance(xpred, ypred, zpred, x, y, z)

  print distopred

  xpred = x
  ypred = y
  zpred = z

print ""

