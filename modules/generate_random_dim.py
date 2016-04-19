import util
import point
import sphere
import common

import random
import math

###############################################################################

def generate_compact_configuration_fixed_r (spheres = [], r):

  zmax = common.botz
  lowest_c = point.point(0.0, 0.0, common.topz + (10.0*common.MAXR))

  s = sphere.sphere()

  radius = r
  s.set_radius(radius)

  for dropped in range(1,common.drop_sphere_n_times):
            
    cx = random.uniform(common.botx, common.topx)
    cy = random.uniform(common.boty, common.topy)
    cz = common.topz + (2.0 * common.MAXR)
                                    
    c = point.point(cx, cy, cz)
    s.set_center(c)

    # seleziona un set di possibili vicini, distanti nel
    # piano x,y al massimo 4R
    near_spheres = []
    overlap, near_spheres = get_subset_of_near_spheres(spheres, s)

    # probabilmente la sfera generata si sovrappone
    # con una gia' esistente
    if overlap:
      dropped = dropped - 1
      continue

    # muovi la sfera verso il basso fino che 
    # non incontra altra sfera
    deltaz = common.start_deltaz

    while (c.get_z()+radius) > common.botz:
      c.set_z(c.get_z() - deltaz)

      touching_spheres = touched_other_sphere(near_spheres, s)

      if (touching_spheres):
        c.set_z(c.get_z() + deltaz)
        deltaz = deltaz/10.0
        if (deltaz <= common.min_decrement):
          c.set_z(c.get_z() - (deltaz*10.0))
          if (len(touching_spheres) < 3):
            rotate_sphere (near_spheres, touching_spheres, s)
          break

    if (c.get_z()+radius < common.botz):
      c.set_z(common.botz+radius)
      lowest_c = c
      break

    if (c.get_z() < lowest_c.get_z()):
      lowest_c = c

  s.set_center(lowest_c)

  if ((lowest_c.get_z()+radius) > zmax):
    zmax = lowest_c.get_z()+radius

  spheres.append(s)

  return zmax

###############################################################################

def generate_compact_configuration_random_r (spheres = []):

  zmax = common.botz
  lowest_c = point.point(0.0, 0.0, common.topz + (10.0*common.MAXR))

  s = sphere.sphere()

  radius = random.uniform(common.MINR, common.MAXR)
  s.set_radius(radius)

  for dropped in range(1,common.drop_sphere_n_times):
            
    cx = random.uniform(common.botx, common.topx)
    cy = random.uniform(common.boty, common.topy)
    cz = common.topz + (2.0 * common.MAXR)
                                    
    c = point.point(cx, cy, cz)
    s.set_center(c)

    # seleziona un set di possibili vicini, distanti nel
    # piano x,y al massimo 4R
    near_spheres = []
    overlap, near_spheres = get_subset_of_near_spheres(spheres, s)

    # probabilmente la sfera generata si sovrappone
    # con una gia' esistente
    if overlap:
      dropped = dropped - 1
      continue

    # muovi la sfera verso il basso fino che 
    # non incontra altra sfera
    deltaz = common.start_deltaz

    while (c.get_z()+radius) > common.botz:
      c.set_z(c.get_z() - deltaz)

      touching_spheres = touched_other_sphere(near_spheres, s)

      if (touching_spheres):
        c.set_z(c.get_z() + deltaz)
        deltaz = deltaz/10.0
        if (deltaz <= common.min_decrement):
          c.set_z(c.get_z() - (deltaz*10.0))
          if (len(touching_spheres) < 3):
            rotate_sphere (near_spheres, touching_spheres, s)
          break

    if (c.get_z()+radius < common.botz):
      c.set_z(common.botz+radius)
      lowest_c = c
      break

    if (c.get_z() < lowest_c.get_z()):
      lowest_c = c

  s.set_center(lowest_c)

  if ((lowest_c.get_z()+radius) > zmax):
    zmax = lowest_c.get_z()+radius

  spheres.append(s)

  return zmax

###############################################################################

def get_subset_of_near_spheres(spheres, s):

  c = s.get_center()
  overlap = False
  near_spheres = []
  for sp in spheres:
    center = sp.get_center()

    dx = center.get_x() - c.get_x()
    dy = center.get_y() - c.get_y()

    dist = math.sqrt(dx*dx + dy*dy)

    if (dist <= 4*common.MAXR):
      near_spheres.append(sp)

    # e'sovrapposta ad un'altra sfera 
    sumofradius = s.get_radius() + sp.get_radius()
    if (c.get_distance_from(center) < sumofradius):
      overlap = True

  return overlap, near_spheres

###############################################################################

def touched_other_sphere(spheres, s):

  touching_spheres = []
  c = s.get_center()

  for sp in spheres:
    center = sp.get_center()

    radiussum = s.get_radius() + sp.get_radius()
    if (center.get_distance_from(c) <= radiussum):
      touching_spheres.append(sp)

  return touching_spheres

###############################################################################

def rotate_sphere (near_spheres, touching_spheres, s):

  if (len(touching_spheres) == 1):
    p0 = touching_spheres[0].get_center()
    
    p1x = random.uniform(common.botx, common.topx)
    p1y = random.uniform(common.boty, common.topy)
    p1z = p0.get_z()
    
    p1 = point.point(p1x, p1y, p1z)

    touching_spheres_now = rotate_as_possible(s, p0, p1, near_spheres, 2)

    if (len(touching_spheres_now) == 2):
      p0 = touching_spheres_now[0].get_center()
      p1 = touching_spheres_now[1].get_center()

      rotate_as_possible(s, p0, p1, near_spheres, 3)

  elif (len(touching_spheres) == 2):
    p0 = touching_spheres[0].get_center()
    p1 = touching_spheres[1].get_center()

    touching_spheres_now = rotate_as_possible(s, p0, p1, near_spheres, 3)

  return

###############################################################################

def rotate_as_possible(s, p0, p1, near_spheres, numbertostop):
    
  touching_spheres_now = []

  dtetha = common.dtetha_start 
  tetha = 0.0
  
  c = s.get_center()
  radius = s.get_radius()
  
  lowest_c = c
  
  while tetha < (2.0 * math.pi):
    tetha += dtetha
    c_start = c
  
    c = util.point_rotate (p0, p1, c, tetha)
    s.set_center(c)
  
    #if (((c.get_z() - radius) < common.botz) or 
    #    ((c.get_z() + radius) > common.topz) or \
    #    ((c.get_x() - radius) < common.botx) or 
    #    ((c.get_x() + radius) > common.topx) or \
    #    ((c.get_y() - radius) < common.boty) or 
    #    ((c.get_y() + radius) > common.topy)):
    #  dtetha = dtetha/10.0
    #  if dtetha <= common.min_dtetha:
    #    if (c.get_z() < lowest_c.get_z()):
    #      lowest_c = c
    #    break
    #  else:
    #    c = c_start
  
    touching_spheres_now = touched_other_sphere(near_spheres, s)
    if (len(touching_spheres_now) >= numbertostop):
      dtetha = dtetha/10.0
      if dtetha <= common.min_dtetha:
        if (c.get_z() < lowest_c.get_z()):
          lowest_c = c
        break
      else:
        c = c_start
        s.set_center(c)
  
    if (c.get_z() < lowest_c.get_z()):
      lowest_c = c
  
  if (lowest_c.get_z() < c.get_z()):
    c = lowest_c
    s.set_center(c)
  
  return touching_spheres_now

###############################################################################
