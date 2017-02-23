import re
import numpy
import math
import point
import util

#####################################################################

def return_rototransl_xyz(p1, p2, theta, xlist, ylist, zlist):

  xlistnew = numpy.asarray(xlist)
  ylistnew = numpy.asarray(ylist)
  zlistnew = numpy.asarray(zlist)

  # Initialize point q
  q = point.point(0.0,0.0,0.0)
  Np = p2 - p1
  Nm = math.sqrt(Np.get_x()**2 + Np.get_y()**2 + Np.get_z()**2)

  # i due punti coincidono, non faccio nulla e ritorno
  if Nm == 0:
    xlistnew = xlistnew + p1.get_x()
    ylistnew = ylistnew + p1.get_y()
    zlistnew = zlistnew + p1.get_z()

    return  xlistnew, ylistnew, zlistnew
    
  # Rotation axis unit vector
  n = point.point(Np.get_x()/Nm, Np.get_y()/Nm, Np.get_z()/Nm)

  # Matrix common factors     
  c = math.cos(theta)
  t = (1 - math.cos(theta))
  s = math.sin(theta)
  X = n.x
  Y = n.y
  Z = n.z

  # Matrix 'M'
  d11 = t*X**2 + c
  d12 = t*X*Y - s*Z
  d13 = t*X*Z + s*Y
  d21 = t*X*Y + s*Z
  d22 = t*Y**2 + c
  d23 = t*Y*Z - s*X
  d31 = t*X*Z - s*Y
  d32 = t*Y*Z + s*X
  d33 = t*Z**2 + c

  #            |p.x|
  # Matrix 'M'*|p.y|
  #            |p.z|
  qx = d11*xlistnew + d12*ylistnew + d13*zlistnew
  qy = d21*xlistnew + d22*ylistnew + d23*zlistnew
  qz = d31*xlistnew + d32*ylistnew + d33*zlistnew

  # Translate axis and rotated point back to original location    
  qx = qx + p1.get_x()
  qy = qy + p1.get_y()
  qz = qz + p1.get_z()

  return  qx, qy, qz

#####################################################################

def read_ncxyz (filename, trans = True):

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
  
  if trans:
    xc = numpy.mean(xlist)
    yc = numpy.mean(ylist)
    zc = numpy.mean(zlist)
  
    for i in range(len(xlist)):
      xlist[i] = xlist[i] - xc
      ylist[i] = ylist[i] - yc
      zlist[i] = zlist[i] - zc
  
  return xlist, ylist, zlist, atoms

#####################################################################

def write_ncxyz (filename, xl, yl, zl, al):

  filep = open(filename, "w")
  
  filep.write("%6d\n"%(len(al)))
  filep.write("\n")
  for i in range(0, len(al)):
      filep.write("%3s %10.5f %10.5f %10.5f\n"%(al[i], xl[i], \
              yl[i], zl[i]))
  
#####################################################################
