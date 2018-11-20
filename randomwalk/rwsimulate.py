import sys
import math
import numpy
import random

from operator import attrgetter

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

        self.release_time = 0.0

    def __lt__(self, other):
        return self.release_time < other.release_time

    def __gt__(self, other):
        return self.release_time > other.release_time

    def __repr__(self):
        return 'R Time({})'.format(self.release_time)

    def x(self):
        return self.__x__

    def y(self):
        return self.__y__

    def z(self):
        return self.__z__

    def get_position(self):
        return numpy.array([self.__x__, self.__y__, self.__z__])

    def electron(self):
        return self.__electron__

    def set_x(self, i):
        self.__x__ = i

    def set_y(self, i):
        self.__y__ = i

    def set_z(self, i):
        self.__z__ = i

    def set_electron(self, i):
        self.__electron__ = i

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

# need to set proper values
v0 = 2.5
t0 = 1.0 / v0
Ec = 10.0
Ei = 11.0 
kB = 1.0
T = 298
numofiter = 1000
mindist = 100.0 # radius of the traps where to jump

# filling the trap initial 
electrons = numpy.random.choice(2, len(traps))
for i in range(len(traps)):
    traps[i].set_electron(electrons[i])

    if electrons[i] == 1:
        R = numpy.random.uniform(0.0, 1.0)
        t = -1.0 * math.log(R) * t0 * math.exp((Ec - Ei)/(kB*T))
        traps[i].release_time = t
        #print traps[i].x(), traps[i].y(), traps[i].z(), traps[i].electron()
    else:
        traps[i].release_time = float('inf')

# sort by releaase time maybe is better not to, so near traps are near in list 
#print ""
#print "Sorting by release time "
#traps.sort(key=lambda x: x.release_time, reverse=False)
print ""
print ""
print "Storing traps' positions"
np_traps_position = numpy.zeros((len(traps), 3), numpy.float)
i = 0
for t in traps:
    np_traps_position[i,:] = t.get_position()
    i = i + 1

for i in range(numofiter):
    idxtomove = traps.index(min(traps, key=attrgetter('release_time')))
    tmin = traps[idxtomove].release_time
    print idxtomove , traps[idxtomove].release_time

    # find near by traps
    dist_2 = numpy.sum((np_traps_position - traps[idxtomove].get_position())**2, axis=1)
    # all indexes of dist_2 where values is lower than 
    idexes = numpy.where(dist_2 < mindist)[0]

    # are they free traps ?
    free_near_traps = []
    for near_i  in idexes:
        if (traps[near_i].electron() == 0):
            free_near_traps.append(near_i)

    if len(free_near_traps) == 0:
        print "No free traps"
        exit(1)

    # randomly choose a trap
    indextojump = 0
    if len(free_near_traps) > 1:
        indextojump = random.randint(0, len(free_near_traps)-1)

    # move electron
    traps[idxtomove].set_electron(0)
    traps[idxtomove].release_time = float('inf')
    traps[indextojump].set_electron(1)

    # new release time is computed and trap 
    R = numpy.random.uniform(0.0, 1.0)
    t = -1.0 * math.log(R) * t0 * math.exp((Ec - Ei)/(kB*T))
    traps[indextojump].release_time = t
 
    # reduce realease time of tmin 
    for t in traps:
        if t.release_time > float("inf"):
            t.release_time -= tmin

    # position = bisect.insort_left(traps, movedtrap)
    #traps.sort(key=lambda x: x.release_time, reverse=False)
