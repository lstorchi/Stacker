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

def move_electron_randmly (idxto, np_alltraps_position, alltraps, \
        trapsidx_for_np):

    newindexto = idxto

    npidx = alltraps[idxto].get_npid()
    trapidtoset = alltraps[idxto].get_id()

    while True:
        newindexto = random.randint(min(trapsidx_for_np[npidx]), \
            max(trapsidx_for_np[npidx])) 
        if (alltraps[newindexto].electron() == 0):
            if alltraps[newindexto].get_id() == trapidtoset:
                break

    return newindexto 

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
        tojumptrpid = alltraps[ival].get_id()
        npid = alltraps[ival].get_npid()
        atomid = alltraps[ival].get_atomid()
        #if (tojumptrpid != alltraps[idx].get_id()): # jump to different TRAPids
        if (npid != alltraps[idx].get_npid()): # jump to different NPs
        #if (atomid != alltraps[idx].get_atomid()): # jump to different atom
           #x, y, z = alltraps[ival].get_position()
           #print ("%10.5f %10.5f %10.5f"%(x, y, z))
           rij = dists[ival]
           alphai = alltraps[idx].get_alpha()
           Ei = alltraps[idx].get_energy()
           Ej = alltraps[ival].get_energy()
           #print ("%10.5f %10.5f "%(Ei, Ej))
           val = ((Ej - Ei + abs(Ej - Ei))/(2.0*kB*T))
           #print("%10.5f %10.5e %10.5f %10.5f %10.5f %10.5e %10.5f "%(R, t0, rij, Ei, Ej, kB, T))
           #print("%10.5e %10.5e %10.5e"%(val, math.exp( ((2.0*rij)/alphai) + val ), t0))
           at = -1.0 * math.log(R) * t0 * math.exp( ((2.0*rij)/alphai) + val )
           #print("%10.5e"%(at))
           if at < t:
               t = at
               idxtojump = ival

    # use a faketime 
    #t = numpy.random.uniform(0.0, 1.0)

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
parser.add_argument("-T", help="T value ", \
        type=float, required=False, default=298.0)
parser.add_argument("--min-dist", help="Cut-off radius to neighboured traps ", \
        type=float, required=False, default=20.0, dest="mindist")
parser.add_argument("-e", "--energy-per-trap", \
        help="energies and alpha values \"id1:energy1:alpha1;id2:energy2:alpha2;...;idN:energyN:alphaN\"  ", \
        type=str, required=True, default="", dest="energy")
parser.add_argument("-l", "--select-always-the-trapid", \
        help="specify the trapidwhere to set the electron", \
        type=int, required=False, default=None, dest="trapid")


if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

fullstart = time.time()

args = parser.parse_args()

filename = args.filename

# need to set proper values
numofiter = args.numofiter
t0 = 1.0e-13
kB = 8.617333262145e-5

T = args.T
mindist = args.mindist # radius of the traps where to jump
trapidtoset = args.trapid

idenergymap = {}
idalphamap = {}
for pair in args.energy.split(";"):
    id, e, alpha = pair.split(":")
   
    print(id, " has energy ", e, " and alpha ", alpha)

    idenergymap[int(id)] = float(e)
    idalphamap[int(id)] = float(alpha)

if trapidtoset is not None:

    if trapidtoset not in idenergymap:
        print(trapidtoset, "is not a valid trapid", file=sys.stderr)
        exit(1)

    if trapidtoset not in idalphamap:
        print(trapidtoset, "is not a valid trapid", file=sys.stderr)
        exit(1)

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

  if not (id in list(idenergymap.keys())):
      print("Error in energies cannot find ", sid)
      exit(1)

  if not (id in list(idalphamap.keys())):
      print("Error in alpha cannot find ", sid)
      exit(1)

  alpha = idalphamap[id]
  energy = idenergymap[id]

  if npnum not in trapsidx_for_np:
      trapsidx_for_np[npnum] = []

  trapsidx_for_np[npnum].append(i)

  t = trap(x, y, z, id, energy)
  t.set_alpha(alpha)
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

  if not verbose:
      progress_bar (i, lineinfile)

end = time.time()

print("")

nplist = list(npset)

numofelectron = min(args.numofelectron, len(nplist))

print("Number of NPs: ", len(nplist)) 
print("Number of electrons: ", numofelectron)
print("")
print("Storing traps' positions")
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

print("")
print("Check should be more or less the same values: ")
print("Traps X min: %10.5f Spheres X min: %10.5f "%(alltrapsxmin, xmin))
print("Traps Y min: %10.5f Spheres Y min: %10.5f "%(alltrapsymin, ymin))
print("Traps Z min: %10.5f Spheres Z min: %10.5f "%(alltrapszmin, zmin))

print("Check should be more or less the same values: ")
print("Traps X max: %10.5f Spheres X max: %10.5f "%(alltrapsxmax, xmax))
print("Traps Y max: %10.5f Spheres Y max: %10.5f "%(alltrapsymax, ymax))
print("Traps Z max: %10.5f Spheres Z max: %10.5f "%(alltrapszmax, zmax))
print("")

# select initial NP to get an electron
# and set electron
setelectron = 0
setofnp = set()
#faket = 0.0
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
                    if trapidtoset is not None:
                        if alltraps[randomtrapidx].get_id() == trapidtoset:
                            break
                    else:
                        break

                t, idxtojump, nomoffree = get_mint (randomtrapidx, np_alltraps_position, alltraps, \
                        dimensions, mindist, kB, T)

                if (t == 0.0) or (t == float("-inf")) \
                        or (t == float("+inf")):
                    print ("Error in the computed release time")
                    exit(1)

                #faket += 0.1
                econtainer = electron()
                econtainer.append_trapid(randomtrapidx)
                alltraps[randomtrapidx].set_electron(1, econtainer)
                alltraps[randomtrapidx].release_time = t
                alltraps[randomtrapidx].set_idxtojump(idxtojump)
                #alltraps[randomtrapidx].release_time = faket
                print(("Set electron %3d to NP %10d at trap %10d in state %10d time %10.5e to %10d"%(\
                        setelectron, npidx, randomtrapidx, alltraps[randomtrapidx].get_id(), \
                        alltraps[randomtrapidx].release_time, alltraps[randomtrapidx].get_idxtojump())))
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

#for idxtotest in range(len(alltraps)):
#    print "  Electron at trap: ", idxtotest , " RT: %10.5e"%(alltraps[idxtotest].release_time), \
#            " Ne: ", alltraps[idxtotest].electron()

totaltime = 0.0

for i in range(numofiter):
    idxfrom = alltraps.index(min(alltraps, key=attrgetter('release_time')))
    tmin = alltraps[idxfrom].release_time

    totaltime += tmin

    idxto = alltraps[idxfrom].get_idxtojump()
    if (idxto >= 0):
          print (idxfrom, tmin, alltraps[idxfrom].electron(), idxto)
          if verbose:
              print("Run: ", i+1, " of ", numofiter)
          
          #if verbose:
          #    for idxtotest in range(len(alltraps)):
          #        if alltraps[idxtotest].electron() != 0:
          #            print "  Electron at trap: ", idxtotest , " RT: %10.5e"%(alltraps[idxtotest].release_time) 
          
          # move electron randmly inside the same trap and same NP 
          idxto = move_electron_randmly (idxto, np_alltraps_position, alltraps, 
                  trapsidx_for_np)
          
          if (alltraps[idxto].electron() != 0):
              print("Error cannot move to occupied trap")
              exit(1)
          
          if verbose:
              print("  Index from: " , idxfrom , " RT ", alltraps[idxfrom].release_time, \
                      " NumOfEle: ", alltraps[idxfrom].electron())
          
          if alltraps[idxfrom].electron() != 1:
              print("ERROR alltraps[idxfrom] has finite release time but zero electron")
              print(alltraps[idxfrom].release_time)
              exit(1)
          
          if not verbose:
              if not numofelectron == 1:
                  progress_bar (i+1, numofiter)
          
          if numofelectron == 1:
              print("From %10.5f %10.5f %10.5f %10d %10d"%( \
                      alltraps[idxfrom].get_position()[0], \
                      alltraps[idxfrom].get_position()[1], \
                      alltraps[idxfrom].get_position()[2],
                      alltraps[idxfrom].get_npid(), \
                      alltraps[idxfrom].get_atomid()))
          
          newtime, newidxtojump, numoffree = get_mint (idxto, np_alltraps_position, alltraps, \
                              dimensions, mindist, kB, T)

          if (newtime == 0.0) or (newtime == float("-inf")) \
                     or (newtime == float("+inf")):
                 print ("Error in the computed release time")
                 exit(1)

          
          if nomoffree == 0:
              print("No free traps near by")
              exit(1)
              #for t in alltraps:
              #    if t.release_time < float("inf"):
              #        t.release_time -= (tmin*0.99)
          else:
              # move electron
              econtainer = alltraps[idxfrom].get_electron_cont()
              alltraps[idxfrom].set_electron(0)
              alltraps[idxfrom].release_time = float('inf')
              
              # reduce realease time of tmin 
              contali = 1
              for t in alltraps:
                  if t.release_time < float("inf"):
                      t.release_time -= tmin
                      contali += t.electron()
                      if verbose:
                          print("  Old RT %10.5e new RT %10.5e"%(t.release_time+tmin, \
                                     t.release_time))
          
              if contali != Nelectron:
                  print("Error started with ", Nelectron, " now we have ", contali)
                  exit(1)
          
              alltraps[idxto].set_idxtojump(newidxtojump)
              econtainer.append_trapid(idxto)
              alltraps[idxto].set_electron(1, econtainer)
              alltraps[idxto].release_time = newtime
          
              # position = bisect.insort_left(alltraps, movedtrap)
              #alltraps.sort(key=lambda x: x.release_time, reverse=False)
              
              if verbose:
                  #print "  IdxFrom: ", idxfrom , " RT: ", alltraps[idxfrom].release_time, \
                  #       " NumOfEle: ", alltraps[idxfrom].electron()
                  print("  IdxTo:   ", idxto , " RT: ", alltraps[idxto].release_time, \
                         " NumOfEle: ", alltraps[idxto].electron())
          
                  #contali = 0
                  #for idxtotest in range(len(alltraps)):
                  #    if alltraps[idxtotest].electron() != 0:
                  #        contali += 1
                  #        print "  Electron at trap: ", idxtotest , " RT: %10.5e"%(alltraps[idxtotest].release_time) 
          
              if numofelectron == 1:
                  print("To %10.5f %10.5f %10.5f %10d %10d"%( \
                          alltraps[newidxtojump].get_position()[0], \
                          alltraps[newidxtojump].get_position()[1], \
                          alltraps[newidxtojump].get_position()[2], \
                          alltraps[newidxtojump].get_npid(), \
                          alltraps[newidxtojump].get_atomid()))
    else:
          print("No free traps near by")
          exit(1)
          #for t in alltraps:
          #    if t.release_time < float("inf"):
          #        t.release_time -= (tmin*0.99)


print(" ")
print("Total run time: ", totaltime)
print(" ")

for trapidx in range(len(alltraps)):
    if (alltraps[trapidx].get_electron_cont() != None):
        print(("Electron in trap %10d of NP %10d and %10.5e release time"%(
            trapidx, alltraps[trapidx].get_npid(), alltraps[trapidx].release_time)))

 
Nfinalelectron = 0
fp = open("final_conf_"+str(numofelectron)+".txt", "w")
#fpe = open("electrons_"+str(numofelectron)+".txt", "w")
i = 1
for t in alltraps:
    if t.electron() != 0:
        fp.write( "%10.4f %10.4f %10.4f\n"%(t.x(), t.y(), t.z()))
        Nfinalelectron += 1
        econtainer = t.get_electron_cont()

        fpe = open("electrons_"+str(i)+"_of_"+ \
                str(numofelectron)+".txt", "w")
        fpe.write("electron_%d\n"%(i))
        x, y, z = econtainer.get_xyz()
        npids = econtainer.get_npid()
        trapids = econtainer.get_trapid()
        #numpy.savetxt(fpe, econtainer.get_allxyz())
        for j in range(len(trapids)):
            fpe.write( "%10.4f %10.4f %10.4f %10d %10d\n"%(x[j], y[j], z[j], \
                    npids[j], trapids[j]))
        fpe.close()
        i = i +1

    #fp.write( "%10.4f %10.4f %10.4f %2d %10.4f\n"%(t.x(), t.y(), t.z(), \
    #        t.electron, t.release_time))
fp.close()

print("")
if Nfinalelectron != Nelectron:
    print("Error number of starting electron is: ", Nelectron)
    print("     number of final electron is: ", Nfinalelectron)
file.close()

fullend = time.time()

print("")
print(("Time to read %10.3f"%(end - start)))
print(("Time compute %10.3f"%((fullend - fullstart)-(end - start))))
print(("Total time to read %10.3f"%(fullend - fullstart)))

