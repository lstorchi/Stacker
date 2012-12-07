import point
import math
import sys

###############################################################################

def closest_point_to_triangle (p, a, b, c):

  ab = b - a
  ac = c - a
  ap = p - a

  d1 = dot(ab, ap)
  d2 = dot(ac, ap)

  if (d1 <= 0.0 and d2 <= 0.0):
    return a 

  bp = p - b

  d3 = dot(ab, bp)
  d4 = dot(ac, bp)
  
  if (d3 >= 0.0 and d4 <= d3):
    return b

  vc = d1*d4 - d3*d2

  if (vc <= 0.0 and d1 >= 0.0 and d3 <= 0.0):
    v = d1 / (d1 - d3)
    return a + sxv(v, ab)

  cp = p - c;
  d5 = dot(ab, cp)
  d6 = dot(ac, cp)
  
  if (d6 >= 0.0 and d5 <= d6):
    return c

  vb = d5*d2 - d1*d6;
  if (vb <= 0.0 and d2 > 0.0 and d6 <= 0.0):
    w = d2 / (d2 - d6)
    return a + sxv(w, ac)
  
  va = d3*d6 - d5*d4;
  if (va <= 0.0 and (d4 - d3) >= 0.0 and (d5 - d6) >= 0.0):
    w = (d4 - d3) / ((d4 - d3) + (d5 - d6))
    return b + sxv(w, (c - b))

  denom = 1.0 / (va + vb + vc)
  v = vb * denom
  w = vc * denom

  return a + ab * v + ac * w

###############################################################################

def point_outside_of_plane (p, a, b, c):
  return dot(p - a, cross(b - a, c - a)) >= 0.0

###############################################################################

def dot (a, b):

  r = a.get_x() * b.get_x() + \
      a.get_y() * b.get_y() + \
      a.get_z() * b.get_z()

  return r

###############################################################################

def cross (a, b):

  p = point.point()

  p.set_x(a.get_y() * b.get_z() - a.get_z() * b.get_y() )
  p.set_y(a.get_z() * b.get_x() - a.get_x() * b.get_z() )
  p.set_z(a.get_x() * b.get_y() - a.get_y() * b.get_x() )

  return p

###############################################################################

def sxv (scalar, v):

  w = point.point(v.get_x() * scalar, \
      v.get_y() * scalar, \
      v.get_z() * scalar)

  return w

###############################################################################

def area_of_triangle (A, B, C):

  ab = A - B
  ac = A - C

  tosqrt = dot(ab, ab) * dot(ac, ac) - dot(ab, ac)**2

  if (tosqrt >= 0.0):
    area = 0.5 * math.sqrt(tosqrt)
  else:
    print >> sys.stderr, "error in area of: "
    print >> sys.stderr, " A: ", A
    print >> sys.stderr, " B: ", B
    print >> sys.stderr, " C: ", C
    area = 0.0

  return area

###############################################################################

def scalar_triple(pq, pc, pb):
  m = cross(pq, pc)
  return dot(pb, m)

###############################################################################

def same_sign(a, b):
  return (a >= 0.0) == (b >= 0.0)

###############################################################################
"""
def intersect_line_triangle(p, q, a, b, c):

  pq = q - p
  pa = a - p
  pb = b - p
  pc = c - p

  u = v = w = float("inf")

  m = cross(pq, pc)
  u = dot(pb, m)
  v = -dot(pa, m)
  if (not same_sign (u, v)):
    return False, u, v, w
  w = scalar_triple(pq, pb, pa);
  if (not same_sign(u, w)):
    return False, u, v, w

  denom = 1.0 / (u + v + w)
  u *= denom
  v *= denom
  w *= denom

  return True, u, v, w
"""
###############################################################################

# http://softsurfer.com/Archive/algorithm_0105/algorithm_0105.htm#intersect_RayTriangle%28%29

def intersect_ray_triangle (p0, p1, v0, v1, v2):
  SMALL_NUM = 0.00000001
  I = point.point(float("inf"), float("inf"), float("inf"))

  u = v1 - v0
  v = v2 - v0
  n = cross(u, v)       

  if (n.get_x() == 0.0 and n.get_y() == 0.0 and n.get_z() == 0.0):
    return -1, I # triangle is degenerate non consideriamo questo caso

  dir = p1 - p0
  w0 = p0 - v0
  a = -dot(n, w0)
  b = dot(n, dir)
  if (math.fabs(b) < SMALL_NUM): # ray is parallel to triangle plane
    if (a == 0.0):
      return 2, I # ray lies in triangle plane
    else: 
      return 0, I # il segmento e' fuori dal piano 

  r = a / b;
  if (r < 0.0):
    return 0, I # no intersect

  I = p0 + dir * r

  uu = dot(u,u)
  uv = dot(u,v)
  vv = dot(v,v)
  w = I - v0
  wu = dot(w,u)
  wv = dot(w,v)
  D = uv * uv - uu * vv

  s = (uv * wv - vv * wu) / D
  if (s < 0.0 or s > 1.0):
    return 0, I # I is outside T
  t = (uv * wu - uu * wv) / D
  if (t < 0.0 or (s + t) > 1.0):
    return 0, I # I is outside T

  return 1, I # intersezione trovata

###############################################################################

