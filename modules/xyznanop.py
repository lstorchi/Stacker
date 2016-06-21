import re
import numpy
import math

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

def read_ncxyz (filename):

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
  
  return xlist, ylist, zlist, atoms

#####################################################################
