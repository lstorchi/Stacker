import sys
import vtk
import re

import random
import numpy
import math

from scipy.spatial import distance

sys.path.append("../modules")

import nanoparticle
import xyznanop
import sphere
import plane
import point
import line
import util
import cube

###############################################################################

def count_dists (group_np1, group_np2, mdist):

    coords1 = numpy.array(group_np1, dtype=float)
    coords2 = numpy.array(group_np2, dtype=float)
    dists = distance.cdist(coords1, coords2)
    counter = 0
    for i in range(dists.shape[0]):
        for j in range(dists.shape[1]):
            if dists[i][j] < mdist:
                counter += 1

    #for i in range(dists.shape[0]):
    #    for j in range(dists.shape[1]):
    #        sys.stdout.write(str(dists[i][j]) + " ")
    #    sys.stdout.write("\n")
    #print numpy.allclose(dists, dists.T, atol=1.0e-8)
    #out = sum(x < 5.0 for x in dists)
                
    return counter

###############################################################################

# init 

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

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
DIST2 = 12.6

nanop1 = nanaparticles[0]
ptop, pbot = nanop1.get_ptop_and_bottom()
l1 = line.line3d()
l1.set_two_point(ptop, pbot)
p1, p2, p3, p4 = nanop1.get_middle_points ()
mdplane = plane.plane(p1, p2, p3)

group1_np1 = []
group2_np1 = []
group3_np1 = []
allnp1 = []

for i in range(len(xlist1)):
  p = point.point(xlist1[i], ylist1[i], zlist1[i])

  dist = mdplane.get_distance(p) * mdplane.check_point_side(p)
  if dist < DITS1:
      group1_np1.append((p.get_x(), p.get_y(), p.get_z()))
  elif dist >= DITS1 and dist < DIST2:
      group2_np1.append((p.get_x(), p.get_y(), p.get_z()))
  else:
      group3_np1.append((p.get_x(), p.get_y(), p.get_z()))

  allnp1.append((p.get_x(), p.get_y(), p.get_z()))

nanop2 = nanaparticles[1]
ptop, pbot = nanop2.get_ptop_and_bottom()
l2 = line.line3d()
l2.set_two_point(ptop, pbot)
p1, p2, p3, p4 = nanop2.get_middle_points ()
mdplane = plane.plane(p1, p2, p3)

p1top, p1bottom = nanop1.get_ptop_and_bottom ()
p2top, p2bottom = nanop2.get_ptop_and_bottom ()

l3d = line.line3d()
angle = l3d.get_angle_two_line(p1top, p1bottom, p2top, p2bottom)

group1_np2 = []
group2_np2 = []
group3_np2 = []
allnp2 = []

for i in range(len(xlist2)):
  p = point.point(xlist2[i], ylist2[i], zlist2[i])

  dist = mdplane.get_distance(p) * mdplane.check_point_side(p)
  if dist < DITS1:
      group1_np2.append((p.get_x(), p.get_y(), p.get_z()))
  elif dist >= DITS1 and dist < DIST2:
      group2_np2.append((p.get_x(), p.get_y(), p.get_z()))
  else:
      group3_np2.append((p.get_x(), p.get_y(), p.get_z()))

  allnp2.append((p.get_x(), p.get_y(), p.get_z()))

coords1 = numpy.array(group1_np1, dtype=float)
coords2 = numpy.array(group1_np2, dtype=float)
dists = distance.cdist(allnp1, allnp2)

MINDIST = 3.5

counter11 = count_dists (group1_np1, group1_np2, MINDIST)
counter22 = count_dists (group2_np1, group2_np2, MINDIST)
counter33 = count_dists (group3_np1, group3_np2, MINDIST)
counter12 = count_dists (group1_np1, group2_np2, MINDIST)
counter13 = count_dists (group1_np1, group3_np2, MINDIST)
counter23 = count_dists (group2_np1, group3_np2, MINDIST)
counter21 = count_dists (group2_np1, group1_np2, MINDIST)
counter31 = count_dists (group3_np1, group1_np2, MINDIST)
counter32 = count_dists (group3_np1, group2_np2, MINDIST)

counter11_5 = count_dists (group1_np1, group1_np2, 5.0)
counter22_5 = count_dists (group2_np1, group2_np2, 5.0)
counter33_5 = count_dists (group3_np1, group3_np2, 5.0)
counter12_5 = count_dists (group1_np1, group2_np2, 5.0)
counter13_5 = count_dists (group1_np1, group3_np2, 5.0)
counter23_5 = count_dists (group2_np1, group3_np2, 5.0)
counter21_5 = count_dists (group2_np1, group1_np2, 5.0)
counter31_5 = count_dists (group3_np1, group1_np2, 5.0)
counter32_5 = count_dists (group3_np1, group2_np2, 5.0)

#print counter11, " , " , counter22, " , " , counter33, " , " , \
#      counter12, " , " , counter13, " , " , counter23, " , " , \
#      counter21, " , " , counter31, " , " , counter32, " , ", \
#      counter11_5, " , " , counter22_5, " , " , counter33_5, " , " , \
#      counter12_5, " , " , counter13_5, " , " , counter23_5, " , " , \
#      counter21_5, " , " , counter31_5, " , " , counter32_5, " , ", \
#      angle

sset = "" 

cc = counter11
ff = counter22
tt = counter33
cf = counter12+counter21
ct = counter13+counter31
ft = counter23+counter32

if (sset == ""):
  if (cc >= 10):
    sset = "CC+"
    if (tt >= 10) or (ct >= 10) or (ft >= 10):
      sset = ""

if (sset == ""):
  if (ct >= 10):
    sset = "CT"
    if (tt >= 10) or (cf >= 10) or (cc >= 10):
      sset = ""

if (sset == ""):
  if (ft >= 10):
    sset = "FT"
    if (cc >= 10) or (tt >= 10) or (cf >= 10) or (ct >= 10):
      sset = ""

if (sset == ""):
  if (cf >= 10):
    sset = "CF"
    if (cc >= 10) or (ff >= 10) or (tt >= 10) or (ct >= 10) or (ft >= 10):
      sset = ""

if (sset == ""):
  if (tt >= 10):
    sset = "TT"
    if (cc >= 10) or (ff >= 10) or (cf >= 10) or (ct >= 10) or (ft >= 10):
      sset = ""

if (sset == ""):
  if (ct >= 10) and (ft >= 10):
    sset = "CTF"
    if (cc >= 10) or (ff >= 10) or (tt >= 10) or (cf >= 10):
      sset = ""

if (sset == ""):
  if (ct >= 10) and (ft >= 10):
    sset = "FCT"
    if (cc >= 10) or (ff >= 10) or (tt >= 10) or (cf >= 10):
      sset = ""

if (sset == ""):
  if (ct >= 10) and (cf >= 10):
    sset = "FCT"
    if (cc >= 10) or (ff >= 10) or (tt >= 10) or (ft >= 10):
      sset = ""

if (sset == ""):
  if (ff >= 10):
    sset = "FF"
    if (cc >= 10) or (ct >= 10) or (tt >= 10) or (ft >= 10):
      sset = ""

print counter11, " , " , counter22, " , " , counter33, " , " , \
      counter12+counter21, " , " , counter13+counter31, " , " , counter23+counter32, " , " , \
      angle, " , " , sset

visualg1 = False

if visualg1:
   camera = vtk.vtkCamera()
   camera.SetPosition(1,1,1)
   camera.SetFocalPoint(0,0,0)
   
   renderer = vtk.vtkRenderer()
   renWin = vtk.vtkRenderWindow()
   renWin.AddRenderer(renderer)
   
   iren = vtk.vtkRenderWindowInteractor()
   iren.SetRenderWindow(renWin)
   
   for nanop in nanaparticles: 
       renderer.AddActor(nanop.get_vtk_actor(color=True,opacity=0.9))
   
   for i in range(dists.shape[0]):
       for j in range(dists.shape[1]):
           if dists[i][j] < MINDIST:
               p1 = point.point(allnp1[i][0], allnp1[i][1], allnp1[i][2])
               p2 = point.point(allnp2[j][0], allnp2[j][1], allnp2[j][2])
               renderer.AddActor(p1.get_actor(1.0, 1.0, 0.0, 0.0))
               renderer.AddActor(p2.get_actor(1.0, 0.0, 1.0, 0.0))
   
   
   renderer.SetActiveCamera(camera)
   renderer.ResetCamera()
   renderer.SetBackground(0,0,0)
   
   renWin.SetSize(1024, 768)
   renWin.Render()
   iren.Start()

