import sys
import math
import numpy

import sys
sys.path.append("../modules")

from cube import *
from point import * 
from sphere import *

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

filename = "final_config.txt"
read_cube = False

if (len(sys.argv)) == 2:
  filename = sys.argv[1]
elif (len(sys.argv)) == 8:
  filename = sys.argv[1]
  read_cube = True

# parto dal presupposto che hanno lo stesso raggio
file = open(filename, "r")

PERCSME = 1.05

spheres = []
mappers = []
actors = []
sources = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

for sp in file:
  x, y, z, r = sp.split(" ")
  center = point(float(x), float(y), float(z))
  s = sphere(center, float(r))
  spheres.append(s)

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

counter = 0
traps = []
# find neighbourhood
for s in spheres:
  c = s.get_center()
  r = s.get_radius()

  nearspheres = []
  for snear in spheres:
      cnear = snear.get_center()
      rnear = snear.get_radius()

      if  cnear.get_x() != c.get_x() and \
              cnear.get_y() != c.get_y() and \
              cnear.get_z() != c.get_z():
          if cnear.get_z() >= c.get_z() + 2 * r:
              break

          xdiff = cnear.get_x() - c.get_x()
          ydiff = cnear.get_y() - c.get_y()
          zdiff = cnear.get_z() - c.get_z()

          dist = math.sqrt((xdiff * xdiff) + (ydiff * ydiff) + \
                  (zdiff * zdiff))
          if dist <= r+rnear:
              nearspheres.append(snear)

  if len(nearspheres) >= 2:

     # generate traps
     numoftraps = 100
     todo = True
     
     trapcounter = 0
     while todo:
         theta = 2.0 * math.pi * numpy.random.uniform(0.0, 1.0)
         phi = math.pi * numpy.random.uniform(0.0, 1.0)
         x = c.get_x() + r * math.sin(phi) * math.cos(theta)
         y = c.get_y() + r * math.sin(phi) * math.sin(theta)
         z = c.get_z() + r * math.cos(phi)
         
         placethetrap = True
     
         for snear in nearspheres:
             cnear = snear.get_center()
             rnear = snear.get_radius()
     
             xdiff = cnear.get_x() - x
             ydiff = cnear.get_y() - y
             zdiff = cnear.get_z() - z
     
             dist = math.sqrt((xdiff * xdiff) + (ydiff * ydiff) + \
                     (zdiff * zdiff))
     
             if dist <= rnear*PERCSME:
                 placethetrap = False
                 break;
     
         if placethetrap:
             traps.append((x, y, z))
             trapcounter += 1
     
         if trapcounter >= numoftraps:
             todo = False

for trap in traps:
    print trap
