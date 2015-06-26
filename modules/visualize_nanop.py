import sys
import vtk

import random
import math

import nanoparticle
import sphere
import point
import util
import cube

# init 

def visualize_nanoparticle_and_point (nanoparticles, x, y, z):

  nanoparticle.POINTINSIDEDIM = 0

  camera = vtk.vtkCamera()
  camera.SetPosition(1,1,1)
  camera.SetFocalPoint(0,0,0)

  renderer = vtk.vtkRenderer()
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(renderer)

  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)

  minbox_x = 100000.0 
  maxbox_x =-100000.0 
  minbox_y = 100000.0
  maxbox_y =-100000.0
  minbox_z = 100000.0
  maxbox_z =-100000.0

  for nanop in nanoparticles: 

    renderer.AddActor(nanop.get_vtk_actor(color=True,opacity=1.0))
 
  ipp = point.point(x, y, z)
  renderer.AddActor(ipp.get_actor(1.0))

  renWin.Render()
  iren.Start()
