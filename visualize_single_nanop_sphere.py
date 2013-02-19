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

# init 

nanoparticle.POINTINSIDEDIM = 0

selected_index = 0

filename = "nanoparticle_final_config.txt"
sfilename = "final_config.txt"

if (len(sys.argv)) == 3:
  filename = sys.argv[1]
  sfilename = sys.argv[2]

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles) 

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

spheres = []

botx, topx, boty, topy, botz, topz = \
    util.file_to_sphere_diffr_list(sfilename, spheres) 

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

for selected_index in range(0,1):
  nanop = nanoparticles[selected_index]
  renderer.AddActor(nanop.get_vtk_actor(True, 1.0))

  s = spheres[selected_index]
  renderer.AddActor(s.get_actor(0.8))

renderer.SetBackground(0,0,0)

renWin.SetSize(1024, 768)

renWin.Render()
iren.Start()
