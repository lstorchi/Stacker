import common

import triangle
import circle
import point
import line

import math

NUMOFCIRCLEPOINTS = 180

# provo a tagliare punti oltre una certa distanza di modo da rendere 
# il calcolo della PSD piu' realistico
MAXDISTANCEFORP = 3.5*common.R

# non elimino nessun punto cosi' cerco di capire che permibilita' inserire per
# ottenere i valori desiderati
# MAXDISTANCEFORP = float("inf")

###############################################################################

def point_distance(p1, p2):

  dx = p1[0] - p2[0]
  dy = p1[1] - p2[1]

  return math.sqrt(dx**2 + dy**2)

###############################################################################

def get_quadrant_respect_to (point, p0):
  
  x = point[0] - p0[0]
  y = point[1] - p0[1]

  if (x >= 0.0) and (y >= 0.0):
    return 1
  elif (x < 0.0) and (y >= 0.0):
    return 2
  elif (x < 0.0) and (y < 0.0):
    return 3
  elif (x >= 0.0) and (y < 0.0):
    return 4

###############################################################################

def get_radius (center, poly_data_points, zplane):

  totarea = 0.0
  for i in range(len(poly_data_points)-1):

    j = i + 1
  
    a = point.point(poly_data_points[i][0], 
        poly_data_points[i][1], zplane)
    b = point.point(poly_data_points[j][0],
        poly_data_points[j][1], zplane)
    c =  point.point(center[0], center[1], zplane)
  
    totarea += triangle.area_of_triangle(a, b, c)

  # aggiungi anche l'ultimo triangolo co unque sia anche se siamo al bordo
  # credo sia meglio prenderlo in cosnsiderazione
  a = point.point(poly_data_points[0][0],
      poly_data_points[0][1], zplane)
  b = point.point(poly_data_points[len(poly_data_points)-1][0],
      poly_data_points[len(poly_data_points)-1][1], zplane)
  c =  point.point(center[0], center[1], zplane)

  totarea += triangle.area_of_triangle(a, b, c)

  return circle.get_radius_given_area(totarea)

###############################################################################

def get_circle_in_plane (spheres, zplane):

  spheres_in_plane = []

  for s in spheres:

    r = s.get_radius()
    c = s.get_center()

    cx = c.get_x()
    cy = c.get_y()
    cz = c.get_z()
  
    if (zplane >= (cz - r)) and (zplane <= (cz + r)):
      spheres_in_plane.append(s)

  circles = []

  for s in spheres_in_plane:
    r = s.get_radius()
    c = s.get_center()
    
    cx = c.get_x()
    cy = c.get_y()
    cz = c.get_z()
    
    circler = math.sqrt(math.pow(r, 2) - math.pow((zplane-cz),2))
    
    cir = circle.circle(cx, cy, circler)
    circles.append(cir)

  return circles

###############################################################################

def is_inside_circles (x, y, circles):

  inside = False
  for cir in circles:
    if (cir.is_point_inside(x, y)):
      return True
      
  return False

###############################################################################

def get_circle_points_list (x, y, circles):

  poly_data_points = []
  
  # x , y e' il primo punto cell retta
  # per generare i secondi punti della circonferenza uso circle
  point_circle = circle.circle(x, y, 1.0)
  second_points = point_circle.generate_circle_points(NUMOFCIRCLEPOINTS)
  
  #print len(second_points)
  
  for pi in second_points:
    l = line.line2d()
    l.set_two_point([x, y], pi)
  
    ref_quadrant = get_quadrant_respect_to (pi, [x, y])
  
    #print "quadrant: ", ref_quadrant
  
    closet_point = [x, y]
    closet_point_min_d = float("inf")
  
    for cir in circles:
      int_points = circle.line_circle_intersection(cir, l)
  
      selected_point = [x, y]
      min_distance = float("inf")
      for ip in int_points:
        if (get_quadrant_respect_to (ip, [x, y]) == ref_quadrant):
          d = point_distance(ip, [x, y])
          if (d > 0.0):
            if (d < min_distance):
              min_distance = d
              selected_point = ip
  
      d = point_distance(selected_point, [x, y])
  
      if d > 0.0:
       if (d < closet_point_min_d):
         closet_point_min_d = d
         closet_point = selected_point
  
    if point_distance(closet_point, [x, y]) > 0.0 :
  
      poly_data_points.append(closet_point)

  return poly_data_points

###############################################################################
