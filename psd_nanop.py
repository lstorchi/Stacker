import re
import sys
import time

sys.path.append("./modules")

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

# no mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0
nanoparticle.POINTINSURFACESTEP = float('inf')

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

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
num_of_points = 1000000

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

poref = open("pore_radius_list_nano.txt", "w")
errof = open("error_file_nano.txt", "w")

for i in range(num_of_points):

  there_are_new_points = False

  perc = 100.0 * float(i)/float(num_of_points)
  if (perc >= reference):
    print perc , " % "
    reference += deltaperc

  px = random.uniform(minbox_x + distacemax, maxbox_x - distacemax)
  py = random.uniform(minbox_y + distacemax, maxbox_y - distacemax)
  pz = random.uniform(minbox_z + distacemax, maxbox_z - distacemax)

  #print px, py, pz

  t0 = time.time()

  selected_nanoparticles = select_near_nanoparticles (
      px, py, pz,
      nanoparticles,
      nanoparticle_center_x, 
      nanoparticle_center_y, 
      nanoparticle_center_z, 
      distacemax)

  print "select nanoparticle: %f " % (time.time() - t0) + " seconds"

  #print len(selected_nanoparticles)

  if (len(selected_nanoparticles) == 0):
    pore_radius_list[i] = distacemax
  else:

    if (not is_inside_a_nanoparticle (px, py, pz, selected_nanoparticles)):

      t0 = time.time()
      
      f, f_px, f_py, f_pz = solvopt_problem(px, py, pz, \
        lx, ly, lz, selected_nanoparticles)

      print "solvopt_problem %f " % (time.time() - t0) + " seconds"

      if (f <= 0):

        pore_radius_list[i] = math.sqrt(-f)
        
        data = str(px) + " " + \
               str(py) + " " + \
               str(pz) + " " + \
               str(f_px) + " " + \
               str(f_py) + " " + \
               str(f_pz) + " " + \
               str(math.sqrt(-f)) + "\n"
        #print math.sqrt(-f)
        poref.write(data)
        poref.flush()
        
        #r = math.sqrt(-f)
        #spheres = []  
        #spheres.append(sphere.sphere(point.point(f_px, f_py, f_pz), r))
        #visualize_collection (minbox_x, minbox_y, minbox_z,
        #    maxbox_x, maxbox_y, maxbox_z, selected_nanoparticles,
        #    spheres)
        #exit()

      if pore_radius_list[i] > radius_of_test_molecule:
        there_are_new_points = True

    else:
      pore_radius_list[i] = -1


  if there_are_new_points:

    # costruisco l'istogramma, credo si possa usare anche numpy.histogram
    # direttamente 
    max_cumm = 0.0
    for i in range(num_of_points):
      if pore_radius_list[i] > radius_of_test_molecule:
       
        for p in range(int(pore_radius_list[i] * RES_PSD) + 2):
    
          if (p >= hist_count):
            print "Problem when computing histogram"
            exit(-1)
    
          PSD_hist[p] += 1.0
          if (PSD_hist[p] > max_cumm):
            max_cumm = PSD_hist[p]

    # per capire quando mi devo fermare a stampare
    max_reached = 0
    for i in range(len(PSD_hist)):
      if (PSD_hist[i] == 0.0):
        max_reached = i + 5
        break

    # come noto -dH(D)/dD  e' il PSD 
    dHD = -1.0 * numpy.diff(PSD_hist)/2.0
    dD = numpy.linspace(0.0, float(len(dHD)-1)/RES_PSD, len(dHD))

    # normalizzo
    dHD = dHD/max(dHD)

    # calcolo l'errore
    count = 0
    err = avg_err = max_err = 0.0
    for i in range(len(dHD)):
      if dHD[i] > 0.0:
        err = math.fabs(dHD[i] - dHD_old[i]) / dHD[i]
        avg_err += err
        if err > max_err:
          max_err = err
        count += 1
    avg_err /= count
    dHD_old = dHD

    data = "%d %f %f\n" % (i, avg_err, max_err)
    errof.write(data)

    histof = open("psd_cumm_nano.txt", "w")
    for i in range(min(max_reached, len(PSD_hist))):
      data = "%f %f\n" % (float(i) / RES_PSD, PSD_hist[i] / max_cumm)
      histof.write(data)
    histof.close()

    diff_histf = open("psd_diff_nano.txt", "w")
    for i in range(min(max_reached, len(dHD))):
      data = "%f %f\n" % (dD[i], dHD[i])
      diff_histf.write(data)
    diff_histf.close()

errof.close()
poref.close()

print "Done" 

# test di visualizzazione
#spheres = []  
#spheres.append(sphere.sphere(point.point(px, py, pz), r))
#visualize_collection (minbox_x, minbox_y, minbox_z,
#    maxbox_x, maxbox_y, maxbox_z, selected_nanoparticles,
#    spheres)
