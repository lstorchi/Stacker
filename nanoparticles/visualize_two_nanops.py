import sys
import vtk
import numpy

import random
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
import line
import util
import cube

# init 

nanoparticle.POINTINSIDEDIM = 0

selected_index = 0

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles) 

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

scx, scy, scz, radius = \
    nanoparticle.nanoparticle_list_to_arrays(nanoparticles)

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ptop1 = point.point (0, 0, 0)
ptop2 = point.point (0, 0, 0)

pbottom1 = point.point (0, 0, 0)
pbottom2 = point.point (0, 0, 0)

for selected_index in range(0,2):
  nanop = nanoparticles[selected_index]
  renderer.AddActor(nanop.get_vtk_actor(True, 1.0))

  for p in nanop.inside_point_grid():
    renderer.AddActor(p.get_actor(0.1, rc = 1.0, gc = 0.0, bc = 0.0))
  renderer.AddActor(nanop.get_vtk_actor(opacity = 0.5))
  p1, p2 = nanop.get_ptop_and_bottom ()
  if (selected_index == 0):
      ptop1 = p1
      pbottom1 = p2
  elif (selected_index == 1):
      ptop2 = p1
      pbottom2 = p2

  renderer.AddActor(p1.get_actor(1.0, 1.0, 0.0, 0.0))
  renderer.AddActor(p2.get_actor(1.0, 1.0, 0.0, 0.0))

l3d = line.line3d()
print l3d.get_angle_two_line(ptop1, pbottom1, ptop2, pbottom2)

renderer.SetBackground(255,255,255)

renWin.SetSize(1024, 768)

renWin.Render()
iren.Start()
