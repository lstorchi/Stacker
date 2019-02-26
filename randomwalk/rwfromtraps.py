import sys
import math
import numpy
import random

from operator import attrgetter

import sys
sys.path.append("../modules")

from cube import *
from traps import *
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

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filename", help="Traps filename", \
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

file = open(filename, "r")

alltraps = []

xmin = float("inf")
ymin = float("inf")
zmin = float("inf")

xmax = float("-inf")
ymax = float("-inf")
zmax = float("-inf")


for line in file:
  mergedline = ' '.join(line.split())
  sid, sx, sy, sz, snpnum = mergedline.split(" ")

  id = int(sid)
  x = float(sx)
  y = float(sy)
  z = float(sz)
  npnum = int(snpnum)

  t = trap(x, y, z)
  t.set_id(id)
  t.set_npid(npnum)

  if x < xmin:
      xmin = x
  if x > xmax:
      xmax = x

  if y < ymin:
      ymin = y
  if y > ymax:
      ymax = y

  if z < zmin:
      zmin = z
  if z > zmax:
      zmax = z

  alltraps.append(t)


# filling the trap initial 
electrons = numpy.random.choice(2, len(alltraps))
for i in range(len(alltraps)):
    alltraps[i].set_electron(electrons[i])

    if electrons[i] == 1:
        R = numpy.random.uniform(0.0, 1.0)
        t = -1.0 * math.log(R) * t0 * math.exp((Ec - Ei)/(kB*T))
        alltraps[i].release_time = t
        #print alltraps[i].x(), alltraps[i].y(), alltraps[i].z(), alltraps[i].electron()
    else:
        alltraps[i].release_time = float('inf')

# check single electron
if checksingle:
    alltraps[0].set_electron(1)
    R = numpy.random.uniform(0.0, 1.0)
    t = -1.0 * math.log(R) * t0 * math.exp((Ec - Ei)/(kB*T))
    alltraps[0].release_time = t
    for i in range(1, len(alltraps)):
        alltraps[i].set_electron(0)
        alltraps[i].release_time = float('inf')

Nelectron = 0
fp = open("starting_conf.txt", "w")
for t in alltraps:
    if t.electron() != 0:
        fp.write( "%10.4f %10.4f %10.4f\n"%(t.x(), t.y(), t.z()))
        Nelectron += 1
    #fp.write( "%10.4f %10.4f %10.4f %2d %10.4f\n"%(t.x(), t.y(), t.z(), \
    #        t._electron(), t.release_time))
fp.close()

# sort by releaase time maybe is better not to, so near traps are near in list 
#print ""
#print "Sorting by release time "
#alltraps.sort(key=lambda x: x.release_time, reverse=False)
print ""
print ""
print "Storing traps' positions"
np_alltraps_position = numpy.zeros((len(alltraps), 3), numpy.float)
i = 0
for t in alltraps:
    np_alltraps_position[i,:] = t.get_position()
    i = i + 1

alltrapsxmin = numpy.amin(np_alltraps_position[:,0])
alltrapsymin = numpy.amin(np_alltraps_position[:,1])
alltrapszmin = numpy.amin(np_alltraps_position[:,2])

alltrapsxmax = numpy.amax(np_alltraps_position[:,0])
alltrapsymax = numpy.amax(np_alltraps_position[:,1])
alltrapszmax = numpy.amax(np_alltraps_position[:,2])

print ""
print "Check should be more or less the same values: "
print "Traps X min: %10.5f Spheres X min: %10.5f "%(alltrapsxmin, xmin)
print "Traps Y min: %10.5f Spheres Y min: %10.5f "%(alltrapsymin, ymin)
print "Traps Z min: %10.5f Spheres Z min: %10.5f "%(alltrapszmin, zmin)

print "Check should be more or less the same values: "
print "Traps X max: %10.5f Spheres X max: %10.5f "%(alltrapsxmax, xmax)
print "Traps Y max: %10.5f Spheres Y max: %10.5f "%(alltrapsymax, ymax)
print "Traps Z max: %10.5f Spheres Z max: %10.5f "%(alltrapszmax, zmax)
print ""

# box dim to be used in the boundary conditions
dimensions = numpy.array(\
        [(alltrapsxmax-alltrapsxmin), (alltrapsxmax-alltrapsymin), (alltrapszmax-alltrapszmin)])

for i in range(numofiter):
    idxfrom = alltraps.index(min(alltraps, key=attrgetter('release_time')))
    tmin = alltraps[idxfrom].release_time
    if verbose:
        print idxfrom , alltraps[idxfrom].release_time, alltraps[idxfrom].electron()

    if alltraps[idxfrom].electron() != 1:
        print "ERROR alltraps[idxfrom] has finite release time but zero electron"
        print alltraps[idxfrom].release_time
        exit(1)
    
    if not verbose:
        if not checksingle:
            progress_bar (i+1, numofiter)

    if checksingle:
        print "%10.5f %10.5f %10.5f"%(alltraps[idxfrom].get_position()[0], \
                alltraps[idxfrom].get_position()[1], \
                alltraps[idxfrom].get_position()[2])

    # find near by alltraps imposing boundary conditions
    dists = distance(np_alltraps_position, alltraps[idxfrom].get_position(), dimensions)
    # without boundary conditions
    # dist_2 = numpy.sum((np_alltraps_position - alltraps[idxfrom].get_position())**2, axis=1)
    # all indexes of dist_2 where values is lower than 
    idexes = numpy.where(dists < mindist)[0]

    # are they free traps ?
    free_near_alltraps = []
    for near_i in idexes:
        if (alltraps[near_i].electron() == 0 and \
                alltraps[near_i].get_npid() != alltraps[idxfrom].get_npid()):
            free_near_alltraps.append(near_i)

    if len(free_near_alltraps) == 0:
        if verbose:
            print "No free traps near by"
        for t in alltraps:
            if t.release_time < float("inf"):
                t.release_time -= tmin
    else:
        # randomly choose a trap
        selectidx = 0
        if len(free_near_alltraps) > 1:
            selectidx = random.randint(0, len(free_near_alltraps)-1)

        indextojump = free_near_alltraps[selectidx]
        
        # move electron
        alltraps[idxfrom].set_electron(0)
        alltraps[idxfrom].release_time = float('inf')

        alltraps[indextojump].set_electron(1)
        
        # new release time is computed and trap 
        R = numpy.random.uniform(0.0, 1.0)
        t = -1.0 * math.log(R) * t0 * math.exp((Ec - Ei)/(kB*T))
        alltraps[indextojump].release_time = t
        
        # reduce realease time of tmin 
        for t in alltraps:
            if t.release_time < float("inf"):
                t.release_time -= tmin
        
        # position = bisect.insort_left(alltraps, movedtrap)
        #alltraps.sort(key=lambda x: x.release_time, reverse=False)
        
        if verbose:
            print idxfrom , alltraps[idxfrom].release_time, alltraps[idxfrom].electron()
            print indextojump , alltraps[indextojump].release_time, alltraps[indextojump].electron()

        if checksingle:
            print "%10.5f %10.5f %10.5f"%(alltraps[indextojump].get_position()[0], \
                alltraps[indextojump].get_position()[1], \
                alltraps[indextojump].get_position()[2])
 
 
Nfinalelectron = 0
fp = open("final_conf.txt", "w")
for t in alltraps:
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
file.close()
