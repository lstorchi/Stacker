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
import line

# init 

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

filename = "nanoparticle_final_config.txt"
xyzfile = "test.xyz"

if (len(sys.argv)) == 3:
  filename = sys.argv[1]
  xyzfile = sys.argv[2]
else:
    print "usage: ", sys.argv[0], " nanofname.txt xyzfname.xyz"
    exit(1)

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles) 

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

minbox_x = 100000.0 
maxbox_x =-100000.0 
minbox_y = 100000.0
maxbox_y =-100000.0
minbox_z = 100000.0
maxbox_z =-100000.0

if len(nanoparticles) != 2:
    print "Error "
    exit(1)

p1top, p1bottom = nanoparticles[0].get_ptop_and_bottom ()
p2top, p2bottom = nanoparticles[1].get_ptop_and_bottom ()

l3d = line.line3d()
angle = l3d.get_angle_two_line(p1top, p1bottom, p2top, p2bottom)

print angle
