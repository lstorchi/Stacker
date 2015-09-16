import sys
sys.path.append("../modules")

import util 
import point
import sphere

import math
import numpy
import random

#######################################################

def get_min_distance (scx, scy, scz, px, py, pz):

  distx = (scx - px)
  disty = (scy - py)
  distz = (scz - pz)

  distx2 = distx * distx
  disty2 = disty * disty
  distz2 = distz * distz

  dist = distx2 + disty2 + distz2

  d = numpy.sqrt(dist)

  return numpy.min(d)

#######################################################

numpy.seterr(invalid='raise')

filename = "final_config.txt"
spheres = []
zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0
R = -1.0

xmin, xmax, ymin, ymax, zmin, zmax, R = \
    util.file_to_sphere_list(filename, spheres) 

volume = (xmax-xmin) * (ymax-ymin) * (zmax-zmin)

print "TopX: ", xmax, "BotX: ", xmin
print "TopY: ", ymax, "BotY: ", ymin
print "TopZ: ", zmax, "BotZ: ", zmin

scx, scy, scz, rads = sphere.sphere_to_arrays (spheres)

# lascio dai bordi uno spazio 2*R 
botx = xmin + (2 * R)
boty = ymin + (2 * R)
botz = zmin + (2 * R)
topx = xmax - (2 * R)
topy = ymax - (2 * R)
topz = zmax - (2 * R)

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

print ""
print "I will use the following box: "
print "TopX: ", topx, "BotX: ", botx
print "TopY: ", topy, "BotY: ", boty
print "TopZ: ", topz, "BotZ: ", botz

numof_points = 100000

mx_possible_r = 0.0
rmin = 0.0
dr = 0.5

pore_radius_list = []

deltaperc = 5.0 
reference = deltaperc

for i in range(numof_points):

  perc = 100.0 * float(i)/float(numof_points)
  if (perc >= reference):
    print perc , " % "
    reference += deltaperc

  px = random.uniform(botx, topx)
  py = random.uniform(boty, topy)
  pz = random.uniform(botz, topz) 
  
  poreradius = get_min_distance (scx, scy, scz, px, py, pz) - R

  if (poreradius > rmin):
    pore_radius_list.append(poreradius)

of = open("all_radius.txt", "w")

for r in pore_radius_list:
  data = str(r) + "\n"
  of.write(data)

of.close()

print "Done" 

# questa dopvrebbe essere la funzione "is easily
# compared with the cumulative pore volume curves often
# calculated in isotherm-based PSD methods" citata in
# Langmuir 1999, 15, 305-308
# ma soprattutto Langmuir 2006, 22, 7726-7731
vporer_dim = int(max(pore_radius_list) / dr) + 1
vporer = numpy.linspace(0.0, 0.0, vporer_dim)

print "Start vporer" 

# binning fatto a mano
for pore_radius in pore_radius_list:
  for i in range(vporer_dim):
    if (pore_radius >= (dr * i)) and (pore_radius < (dr * (i+1))):
      vporer[i] += 1

of = open("vporer.txt", "w")

for i in range(len(vporer)):
  x = (dr * (i+1) + dr * i) / 2.0
  data = str(x) + " " + str(vporer[i]) + "\n"
  of.write( data )

of.close()

print "Done"

print "Start psd"

# adesso la derivata
psd = numpy.linspace(0.0, 0.0, len(vporer)-1)
for i in range(len(vporer)-1):
  psd[i] = -1.0 * ((vporer[i+1]-vporer[i])/dr)

dof = open("psd.txt", "w")
for i in range(len(psd)):
  x = (dr * (i+1) + dr * i) / 2.0
  data = str(x) + " " + str(psd[i]) + "\n"
  dof.write(data)

dof.close()

print "Done"

print "Start vporer 2" 

vporer = numpy.linspace(0.0, 0.0, vporer_dim)

# binning fatto a mano
for pore_radius in pore_radius_list:
  for i in range(vporer_dim):
    if (pore_radius <= (dr * i)):
      vporer[i] += 1

of = open("vporer_2.txt", "w")

for i in range(len(vporer)):
  x = (dr * (i+1) + dr * i) / 2.0
  data = str(x) + " " + str(vporer[i]) + "\n"
  of.write( data )

of.close()

print "Done"

print "Start psd 2"

# adesso la derivata
psd = numpy.linspace(0.0, 0.0, len(vporer)-1)
for i in range(len(vporer)-1):
  psd[i] = -1.0 * ((vporer[i+1]-vporer[i])/dr)

dof = open("psd_2.txt", "w")
for i in range(len(psd)):
  x = (dr * (i+1) + dr * i) / 2.0
  data = str(x) + " " + str(psd[i]) + "\n"
  dof.write(data)

dof.close()

print "Done"

# calcolo l'R piu' alto possibile da usare poi per la 
# procedura descritta nell'introduzione di Langmuir 2006, 22, 7726-7731
# o meglio una variazione sul tema di quella li descritta
print "Bigger R : ", max(pore_radius_list)
