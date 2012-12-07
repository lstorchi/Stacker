import sys
sys.path.append("./modules")

from util import *
from point import *
from sphere import *

import math
import numpy
import random

usew = "random"
if (len(sys.argv)) > 1:
  usew = sys.argv[1]

file = open("final_config.txt", "r")

spheres = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

R = -1.0

for sp in file:
  x, y, z, r = sp.split(" ")
  center = point(float(x), float(y), float(z))
  s = sphere(center, float(r))
  spheres.append(s)

  if (R < 0.0):
    R = s.get_radius()
  else:
    if (R != s.get_radius()):
      print "Error"
      exit()

  if (zmax < (float(z) + float(r))):
    zmax = (float(z) + float(r))
  if (xmax < (float(x) + float(r))):
    xmax = (float(x) + float(r))
  if (ymax < (float(y) + float(r))):
    ymax = (float(y) + float(r))

  if (zmin > (float(z) - float(r))):
    zmin = (float(z) - float(r))
  if (xmin > (float(x) - float(r))):
    xmin = (float(x) - float(r))
  if (ymin > (float(y) - float(r))):
    ymin = (float(y) - float(r))

file.close()

#print "TopX: ", xmax, "BotX: ", xmin
#print "TopY: ", ymax, "BotY: ", ymin
#print "TopZ: ", zmax, "BotZ: ", zmin

scx, scy, scz = sphere_to_arrays (spheres)

botx = xmin 
boty = ymin 
botz = zmin 
topx = xmax 
topy = ymax 
topz = zmax 

topx = botx + 5 * R 
topy = boty + 5 * R
topz = botz + 5 * R


if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error"
  exit()

if usew == "random":
  numof = 10000

  for i in range(numof):
    px = random.uniform(botx, topx)
    py = random.uniform(boty, topy)
    pz = random.uniform(botz, topz) 
  
    if (is_in_the_void(scx, scy, scz, R, \
          px, py, pz)):
      print px, py, pz, "0.05"
elif usew == "grid":
  numof = 20

  dx = (topx - botx)/(numof+1) 
  dy = (topy - boty)/(numof+1)
  dz = (topz - botz)/(numof+1)

  point_inside = 0

  px = botx - dx
  for i in range(numof):
    py = boty - dy
    px += dx  
    for j in range(numof):
      pz = botz - dz
      py += dy
      for k in range(numof):
        pz += dz
 
        if (is_in_the_void(scx, scy, scz, R, \
              px, py, pz)):
          print px, py, pz, "0.02"
