import sys
import scipy.integrate as integrate

sys.path.append("../modules")

from point import *
from sphere import *

import math

#link utili
#http://isaacs.sourceforge.net/phys/rdfs.html
#http://www.physics.emory.edu/~weeks/idl/gofr2.html
#http://www.shocksolution.com/microfluidics-and-biotechnology/calculating-the-pair-correlation-function-in-python/
#http://www.compsoc.man.ac.uk/~lucky/Democritus/Theory/rdf.html
#http://en.wikipedia.org/wiki/Random_close_pack
#http://en.wikipedia.org/wiki/Radial_distribution_function
#http://en.wikipedia.org/wiki/Coordination_number

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

print >> sys.stderr, "TopX: ", xmax, "BotX: ", xmin
print >> sys.stderr, "TopY: ", ymax, "BotY: ", ymin
print >> sys.stderr, "TopZ: ", zmax, "BotZ: ", zmin
print >> sys.stderr, ""
print >> sys.stderr, "R_average: " , R_average

file.close()

# radial distribution function
tuple_box = (xmax-xmin, ymax-ymin, zmax-zmin)

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

spheres_selected = []

for s in spheres:
  c = s.get_center()
  if ((c.get_x() - xmin) > R_max)  and ((xmax - c.get_x()) > R_max):
    if ((c.get_y() - ymin) > R_max)  and ((ymax - c.get_y()) > R_max):
      if ((c.get_z() - zmin) > R_max)  and ((zmax - c.get_z()) > R_max):
        spheres_selected.append(s)
  
print >> sys.stderr, "Selected spheres: ", len(spheres_selected)

zmax = xmax = ymax = -10000000.0
zmin = xmin = ymin =  10000000.0

for s in spheres_selected:
  c = s.get_center()
  cx = c.get_x()
  cy = c.get_y()
  cz = c.get_z()
  r = s.get_radius()

  if (zmax < (cz + r)):
    zmax = (cz + r)
  if (xmax < (cx + r)):
    xmax = (cx + r)
  if (ymax < (cy + r)):
    ymax = (cy + r)

  if (zmin > (cz - r)):
    zmin = (cz - r)
  if (xmin > (cx - r)):
    xmin = (cx - r)
  if (ymin > (cy - r)):
    ymin = (cy - r)

totv = (xmax-xmin)*(ymax-ymin)*(zmax-zmin)
density = len(spheres_selected)/totv
print >> sys.stderr, "Density: ", density

dr = 0.05
ngr = (R_max/dr)

conts = 0
for s in spheres_selected:
  r = dr
  c = s.get_center()
  
  conts += 1

  print >> sys.stderr, conts, " of ", len(spheres_selected)

  gr = linspace( 0.0, 0.0, int(ngr))
  rv = linspace( 0.0, 0.0, int(ngr))

  cont = 0
  while r < R_max:
    d = sqrt((c.get_x()-x)**2 + (c.get_y()-y)**2 + (c.get_z()-z)**2)

    bools1 = d > r
    bools2 = d < (r+dr)

    interior_indices, = where(bools1*bools2)
    num_particles = len(interior_indices)

    volume = (4.0 * math.pi * r**2) * dr

    #print r, num_particles / (density * volume)

    if (cont < int(ngr)):
      gr[cont] = num_particles / (density * volume)
      rv[cont] = r

    cont += 1
    r += dr

  # devo integrate r**2 * g(r) * density vedi wikipedia
  
  r = dr
  for i in range(1, int(ngr)):
    gr[i] = r**2 * gr[i] * density 
    r += dr

  r = 2.0*dr
  sum = 0.0
  maxvalue = -1.0
  maxtoint = -1
  for i in range(1, int(ngr)):
    rstep = r/s.get_radius()
    r += dr

    if (rstep > 1.7) and (rstep < 2.3) :
      sum += dr * ((gr[i]+gr[i-1])/2.0)
      maxtoint = i
      if gr[i] > maxvalue :
        maxvalue = gr[i]

  print >> sys.stderr, "Integrated: ", 4.0 * math.pi * sum 
  print >> sys.stderr, "Max value:  ", maxvalue

  print >> sys.stderr, "Integrated scipy: ", 4.0 * math.pi * \
      integrate.simps(gr[:maxtoint], rv[:maxtoint])



"""

colcola la funzione di distribuzione 

dr = 0.4
ngr = (R_max/dr)
gr = linspace( 0.0, 0.0, int(ngr))

conts = 0
for s in spheres_selected:
  r = dr
  c = s.get_center()
  
  conts += 1

  print conts, " of ", len(spheres_selected)

  cont = 0
  while r < R_max:
    d = sqrt((c.get_x()-x)**2 + (c.get_y()-y)**2 + (c.get_z()-z)**2)

    bools1 = d > r
    bools2 = d < (r+dr)

    interior_indices, = where(bools1*bools2)
    num_particles = len(interior_indices)

    volume = (4.0 * math.pi * r**2) * dr

    #print r, num_particles / (density * volume)

    if (cont < int(ngr)):
      gr[cont] += num_particles / (density * volume)

    cont += 1
    r += dr

for i in range(0, int(ngr)):
  gr[i] = gr[i] / len(spheres_selected)

  print i, gr[i]

"""
