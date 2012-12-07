from util import *
from point import *
from sphere import *
from common import *

import random
import math

###############################################################################

def get_subset_of_near_spheres(spheres, c):

  overlap = False
  near_spheres = []
  for s in spheres:
    center = s.get_center()

    dx = center.get_x() - c.get_x()
    dy = center.get_y() - c.get_y()

    dist = math.sqrt(dx*dx + dy*dy)

    if (dist <= 4*R):
      near_spheres.append(s)

    # e'sovrapposta ad un'altra sfera 
    if (c.get_distance_from(center) < (2*R)):
      overlap = True

  return overlap, near_spheres

###############################################################################

def touched_other_sphere(spheres, c):

  touching_spheres = []

  for s in spheres:
    center = s.get_center()
    if (center.get_distance_from(c) <= 2*R):
      touching_spheres.append(s)

  return touching_spheres

###############################################################################

def rotate_as_possible(c, p0, p1, near_spheres, numbertostop):
    touching_spheres_now = []

    dtetha = dtetha_start 
    tetha = 0.0

    lowest_c = c

    # ho fatto un giro completo senza effetti
    while tetha < (2.0 * math.pi):
      tetha += dtetha
      c_start = c

      c = point_rotate (p0, p1, c, tetha)
      # controllo se tocco i bordi
      if (((c.get_z() - R) < botz) or ((c.get_z() + R) > topz) or \
          ((c.get_x() - R) < botx) or ((c.get_x() + R) > topx) or \
          ((c.get_y() - R) < boty) or ((c.get_y() + R) > topy)):
        dtetha = dtetha/10.0
        if dtetha <= min_dtetha:
          if (c.get_z() < lowest_c.get_z()):
            lowest_c = c
          break
        else:
          c = c_start

      # controlla se tocco altre sfere
      touching_spheres_now = touched_other_sphere(near_spheres, c)
      if (len(touching_spheres_now) >= numbertostop):
        dtetha = dtetha/10.0
        if dtetha <= min_dtetha:
          if (c.get_z() < lowest_c.get_z()):
            lowest_c = c
          break
        else:
          c = c_start

      if (c.get_z() < lowest_c.get_z()):
        lowest_c = c

    if (lowest_c.get_z() < c.get_z()):
      c = lowest_c
      #print "problema " , lowest_c.get_z() - c.get_z()
    
    return touching_spheres_now

###############################################################################

def rotate_sphere (near_spheres, touching_spheres, c):
  # matrice di ruotazione intorno all'asse u = (ux, uy, uz)
  #      
  #      [  cos(t) + pow(uz,2) * (1 - cos(t))     ux * uy * (1-cos(t)-uz*sin(t)  ux*uz*(1-cos(t)) + uy*sin(t) ]
  #  R = [ uy * ux * (1 - cos(t)) + uz * sin(t)   cos(t) + pow(uy,2) * (1-cos(t) uy*uz*(1-cos(t)) - ux*sin(t) ]
  #      [ uz * ux * (1 - cos(t)) - uy * sin(t)   uz*uy*(1-cos(t)) + ux*sin(t)    cos(t)+pow(uz,2)*(1-cos(t)) ]
  #      

  if (len(touching_spheres) == 1):
    # una sfera asse passante per il centro della sfera 
    # che tocco. Faccio la ratazione per asse che passa per il centro della 
    # sfera che tocco e poi un punto 
    p0 = touching_spheres[0].get_center()
    
    # un punto random fuori dalla sfera che tocco
    p1x = random.uniform(botx, topx)
    p1y = random.uniform(boty, topy)
    p1z = p0.get_z()
    
    # un punto random fuori dalla sfera che tocco
    #p1x = p0.get_x() + 1.0
    #p1y = p0.get_y()
    #p1z = p0.get_z()
    
    p1 = point(p1x, p1y, p1z)

    touching_spheres_now = rotate_as_possible(c, p0, p1, near_spheres, 2)

    if (len(touching_spheres_now) == 2):
      p0 = touching_spheres_now[0].get_center()
      p1 = touching_spheres_now[1].get_center()

      rotate_as_possible(c, p0, p1, near_spheres, 3)

  elif (len(touching_spheres) == 2):
    # la sfera ne tocca altre due quindi routa intorno all'asse che unisce
    # le due che tocca
    p0 = touching_spheres[0].get_center()
    p1 = touching_spheres[1].get_center()

    touching_spheres_now = rotate_as_possible(c, p0, p1, near_spheres, 3)

  return

###############################################################################

def generate_compact_configuration (spheres = []):

  zmax = botz
  spheres_volume = 0.0
  lowest_c = point(0.0, 0.0, topz + (10.0*R))

  for dropped in range(1,drop_sphere_n_times):
            
    cx = random.uniform(botx+R, topx-R)
    cy = random.uniform(boty+R, topy-R)

    cz = topz + (2.0 * R)
                                    
    c = point(cx, cy, cz)

    # seleziona un set di possibili vicini, distanti nel
    # piano x,y al massimo 4R
    near_spheres = []
    overlap, near_spheres = get_subset_of_near_spheres(spheres, c)

    # probabilmente la sfera generata si sovrappone
    # con una gia' esistente
    if overlap:
      dropped = dropped - 1
      continue

    # muovi la sfera verso il basso fino che 
    # non incontra altra sfera
    deltaz = start_deltaz

    while (c.get_z()+R) > botz:
      c.set_z(c.get_z() - deltaz)

      touching_spheres = touched_other_sphere(near_spheres, c)
      if (touching_spheres):
        # print "  ", len(touching_spheres)
        # riduco deltaz e riprovo ad abbassre di meno fino
        # che deltaz non ha raggiunto un valore  di soglia
        c.set_z(c.get_z() + deltaz)
        deltaz = deltaz/10.0
        if (deltaz <= min_decrement):
          # rimetto nella posizione origionale
          c.set_z(c.get_z() - (deltaz*10.0))
          # se tocco meno di tre sfere provo a ruotare
          if (len(touching_spheres) < 3):
            # deltaz ha raggiunto la soglia quindi devo ruotare 
            # scelgo di ruotare in una direzione 
            rotate_sphere (near_spheres, touching_spheres, c)
          break

    if (c.get_z()+R < botz):
      c.set_z(botz+R)
      lowest_c = c
      break

    if (c.get_z() < lowest_c.get_z()):
      lowest_c = c

  s = sphere(lowest_c, R)

  if ((lowest_c.get_z()+R) > zmax):
    zmax = lowest_c.get_z()+R
  spheres.append(s)

  #print "Sphere : ", num

  return zmax

###############################################################################

def fill_the_top (max_dropped, spheres = []):

  zmax = botz
  lowest_c = point(0.0, 0.0, topz + (10.0 * R))

  for i in range(1,max_dropped):
    print "Filling the top : ", i
    toadd = False

    for dropped in range(1,drop_sphere_n_times):
      cx = random.uniform(botx+R, topx-R)
      cy = random.uniform(boty+R, topy-R)

      cz = topz + (2.0 * R)
                                      
      ctoadd = point(cx, cy, cz)
    
      # seleziona un set di possibili vicini, distanti nel
      # piano x,y al massimo 4R
      near_spheres = []
      overlap, near_spheres = get_subset_of_near_spheres(spheres, ctoadd)
    
      if overlap:
        continue

      c = ctoadd
      toadd = True

      # muovi la sfera verso il basso fino che 
      # non incontra altra sfera
      deltaz = start_deltaz
    
      while (c.get_z()+R) > botz:
        c.set_z(c.get_z() - deltaz)
    
        touching_spheres = touched_other_sphere(near_spheres, c)
        if (touching_spheres):
          # print "  ", len(touching_spheres)
          # riduco deltaz e riprovo ad abbassre di meno fino
          # che deltaz non ha raggiunto un valore  di soglia
          c.set_z(c.get_z() + deltaz)
          deltaz = deltaz/10.0
          if (deltaz <= min_decrement):
            # rimetto nella posizione origionale
            c.set_z(c.get_z() - (deltaz*10.0))
            # se tocco meno di tre sfere provo a ruotare
            if (len(touching_spheres) < 3):
              # deltaz ha raggiunto la soglia quindi devo ruotare 
              # scelgo di ruotare in una direzione 
              rotate_sphere (near_spheres, touching_spheres, c)
            break
    
      if (c.get_z()+R < botz):
        c.set_z(botz+R)
        break;
    
      if (c.get_z() < lowest_c.get_z()):
        lowest_c = c
    
    if toadd:
      s = sphere(lowest_c, R)
      if ((lowest_c.get_z()+R) > zmax):
        zmax = lowest_c.get_z()+R

      if (zmax <= topz):
        spheres.append(s)

###############################################################################
