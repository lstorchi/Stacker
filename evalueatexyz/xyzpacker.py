import sys 
import re
import numpy

sys.path.append("../modules")

import nanoparticle
import point
import util


#####################################################################

def get_color (atom):

  if (atom == 'O'):
    return 0.0, 0.0, 1.0
  elif (atom == 'Ti'):
    return 1.0, 0.0, 0.0

  return 0.0, 0.0, 0.0

#####################################################################

filename = ""
nanopfile = ""
nanoparticle.POINTINSIDEDIM = 0

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

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
        nanoparticle.file_to_nanoparticle_list(nanopfile, nanoparticles) 

for nanop in  nanoparticles:
  xlistnew = xlist
  ylistnew = ylist
  zlistnew = zlist 

  # translate
  xc, yc, zc = nanop.get_center()
  
  for i in range(len(xlist)):
    xlistnew[i] = xlistnew[i] + xc
    ylistnew[i] = ylistnew[i] + yc
    zlistnew[i] = zlistnew[i] + zc
  
  theta = nanop.get_theta()
  p2 = nanop.get_p2()
  p1 = point.point(xc, yc, zc)
  
  for i in range(len(xlist)):
    p0 = point.point(xlistnew[i], ylistnew[i], zlistnew[i])
    p0 = util.point_rotate(p1, p2, p0, theta)
    xlistnew[i] = p0.get_x()
    ylistnew[i] = p0.get_y()
    zlistnew[i] = p0.get_z()

  for i in range(len(xlist)):
    print atoms[i] , " ", xlistnew[i], " ", ylistnew[i] , " " ,\
            zlistnew[i]

