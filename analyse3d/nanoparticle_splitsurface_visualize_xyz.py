import sys
import vtk
import re

import random
import math

sys.path.append("../modules")

import nanoparticle
import xyznanop
import sphere
import plane
import point
import line
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

xlist, ylist, zlist, atoms = xyznanop.read_ncxyz(xyzfile, False)

xlist1 = xlist[:len(xlist)/2]
ylist1 = ylist[:len(ylist)/2]
zlist1 = zlist[:len(zlist)/2]
atoms1 = atoms[:len(atoms)/2]
             
xlist2 = xlist[len(xlist)/2:]
ylist2 = ylist[len(ylist)/2:]
zlist2 = zlist[len(zlist)/2:]
atoms2 = atoms[len(atoms)/2:]

if len(nanaparticles) != 2:
    print "Only two nanoparticles can be used"
    exit(1)

DITS1 = 2.6
DIST2 = 11.4

nanop1 = nanaparticles[0]
ptop, pbot = nanop1.get_ptop_and_bottom()
#renderer.AddActor(ptop.get_actor(2.0, 0.0, 1.0, 0.0))
#renderer.AddActor(pbot.get_actor(2.0, 0.0, 1.0, 0.0))
#renderer.AddActor(nanop1.get_vtk_actor(color=True,opacity=1.0))
l1 = line.line3d()
l1.set_two_point(ptop, pbot)
p1, p2, p3, p4 = nanop1.get_middle_points ()
mdplane = plane.plane(p1, p2, p3)
#renderer.AddActor(p1.get_actor(1.0))
#renderer.AddActor(p2.get_actor(1.0))
#renderer.AddActor(p3.get_actor(1.0))
for i in range(len(xlist1)):
  p = point.point(xlist1[i], ylist1[i], zlist1[i])

  dist = mdplane.get_distance(p) * mdplane.check_point_side(p)
  if dist < DITS1:
      #dline3d = l1.get_distance(p)
      #if dline3d > 9.0:
      renderer.AddActor(p.get_actor(1.0, 1.0, 0.0, 0.0))
  elif dist >= DITS1 and dist < DIST2:
      #dline3d = l1.get_distance(p)
      #if dline3d > 7.0:
      renderer.AddActor(p.get_actor(1.0, 0.0, 1.0, 0.0))
  else:
      renderer.AddActor(p.get_actor(1.0, 0.0, 0.0, 1.0))


nanop2 = nanaparticles[1]
ptop, pbot = nanop2.get_ptop_and_bottom()
#renderer.AddActor(nanop2.get_vtk_actor(color=True,opacity=1.0))
l2 = line.line3d()
l2.set_two_point(ptop, pbot)
p1, p2, p3, p4 = nanop2.get_middle_points ()
mdplane = plane.plane(p1, p2, p3)
#renderer.AddActor(p1.get_actor(1.0))
#renderer.AddActor(p2.get_actor(1.0))
#renderer.AddActor(p3.get_actor(1.0))
for i in range(len(xlist2)):
  p = point.point(xlist2[i], ylist2[i], zlist2[i])

  dist = mdplane.get_distance(p) * mdplane.check_point_side(p)
  if dist < DITS1:
      #dline3d = l2.get_distance(p)
      #if dline3d > 9.0:
      
      renderer.AddActor(p.get_actor(1.0, 1.0, 0.0, 0.0))
  elif dist >= DITS1 and dist < DIST2:
      #dline3d = l2.get_distance(p)
      #if dline3d > 7.0:
      
      renderer.AddActor(p.get_actor(1.0, 0.0, 1.0, 0.0))
  else:
      renderer.AddActor(p.get_actor(1.0, 0.0, 0.0, 1.0))


renderer.SetActiveCamera(camera)
renderer.ResetCamera()
renderer.SetBackground(0,0,0)

renWin.SetSize(1024, 768)
renWin.Render()
iren.Start()

