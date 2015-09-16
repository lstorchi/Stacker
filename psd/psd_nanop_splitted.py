import re
import sys
import time

sys.path.append("../modules")

import nanoparticle
import sphere
import point

import math
import numpy
import random

#######################################################

def select_near_nanoparticles (
    px, py, pz,
    nanoparticles,
    nanoparticle_center_x, 
    nanoparticle_center_y, 
    nanoparticle_center_z, 
    distacemax):

  selected_n = []

  dx = (nanoparticle_center_x - px) * \
       (nanoparticle_center_x - px)
  dy = (nanoparticle_center_y - py) * \
       (nanoparticle_center_y - py)
  dz = (nanoparticle_center_z - pz) * \
       (nanoparticle_center_z - pz)

  dist = numpy.sqrt(dx + dy + dz)

  bools = (dist <= distacemax) 

  indices, = numpy.where(bools)

  for i in range(len(indices)):
    selected_n.append(nanoparticles[indices[i]])
    #print nanoparticles[indices[i]].get_center()

  return selected_n

#######################################################

def is_inside_a_nanoparticle (px, py, pz, nanoparticles):

  t0 = time.time()
      
  for n in nanoparticles:
    if (n.is_point_inside([px, py, pz])):
      return True

  print "is_inside_a_nanoparticle %f " % (time.time() - t0) + " seconds"

  return False

#######################################################

def get_biggest_sphere_possible (px, py, pz, 
    nanoparticles, smallest_r, dr):

  t0 = time.time()

  radius = smallest_r

  while (True):

    s = sphere.sphere(point.point(px, py, pz), radius)
     
    for n in nanoparticles:
      if (n.sphere_touch_me(s)):
        return radius - dr

    radius += dr

  print "get_biggest_sphere_possible %f " % (time.time() - t0) + " seconds"

  return radius

#######################################################

def function_for_distance_fast (px, py, pz, \
    lx, ly, lz, nanoparticles):

  p = point.point(px, py, pz)

  minr2 = float('inf')
  for n in nanoparticles:
    #q = n.closest_point_outside(p)
    #rf = q.get_distance_from(p)

    rf = n.get_distance(p)

    if (rf < minr2):
      minr2 = rf

  return -minr2 * minr2

#######################################################

def function_for_distance_fast_old (px, py, pz, \
    lx, ly, lz, nanoparticles):

  radius = 0.1
  dr = 0.1

  found = True

  p = point.point(px, py, pz)

  numofsp = 20
  
  s = sphere.sphere(p, radius)
  
  while (found):
  
    s.set_radius(radius)
  
    surf_points = s.generate_surface_points(numofsp)
     
    for n in nanoparticles:
      if (n.sphere_touch_me_surface_points(s.get_radius(), 
            s.get_center(), surf_points)):
        minr2 = radius - dr
        found = False
        break
  
    if (found):
      radius += dr
      #numofsp = numofsp * 2
      #if (numofsp > 20):
      #  numofsp = 20
      #print numofsp, radius
  
  return -minr2 * minr2


#######################################################

def visualize_collection (minbox_x, minbox_y, minbox_z,
    maxbox_x, maxbox_y, maxbox_z, nanoparticles, spheres):

  import vtk

  camera = vtk.vtkCamera()
  camera.SetPosition(1,1,1)
  camera.SetFocalPoint(0,0,0)

  renderer = vtk.vtkRenderer()
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(renderer)

  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)

  cube_actors = cube.cube_to_actors(minbox_x, minbox_y, minbox_z, \
        maxbox_x, maxbox_y, maxbox_z, 1.0, 1.0, 1.0)
  for a in cube_actors:
    renderer.AddActor(a)

  for s in spheres:
    renderer.AddActor(s.get_actor())

    surface_points = s.generate_surface_points(20)

    for sp in surface_points:
      renderer.AddActor(sp.get_actor(0.2))

  for n in nanoparticles:
    renderer.AddActor(n.get_vtk_actor())

  renderer.SetActiveCamera(camera)
  renderer.ResetCamera()
  renderer.SetBackground(0,0,0)

  renWin.SetSize(300,300)

  renWin.Render()
  iren.Start()

  return
 
#######################################################

def solvopt_problem(px, py, pz, lx, ly, lz, 
    selected_nanoparticles):

  import pyOpt

  def objfunc(x):

    f = 0.0
    f = function_for_distance_fast (x[0], x[1], x[2], lx, ly, lz, \
        selected_nanoparticles)

    g = [0.0]

    minr2 = -1.0 * f
    maxcon = -1e10;
    dis = (px - x[0]) * (px - x[0]) + \
        (py - x[1]) * (py - x[1]) + \
        (pz - x[2]) * (pz - x[2])

    maxcon = -minr2 + dis

    g[0] = max (0, maxcon)

    fail = 0
    return f,g, fail

  opt_prob = pyOpt.Optimization('TP37 Constrained Problem',objfunc)

  opt_prob.addObj('f')

  opt_prob.addVar('x1','c',lower=float('-inf'),upper=float('inf'),value=px)
  opt_prob.addVar('x2','c',lower=float('-inf'),upper=float('inf'),value=py)
  opt_prob.addVar('x3','c',lower=float('-inf'),upper=float('inf'),value=pz)

  opt_prob.addConGroup('g',1,'i')

  #print opt_prob

  solvopt = pyOpt.SOLVOPT()
  #solvopt = pyOpt.PSQP()
  solvopt.setOption('ftol', 1.0e-3)
  solvopt.setOption('iprint', -1)
  [fstr, xstr, inform] = solvopt(opt_prob,sens_type='FD')

  if len(xstr) < 3:
    print "error in solvopt"
    exit()

  f_px = float(xstr[0])
  f_py = float(xstr[1])
  f_pz = float(xstr[2])

  #print opt_prob.solution(0)

  return float(fstr), f_px, f_py, f_pz

#######################################################

#numpy.seterr(invalid='raise')

MAX_POINT_TODO = 1773
count_point_inside = 0

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

filename = "nanoparticle_final_config.txt"
to_append = ""

if (len(sys.argv)) > 1:
  filename = sys.argv[1]
  if (len(sys.argv) == 3):
    to_append = sys.argv[2]

nanoparticles = []

botx, topx, boty, topy, botz, topz = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles) 

if (botx >= topx) or (boty >= topy) or (boty >= topy):
  print "Error Invalid BOX"
  exit()

print botx, topx, boty, topy, botz, topz

thefirst = True

minbox_x = 100000.0 
maxbox_x =-100000.0 
minbox_y = 100000.0
maxbox_y =-100000.0
minbox_z = 100000.0
maxbox_z =-100000.0

distacemax = 0.0

for nanop in nanoparticles: 

  if thefirst :
    print "Volume: " , nanop.get_volume() 
    thefirst = False

  cx, cy, cz = nanop.get_center()
  A, B, H = nanop.get_dimensions()

  dm = max(H, B, A) / 2.0

  if (dm > distacemax):
    distacemax = 2.0 * dm

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

lx = maxbox_x-minbox_x
ly = maxbox_y-minbox_y
lz = maxbox_z-minbox_z

nanoparticle_center_x = numpy.linspace( 0.0, 0.0, len(nanoparticles))
nanoparticle_center_y = numpy.linspace( 0.0, 0.0, len(nanoparticles))
nanoparticle_center_z = numpy.linspace( 0.0, 0.0, len(nanoparticles))

i = 0
for nanop in nanoparticles:
  cx, cy, cz = nanop.get_center()

  # dovrei rifare la ruotazione IMPORTANTE
  #cx = cx - botx
  #cy = cy - boty
  #cz = cz - botz

  #nanop.set_center(cx, cy, cz)

  nanoparticle_center_x[i] = cx
  nanoparticle_center_y[i] = cy
  nanoparticle_center_z[i] = cz

  i += 1


# il numero di punti random che genero 
num_of_points = 8000

distacemax = distacemax + (0.2 * distacemax)

# raggio della molecola di test e anche dunque raggio minimo di test
radius_of_test_molecule = 0.1
# di quanto incremento il raggio ogni volta
dr = 0.1
# credo abbia senso definirla quanto il dr
RES_PSD = 1.0 / 0.1
hist_count = int(round (max (max (lx, ly), lz) * RES_PSD)) + 1
# questo e' l'istogramma 
PSD_hist = numpy.linspace(0.0, 0.0, hist_count)
# questa e' la sua derivata mi server un old per poter poi 
# calcolare l'errore
dHD_old = numpy.diff(PSD_hist)

deltaperc = 5.0
reference = deltaperc

pore_radius_list = numpy.linspace(0.0, 0.0, num_of_points)

out_filename = "pore_radius_list_nano.txt"

if to_append != "":
  out_filename += "_" + to_append 

poref = open(out_filename, "w")

i = 0
while (i < num_of_points):

  perc = 100.0 * float(i)/float(num_of_points)
  if (perc >= reference):
    print perc , " % "
    reference += deltaperc

  px = random.uniform(minbox_x + distacemax, maxbox_x - distacemax)
  py = random.uniform(minbox_y + distacemax, maxbox_y - distacemax)
  pz = random.uniform(minbox_z + distacemax, maxbox_z - distacemax)

  t0 = time.time()

  selected_nanoparticles = select_near_nanoparticles (
      px, py, pz,
      nanoparticles,
      nanoparticle_center_x, 
      nanoparticle_center_y, 
      nanoparticle_center_z, 
      distacemax)

  print "select nanoparticle: %f " % (time.time() - t0) + " seconds"

  if (len(selected_nanoparticles) > 0):
    if (not is_inside_a_nanoparticle (px, py, pz, selected_nanoparticles)):

      t0 = time.time()
      
      f, f_px, f_py, f_pz = solvopt_problem(px, py, pz, \
        lx, ly, lz, selected_nanoparticles)

      print "solvopt_problem %f " % (time.time() - t0) + " seconds"

      if (f <= 0):

        pore_r = math.sqrt(-f)

        if pore_r > radius_of_test_molecule:

          pcenter = point.point(f_px, f_py, f_pz)
          pore = sphere.sphere(pcenter, pore_r)
          psurface_points = pore.generate_surface_points(20)

          tto = time.time()

          touch_nanoparticle = False
          for nanop in selected_nanoparticles:
            if (nanop.sphere_touch_me_surface_points(pore_r, pcenter, \
                psurface_points)):
              touch_nanoparticle = True
              break;

          print "touch_nanoparticle %f " % (time.time() - tto) + " seconds"

          if not touch_nanoparticle:
            pore_radius_list[i] = pore_r 

            data = str(px) + " " + \
                   str(py) + " " + \
                   str(pz) + " " + \
                   str(f_px) + " " + \
                   str(f_py) + " " + \
                   str(f_pz) + " " + \
                   str(pore_radius_list[i]) + "\n"
            poref.write(data)
            poref.flush()

            count_point_inside += 1

            if (count_point_inside >= MAX_POINT_TODO) : 
              print "Max point reached" 
              poref.close()
              exit(1)
          
            i += 1 

poref.close()

print "Done" 

