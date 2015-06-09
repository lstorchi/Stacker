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

LUNCUBE = 0.633

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#print ("Now work using direcly perovskite")

botx = 0.0
boty = 0.0
botz = 0.0

topx = LUNCUBE * 10
topy = LUNCUBE * 10
topz = LUNCUBE * 10

sources = []

cube.addcube_to_source (sources, botx, boty, botz, \
   topx, topy, topy)


nomofx = int((topx - botx) / LUNCUBE) + 1
nomofy = int((topy - boty) / LUNCUBE) + 1
nomofz = int((topz - botz) / LUNCUBE) + 1

lines = []

x = botx
for i in range(0,nomofx):
  y = boty
  for j in range(0,nomofy):
    z = botz
    for a in range(0,nomofz):
      source = vtk.vtkSphereSource()
      source.SetCenter(x, y, z)
      source.SetRadius(0.175)

      sources.append(source)

      lines.append("Pb  "+str(x*10.0) + " " + str (y*10.0) + " " + \
          str(z*10.0))

      if (j < (nomofy-1)):
        source = vtk.vtkSphereSource()
        source.SetCenter(x, y+(LUNCUBE/2.0), z)
        source.SetRadius(0.133)

        sources.append(source)

        lines.append(" I  "+str(x*10.0) + " " + \
            str ((y+(LUNCUBE/2.0))*10.0) + " " + \
            str(z*10.0))

      if (i < (nomofx-1)):
        source = vtk.vtkSphereSource()
        source.SetCenter(x+(LUNCUBE/2.0), y, z)
        source.SetRadius(0.133)
        sources.append(source)

        lines.append(" I  "+str((x+(LUNCUBE/2.0))*10.0) + " " + \
            str (y*10.0) + " " + \
            str(z*10.0))

      if (a < (nomofz-1)):
        source = vtk.vtkSphereSource()
        source.SetCenter(x, y, z+(LUNCUBE/2.0))
        source.SetRadius(0.133)
        sources.append(source)

        lines.append(" I  "+str(x*10.0) + " " + str (y*10.0) + " " + \
            str((z+(LUNCUBE/2.0))*10.0))

      if ((j < (nomofy-1)) and (i < (nomofx-1)) and (a < (nomofz-1))):

        source = vtk.vtkSphereSource()
        source.SetCenter(x+(LUNCUBE/2.0), y+(LUNCUBE/2.0), z+(LUNCUBE/2.0))
        source.SetRadius(0.265)
        sources.append(source)

        lines.append("Cs  "+str((x+(LUNCUBE/2.0))*10.0) + " " + \
            str((y+(LUNCUBE/2.0))*10.0) + " " + \
            str((z+(LUNCUBE/2.0))*10.0))


      z = z + LUNCUBE
    y = y + LUNCUBE
  x = x + LUNCUBE

print(str(len(lines)))
print (" ")
for l in lines:
  print (l)

# mapper
mappers = []

for source in sources:
  mapper = vtk.vtkPolyDataMapper()
  #mapper.SetInput(source.GetOutput())
  mapper.SetInputConnection(source.GetOutputPort())
  
  mappers.append(mapper)

# actor
actors = []

for mapper in mappers:
  actor = vtk.vtkActor()
  actor.GetProperty().SetOpacity(0.5)
  actor.SetMapper(mapper)

  actors.append(actor);
 
# assign actor to the renderer

for actor in actors:
  ren.AddActor(actor)

# enable user interface interactor
try:
  iren.Initialize()
  renWin.Render()
  #writer = vtk.vtkGL2PSExporter()
  #writer.SetRenderWindow(renWin)
  #writer.SetFileFormatToSVG ()
  #writer.SetFilePrefix("largeImage")
  #writer.Write()
  iren.Start()
except Exception as e:
  print (e)
