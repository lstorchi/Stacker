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
parser.add_argument("-d","--dimensions", help="dimension \"xdim:ydim:zdim\"", \
        type=str, required=True)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()
filename = args.filename
sxdim, sydim, szdim = args.dimensions.split(":")
xdim = float(sxdim)
ydim = float(sydim)
zdim = float(szdim)

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

svalue = 200.0

xsum = 0.0
ysum = 0.0
zsum = 0.0

for line in file:
  mergedline = ' '.join(line.split())
  sx, sy, sz, snpnum, stpidx = mergedline.split(" ")

  x = float(sx) + xsum
  y = float(sy) + ysum
  z = float(sz) + zsum

  tosumx = False
  tosumy = False
  tosumz = False

  if abs(x-xpred) > svalue: 
      tosumx = True
      if x-xpred > 0.0:
          xsum = -xdim
      else:
          xsum = +xdim

  if abs(y-ypred) > svalue: 
      tosumy = True
      if y-ypred > 0.0:
          ysum = -ydim
      else:
          ysum = +ydim

  if abs(z-zpred) > svalue: 
      tosumz = True
      if z-zpred > 0.0:
          zsum = -zdim
      else:
          zsum = +zdim

  xpred = x 
  if (tosumx):
      xpred += xsum
  ypred = y 
  if (tosumy):
      ypred += ysum
  zpred = z 
  if (tosumz):
      zpred += zsum

  print xpred, ypred, zpred

print ""

