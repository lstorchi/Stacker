import sys 
import re
import numpy
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
import common
import util


#####################################################################

def get_color (atom):

  if (atom == 'O'):
    return 0.0, 0.0, 1.0
  elif (atom == 'Ti'):
    return 1.0, 0.0, 0.0

  return 0.0, 0.0, 0.0

#####################################################################

def return_rototransl_xyz(nanop, xlist, ylist, zlist):

  xlistnew = []
  ylistnew = []
  zlistnew = []

  for i in range(len(xlist)):
    xlistnew.append(xlist[i])
    ylistnew.append(ylist[i])
    zlistnew.append(zlist[i])

  xcn, ycn, zcn = nanop.get_center()

  for i in range(len(xlist)):
    xlistnew[i] = xlistnew[i] + xcn
    ylistnew[i] = ylistnew[i] + ycn
    zlistnew[i] = zlistnew[i] + zcn

  theta =nanop.get_theta()
  p2 = nanop.get_p2()
  p1 = point.point(xcn, ycn, zcn)
  
  for i in range(len(xlist)):
    p0 = point.point(xlistnew[i], ylistnew[i], zlistnew[i])
    p0 = util.point_rotate(p1, p2, p0, theta)
    xlistnew[i] = p0.get_x()
    ylistnew[i] = p0.get_y()
    zlistnew[i] = p0.get_z()

  return  xlistnew, ylistnew, zlistnew

#####################################################################


filename = ""
nanopfile = ""
nanoparticle.POINTINSIDEDIM = 0
#nanoparticle.POINTINSURFACESTEP = 0.0

if (len(sys.argv)) == 3:
  filename = sys.argv[1]
  nanopfile = sys.argv[2]
else:
  print "usage :", sys.argv[0] , " xyzfile nanopfile.txt"
  exit(1)

filep = open(filename, "r")

filep.readline()
filep.readline()

xlist = []
ylist = []
zlist = []
atoms = []

for line in filep:
  p = re.compile(r'\s+')
  line = p.sub(' ', line)
  line = line.lstrip()
  line = line.rstrip()

  plist =  line.split(" ")

  if (len(plist) == 4):
   atomname = plist[0]
   x = plist[1]
   y = plist[2]
   z = plist[3]

   xlist.append(float(x))
   ylist.append(float(y))
   zlist.append(float(z))
   atoms.append(atomname)

filep.close()

xc = numpy.mean(xlist)
yc = numpy.mean(ylist)
zc = numpy.mean(zlist)

for i in range(len(xlist)):
  xlist[i] = xlist[i] - xc
  ylist[i] = ylist[i] - yc
  zlist[i] = zlist[i] - zc

nanoparticles_init = []

botx, topx, boty, topy, botz, topz = \
        nanoparticle.file_to_nanoparticle_list(nanopfile, nanoparticles_init)

print >> sys.stderr, "Read done"
 
nanoparticles = []
for selectedid in range(len(nanoparticles_init)):
  nanop = nanoparticles_init[selectedid]
  pcx, pcy, pcz = nanop.get_center()

  # seleziona solo particelle interne
  distx = min(math.fabs(pcx-botx), math.fabs(pcx-topx))
  disty = min(math.fabs(pcy-boty), math.fabs(pcy-topy))
  distz = min(math.fabs(pcz-botz), math.fabs(pcz-topz))

  #print min(distx, disty, distz), 2.0 * common.R

  if (min(distx, disty, distz) > (2.0 * common.R)):
    nanoparticles.append(nanop)

print >> sys.stderr, "Near done"
radius = {'O':0.60, 'Ti':1.40}
 
for selectedid in range(len(nanoparticles)):
  nanop = nanoparticles[selectedid]
  pcx, pcy, pcz = nanop.get_center()

  nearnanop, neardst = nanoparticle.get_near_nanoparticle (nanoparticles, \
      pcx, pcy, pcz, (2.0 * nanop.get_max_sphere()))

  count = 1
  for a in range(len(nearnanop)):
    for b in range(len(nearnanop)):
      if (a != b):
        xlistnew, ylistnew, zlistnew = return_rototransl_xyz(nearnanop[a], xlist, ylist, zlist)

        n = len(nearnanop)
        print "running ", count , " of ", n**2-n

        todo = False

        xlistnewa = []
        ylistnewa = []
        zlistnewa = []
        atomsa = []

        for i in range(len(xlist)):
          center = point.point(xlistnew[i], ylistnew[i], zlistnew[i])
          s = sphere.sphere(center, radius[atoms[i]])
          if (nearnanop[b].sphere_touch_me(s)):
            todo = True
          else:
            xlistnewa.append(xlistnew[i])
            ylistnewa.append(ylistnew[i])
            zlistnewa.append(zlistnew[i])
            atomsa.append(atoms[i])

        print "         ", todo

        if (todo):
          xlistnew, ylistnew, zlistnew = return_rototransl_xyz(nearnanop[b], xlist, ylist, zlist)

          filename = str(a) + "_" + str(b) + ".xyz"
          target = open(filename, 'w')
          target.write(str(len(xlistnew)+len(xlistnewa))+"\n")
          target.write("\n")
          
          for i in range(len(xlistnewa)):
            target.write(str(atomsa[i]) + " " + \
                      str(xlistnewa[i]) + " " + \
                      str(ylistnewa[i]) + " " + \
                      str(zlistnewa[i]))
            target.write("\n")
          
          for i in range(len(xlist)):
            target.write(str(atoms[i]) + " " + \
                      str(xlistnew[i]) + " " + \
                      str(ylistnew[i]) + " " + \
                      str(zlistnew[i]))
            target.write("\n")
          
          target.close()

        count = count + 1

  exit() 
