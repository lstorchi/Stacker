import math
import time

import sys
sys.path.append("../modules")

import point
import sphere
import common
import generate_random_dim

spheres = []
#generate_random_spheres (spheres)

outfile = open("actual_config.txt", "wa")

# 10% piu' piu' grande di quello necessario ad avere sfere dello stesso volume
Radius = float(28.909/1.90602)
common.botx = 0.0 
common.topx = 500.0
common.boty = 0.0 
common.topy = 500.0
common.botz = 0.0 
common.topz = 500.0

z = common.botz
while (z < common.topz):
#for numof in range(1,1200):
  z = generate_random_dim.generate_compact_configuration_fixed_r(Radius, spheres)
  print "Dropped " , len(spheres), " spheres z: ", z

  s = spheres[len(spheres)-1]
  c = s.get_center()

  data = str(c.get_x()) + " " + str(c.get_y()) + " " + \
      str(c.get_z()) + " " + str(s.get_radius()) + "\n"

  outfile.write(data)
  outfile.flush()


outfile.close()


outfile = open("final_config.txt", "w")

zmax = common.botz - 1.0
for s in spheres:
  c = s.get_center()
  if zmax < c.get_z():
    zmax = c.get_z()

  data = str(c.get_x()) + " " + str(c.get_y()) + " " + \
      str(c.get_z()) + " " + str(s.get_radius()) + "\n"

  outfile.write(data)

outfile.close()

volume = (common.topx-common.botx) * (common.topy-common.boty) * (zmax-common.botz)
spheres_volume = spheres[0].get_volume() * len(spheres)
print "Porosity: " , (volume-spheres_volume)/volume
