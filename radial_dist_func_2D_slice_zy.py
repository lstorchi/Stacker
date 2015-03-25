import sys
sys.path.append("./modules")

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

print "xmin -> xmax ", xmin , xmax

file.close()

# il piano deve essere tra xmin e xmax 
# equazione del piano

gval_average = numpy.ndarray
radiival = numpy.ndarray
thefirst = True
counter = 0.0
for xplane in drange (xmin+R_average, xmax-R_average, 2.0*R_average):
  
  spheres_in_plane = []
  
  for s in spheres:
  
    r = s.get_radius()
    c = s.get_center()
  
    cx = c.get_x()
    cy = c.get_y()
    cz = c.get_z()
  
    if (xplane >= (cx - r)) and (xplane <= (cx + r)):
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
  
    circler = math.sqrt(math.pow(r, 2) - math.pow((xplane-cx),2))
  
    cir = circle(cz, cy, circler)
    
    circles.append(cir)
  
  
  z = numpy.linspace( 0.0, 0.0, len(circles)) 
  y = numpy.linspace( 0.0, 0.0, len(circles))
  
  zmin = ymin =  100000000.0
  zmax = ymax = -100000000.0
  
  R_average_circle = 0.0
  i = 0
  for s in circles:
    zv = 0.0
    yv = 0.0 
  
    zv, yv = s.get_center()
  
    z[i] = zv
    y[i] = yv
  
    zv = z[i] - s.get_radius()
    if (zv < zmin):
      zmin = zv
  
    yv = y[i] - s.get_radius()
    if (yv < ymin):
      ymin = yv
  
    zv = z[i] + s.get_radius()
    if (zv > zmax):
      zmax = zv
  
    yv = y[i] + s.get_radius()
    if (yv > ymax):
      ymax = yv
  
    R_average_circle = R_average_circle + s.get_radius()
  
    i += 1
  
  R_average_circle = R_average_circle / float(i)
  
  print "TopZ: ", zmax, "BotZ: ", zmin
  print "TopY: ", ymax, "BotY: ", ymin
  print ""
  print "R_average_circle: " , R_average_circle
  print "I will use R_average: " , R_average
  
  tuple_box = (zmax-zmin, ymax-ymin)
  R_max = min(min(tuple_box)/2.0, 10.0*R_average)
  dr = 0.8
  
  g_average, radii, z, y, indxs = pairCorrelationFunction_2D (z, y, \
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
    gval_average[i] = gval_average[i] + g_average[i]/total
    radiival[i] = radii[i]/(R_average)
  
  sum = 0.0
  for i in range(1,radii.size):
  
    if (radii[i]/R_average) < 2.9 :
      gv = (g_average[i]/total + g_average[i-1]/total)/2.0
      dr = radii[i]-radii[i-1]
  
      sum += gv*dr
  
  print sum

outf = open ("radial_distribution.txt", "w")
for i in range(0,radii.size):
  data = str(radiival[i]) + \
      " " + str(gval_average[i]/counter) + "\n"
  outf.write(data)
outf.close()
