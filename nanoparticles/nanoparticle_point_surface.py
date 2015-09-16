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
nanoparticle.POINTINSURFACESTEP = 1.0

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

selected_index = 0
nanop = nanoparticles[selected_index]

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#renderer.AddActor(nanop.get_vtk_actor(True, 0.4))

for p in nanop.get_surface_points():
  renderer.AddActor(p.get_actor(r = 0.1, rc = 1.0, gc = 1.0, bc = 1.0))

renderer.SetBackground(0,0,0)

renWin.SetSize(1024, 768)

renWin.Render()
iren.Start()
