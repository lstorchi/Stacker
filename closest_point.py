import sys
import vtk

import random
import math

sys.path.append("./modules")

import nanoparticle
import triangle
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

nanoparticle.POINTINSIDEDIM = 0

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

if (selected_nanaop >= len(nanoparticles)):
  print "error invalid particle selected "
  exit()

nanop = nanoparticles[selected_nanaop]

print "Volume: " , nanop.get_volume() 
print "Volume of sphere: ", sphere.sphere(point.point(), \
    nanop.get_max_sphere()).get_volume()

#renderer.AddActor(nanop.get_vtk_actor(False, 0.8))

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

"""
p = point.point(cx + dm/2.0, cy-dm, cz+dm/4.0)
renderer.AddActor(p.get_actor(0.5, 1.0, 0.0, 0.0))

pp = nanop.project_point(p)
renderer.AddActor(pp.get_actor(0.5))

dist = nanop.get_distance(p)
renderer.AddActor(p.get_actor(dist))
"""

p = point.point(cx + dm, cy-dm/2.0, cz+dm/1.5)
renderer.AddActor(p.get_actor(0.5, 1.0, 0.0, 0.0))

pp = nanop.project_point(p)
renderer.AddActor(pp.get_actor(0.5))

"""
dist = nanop.get_distance(p)
renderer.AddActor(p.get_actor(dist))

p = point.point(cx + dm/1.9, cy-dm/1.45, cz+dm/1.5)
renderer.AddActor(p.get_actor(0.5, 1.0, 0.0, 0.0))

pp = nanop.project_point(p)
renderer.AddActor(pp.get_actor(0.5))

dist = nanop.get_distance(p)
renderer.AddActor(p.get_actor(dist))

p = point.point(cx, cy, cz+2.0*dm)
renderer.AddActor(p.get_actor(0.5))

pp = nanop.project_point(p)
renderer.AddActor(pp.get_actor(0.5))

dist = nanop.get_distance(p)
renderer.AddActor(p.get_actor(dist))
"""

trpointslist = nanop.get_triangle_points()

i = 0
for p1, p2, p3 in trpointslist:
  rc, gc, bc = util.get_rgb (i, 0, len(trpointslist))
  renderer.AddActor(triangle.get_vtk_actor(p1, p2, p3, 0.6, 
    float(rc)/255.0, float(gc)/255.0, float(bc)/255.0))
  i += 1

  #s = sphere.sphere(p1, 1.0)
  #renderer.AddActor(s.get_actor())
  #s = sphere.sphere(p2, 1.0)
  #renderer.AddActor(s.get_actor())
  #s = sphere.sphere(p3, 1.0)
  #renderer.AddActor(s.get_actor())


renderer.SetActiveCamera(camera)
renderer.ResetCamera()
renderer.SetBackground(0,0,0)

renWin.SetSize(300,300)

renWin.Render()
iren.Start()
