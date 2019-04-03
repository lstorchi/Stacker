import sys

import random
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
import util
import cube

# init 

BOXDIM = 100.0

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

nanaparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanaparticles) 

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

boxcentex = (topx - botx) / 2.0
boxcentey = (topy - boty) / 2.0
boxcentez = (topz - botz) / 2.0

minx = boxcentex - BOXDIM/2.0
maxx = boxcentex + BOXDIM/2.0

miny = boxcentey - BOXDIM/2.0
maxy = boxcentey + BOXDIM/2.0

minz = boxcentez - BOXDIM/2.0
maxz = boxcentez + BOXDIM/2.0

minbox_x = 100000.0 
maxbox_x =-100000.0 
minbox_y = 100000.0
maxbox_y =-100000.0
minbox_z = 100000.0
maxbox_z =-100000.0

for np in nanaparticles:
    cx, cy, cz = np.get_center()

    if cx >= minx and cx <= maxx:
        if cy >= miny and cy <= maxy:
            if cz >= minz and cz <= maxz:

                A, B, H = np.get_dimensions()
                p2 = np.get_p2()
                tetha = np.get_theta()

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

                print cx, cy, cz, A, B, H, p2.get_x(), \
                        p2.get_y(), p2.get_z(), tetha 



#print minbox_x, maxbox_x
#print minbox_y, maxbox_y
print minbox_z, maxbox_z
