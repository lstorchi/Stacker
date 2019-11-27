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

title = file.readline()

coordinates = []
for line in file:
  mergedline = ' '.join(line.split())
  sx, sy, sz, snpnum, stpidx = mergedline.split(" ")

  x = float(sx)
  y = float(sy)
  z = float(sz)

  coordinates.append([x, y, z, int(snpnum), int(stpidx)])

file.close()

x0 = coordinates[0][0]
y0 = coordinates[0][1]
z0 = coordinates[0][2]

print("%10.5f %10.5f %10.5f %10d %10d"%(x0, y0, z0, \
        coordinates[0][3], coordinates[0][4]))

xpred = x0
ypred = y0
zpred = z0

svalue = 200.0

for i in range(1, len(coordinates)):

  x = coordinates[i][0]
  y = coordinates[i][1]
  z = coordinates[i][2]

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

  if tosumx or tosumy or tosumz:
    for j in range(i, len(coordinates)):
      if (tosumx):
        coordinates[j][0] += xsum 
      if (tosumy):
        coordinates[j][1] += ysum
      if (tosumz):
        coordinates[j][2] += zsum

  x = coordinates[i][0]
  y = coordinates[i][1]
  z = coordinates[i][2]

  xpred = x 
  ypred = y 
  zpred = z 

  print("%10.5f %10.5f %10.5f %10d %10d"%(xpred, ypred, zpred, \
        coordinates[i][3], coordinates[i][4]))

