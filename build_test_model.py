import math
import random

import sys
sys.path.append("./modules")

from util import *
from point import * 
from sphere import *
from generate import *

# dimensioni box cosi' come da Langmuir 2006, 22, 7726
# in armstrong
botx = 0.0
boty = 0.0
botz = 0.0
topx = 60.0
topy = 60.0
topz = 60.0

# usiamo pori di dimensione 20 A di diametro in media
# ne uso how_many_pores
how_many_pores = 1

# raggio delle sfere
R_sphere = 5.0

pores = []

hm = 0
while len(pores) < how_many_pores:
  # il diametro e' genrato con una distribuzione
  # gaussiana con deviazione 3.33 e diametro 40.0
  r = random.gauss(40.0, 3.33)/2.0
  
  cx = random.uniform(botx+r, topx-r)
  cy = random.uniform(boty+r, topy-r)
  cz = random.uniform(botz+r, topz-r)
  
  c = point(cx, cy, cz)
  s = sphere(c, r)
  
  # controllo che non tocchi troppo gli altri pori

  if len(pores) == 0:
    pores.append(s)
  else:
    hmd = 0
    for p in pores:
      cp = p.get_center()
      rp = p.get_radius()
    
      if cp.get_distance_from(c) > (rp+r+2.0*R_sphere):
        hmd += 1

    if hmd == len(pores):
      pores.append(s)
    

outfile = open("final_pores_config.txt", "w")

for p in pores:
  c = p.get_center()
  r = p.get_radius()
  data = str(c.get_x()) + " " + str(c.get_y()) + " " + \
      str(c.get_z()) + " " + str(s.get_radius()) + "\n"

  outfile.write(data)

outfile.close()

# adesso metto le sfere in modo uniforme con raggio R_sphere
# posso usare questo step per decidere di mettere a posteriori con 
# approccio monte carlo delle sfere. Cioe' questo passomi dice quante 
# sfere al massimo mettere
#nx = (topx - botx)/(R_sphere*2.0)
#ny = (topy - boty)/(R_sphere*2.0)
#nz = (topz - botz)/(R_sphere*2.0)
# non volgio creare altri buchi a parte quelli esistenti quindi semplicemente
# mi sposto di R invece che 2R, le sfere si sovcrapporrano, ma non avro' buchi
# altra possibilita' e' un pacckin esagonale 
nx = (topx - botx)/(R_sphere)
ny = (topy - boty)/(R_sphere)
nz = (topz - botz)/(R_sphere)

howmanytoadd = 0

spheres = []

numof_added_spheres = 0

x = botx + R_sphere
for i in range(int(nx)):
  y = botx + R_sphere
  for j in range(int(ny)):
    z = botz + R_sphere
    for k in range(int(nz)):

      c = point(x, y, z)

      toadd = True
      for p in pores:
        cp = p.get_center()

        d = cp.get_distance_from(c)

        if d < (p.get_radius() + R_sphere - (0.20 * R_sphere)):
          toadd = False
          break

      if toadd:
        numof_added_spheres += 1
        s = sphere(c, R_sphere)
        spheres.append(s)
        howmanytoadd += 1

        print "Adding sphere: " , numof_added_spheres

      z += R_sphere
    y += R_sphere
  x += R_sphere

print " Ordered spheres: " , howmanytoadd


"""
tot = 10000*howmanytoadd

for i in range(tot):
  cx = random.uniform(botx, topx)
  cy = random.uniform(boty, topy)
  cz = random.uniform(botz, topz)

  toadd = True
  for p in pores:
    cp = p.get_center()

    d = cp.get_distance_from(c)

    if d < (p.get_radius() + R_sphere):
      toadd = False
      break

  if toadd:
    c = point(cx, cy, cz)
    s = sphere(c, R_sphere)
    spheres.append(s)
    print "Adding ",  i+1, " of ", tot

"""

outfiles = open("final_config.txt", "w")

for s in spheres:
  c = s.get_center()

  data = str(c.get_x()) + " " + str(c.get_y()) + " " + \
      str(c.get_z()) + " " + str(s.get_radius()) + "\n"

  outfiles.write(data)

outfiles.close()


outfiles = open("xyz_file", "w")

data = str(len(spheres)) + "\n"
outfiles.write(data)
data = "test model\n"
outfiles.write(data)

for s in spheres:
  c = s.get_center()

  data = "XX          %11.6f %11.6f %11.6f\n" % (c.get_x(),\
      c.get_y(), c.get_z())

  outfiles.write(data)

outfiles.close()
