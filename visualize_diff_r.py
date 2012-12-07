import vtk
import sys

import sys
sys.path.append("./modules")

from cube import *
from point import * 
from sphere import *

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

filename = "final_config.txt"
read_cube = False

if (len(sys.argv)) == 2:
  filename = sys.argv[1]
elif (len(sys.argv)) == 8:
  filename = sys.argv[1]
  read_cube = True

# parto dal presupposto che hanno lo stesso raggio
file = open(filename, "r")

spheres = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

for sp in file:
  x, y, z, r = sp.split(" ")
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

file.close()

sources = []

# add cube
sources = []

if read_cube:
  rxmin = float(sys.argv[2])
  rymin = float(sys.argv[3])
  rzmin = float(sys.argv[4])
  rxmax = float(sys.argv[5])
  rymax = float(sys.argv[6])
  rzmax = float(sys.argv[7])

  addcube_to_source (sources, rxmin, rymin, rzmin, \
     rxmax, rymax, rzmax)
else:
  addcube_to_source (sources, xmin, ymin, zmin, \
     xmax, ymax, zmax)

for s in spheres:
  c = s.get_center()
  r = s.get_radius()
  source = vtk.vtkSphereSource()
  source.SetCenter(c.get_x(), c.get_y(), c.get_z())
  source.SetRadius(r)

  sources.append(source)

# mapper
mappers = []

for source in sources:
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInput(source.GetOutput())
  
  mappers.append(mapper)

# actor
actors = []

for mapper in mappers:
  actor = vtk.vtkActor()
  #actor.GetProperty().SetOpacity(0.5)
  actor.SetMapper(mapper)

  actors.append(actor);
 
# assign actor to the renderer

for actor in actors:
  ren.AddActor(actor)

# enable user interface interactor
try:
  iren.Initialize()
  renWin.Render()
  iren.Start()
except Exception as e:
  print e
