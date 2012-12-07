import sys
sys.path.append("./modules")

import point 
import sphere

import math
import numpy
import random
import common

#######################################################

def get_spheres_in_anchor(scx, scy, scz, radius, \
      anchor_botx, anchor_boty, anchor_botz, \
      anchor_topx, anchor_topy, anchor_topz):

  inner_spheres = []

  bools1 = (scx + radius) > anchor_botx
  bools2 = (scx - radius) < anchor_topx
  bools3 = (scy + radius) > anchor_boty
  bools4 = (scy - radius) < anchor_topy
  bools5 = (scz + radius) > anchor_botz
  bools6 = (scz - radius) < anchor_topz

  interior_indices, = numpy.where(bools1*bools2*bools3*\
      bools4*bools5*bools6)

  for i in interior_indices:
    c = point.point(scx[i], scy[i], scz[i])
    s = sphere.sphere(c, radius[i])

    inner_spheres.append(s)

  return inner_spheres

#######################################################

def get_porosity_in_anchor(inner_spheres, mc_points, \
      anchor_botx, anchor_boty, anchor_botz, \
      anchor_topx, anchor_topy, anchor_topz):

  porosity = 0.0
  point_inside = 0

  # ogni 1000 punti controllo quanto e' cambiata la porosita'
  to_check_np = 1000
  # dirrenza minima oltre la qule vado ancora avanti
  difference = 0.005

  counter = 0
  for i in range(1,mc_points):
    p1x = random.uniform(anchor_botx, anchor_topx)
    p1y = random.uniform(anchor_boty, anchor_topy)
    p1z = random.uniform(anchor_botz, anchor_topz)

    for s in inner_spheres:
      if (s.is_point_inside(p1x, p1y, p1z)):
        point_inside += 1
        break

    counter += 1

    if (counter == to_check_np):
      counter = 0
      actual_porosity = (float(i)-float(point_inside))/float(i)
      if (porosity == 0.0):
        porosity = actual_porosity
        print "      Actual porosity: ", actual_porosity
      else:
        diff = math.fabs(actual_porosity - porosity)
        print "      Actual porosity: ", actual_porosity , \
            " +/- ", diff
        if diff <= difference:
          return actual_porosity

  porosity = (float(mc_points)-float(point_inside))/float(mc_points)

  return porosity

#######################################################

def get_porosity_in_anchor_grid(inner_spheres, grid_points, \
      anchor_botx, anchor_boty, anchor_botz, \
      anchor_topx, anchor_topy, anchor_topz):

  porosity = 0.0

  dx = (anchor_topx - anchor_botx)/(grid_points+1) 
  dy = (anchor_topy - anchor_boty)/(grid_points+1)
  dz = (anchor_topz - anchor_botz)/(grid_points+1)

  point_inside = 0

  x = anchor_botx - dx
  for i in range(grid_points):
    y = anchor_boty - dy
    x += dx  
    for j in range(grid_points):
      z = anchor_botz - dz
      y += dy
      for k in range(grid_points):
        z += dz

        for s in inner_spheres:
          if (s.is_point_inside(x, y, z)):
            point_inside += 1
            break

  grid_points_3 = grid_points*grid_points*grid_points

  porosity = (float(grid_points_3)-float(point_inside))/float(grid_points_3)

  return porosity

#######################################################

filename = "final_config.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

file = open(filename, "r")

spheres = []

volume_of_sphere = 0.0
zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

for sp in file:
  x, y, z, r = sp.split(" ")
  center = point.point(float(x), float(y), float(z))
  s = sphere.sphere(center, float(r))
  spheres.append(s)

  volume_of_sphere += s.get_volume()

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

volume = (xmax-xmin) * (ymax-ymin) * (zmax-zmin)

print "TopX: ", xmax, "BotX: ", xmin
print "TopY: ", ymax, "BotY: ", ymin
print "TopZ: ", zmax, "BotZ: ", zmin

scx = numpy.linspace( 0.0, 0.0, len(spheres)) 
scy = numpy.linspace( 0.0, 0.0, len(spheres))
scz = numpy.linspace( 0.0, 0.0, len(spheres))
radius = numpy.linspace( 0.0, 0.0, len(spheres))

i = 0
for s in spheres:
  c = s.get_center()
  scx[i] = c.get_x()
  scy[i] = c.get_y()
  scz[i] = c.get_z()
  radius[i] = s.get_radius()
  i += 1

porosity = (volume-volume_of_sphere)/volume

print ""
print "Porosity estimation: ", porosity

file.close()

# lascio dai bordi uno spazio 2*R 
botx = xmin + (2 * common.MAXR)
boty = ymin + (2 * common.MAXR)
botz = zmin + (2 * common.MAXR)
topx = xmax - (2 * common.MAXR)
topy = ymax - (2 * common.MAXR)
topz = zmax - (2 * common.MAXR)

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error"
  exit()

# spessore del tasselamento 5*R
thickness = 5 * common.MAXR
# mi sposto in alto ogni volta di 2 * R
moveup = 2 * common.MAXR
# tassello da cui parto
anchor_botx = botx
anchor_boty = boty
anchor_botz = botz 
anchor_topx = topx
anchor_topy = topy
anchor_topz = anchor_botz + thickness

print ""

# numero massimo di punti da usare
mc_points_to_use = 5000

tp = 0.0

counter = 1
while anchor_topz < topz:

  print "Anchor : ", counter

  #seleziono le sfere che si trovano nel tassello attuale
  inner_spheres = get_spheres_in_anchor(scx, scy, scz, radius, \
      anchor_botx, anchor_boty, anchor_botz, \
      anchor_topx, anchor_topy, anchor_topz)

  print "  ", len(inner_spheres), " spheres inside"

  p = get_porosity_in_anchor(inner_spheres, mc_points_to_use, \
      anchor_botx, anchor_boty, anchor_botz, \
      anchor_topx, anchor_topy, anchor_topz)

  tp += p

  print "   Porosity in anchor: ", p

  counter += 1
  anchor_botz = anchor_botz + moveup
  anchor_topz = anchor_botz + thickness

print ""
print "Porosity MC: ", tp/(counter-1)

# tassello da cui parto
anchor_botx = botx
anchor_boty = boty
anchor_botz = botz 
anchor_topx = topx
anchor_topy = topy
anchor_topz = anchor_botz + thickness


#punti da usare per la griglia
grid_points = 20

tp = 0.0

counter = 1
while anchor_topz < topz:

  print "Anchor : ", counter

  #seleziono le sfere che si trovano nel tassello attuale
  inner_spheres = get_spheres_in_anchor(scx, scy, scz, radius, \
      anchor_botx, anchor_boty, anchor_botz, \
      anchor_topx, anchor_topy, anchor_topz)

  print "  ", len(inner_spheres), " spheres inside"

  p = get_porosity_in_anchor_grid(inner_spheres, grid_points, \
      anchor_botx, anchor_boty, anchor_botz, \
      anchor_topx, anchor_topy, anchor_topz)

  tp += p

  print "   Porosity in anchor: ", p

  counter += 1
  anchor_botz = anchor_botz + moveup
  anchor_topz = anchor_botz + thickness

print ""
print "Porosity Grid: ", tp/(counter-1)
