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

  for nanop in nanaparticles: 

    x = nanop.get_edge_points()
    pts = nanop.get_points_connection()
    renderer.AddActor(nanop.get_vtk_actor(color=True,opacity=1.0))
    #renderer.AddActor(nanop.get_vtk_actor())
 
    cx, cy, cz = nanop.get_center()
    A, B, H = nanop.get_dimensions()
 
    dm = max(H, B, A) / 2.0
 
    if (maxbox_x < (cx + dm)):
      maxbox_x = (cx + dm)
    if (maxbox_y < (cy + dm)):
      maxbox_y = (cy + dm)
    if (maxbox_z < (cz + dm)):
      maxbox_z = (cz + dm)
    
    if (minbox_x > (cx - dm)):
      minbox_x = (cx - dm)
    if (minbox_y > (cy - dm)):
      minbox_y = (cy - dm)
    if (minbox_z > (cz - dm)):
      minbox_z = (cz - dm)
    
  ipp = point.point(x, y, z)
  render.AddActor(ipp.get_actor(0.5)

  cube_actors = cube.cube_to_actors(minbox_x, minbox_y, minbox_z, \
      maxbox_x, maxbox_y, maxbox_z, 1.0, 1.0, 1.0)

  for a in cube_actors:
    renderer.AddActor(a)

  renderer.SetActiveCamera(camera)
  renderer.ResetCamera()
  renderer.SetBackground(0,0,0)

  renWin.SetSize(1024, 768)

  renderLarge = vtk.vtkRenderLargeImage()
  renderLarge.SetInput(renderer)
  renderLarge.SetMagnification(4)

  renWin.Render()
  iren.Start()
