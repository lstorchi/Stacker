import sys
sys.path.append("../modules")

from point import *
from sphere import *

import math

filename = "final_config.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

file = open(filename, "r")

spheres = []

zmax = xmax = ymax = -10000000.0
zmin = xmin = ymin =  10000000.0

R_average = 0.0

for sp in file:
  x, y, z, r = sp.split(" ")
  center = point(float(x), float(y), float(z))
  s = sphere(center, float(r))
  spheres.append(s)

  R_average += float(r)

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

R_average = R_average / len(spheres)

print "TopX: ", xmax, "BotX: ", xmin
print "TopY: ", ymax, "BotY: ", ymin
print "TopZ: ", zmax, "BotZ: ", zmin
print ""
print "R_average: " , R_average

volume = (zmax - zmin) * (xmax - xmin) * (ymax - ymin)
ndens = len(spheres) / volume

print "Dens: ", ndens


file.close()

# radial distribution function
dr = 0.4
tuple_box = (xmax-xmin, ymax-ymin, zmax-zmin)

outf = open ("radial_distribution.txt", "w")

from paircorrelation import *
from numpy import *

x = linspace( 0.0, 0.0, len(spheres)) 
y = linspace( 0.0, 0.0, len(spheres))
z = linspace( 0.0, 0.0, len(spheres))

i = 0
for s in spheres:
  c = s.get_center()
  x[i] = c.get_x()
  y[i] = c.get_y()
  z[i] = c.get_z()
  i += 1

R_max = min(min(tuple_box)/2.0, 10.0*R_average)
Radius_to_use = R_average

g_average, radii, x, y, z, indxs = pair_correlation_function(x, y, z, \
    max(tuple_box)+(R_average),R_max,dr)

# per normalizzare a uno
#total = 1.0

total = -1000.0
for i in range(0,radii.size):
  if g_average[i] > total:
    total = g_average[i]


for i in range(0,radii.size):
  #data = str(radii[i]/(R_average)) + \
  #    " " + str(g_average[i]/total) + "\n"
  #vol = 4.0*numpy.pi*(numpy.power((radii[i]-radii[i-1])/2.0,2))
  #vol = 4.0*numpy.pi*(numpy.power((radii[i]-radii[i-1])/2.0,3))
  #rdf = g_average[i]*vol
  rdf = g_average[i]
  data = str(radii[i]/(R_average)) + \
      " " + str(rdf) + "\n"
  outf.write(data)


density = 1

sum = 0.0
for i in range(0,radii.size):

  if (radii[i]/R_average) < 3.0 :
    #gv = (g_average[i]/total + g_average[i-1]/total)/2.0
    #gv = (g_average[i] + g_average[i-1])/2.0
    dr = radii[i]-radii[i-1]
    vol = 4.0*numpy.pi*numpy.power((radii[i]-radii[i-1])/2.0,2)
    #print dr, g_average[i]
    sum += g_average[i]*vol*dr

print sum


outf.close()
