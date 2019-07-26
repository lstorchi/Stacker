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

def get_mint (idx, np_alltraps_position, alltraps, dimensions, mindist, kB, T):

    # find near by alltraps imposing boundary conditions
    dists = distance(np_alltraps_position, \
            alltraps[idx].get_position(), dimensions)
    # without boundary conditions
    # dist_2 = numpy.sum((np_alltraps_position - 
    #    alltraps[idxfrom].get_position())**2, axis=1)
    # all indexes of dist_2 where values is lower than 
    nearindex = numpy.where(dists < mindist)[0]

    free_nearindex = []
    for ival in nearindex:
        if (alltraps[ival].electron() == 0):
            free_nearindex.append(ival)

    idxtojump = -1
    t = float("+inf")
    R = numpy.random.uniform(0.0, 1.0)
    for ival in free_nearindex:
        #x, y, z = alltraps[ival].get_position()
        #print ("%10.5f %10.5f %10.5f"%(x, y, z))
        rij = dists[ival]
        aij = 1.0 # need to be defined
        Ei = alltraps[idx].get_energy()
        Ej = alltraps[ival].get_energy()
        #print ("%10.5f %10.5f "%(Ei, Ej))
        at = -1.0 * math.log(R) * t0 * math.exp( ((2.0*rij)/aij) + \
                ((Ej - Ei + abs(Ej + Ei))/(2.0*kB*T)) )
        if at < t:
            t = at
            idxtojump = ival

    return t, idxtojump, len(free_nearindex)
 
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
parser.add_argument("--t0", help="t0 value ", \
        type=float, required=False, default=2.5)
parser.add_argument("-T", help="T value ", \
        type=float, required=False, default=298.0)
parser.add_argument("--min-dist", help="Cut-off radius to neighboured traps ", \
        type=float, required=False, default=20.0, dest="mindist")
parser.add_argument("-e", "--energy-per-trap", \
        help="energies \"id1:energy1;id2:energy2;...;idN:energyN\"  ", \
        type=str, required=True, default="", dest="energy")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

fullstart = time.time()

args = parser.parse_args()

filename = args.filename

# need to set proper values
numofiter = args.numofiter
t0 = args.t0
T = args.T
kB = 1.0
mindist = args.mindist # radius of the traps where to jump

idenergymap = {}
for pair in args.energy.split(";"):
    id, e = pair.split(":")
   
    print >> sys.stderr, id, " has energy ", e

    idenergymap[int(id)] = float(e)


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

  if not (id in idenergymap.keys()):
      print "Error in energies cannot find ", sid
      exit(1)

  energy = idenergymap[id]

  if npnum not in trapsidx_for_np:
      trapsidx_for_np[npnum] = []

  trapsidx_for_np[npnum].append(i)

  t = trap(x, y, z, id, energy)
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

# box dim to be used in the boundary conditions
dimensions = numpy.array(\
        [(alltrapsxmax-alltrapsxmin), (alltrapsxmax-alltrapsymin), (alltrapszmax-alltrapszmin)])

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

# select initial NP to get an electron
# and set electron
setelectron = 0
setofnp = set()
#faket = 1.0
while setelectron < numofelectron:
    yesorno = numpy.random.choice(2)
    if yesorno == 1:
        setelectron += 1

        while True:
            setnp = random.randint(0, len(nplist)-1)
            npidx = nplist[setnp]

            if npidx not in setofnp: 
                
                randomtrapidx = -1

                while True:
                    randomtrapidx = random.randint(min(trapsidx_for_np[npidx]), \
                        max(trapsidx_for_np[npidx])) 
                    # always select the lowet trap
                    if alltraps[randomtrapidx].get_id() == 2937:
                        break

                t, idxtojump, nomoffree = get_mint (randomtrapidx, np_alltraps_position, alltraps, \
                        dimensions, mindist, kB, T)

                #faket = +0.1
                econtainer = electron()
                alltraps[randomtrapidx].set_electron(1, econtainer)
                alltraps[randomtrapidx].release_time = t
                alltraps[randomtrapidx].set_idxtojump(idxtojump)
                #alltraps[randomtrapidx].release_time = faket
                print ("Set electron %3d to NP %10d at trap %10d in state %10d time %10.5f to %10d"%(\
                        setelectron, npidx, randomtrapidx, alltraps[randomtrapidx].get_id(), \
                        alltraps[randomtrapidx].release_time, alltraps[randomtrapidx].get_idxtojump()))
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

    t, idxtojump, nomoffree = get_mint (idxfrom, np_alltraps_position, alltraps, \
                        dimensions, mindist, kB, T)


    if nomoffree == 0:
        if verbose:
            print "No free traps near by"
        for t in alltraps:
            if t.release_time < float("inf"):
                t.release_time -= tmin
    else:
        # move electron
        econtainer = alltraps[idxfrom].get_electron_cont()
        alltraps[idxfrom].set_electron(0)
        alltraps[idxfrom].release_time = float('inf')

        alltraps[idxtojump].set_electron(1, econtainer)
        alltraps[idxtojump].release_time = t
        
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
fpe = open("electrons_"+str(numofelectron)+".txt", "w")
i = 1
for t in alltraps:
    if t.electron() != 0:
        fp.write( "%10.4f %10.4f %10.4f\n"%(t.x(), t.y(), t.z()))
        Nfinalelectron += 1
        econtainer = t.get_electron_cont()
        fpe.write("electron_%d\n"%(i))
        numpy.savetxt(fpe, econtainer.get_allxyz())
        i = i +1

    #fp.write( "%10.4f %10.4f %10.4f %2d %10.4f\n"%(t.x(), t.y(), t.z(), \
    #        t.electron, t.release_time))
fp.close()
fpe.close()

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

