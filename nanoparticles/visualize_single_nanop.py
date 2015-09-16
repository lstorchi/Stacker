import sys
import vtk
import numpy

import random
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
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


for selected_index in range(0,1):
  nanop = nanoparticles[selected_index]
  renderer.AddActor(nanop.get_vtk_actor(True, 1.0))

  for p in nanop.inside_point_grid():
    renderer.AddActor(p.get_actor(0.1, rc = 1.0, gc = 0.0, bc = 0.0))
  renderer.AddActor(nanop.get_vtk_actor(opacity = 0.5))

renderer.SetBackground(255,255,255)

renWin.SetSize(1024, 768)

renWin.Render()
iren.Start()
