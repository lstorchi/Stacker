import sys
import vtk
import re

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

#####################################################################

def get_color (atom):

  if (atom == 'O'):
    return 0.0, 0.0, 1.0
  elif (atom == 'Ti'):
    return 1.0, 0.0, 0.0

  return 0.0, 0.0, 0.0

#####################################################################



filename = "nanoparticle_final_config.txt"
xyzfile = "test.xyz"

if (len(sys.argv)) == 3:
  filename = sys.argv[1]
  xyzfile = sys.argv[2]
else:
    print "usage: ", sys.argv[0], " nanofname.txt xyzfname.xyz"
    exit(1)

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

print minbox_x, minbox_y, minbox_z, maxbox_x, maxbox_y, maxbox_z

# in A
radius = {'O':0.60, 'Ti':1.40}

filep = open(xyzfile, "r")

filep.readline()
filep.readline()

actors = []
xlist = []
ylist = []
zlist = []

for line in filep:
  p = re.compile(r'\s+')
  line = p.sub(' ', line)
  line = line.lstrip()
  line = line.rstrip()

  plist =  line.split(" ")

  if (len(plist) == 4):
   atomname = plist[0]
   x = plist[1]
   y = plist[2]
   z = plist[3]

   xlist.append(float(x))
   ylist.append(float(y))
   zlist.append(float(z))

   if atomname in radius:
     print atomname, " has ", radius[atomname], x, y, z

     source = vtk.vtkSphereSource()
     source.SetCenter(float(x),float(y),float(z))
     source.SetRadius(radius[atomname])

     mapper = vtk.vtkPolyDataMapper()
     if vtk.VTK_MAJOR_VERSION <= 5:
       mapper.SetInput(source.GetOutput())
     else:
       mapper.SetInputConnection(source.GetOutputPort())
                 
     actor = vtk.vtkActor()
     actor.SetMapper(mapper)
     actor.GetProperty().SetColor(get_color(atomname)); #(R,G,B)
     actors.append(actor)

filep.close()

for a in actors:
  renderer.AddActor(a)

renderLarge = vtk.vtkRenderLargeImage()
renderLarge.SetInput(renderer)
renderLarge.SetMagnification(4)

writer = vtk.vtkTIFFWriter()
writer.SetInputConnection (renderLarge.GetOutputPort())
writer.SetFileName("largeImage.tif")
writer.Write()

renWin.Render()
iren.Start()
