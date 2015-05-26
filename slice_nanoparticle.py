from __future__ import print_function

import sys

sys.path.append("./modules")

import nanoparticle
import sphere
import point
import util
import cube

import math

import vtk

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) == 2:
  filename = sys.argv[1]

nanoparticles = []

print ('Start reading '+filename+' ...')
botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles) 
print ('Done')

if (botx >= topx) or (boty >= topy) or \
   (boty >= topy):
  print ('Error Invalid BOX\n')
  exit()

# nanoparticle

minbox_x = 100000.0 
maxbox_x =-100000.0 
minbox_y = 100000.0
maxbox_y =-100000.0
minbox_z = 100000.0
maxbox_z =-100000.0

r = 0.0
for nanop in nanoparticles: 
  cx, cy, cz = nanop.get_center()
  A, B, H = nanop.get_dimensions()

  dm = max(H, B, A) / 2.0

  r += nanop.get_max_sphere()

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

mead_d = 2.0 * (r/float(len(nanoparticles)))

print ('Box limits: '+str(minbox_x)+' '+str(maxbox_x)+ \
    ' '+str(minbox_y)+' '+str(maxbox_y)+ \
    ' '+ str(minbox_z)+' '+str(maxbox_z)+'\n')

# equazione del piano
zplane = minbox_z + ((maxbox_z - minbox_z)/2.0) 

nanoparicles_in_plane = []

for nanop in nanoparticles:

  cx, cy, cz = nanop.get_center()
  r = nanop.get_max_sphere()

  if (zplane >= (cz - r)) and (zplane <= (cz + r)):
    nanoparicles_in_plane.append(nanop)

filetoprint = open("selected_slice_nanop.txt", "w")

for nanop in nanoparicles_in_plane:

  cx, cy, cz, A, B, H, p2x, p2y, p2z, tetha = \
      nanop.get_to_print()

  data = str(cx) + " " + \
         str(cy) + " " + \
         str(cz) + " " + \
         str(A) + " " + \
         str(B) + " " + \
         str(H) + " " + \
         str(p2x) + " " + \
         str(p2y) + " " + \
         str(p2z) + " " + \
         str(tetha) + "\n"

  filetoprint.write(data)

filetoprint.close()


'''

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


dt = (2.0 * math.pi)/(np)

for s in spheres_in_plane:
  r = s.get_radius()
  c = s.get_center()

  cx = c.get_x()
  cy = c.get_y()
  cz = c.get_z()

  circler = math.sqrt(math.pow(r, 2) - math.pow((zplane-cz),2))

  cir = circle(cx, cy, circler)
  ren.AddActor(cir.get_actor(zplane))

  t = 0.0
 
  for i in range(1,np):
 
    t = t + dt
 
    x = cx + circler * math.cos(t)
    y = cy + circler * math.sin(t)
    print x, y
    sys.stdout.flush()

sys.stdout.flush()

ren.SetBackground(0,0,0)
renWin.SetSize(1024, 768)
renWin.Render()

renderLarge = vtk.vtkRenderLargeImage()
renderLarge.SetInput(ren)
renderLarge.SetMagnification(4)

writer = vtk.vtkTIFFWriter()
writer.SetInputConnection (renderLarge.GetOutputPort())
writer.SetFileName("largeImage.tif")
writer.Write()

iren.Start()
'''
