from __future__ import print_function

import sys
import vtk

import random
import math

sys.path.append("./modules")

import nanoparticle
import sphere
import point
import util
import cube

###############################################################################

def is_in_the_void_nanoparticle(nanoparticles, px, py, pz):

  for nanop in nanoparticles: 
    if (nanop.is_point_inside ([px, py, pz])):
      return False

  return True

###############################################################################

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles) 

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print ('Error Invalid BOX\n')
  exit()

# nanoparticle

minbox_x = 100000.0 
maxbox_x =-100000.0 
minbox_y = 100000.0
maxbox_y =-100000.0
minbox_z = 100000.0
maxbox_z =-100000.0

for nanop in nanoparticles: 
  cx, cy, cz = nanop.get_center()
  A, B, H = nanop.get_dimensions()

  dm = max(H, B, A) / 2.0

  if (maxbox_x < (cx + dm)):
    maxbox_x = (cx + dm)
  if (maxbox_y < (cy + dm)):
    maxbox_y = (cy + dm)
  if (maxbox_z < (cz + dm)):
    maxbox_z = (cz + dm)
  
  if (minbox_x > (cx - dm)):
    minbox_x = (cx - dm)
  if (minbox_y > (cy - dm)):
    minbox_y = (cy - dm)
  if (minbox_z > (cz - dm)):
    minbox_z = (cz - dm)

print ('Box limits: '+str(minbox_x)+' '+str(minbox_y)+ \
    ' '+str(minbox_z)+' '+str(maxbox_x)+' '+ \
    str(maxbox_y)+' '+str(maxbox_z)+'\n')

vfile = open("void.txt", "w")

numof = 500

dx = (maxbox_x - minbox_x)/(numof+1) 
dy = (maxbox_y - minbox_y)/(numof+1)
dz = (maxbox_z - minbox_z)/(numof+1)

counter = 0
px = botx - dx
for i in range(numof):
  py = boty - dy
  px += dx  
  for j in range(numof):
    pz = botz - dz
    py += dy
    for k in range(numof):
      pz += dz
      counter = counter + 1

      if (is_in_the_void_nanoparticle(nanoparticles, \
            px, py, pz)):
        line = str(px) + " " + str(py) + " " + str(pz) + " 0.50\n"
        vfile.write(line)

      print(100.0*(float(counter)/float(numof*numof*numof))+' % done!', end='\r')

vflie.close()
