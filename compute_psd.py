import re
import sys
import vtk
import time

sys.path.append("./modules")

import util
import point
import sphere

import math
import numpy
import random

filename = "pore_radius_list.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

file = open(filename, "r")

spheres = []

contatore = 1
for sp in file:
  x, y, z, cx, cy, cz, r = sp.split(" ")

  center = point.point(float(cx), float(cy), float(cz))
  s = sphere.sphere(center, float(r))
  spheres.append(s)

  print "line: ", contatore
  contatore = contatore + 1

file.close()

scx, scy, scz, radius = util.sphere_to_arrays (spheres)

botx = min(scx)
boty = min(scy)
botz = min(scz)
topx = max(scx)
topy = max(scy)
topz = max(scz)

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

lx = topx-botx
ly = topy-boty
lz = topz-botz

print ""
print "Lattice dimension"
print "lX: ", lx, "lY: ", ly, "lZ: ", lz

radius_of_test_molecule = 0.17045
RES_PSD = 1.0 / 0.5
hist_count = int(round (max (max (lx, ly), lz) * RES_PSD)) + 1
PSD_hist = numpy.linspace(0.0, 0.0, hist_count)

max_cumm = 0.0

for s in spheres:
  r = s.get_radius()

  if (r > radius_of_test_molecule):
    for p in range(int(r * RES_PSD) + 2):
      if (p >= hist_count):
        print "Problem when computing histogram"
        exit(-1)

      PSD_hist[p] += 1.0
      if (PSD_hist[p] > max_cumm):
        max_cumm = PSD_hist[p]

# come noto -dH(D)/dD  e' il PSD 
dHD = -1.0 * numpy.diff(PSD_hist)/2.0
dD = numpy.linspace(0.0, float(len(dHD)-1)/RES_PSD, len(dHD))

# normalizzo
dHD = dHD/max(dHD)

max_reached = 0
for i in range(len(PSD_hist)):
  if (PSD_hist[i] == 0.0):
    max_reached = i + 5
    break

diff_histf = open("psd_diff_compute.txt", "w")
for i in range(min(max_reached, len(dHD))):
  data = "%f %f\n" % (dD[i], dHD[i])
  diff_histf.write(data)
diff_histf.close()

histof = open("psd_cumm_compute.txt", "w")
for i in range(min(max_reached, len(PSD_hist))):
  data = "%f %f\n" % (float(i) / RES_PSD, PSD_hist[i] / max_cumm)
  histof.write(data)
histof.close()

"""
# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

for s in spheres:
  ren.AddActor(s.get_actor())

# enable user interface interactor
try:
  iren.Initialize()
  renWin.Render()
  iren.Start()
except Exception as e:
  print e
"""
