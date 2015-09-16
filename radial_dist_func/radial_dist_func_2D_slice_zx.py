import sys
sys.path.append("../modules")

from point import *
from sphere import *
from circle import *
from paircorrelation import *

import math
import sys

import numpy

#####################################################################

def drange(start, stop, step):
  r = start
  while r < stop:
    yield r
    r += step

#####################################################################

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
file = open("final_config.txt", "r")

spheres = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

R_average = 0.0
for sp in file:
  x, y, z, r = sp.split(" ")
  center = point(float(x), float(y), float(z))
  s = sphere(center, float(r))
  spheres.append(s)

  R_average = R_average + float(r)

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

volume = (xmax-xmin) * (ymax-ymin) * (zmax-zmin)

R_average = R_average / float(len(spheres))

print "ymin -> ymax ", ymin , ymax

file.close()

# il piano deve essere tra zmin e zmax 
# equazione del piano

gval_average = numpy.ndarray
radiival = numpy.ndarray
thefirst = True
counter = 0.0
for yplane in drange (ymin+R_average, ymax-R_average, 2.0*R_average):
  
  spheres_in_plane = []
  
  for s in spheres:
  
    r = s.get_radius()
  
    c = s.get_center()
  
    cx = c.get_x()
    cy = c.get_y()
    cz = c.get_z()
  
    if (yplane >= (cy - r)) and (yplane <= (cy + r)):
      spheres_in_plane.append(s)
  
  circles = []
  
  if (len(spheres_in_plane) > 0):
    counter = counter + 1.0

  for s in spheres_in_plane:
    r = s.get_radius()
    c = s.get_center()
  
    cx = c.get_x()
    cy = c.get_y()
    cz = c.get_z()
  
    circler = math.sqrt(math.pow(r, 2) - math.pow((yplane-cy),2))
  
    cir = circle(cx, cz, circler)
    
    circles.append(cir)
  
  
  x = numpy.linspace( 0.0, 0.0, len(circles)) 
  z = numpy.linspace( 0.0, 0.0, len(circles))
  
  xmin = zmin =  100000000.0
  xmax = zmax = -100000000.0
  
  R_average_circle = 0.0
  i = 0
  for s in circles:
    xv = 0.0
    zv = 0.0 
  
    xv, zv = s.get_center()
  
    x[i] = xv
    z[i] = zv
  
    xv = x[i] - s.get_radius()
    if (xv < xmin):
      xmin = xv
  
    zv = z[i] - s.get_radius()
    if (zv < zmin):
      zmin = zv
  
    xv = x[i] + s.get_radius()
    if (xv > xmax):
      xmax = xv
  
    zv = z[i] + s.get_radius()
    if (zv > zmax):
      zmax = zv
  
    R_average_circle = R_average_circle + s.get_radius()
  
    i += 1
  
  R_average_circle = R_average_circle / float(i)
  
  print "TopX: ", xmax, "BotX: ", xmin
  print "TopZ: ", zmax, "BotZ: ", zmin
  print ""
  print "R_average_circle: " , R_average_circle
  print "I will use R_average: " , R_average
  
  tuple_box = (xmax-xmin, zmax-zmin)
  R_max = min(min(tuple_box)/2.0, 10.0*R_average)
  dr = 0.4
  
  g_average, radii, x, z, indxs = pairCorrelationFunction_2D (x, z, \
        max(tuple_box)+(R_average),R_max,dr)
  
  # per normalizzare a uno
  #total = 1.0
  
  total = -1000.0
  for i in range(0,radii.size):
    if g_average[i] > total:
      total = g_average[i]

  if thefirst:
    gval_average = numpy.linspace( 0.0, 0.0, len(g_average))
    radiival = numpy.linspace( 0.0, 0.0, len(radii))
    thefirst = False;

  for i in range(0,radii.size):
    #gval_average[i] = gval_average[i] + g_average[i]/total
    gval_average[i] = gval_average[i] + g_average[i]
    radiival[i] = radii[i]/(R_average)
  
  sum = 0.0
  for i in range(1,radii.size):
  
    if (radii[i]/R_average) < 2.9 :
      gv = (g_average[i]/total + g_average[i-1]/total)/2.0
      dr = radii[i]-radii[i-1]
  
      sum += gv*dr
  
  print sum

outf = open ("radial_distribution_zx.txt", "w")
for i in range(0,radii.size):
  data = str(radiival[i]) + \
      " " + str(gval_average[i]/counter) + "\n"
  outf.write(data)
outf.close()
