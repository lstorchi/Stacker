import sys
import vtk
import re

import random
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
import util
import cube

##################################################################

def get_color (atom):

  if (atom == 'O'):
    return 0.0, 0.0, 1.0
  elif (atom == 'Ti'):
    return 1.0, 0.0, 0.0

  return 0.0, 0.0, 0.0

#####################################################################

def get_xyz_avtors (xyzfile):

   radius = {'O':0.60, 'Ti':1.40}
   
   filep = open(xyzfile, "r")
   
   filep.readline()
   filep.readline()
   
   actors = []
   xlist = []
   ylist = []
   zlist = []
   
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
   
      if atomname in radius:
        print atomname, " has ", radius[atomname], x, y, z
   
        source = vtk.vtkSphereSource()
        source.SetCenter(float(x),float(y),float(z))
        source.SetRadius(radius[atomname])
   
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
          mapper.SetInput(source.GetOutput())
        else:
          mapper.SetInputConnection(source.GetOutputPort())
                    
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(get_color(atomname)); #(R,G,B)
        actors.append(actor)
   
   filep.close()
   
   return actors
