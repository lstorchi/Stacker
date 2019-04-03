import sys
import math
import time
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

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

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
parser.add_argument("--num-of-electrons", help="set number of electron to place", \
        type=int, default=1, dest="numofelectron")
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

fullstart = time.time()

args = parser.parse_args()

filename = args.filename

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

npset = set()

trapsidx_for_np = {}

i = 0
lineinfile = file_len(filename)

start = time.time()

for line in file:
  mergedline = ' '.join(line.split())
  sid, sx, sy, sz, snpnum, satomid = mergedline.split(" ")

  id = int(sid)
  x = float(sx)
  y = float(sy)
  z = float(sz)
  npnum = int(snpnum)
  atomid = int(satomid)

  if npnum not in trapsidx_for_np:
      trapsidx_for_np[npnum] = []

  trapsidx_for_np[npnum].append(id)

  t = trap(x, y, z)
  t.set_id(id)
  t.set_npid(npnum)
  t.set_atomid(atomid)
  t.set_electron(0)
  t.release_time = float('inf')

  npset.add(npnum)

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

  i += 1

  progress_bar (i, lineinfile)

end = time.time()

print ""

nplist = list(npset)

numofelectron = min(args.numofelectron, len(nplist))

print "Number of NPs: ", len(nplist) 
print "Number of electrons: ", numofelectron

# select initial NP to get an electron
# and set electron
setelectron = 0
setofnp = set()
while setelectron < numofelectron:
    yesorno = numpy.random.choice(2)
    if yesorno == 1:
        setelectron += 1

        while True:
            setnp = random.randint(0, len(nplist)-1)
            npidx = nplist[setnp]

            if npidx not in setofnp: 
                randomtrapidx = random.randint(0, \
                        len(trapsidx_for_np[npidx])) 

                R = numpy.random.uniform(0.0, 1.0)
                t = -1.0 * math.log(R) * t0 * math.exp((Ec - Ei)/(kB*T))
                alltraps[randomtrapidx].set_electron(1)
                alltraps[randomtrapidx].release_time = t
                print ("Set electron %3d to NP %10d at trap %10d"%(\
                        setelectron, npidx, randomtrapidx))
                setofnp.add(npidx)
                break

Nelectron = 0
fp = open("starting_conf_"+str(numofelectron)+".txt", "w")
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
        if not numofelectron == 1:
            progress_bar (i+1, numofiter)

    if numofelectron == 1:
        print "From %10.5f %10.5f %10.5f %10d %10d"%( \
                alltraps[idxfrom].get_position()[0], \
                alltraps[idxfrom].get_position()[1], \
                alltraps[idxfrom].get_position()[2],
                alltraps[idxfrom].get_npid(), \
                alltraps[idxfrom].get_atomid())

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

        if numofelectron == 1:
            print "To %10.5f %10.5f %10.5f %10d %10d"%( \
                    alltraps[indextojump].get_position()[0], \
                    alltraps[indextojump].get_position()[1], \
                    alltraps[indextojump].get_position()[2], \
                    alltraps[indextojump].get_npid(), \
                    alltraps[indextojump].get_atomid())

 
Nfinalelectron = 0
fp = open("final_conf_"+str(numofelectron)+".txt", "w")
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

fullend = time.time()

print ""
print("Time to read %10.3f"%(end - start))
print("Time compute %10.3f"%((fullend - fullstart)-(end - start)))
print("Total time to read %10.3f"%(fullend - fullstart))

