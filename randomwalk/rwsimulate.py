import sys
import math
import numpy

import sys
sys.path.append("../modules")

from cube import *
from point import * 
from sphere import *

###############################################################################

def progress_bar (count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 

###############################################################################

class trap:
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.__electron__ = 0
        self.__x__ = x
        self.__y__ = y
        self.__z__ = z
        self.__release_time__ = 0.0

    def x(self):
        return self.__x__

    def y(self):
        return self.__y__

    def z(self):
        return self.__z__

    def electron(self):
        return self.__electron__

    def release_time(self):
        return self.__release_time__

    def set_x(self, i):
        self.__x__ = i

    def set_y(self, i):
        self.__y__ = i

    def set_z(self, i):
        self.__z__ = i

    def set_electron(self, i):
        self.__electron__ = i

    def set_release_time(self, i):
        self.__release_time__ = i

###############################################################################


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

  progress_bar (counter, len(spheres))
  counter += 1

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
             t = trap(x, y, z)
             traps.append(t)
             trapcounter += 1
     
         if trapcounter >= numoftraps:
             todo = False

electrons = numpy.random.choice(2, len(traps))

v0 = 2.5
t0 = 1.0 /v0
Ec = 10.0
Ei = 11.0 
kB = 1.0
T = 298

for i in range(len(traps)):
    traps[i].set_electron(electrons[i])
    R = numpy.random.uniform(0.0, 1.0)
    t = -1.0 * math.log(R) * t0 * math.exp((Ec - Ei)/(kB*T))
    traps[i].set_release_time(t)
    print traps[i].x(), traps[i].y(), traps[i].z(), traps[i].electron()
