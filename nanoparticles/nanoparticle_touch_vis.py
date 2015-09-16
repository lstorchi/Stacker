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

selected_index = 0

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

nanaparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanaparticles) 

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

scx, scy, scz, radius = \
    nanoparticle.nanoparticle_list_to_arrays(nanaparticles)

nanop = nanaparticles[selected_index]

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

renderer.AddActor(nanop.get_vtk_actor(True, 0.4))

#for p in nanop.inside_point_grid():
#  renderer.AddActor(p.get_actor(0.1))

for i in nanoparticle.get_near_nanoparticles_index_to (0, \
    scx, scy, scz, radius):
  if (i != selected_index):
    #renderer.AddActor(nanaparticles[i].get_vtk_actor())
    if (nanop.nanoparticle_touch_me(nanaparticles[i])):
      renderer.AddActor(nanaparticles[i].get_vtk_actor())

#cx, cy, cz = nanop.get_center()
#r = nanop.get_max_sphere()
#p = point.point(cx, cy, cz)
#s = sphere.sphere(p, r)
#renderer.AddActor(s.get_actor(0.5))

renderer.SetBackground(0,0,0)

renWin.SetSize(1024, 768)

renWin.Render()
iren.Start()
