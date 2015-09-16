import sys
sys.path.append("../modules")

from point import *
from sphere import *
from circle import *

import math
import sys

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

filename = "final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

file = open(filename, "r")

spheres = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

for sp in file:
  x, y, z, r = sp.split(" ")
  r = 1.0
  center = point(float(x), float(y), float(z))
  s = sphere(center, float(r))
  spheres.append(s)

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

print "xmax: ", xmax, "xmin: ",xmin, "ymax: ", ymax, \
    "ymin: ", ymin, "zmax: ", zmax, "zmin: ", zmin

file.close()

# il piano deve essere tra zmin e zmax 
# equazione del piano

zplane = 110.0

np = 50
ns = 1

spheres_in_plane = []

for s in spheres:

  r = s.get_radius()
  c = s.get_center()

  cx = c.get_x()
  cy = c.get_y()
  cz = c.get_z()

  if (zplane >= (cz - r)) and (zplane <= (cz + r)):
    spheres_in_plane.append(s)

dt = (2.0 * math.pi)/(np)

for s in spheres_in_plane:
  r = s.get_radius()
  c = s.get_center()

  cx = c.get_x()
  cy = c.get_y()
  cz = c.get_z()

  circler = math.sqrt(math.pow(r, 2) - math.pow((zplane-cz),2))

  cir = circle(cx, cy, circler)
  ren.AddActor(cir.get_actor(zplane))

  t = 0.0
 
  for i in range(1,np):
 
    t = t + dt
 
    x = cx + circler * math.cos(t)
    y = cy + circler * math.sin(t)
    print x, y
    sys.stdout.flush()

sys.stdout.flush()

zplane = 115.0

np = 50
ns = 1

spheres_in_plane = []

for s in spheres:

  r = s.get_radius()
  c = s.get_center()

  cx = c.get_x()
  cy = c.get_y()
  cz = c.get_z()

  if (zplane >= (cz - r)) and (zplane <= (cz + r)):
    spheres_in_plane.append(s)

dt = (2.0 * math.pi)/(np)

for s in spheres_in_plane:
  r = s.get_radius()
  c = s.get_center()

  cx = c.get_x()
  cy = c.get_y()
  cz = c.get_z()

  circler = math.sqrt(math.pow(r, 2) - math.pow((zplane-cz),2))

  cir = circle(cx, cy, circler)
  ren.AddActor(cir.get_actor(zplane))

  t = 0.0
 
  for i in range(1,np):
 
    t = t + dt
 
    x = cx + circler * math.cos(t)
    y = cy + circler * math.sin(t)
    print x, y
    sys.stdout.flush()

sys.stdout.flush()



ren.SetBackground(0,0,0)
renWin.SetSize(1024, 768)
renWin.Render()

renderLarge = vtk.vtkRenderLargeImage()
renderLarge.SetInput(ren)
renderLarge.SetMagnification(4)

writer = vtk.vtkTIFFWriter()
writer.SetInputConnection (renderLarge.GetOutputPort())
writer.SetFileName("largeImage.tif")
writer.Write()

iren.Start()
