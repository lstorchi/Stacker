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

def distance(x0, x1, dimensions):
    delta = numpy.abs(x0 - x1)
    delta = numpy.where(delta > 0.5 * dimensions, delta - dimensions, delta)
    return numpy.sqrt((delta ** 2).sum(axis=-1))

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

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filename", help="Packed spheres filename", \
        type=str, required=True, dest="filename")
parser.add_argument("-v", "--verbose", help="increase output verbosity", \
        default=False, action="store_true")
parser.add_argument("--checksingleelectron", help="use a single electron for debugging", \
        default=False, action="store_true")
parser.add_argument("-n", "--num-of-iter", help="Number of iterations ", \
        type=int, required=False, default=100, dest="numofiter")
parser.add_argument("--v0", help="v0 value ", \
        type=float, required=False, default=2.5)
parser.add_argument("--Ec", help="Ec value ", \
        type=float, required=False, default=10.0)
parser.add_argument("--Ei", help="Ei value ", \
        type=float, required=False, default=11.0)
parser.add_argument("-T", help="T value ", \
        type=float, required=False, default=298.0)
parser.add_argument("--min-dist", help="Cut-off radius to neighboured traps ", \
        type=float, required=False, default=20.0, dest="mindist")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

filename = args.filename

checksingle = args.checksingleelectron

# need to set proper values
numofiter = args.numofiter
v0 = args.v0
t0 = 1.0 / v0
Ec = args.Ec
Ei = args.Ei
T = args.T
mindist = args.mindist # radius of the traps where to jump

kB = 1.0

verbose = args.verbose

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

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

print "Generate traps only if a NP has at least two near NPs"

counter = 1
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

# check single electron
if checksingle:
    traps[0].set_electron(1)
    R = numpy.random.uniform(0.0, 1.0)
    t = -1.0 * math.log(R) * t0 * math.exp((Ec - Ei)/(kB*T))
    traps[0].release_time = t
    for i in range(1, len(traps)):
        traps[i].set_electron(0)
        traps[i].release_time = float('inf')

Nelectron = 0
fp = open("starting_conf.txt", "w")
for t in traps:
    if t.electron() != 0:
        fp.write( "%10.4f %10.4f %10.4f\n"%(t.x(), t.y(), t.z()))
        Nelectron += 1
    #fp.write( "%10.4f %10.4f %10.4f %2d %10.4f\n"%(t.x(), t.y(), t.z(), \
    #        t._electron(), t.release_time))
fp.close()

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

trapsxmin = numpy.amin(np_traps_position[:,0])
trapsymin = numpy.amin(np_traps_position[:,1])
trapszmin = numpy.amin(np_traps_position[:,2])

trapsxmax = numpy.amax(np_traps_position[:,0])
trapsymax = numpy.amax(np_traps_position[:,1])
trapszmax = numpy.amax(np_traps_position[:,2])

print ""
print "Check should be more or less the same values: "
print "Traps X min: %10.5f Spheres X min: %10.5f "%(trapsxmin, xmin)
print "Traps Y min: %10.5f Spheres Y min: %10.5f "%(trapsymin, ymin)
print "Traps Z min: %10.5f Spheres Z min: %10.5f "%(trapszmin, zmin)

print "Check should be more or less the same values: "
print "Traps X max: %10.5f Spheres X max: %10.5f "%(trapsxmax, xmax)
print "Traps Y max: %10.5f Spheres Y max: %10.5f "%(trapsymax, ymax)
print "Traps Z max: %10.5f Spheres Z max: %10.5f "%(trapszmax, zmax)
print ""

# box dim to be used in the boundary conditions
dimensions = numpy.array(\
        [(trapsxmax-trapsxmin), (trapsxmax-trapsymin), (trapszmax-trapszmin)])

for i in range(numofiter):
    idxfrom = traps.index(min(traps, key=attrgetter('release_time')))
    tmin = traps[idxfrom].release_time
    if verbose:
        print idxfrom , traps[idxfrom].release_time, traps[idxfrom].electron()

    if traps[idxfrom].electron() != 1:
        print "ERROR traps[idxfrom] has finite release time but zero electron"
        print traps[idxfrom].release_time
        exit(1)
    
    if not verbose:
        if not checksingle:
            progress_bar (i+1, numofiter)

    if checksingle:
        print "%10.5f %10.5f %10.5f"%(traps[idxfrom].get_position()[0], \
                traps[idxfrom].get_position()[1], \
                traps[idxfrom].get_position()[2])

    # find near by traps imposing boundary conditions
    dists = distance(np_traps_position, traps[idxfrom].get_position(), dimensions)
    # without boundary conditions
    # dist_2 = numpy.sum((np_traps_position - traps[idxfrom].get_position())**2, axis=1)
    # all indexes of dist_2 where values is lower than 
    idexes = numpy.where(dists < mindist)[0]

    # are they free traps ?
    free_near_traps = []
    for near_i in idexes:
        if (traps[near_i].electron() == 0):
            free_near_traps.append(near_i)

    if len(free_near_traps) == 0:
        if verbose:
            print "No free traps near by"
        for t in traps:
            if t.release_time < float("inf"):
                t.release_time -= tmin
    else:
        # randomly choose a trap
        selectidx = 0
        if len(free_near_traps) > 1:
            selectidx = random.randint(0, len(free_near_traps)-1)

        indextojump = free_near_traps[selectidx]
        
        # move electron
        traps[idxfrom].set_electron(0)
        traps[idxfrom].release_time = float('inf')

        traps[indextojump].set_electron(1)
        
        # new release time is computed and trap 
        R = numpy.random.uniform(0.0, 1.0)
        t = -1.0 * math.log(R) * t0 * math.exp((Ec - Ei)/(kB*T))
        traps[indextojump].release_time = t
        
        # reduce realease time of tmin 
        for t in traps:
            if t.release_time < float("inf"):
                t.release_time -= tmin
        
        # position = bisect.insort_left(traps, movedtrap)
        #traps.sort(key=lambda x: x.release_time, reverse=False)
        
        if verbose:
            print idxfrom , traps[idxfrom].release_time, traps[idxfrom].electron()
            print indextojump , traps[indextojump].release_time, traps[indextojump].electron()

        if checksingle:
            print "%10.5f %10.5f %10.5f"%(traps[indextojump].get_position()[0], \
                traps[indextojump].get_position()[1], \
                traps[indextojump].get_position()[2])
 
 
Nfinalelectron = 0
fp = open("final_conf.txt", "w")
for t in traps:
    if t.electron() != 0:
        fp.write( "%10.4f %10.4f %10.4f\n"%(t.x(), t.y(), t.z()))
        Nfinalelectron += 1
    #fp.write( "%10.4f %10.4f %10.4f %2d %10.4f\n"%(t.x(), t.y(), t.z(), \
    #        t.electron, t.release_time))
fp.close()

print ""
if Nfinalelectron != Nelectron:
    print "Error number of starting electron is: ", Nelectron
    print "     number of final electron is: ", Nfinalelectron
