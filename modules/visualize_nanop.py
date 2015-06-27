import sys
import vtk

import random
import math

import nanoparticle
import sphere
import point
import util
import cube


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

  for nanop in nanoparticles: 

    renderer.AddActor(nanop.get_vtk_actor(color=True,opacity=1.0))
 
  ipp = point.point(x, y, z)
  renderer.AddActor(ipp.get_actor(1.0))

  renWin.Render()
  iren.Start()

def visualize_nanoparticle_and_actor (nanoparticles, ac):

  nanoparticle.POINTINSIDEDIM = 0

  camera = vtk.vtkCamera()
  camera.SetPosition(1,1,1)
  camera.SetFocalPoint(0,0,0)

  renderer = vtk.vtkRenderer()
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(renderer)

  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)

  for nanop in nanoparticles: 

    renderer.AddActor(nanop.get_vtk_actor(color=True,opacity=1.0))
 
  renderer.AddActor(ac)

  renWin.Render()
  iren.Start()
