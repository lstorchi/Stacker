import re
import sys
import time

sys.path.append("./modules")

import util
import point
import sphere

import math
import numpy
import random

# in caso di uso di cython 
# from fastfunc import function_for_distance_fast

#######################################################

def get_spheres_in_anchor(scx, scy, scz, radius, \
      anchor_botx, anchor_boty, anchor_botz, \
      anchor_topx, anchor_topy, anchor_topz):

  bools1 = (scx + radius) > (anchor_botx - radius)
  bools2 = (scx - radius) < (anchor_topx + radius)
  bools3 = (scy + radius) > (anchor_boty - radius)
  bools4 = (scy - radius) < (anchor_topy + radius)
  bools5 = (scz + radius) > (anchor_botz - radius)
  bools6 = (scz - radius) < (anchor_topz + radius)

  interior_indices, = numpy.where(bools1*bools2*bools3*\
      bools4*bools5*bools6)

  inner_scx = numpy.linspace( 0.0, 0.0, len(interior_indices))
  inner_scy = numpy.linspace( 0.0, 0.0, len(interior_indices))
  inner_scz = numpy.linspace( 0.0, 0.0, len(interior_indices))
  inner_radius = numpy.linspace( 0.0, 0.0, len(interior_indices))

  j = 0
  for i in interior_indices:
    inner_scx[j] = scx[i]
    inner_scy[j] = scy[i]
    inner_scz[j] = scz[i]
    inner_radius[j] = radius[i]
    j += 1

  return inner_scx, inner_scy, inner_scz, inner_radius

#######################################################

def function_for_distance (px, py, pz, lx, ly, lz, \
    scx, scy, scz, radius):

  t0 = time.time()

  minr2 = 1e10

  for i in range(len(scx)):
    rx = math.fabs (px - scx[i])
    ry = math.fabs (py - scy[i]) 
    rz = math.fabs (pz - scz[i])
    if (rx > 0.5 * lx):
      rx -= lx
    if (ry > 0.5 * ly):
      ry -= ly
    if (rz > 0.5 * lz):
      rz -= lz;

    dis = math.sqrt ((rx * rx) + (ry * ry) + (rz * rz)) \
        - radius[i];
    if (dis < minr2):
      minr2 = dis

  print "%f " % (time.time() - t0) + " seconds"

  if minr2 > 0:
    return -minr2 * minr2
  
  return 0.0

#######################################################

def function_for_distance_fast (px, py, pz, lx, ly, lz, \
    scx, scy, scz, radius):

  #t0 = time.time()
  
  _fabs = numpy.fabs
  _array = numpy.array
  _sqrt = numpy.sqrt

  minr2 = 1e10

  rx = _fabs (px - scx)
  ry = _fabs (py - scy) 
  rz = _fabs (pz - scz)

  rx -= _array((rx > (0.5 * lx)), dtype=float)*lx
  ry -= _array((ry > (0.5 * ly)), dtype=float)*ly
  rz -= _array((rz > (0.5 * lz)), dtype=float)*lz

  dis = (_sqrt ((rx * rx) + (ry * ry) + (rz * rz)) \
      - radius).min()

  #dis = min(((rx * rx) + (ry * ry) + (rz * rz)))

  minr2 = dis

  #print "%f " % (time.time() - t0) + " seconds"

  if minr2 > 0:
    return -minr2 * minr2
  
  return 0.0

#######################################################

def solvopt_problem (px, py, pz, lx, ly, lz, \
    scx, scy, scz, radius):

  import pyOpt

  def objfunc(x):

    f = function_for_distance_fast (x[0], x[1], x[2], lx, ly, lz, \
        scx, scy, scz, radius)

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

filename = "final_config.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

spheres = []
zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    util.file_to_sphere_diffr_list(filename, spheres) 

scx, scy, scz, radius = util.sphere_to_arrays (spheres)

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

lx = topx-botx
ly = topy-boty
lz = topz-botz

print ""
print "Lattice dimension"
print "lX: ", lx, "lY: ", ly, "lZ: ", lz

# cerco semplicemente di trscrivere quanto fatto da psdsolv
# quindi come prima cosa sposto le sfere verso il basso
# o meglio centro il cluster in 0,0,0
scx = scx - botx
scy = scy - boty
scz = scz - botz

# il numero di punti random che genero ogni volta
num_of_points = 10

# posso anche leggere i punti invece di generarli
read_points = False
random_point_f = file
# Raggio della molecola che uso come tester, e quindi come probe per misurare i
# pori 3.409 A Argon quindi 0.3409 nm
radius_of_test_molecule = 0.17045
# risoluzione che voglio usare in genarale consigliano 0.25 A (0.025 nm), ma credo dovrei
# relazionare questa risoluzione anche a quela di SOLVOPT
RES_PSD = 1.0 / 0.5
# numero di bins nell'istogramma 
hist_count = int(round (max (max (lx, ly), lz) * RES_PSD)) + 1
# questo e' l'istogramma 
PSD_hist = numpy.linspace(0.0, 0.0, hist_count)
# questa e' la sua derivata mi server un old per poter poi 
# calcolare l'errore
dHD_old = numpy.diff(PSD_hist)

if (len(sys.argv)) == 3:
  filename = sys.argv[1]
  read_points = True
  random_point_f = open(filename, "r")

errof = open("error_file.txt", "w")
poref = open("pore_radius_list.txt", "w")

step_number = 1
term = True
while term:

  found_radius = numpy.linspace(0.0, 0.0, num_of_points)

  there_are_new_points = False

  for i in range(num_of_points):

    px = py = pz = 0.0

    if not read_points:
      # genero un punto random 
      px = random.uniform(0.0, lx)
      py = random.uniform(0.0, ly)
      pz = random.uniform(0.0, lz)
    else:
      # come test posso leggere i punti 
      line = ""
      rline = random_point_f.readline()
      if rline == "":
        term = False
      else:
        p = re.compile(r'\s+')
        line = p.sub(' ', rline)
        plist = line.split(" ")
        
        if len(plist) < 3:
          print "error in file"
          exit()

        px = float(plist[0])
        py = float(plist[1])
        pz = float(plist[2])

    dis = -1.0 * function_for_distance_fast (px, py, pz, \
        lx, ly, lz, scx, scy, scz, radius)

    if (dis > 0): # non sono dentro nessun sfera
      # qui ma messa la solvopt

      f, f_px, f_py, f_pz = solvopt_problem(px, py, pz, \
          lx, ly, lz, scx, scy, scz, radius)

      #print f_px, f_py, f_pz

      if (f <= 0.0):

        found_radius[i] = math.sqrt(-f)

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

      if found_radius[i] > radius_of_test_molecule:
        there_are_new_points = True

    else:
      found_radius[i] = -1.0

    #print dis, " and opt r: ", found_radius[i] 

  if there_are_new_points:

    # costruisco l'istogramma, credo si possa usare anche numpy.histogram
    # direttamente 
    max_cumm = 0.0
    for i in range(num_of_points):
      if found_radius[i] > radius_of_test_molecule:
       
        for p in range(int(found_radius[i] * RES_PSD) + 2):
    
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

    # mi fermo quando l'errore medio e' inferiore a 0.001
    #if not read_points:
    #  if avg_err < 0.00001:
    #    term = False

    data = "%d %f %f\n" % (step_number, avg_err, max_err)
    errof.write(data)

    histof = open("psd_cumm.txt", "w")
    for i in range(min(max_reached, len(PSD_hist))):
      data = "%f %f\n" % (float(i) / RES_PSD, PSD_hist[i] / max_cumm)
      histof.write(data)
    histof.close()

    diff_histf = open("psd_diff.txt", "w")
    for i in range(min(max_reached, len(dHD))):
      data = "%f %f\n" % (dD[i], dHD[i])
      diff_histf.write(data)
    diff_histf.close()


  print "  Step ", step_number
  step_number += 1

  #if (step_number == 50):
  #  exit()

errof.close()
poref.close()

if read_points:
  random_point_f.close()
