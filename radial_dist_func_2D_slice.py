import sys
sys.path.append("./modules")

from point import *
from sphere import *
from circle import *
from paircorrelation import *

import math
import sys

import numpy

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

for sp in file:
  x, y, z, r = sp.split(" ")
  center = point(float(x), float(y), float(z))
  s = sphere(center, float(r))
  spheres.append(s)

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

#print "xmax: ", xmax, "xmin: ",xmin, "ymax: ", ymax, \
#    "ymin: ", ymin, "zmx: ", zmax, "zmin: ", zmin

file.close()

# il piano deve essere tra zmin e zmax 
# equazione del piano
zplane = 50.0

np = 55
ns = 1

spheres_in_plane = []

for s in spheres:

  r = s.get_radius()
  c = s.get_center()

  cx = c.get_x()
  cy = c.get_y()
  cz = c.get_z()

  if (zplane >= (cz - r)) and (zplane <= (cz + r)):
    spheres_in_plane.append(s)

dt = (2.0 * math.pi)/(np)

circles = []


for s in spheres_in_plane:
  r = s.get_radius()
  c = s.get_center()

  cx = c.get_x()
  cy = c.get_y()
  cz = c.get_z()

  circler = math.sqrt(math.pow(r, 2) - math.pow((zplane-cz),2))

  cir = circle(cx, cy, circler)
  
  circles.append(cir)

x = numpy.linspace( 0.0, 0.0, len(circles)) 
y = numpy.linspace( 0.0, 0.0, len(circles))

xmin = ymin =  100000000.0
xmax = ymax = -100000000.0

R_average = 0.0
i = 0
for s in circles:
  xv = 0.0
  yv = 0.0 

  xv, yv = s.get_center()

  x[i] = xv
  y[i] = yv

  xv = x[i] - s.get_radius()
  if (xv < xmin):
    xmin = xv

  yv = y[i] - s.get_radius()
  if (yv < ymin):
    ymin = yv

  xv = x[i] + s.get_radius()
  if (xv > xmax):
    xmax = xv

  yv = y[i] + s.get_radius()
  if (yv > ymax):
    ymax = yv

  R_average = R_average + s.get_radius()

  i += 1

R_average = R_average / float(i)

print "TopX: ", xmax, "BotX: ", xmin
print "TopY: ", ymax, "BotY: ", ymin
print ""
print "R_average: " , R_average

tuple_box = (xmax-xmin, ymax-ymin)
R_max = min(min(tuple_box)/2.0, 10.0*R_average)
dr = 0.4

g_average, radii, x, y, indxs = pairCorrelationFunction_2D (x, y, \
      max(tuple_box)+(R_average),R_max,dr)

outf = open ("radial_distribution.txt", "w")

# per normalizzare a uno
#total = 1.0

total = -1000.0
for i in range(0,radii.size):
  if g_average[i] > total:
    total = g_average[i]

for i in range(0,radii.size):
  data = str(radii[i]/(R_average)) + \
      " " + str(g_average[i]/total) + "\n"
  outf.write(data)

sum = 0.0
for i in range(1,radii.size):

  if (radii[i]/R_average) < 2.9 :
    gv = (g_average[i]/total + g_average[i-1]/total)/2.0
    dr = radii[i]-radii[i-1]

    sum += gv*dr

print sum

outf.close()
