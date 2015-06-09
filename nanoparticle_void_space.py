from __future__ import print_function

import sys
import vtk

import numpy 

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

print ('Box limits: '+str(minbox_x)+' '+str(maxbox_x)+ \
    ' '+str(minbox_y)+' '+str(maxbox_y)+ \
    ' '+ str(minbox_z)+' '+str(maxbox_z)+'\n')

r = 0.0
for nanop in nanoparticles:
  r += nanop.get_max_sphere()

mead_d = 2.0 * (r/float(len(nanoparticles)))

print ('Mean D: '+str(mead_d)+'\n')

px = minbox_x+3.0*mead_d
py = minbox_y+3.0*mead_d
pz = minbox_z+3.0*mead_d

# seleziono solo le nanoparticelle con il centro dentro la box visto che poi 
# dal calcolo della psd escludo comunque i punti ai bordi della box

box_botx = px
box_topx = px + 6.0*mead_d
box_boty = py
box_topy = py + 6.0*mead_d
box_botz = pz
box_topz = pz + 6.0*mead_d

print ('Selected Box limits: '+str(box_botx)+' '+str(box_topx)+ \
    ' '+str(box_boty)+' '+str(box_topy)+ \
    ' '+str(box_botz)+' '+str(box_topz)+'\n')

nanopscx, nanopscy, nanopscz = \
        nanoparticle.nanoparticle_to_arrays (nanoparticles)

bools1 = (nanopscx >= box_botx)
bools2 = (nanopscy >= box_boty)
bools3 = (nanopscz >= box_botz)

bools4 = (nanopscx <= box_topx)
bools5 = (nanopscy <= box_topy)
bools6 = (nanopscz <= box_topz)

interior_indices, = numpy.where(bools1*bools2*bools3*bools4*bools5*bools6)

selected_nanoparticles = []

filetoprint = open("selected_nanop.txt", "w")

for id in interior_indices:
  selected_nanoparticles.append(nanoparticles[id])

  cx, cy, cz, A, B, H, p2x, p2y, p2z, tetha = \
      nanoparticles[id].get_to_print()

  data = str(cx) + " " + \
         str(cy) + " " + \
         str(cz) + " " + \
         str(A) + " " + \
         str(B) + " " + \
         str(H) + " " + \
         str(p2x) + " " + \
         str(p2y) + " " + \
         str(p2z) + " " + \
         str(tetha) + "\n"

  filetoprint.write(data)

filetoprint.close()

vfile = open("void.txt", "w")

numof = 60

# vedo solo la parte interna ovviamente
box_botx = box_botx+mead_d
box_topx = box_topx-mead_d
box_boty = box_boty+mead_d
box_topy = box_topy-mead_d
box_botz = box_botz+mead_d
box_topz = box_topz-mead_d

box_botx = box_botx+mead_d
box_topx = box_botx+1.5*mead_d

box_boty = box_boty+mead_d
box_topy = box_boty+1.5*mead_d

box_botz = box_botz+mead_d
box_topz = box_botz+1.5*mead_d


print ('Box looking for void limits: '+\
       str(box_botx)+' '+str(box_topx)+ \
    ' '+str(box_boty)+' '+str(box_topy)+ \
    ' '+str(box_botz)+' '+str(box_topz)+'\n')

dx = (box_topx - box_botx)/(numof+1) 
dy = (box_topy - box_boty)/(numof+1)
dz = (box_topz - box_botz)/(numof+1)

print ('Deltas: '+str(dx)+' '+str(dy)+' '+str(dz))

point_in_the_void = 0
counter = 0
px = box_botx - dx
for i in range(numof):
  py = box_boty - dy
  px += dx  
  for j in range(numof):
    pz = box_botz - dz
    py += dy
    for k in range(numof):
      pz += dz
      counter = counter + 1

      if (is_in_the_void_nanoparticle(selected_nanoparticles, \
            px, py, pz)):
        line = str(px) + " " + str(py) + " " + str(pz) + " 0.50\n"
        vfile.write(line)
        point_in_the_void = point_in_the_void + 1

      print(str(100.0*(float(counter)/float(numof*numof*numof))) \
          +' % ', end='\r')

print ('Perc in the void: '+ \
    str(100.0*float(point_in_the_void)/(float(numof*numof*numof))))

print "Now work using direcly perovskite"



vfile.close()
