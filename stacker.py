import math
import time

import sys
sys.path.append("../modules")

import util
import point
import sphere
import common
import generate

spheres = []
#generate_random_spheres (spheres)

outfile = open("actual_config.txt", "wa")

z = common.botz
while (z < common.topz):
#for numof in range(1,1200):
  z = generate.generate_compact_configuration(spheres)
  print "Dropped " , len(spheres), " spheres z: ", z

  s = spheres[len(spheres)-1]
  c = s.get_center()

  data = str(c.get_x()) + " " + str(c.get_y()) + " " + \
      str(c.get_z()) + " " + str(s.get_radius()) + "\n"

  outfile.write(data)
  outfile.flush()


outfile.close()


# aggiungiamo qualche sfera in cima
# primo parametro e' il numero massimo di sfere con cui provare 
# a riempire il top della scatola
if (common.to_fill_the_top):
  generate.fill_the_top(common.sphere_to_fill_the_top, spheres)

# adesso potrei provare a muovere a destra o sinistra le sfere che non toccano
# nessun'altra sfera e poi provare ad abbassssare tutto le altre e cosi' via

# aumento il raggio delle sfere di un certo valore

if common.increase_radius:
  for i in range(0,len(spheres)):
    spheres[i].set_radius(R+(R*common.perc_aug))

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
