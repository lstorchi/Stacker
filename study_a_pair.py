import sys
import vtk

import random
import math

sys.path.append("./modules")

import nanoparticle
import sphere
import point
import util
import cube

# init 

camera = vtk.vtkCamera()
camera.SetPosition(1,1,1)
camera.SetFocalPoint(0,0,0)

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

filename = "nano_final_config.txt"

selected_nanaop = 1

if (len(sys.argv)) >= 2:
  filename = sys.argv[1]
  if (len(sys.argv) == 3):
    selected_nanaop = int(sys.argv[2])

selected_nanaop = selected_nanaop - 1

nanoparticles = []
zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles) 

dmax = -1.0
for n in nanoparticles:
  d = n.get_max_sphere()
  if (d > dmax):
    dmax = d

scx, scy, scz = nanoparticle.nanoparticle_to_arrays (nanoparticles)

botx = min(scx)
boty = min(scy)
botz = min(scz)
topx = max(scx)
topy = max(scy)
topz = max(scz)

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print "Error Invalid BOX"
  exit()

if (selected_nanaop >= len(scx)):
  print "error invalid particle selected "
  exit()

dist = dmax * 2.2
selected, distance = nanoparticle.get_near_nanoparticle(nanoparticles, \
    scx[selected_nanaop], scy[selected_nanaop], \
    scz[selected_nanaop], dist)

minbox_x = 100000.0 
maxbox_x =-100000.0 
minbox_y = 100000.0
maxbox_y =-100000.0
minbox_z = 100000.0
maxbox_z =-100000.0

i = 0
for nanop in selected: 
  cx, cy, cz = nanop.get_center()
  A, B, H = nanop.get_dimensions()

  #nanop.is_point_inside([cx, cy, cz+0.5])

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

  print "Volume: " , nanop.get_volume() 
  print "Volume of sphere: ", sphere.sphere(point.point(), \
      nanop.get_max_sphere()).get_volume()

  if distance[i] == 0.0:
    selected_index = i  

  renderer.AddActor(nanop.get_vtk_actor((distance[i] == 0.0), 0.8))

  i += 1

# per vedere la box
cube_actors = cube.cube_to_actors(minbox_x, minbox_y, minbox_z, \
    maxbox_x, maxbox_y, maxbox_z)
for a in cube_actors:
  renderer.AddActor(a)

#print minbox_x, maxbox_x, minbox_y, maxbox_y, minbox_z, maxbox_z

# adesso creo una griglia e determino i punti sovrapposti
# ma lo faccio usando come box il paralleloepipedo che inscrive la
# nanorpaticella centrale
nanop = selected[selected_index]

cx, cy, cz = nanop.get_center()
A, B, H = nanop.get_dimensions()
dm = max(B, A, H)/2.0

maxbox_x = cx + dm
minbox_x = cx - dm
maxbox_y = cy + dm
minbox_y = cy - dm
maxbox_z = cz + dm
minbox_z = cz - dm

cube_actors = cube.cube_to_actors(minbox_x, minbox_y, minbox_z, \
    maxbox_x, maxbox_y, maxbox_z, 1.0, 0.0, 0.0)
for a in cube_actors:
  renderer.AddActor(a)


insidepoint = 0
totpoint = 0
numofp = 30
dx = (maxbox_x - minbox_x) / (numofp + 1)
dy = (maxbox_y - minbox_y) / (numofp + 1)
dz = (maxbox_z - minbox_z) / (numofp + 1)
for i in range(numofp):
  x = minbox_x + (i * dx)
  for j in range(numofp):
    y = minbox_y + (j * dy)
    for k in range(numofp):
      z = minbox_z + (k * dz)

      if nanop.is_point_inside([x, y, z]):
        for a in  range(len(selected)):
          if (a != selected_index):
            other_particle = selected[a]
            if other_particle.is_point_inside([x, y, z]):
              insidepoint += 1
              p = point.point(x, y, z)
              renderer.AddActor(p.get_actor(0.2))
       
      totpoint += 1


box_V = (maxbox_x - minbox_x) * (maxbox_y - minbox_y) *\
    (maxbox_z - minbox_z)
V = box_V * (float(insidepoint)/float(totpoint)) 
print "Volume sovrapposto: ", V
print "Volume Totale box: ", box_V



"""
# calcolo del volume
insidepoint = 0
totpoint = 0
numofp = 20
dx = (maxbox_x - minbox_x) / (numofp + 1)
dy = (maxbox_y - minbox_y) / (numofp + 1)
dz = (maxbox_z - minbox_z) / (numofp + 1)
for i in range(numofp):
  x = minbox_x + (i * dx)
  for j in range(numofp):
    y = minbox_y + (j * dy)
    for k in range(numofp):
      z = minbox_z + (k * dz)

      if nanop.is_point_inside([x, y, z]):
        insidepoint += 1
        p = point.point(x, y, z)
        renderer.AddActor(p.get_actor(0.01))

      totpoint += 1

box_V = (maxbox_x - minbox_x) * (maxbox_y - minbox_y) *\
    (maxbox_z - minbox_z)
V = box_V * (float(insidepoint)/float(totpoint)) 
print V
print box_V
"""

# rendi

renderer.SetActiveCamera(camera)
renderer.ResetCamera()
renderer.SetBackground(0,0,0)

renWin.SetSize(300,300)

renWin.Render()
iren.Start()
