import sys
import vtk

import random
import math

sys.path.append("../modules")

import nanoparticle
import sphere
import point
import util
import cube

# init 

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

camera = vtk.vtkCamera()
camera.SetPosition(1,1,1)
camera.SetFocalPoint(0,0,0)

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

filename = "nanoparticle_final_config.txt"
xyzfile = "test.xyz"

if (len(sys.argv)) == 3:
  filename = sys.argv[1]
  xyzfile = sys.argv[2]

nanaparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanaparticles) 

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

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

  print nanop.get_surface()

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


# rendi

# visualizza se necessario la sfera

usesphere = False

if usesphere :
  sphere = vtk.vtkSphereSource()
  sphere.SetCenter(0, 0, 0)
  sphere.SetRadius(float(9.5))
  sphere.SetThetaResolution(10)
  sphere.SetPhiResolution(10)
 
  spheremapper = vtk.vtkPolyDataMapper()
  #spheremapper.SetInput(sphere.GetOutput())
  spheremapper.SetInputConnection(sphere.GetOutputPort())

     
  sphereactor = vtk.vtkActor()
  sphereactor.SetMapper(spheremapper)
  sphereactor.GetProperty().SetOpacity(1)
 
  renderer.AddActor(sphereactor)

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

writer = vtk.vtkTIFFWriter()
writer.SetInputConnection (renderLarge.GetOutputPort())
writer.SetFileName("largeImage.tif")
writer.Write()

print minbox_x, minbox_y, minbox_z, maxbox_x, maxbox_y, maxbox_z

renWin.Render()
iren.Start()
