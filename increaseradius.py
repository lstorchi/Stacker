import sys

sys.path.append("./modules")

import util
import point
import sphere

filename = "final_config.txt"

perc = 0.1

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

spheres = []
zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0
R = -1.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    util.file_to_sphere_diffr_list(filename, spheres)

for s in spheres:
  c = s.get_center()

  data = str(c.get_x()) + " " + str(c.get_y()) + " " + \
      str(c.get_z()) + " " + \
      str(s.get_radius()+s.get_radius()*perc) 

  print data
