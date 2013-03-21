import vtk
import util
import math
import point
import numpy
import plane
import triangle

POINTINSIDEDIM = 10
POINTINSURFACESTEP = float('inf')

class nanotio2:

  __pts = [[0,4,6,2], [6,7,3,2], \
           [7,5,1,3], [0,4,5,1], \
           [0,8,10,2], [2,3,11,10], \
           [1,3,11,9], [0,1,9,8], \
           [8,9,11,10], [4,5,7,6]]


  def __init__ (self, cx = 0.0, cy = 0.0, cz = 0.0, A = 10.7, 
      B = 23.6, H = 34.0):

    #self._d = numpy.linspace( 0.0, 0.0, 12)

    self._fixed = False

    self._cx = 0.0
    self._cy = 0.0
    self._cz = 0.0
    self._H = 1.0
    self._A = 1.0
    self._B = 1.0

    # not call set center and dimentsion to avoid call compute trhree time

    self._p1 = point.point(cx, cy, cz)
    self._p2 = point.point(cx, cy, cz)

    self._cx = cx
    self._cy = cy
    self._cz = cz

    if H == 0.0:
      H = 34.0

    if B == 0.0:
      B = 23.6

    if A == 0.0:
      A = 10.7

    self._H = H
    self._A = A
    self._B = B

    self.__compute()

  def set_fixed (self):
    self._fixed = True


  def get_fixed (self):
    return self._fixed;


  def get_distance (self, pp):

    dist = float("inf")

    p = self._UP_pright.project_point(pp)
    if (self.__is_in_polyhedra(0, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(0, pp)
      if (d < dist):
        dist = d

    p = self._UP_pback.project_point(pp) 
    if (self.__is_in_polyhedra(1, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(1, pp)
      if (d < dist):
        dist = d

    p = self._UP_pleft.project_point(pp) 
    if (self.__is_in_polyhedra(2, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(2, pp)
      if (d < dist):
        dist = d

    p = self._UP_pfront.project_point(pp) 
    if (self.__is_in_polyhedra(3, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(3, pp)
      if (d < dist):
        dist = d

    p = self._UP_ptop.project_point(pp) 
    if (self.__is_in_polyhedra(4, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(4, pp)
      if (d < dist):
        dist = d

    p = self._DOWN_pright.project_point(pp) 
    if (self.__is_in_polyhedra(5, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(5, pp)
      if (d < dist):
        dist = d

    p = self._DOWN_pback.project_point(pp) 
    if (self.__is_in_polyhedra(6, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(6, pp)
      if (d < dist):
        dist = d

    p = self._DOWN_pleft.project_point(pp) 
    if (self.__is_in_polyhedra(7, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(7, pp)
      if (d < dist):
        dist = d

    p = self._DOWN_pfront.project_point(pp) 
    if (self.__is_in_polyhedra(8, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(8, pp)
      if (d < dist):
        dist = d

    p = self._DOWN_pbottom.project_point(pp) 
    if (self.__is_in_polyhedra(9, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
    else:
      d = self.__get_perimeter_distance(9, pp)
      if (d < dist):
        dist = d


    return dist


  def project_point (self, pp):

    dist = float("inf")
    pret = point.point()

    p = self._UP_pright.project_point(pp)
    if (self.__is_in_polyhedra(0, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(0, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    p = self._UP_pback.project_point(pp) 
    if (self.__is_in_polyhedra(1, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(1, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    p = self._UP_pleft.project_point(pp) 
    if (self.__is_in_polyhedra(2, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(2, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    p = self._UP_pfront.project_point(pp) 
    if (self.__is_in_polyhedra(3, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(3, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    p = self._UP_ptop.project_point(pp) 
    if (self.__is_in_polyhedra(4, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(4, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    p = self._DOWN_pright.project_point(pp) 
    if (self.__is_in_polyhedra(5, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(5, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    p = self._DOWN_pback.project_point(pp) 
    if (self.__is_in_polyhedra(6, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(6, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    p = self._DOWN_pleft.project_point(pp) 
    if (self.__is_in_polyhedra(7, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(7, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    p = self._DOWN_pfront.project_point(pp) 
    if (self.__is_in_polyhedra(8, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(8, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    p = self._DOWN_pbottom.project_point(pp) 
    if (self.__is_in_polyhedra(8, p)):
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p
    else:
      p = self.__get_perimeter_point(9, pp)
      d = p.get_distance_from(pp)
      if (d < dist):
        dist = d
        pret = p

    return pret


  def set_center(self, cx = 0.0, cy = 0.0, cz = 0.0):
    self._cx = cx
    self._cy = cy
    self._cz = cz

    self._p1 = point.point(cx, cy, cz)

    self.__compute()


  def get_center(self):
    return self._cx, self._cy, self._cz


  def get_max_sphere(self):

    maxdist = -1.0

    NUMOFP = len(self._x)

    for i in range(NUMOFP):
      p0 = point.point(self._x[i][0], self._x[i][1], self._x[i][2])
      d = p0.get_distance_from(point.point(self._cx, self._cy, self._cz))
      if (d > maxdist):
        maxdist = d

    return maxdist


  def set_dimensions (self, A = 10.7, B = 23.6, H = 34.0):

    if H == 0.0:
      H = 34.0

    if B == 0.0:
      B = 23.6

    if A == 0.0:
      A = 10.7

    self._H = H
    self._A = A
    self._B = B

    self.__compute()


  def get_triangle_points (self):
    return self._triangles_points
      

  def get_dimensions (self):
    return self._A, self._B, self._H


  def get_to_print (self):
    return self._cx, self._cy, self._cz, \
        self._A, self._B, self._H, self._p2.get_x(), \
        self._p2.get_y(), self._p2.get_z(), self._theta

  
  def get_theta (self):
    return self._theta


  def get_p2 (self):
    return self._p2


  def get_edge_points (self):
 
    return self._x


  def get_points_connection (self):

    return self.__pts


  def get_polydata(self):
    return self._polydata

 
  def get_rotation_info (self):
    return self._p1, self._p2, self._theta
  

  def rotate_nanoparticle (self, p1, p2, theta):

    self._p1 = p1
    self._p2 = p2
    self._theta = theta

    NUMOFP = len(self._x)

    for i in range(NUMOFP):
      p0 = point.point(self._x[i][0], self._x[i][1], self._x[i][2])
      p0 = util.point_rotate(p1, p2, p0, theta)
      self._x[i][0] = p0.get_x()
      self._x[i][1] = p0.get_y()
      self._x[i][2] = p0.get_z()

    # faccio cosi' altrimenti annullo le label
    for i in range(len(self._pinside_list)):
      p = self._pinside_list[i]
      p = util.point_rotate(p1, p2, p, theta)
      self._pinside_list[i].set_x(p.get_x())
      self._pinside_list[i].set_y(p.get_y())
      self._pinside_list[i].set_z(p.get_z())

    for i in range(len(self._psurface_list)):
      #print "Rotate: \"", self._psurface_list[i].get_label(), "\""
      p = self._psurface_list[i]
      p = util.point_rotate(p1, p2, p, theta)
      self._psurface_list[i].set_x(p.get_x())
      self._psurface_list[i].set_y(p.get_y())
      self._psurface_list[i].set_z(p.get_z())
      #print "Rotate: \"", self._psurface_list[i].get_label(), "\""

    self.__compute_triangles()
    self.__compute_polydata()
    self.__compute_plane()


  def get_vtk_actor (self, color = False, opacity = 1.0):

    if color:
      self.__compute_triangles()
      self.__compute_polydata(color)
      self.__compute_plane()
   
    nanopMapper = vtk.vtkPolyDataMapper()
    nanopMapper.SetInput(self._polydata)

    if not color:
      nanopMapper.SetScalarRange(0,1)

    nanopActor = vtk.vtkActor()
    nanopActor.SetMapper(nanopMapper)
    nanopActor.GetProperty().SetOpacity(opacity)

    if color:
      nanopActor.GetProperty().SetColor(1,1,1)

    return nanopActor


  def get_surface (self):

    count001 = 0
    count101 = 0
    for i in range(len(self._psurface_list)):
      label = self._psurface_list[i].get_label()
      if (label == "001"):
        count001 = count001 + 1
      elif (label == "101"):
        count101 = count101 + 1

    #print "rapporto: ", float(count101)/float(count001)

    p1  = point.point(self._x[0][0], self._x[0][1], self._x[0][2])
    p2  = point.point(self._x[1][0], self._x[1][1], self._x[1][2])
    p3  = point.point(self._x[2][0], self._x[2][1], self._x[2][2])
    p4  = point.point(self._x[3][0], self._x[3][1], self._x[3][2])
    p5  = point.point(self._x[4][0], self._x[4][1], self._x[4][2])
    p6  = point.point(self._x[5][0], self._x[5][1], self._x[5][2])
    p7  = point.point(self._x[6][0], self._x[6][1], self._x[6][2])
    p8  = point.point(self._x[7][0], self._x[7][1], self._x[7][2])
    p9  = point.point(self._x[8][0], self._x[8][1], self._x[8][2])
    p10 = point.point(self._x[9][0], self._x[9][1], self._x[9][2])
    p11 = point.point(self._x[10][0], self._x[10][1], self._x[10][2])
    p12 = point.point(self._x[11][0], self._x[11][1], self._x[11][2])

    areaUP_top = triangle.area_of_triangle (p5, p6, p8) + \
                 triangle.area_of_triangle (p5, p8, p7)
    areaUP_right = triangle.area_of_triangle (p1, p2, p5) + \
                   triangle.area_of_triangle (p5, p2, p6)
    areaUP_left = triangle.area_of_triangle (p3, p4, p8) + \
                  triangle.area_of_triangle (p8, p3, p7)
    areaUP_back = triangle.area_of_triangle (p2, p4, p8) + \
                  triangle.area_of_triangle (p8, p2, p6)
    areaUP_front = triangle.area_of_triangle (p1, p3, p5) + \
                   triangle.area_of_triangle (p5, p3, p7)

    #print areaUP_top, areaUP_right, areaUP_left, areaUP_back, areaUP_front

    areaDOWN_bottom = triangle.area_of_triangle (p9, p10, p12) + \
                   triangle.area_of_triangle (p12, p9, p11)
    areaDOWN_right = triangle.area_of_triangle (p10, p12, p2) + \
                     triangle.area_of_triangle (p2, p12, p4)
    areaDOWN_back  = triangle.area_of_triangle (p12, p11, p4) + \
                     triangle.area_of_triangle (p4, p11, p3)
    areaDOWN_left  = triangle.area_of_triangle (p9, p11, p1) + \
                     triangle.area_of_triangle (p1, p11, p3)
    areaDOWN_front = triangle.area_of_triangle (p9, p10, p2) + \
                     triangle.area_of_triangle (p2, p9, p1)

    #print areaDOWN_bottom, areaDOWN_right, areaDOWN_left, areaDOWN_back, areaDOWN_front

    area = areaUP_top + areaUP_right + areaUP_left + areaUP_back + areaUP_front + \
        areaDOWN_bottom + areaDOWN_right + areaDOWN_left + areaDOWN_back + areaDOWN_front

    #print "rapporto analitico: ", (8.0*areaUP_right)/(2.0*areaUP_top)

    return area, areaUP_top, areaUP_right, areaUP_left, areaUP_back, areaUP_front, \
           areaDOWN_bottom, areaDOWN_right, areaDOWN_left, areaDOWN_back, areaDOWN_front


  def get_volume (self):

    # http://www.emathzone.com/tutorials/geometry/frustum-of-a-pyramid.html
    # volume of a frustum of a pyramid

    A1 = self._A * self._A
    A2 = self._B * self._B
    h = self._H

    #print "dim: ", A1, A2, h

    volume = (1.0/3.0) * h * (A1 + A2 + math.sqrt(A1*A2))

    return (volume)


  def is_point_inside (self, p):
    # forse mi perdo i punti in superficie
    # molto liberamente ispirato a questo:
    # http://www.gamedev.net/topic/593430-finding-out-whether-a-point-is-in-a-frustum/

    ptc = point.point(p[0], p[1], p[2])

    if (self._UP_pright.check_point_side (ptc) !=
        self._UP_pleft.check_point_side (ptc)):
      if (self._UP_pbottom.check_point_side (ptc) != 
          self._UP_ptop.check_point_side (ptc)):
        if (self._UP_pback.check_point_side (ptc) !=
            self._UP_pfront.check_point_side (ptc)):
          return True

    if (self._DOWN_pright.check_point_side (ptc) !=
        self._DOWN_pleft.check_point_side (ptc)):
      if (self._DOWN_pbottom.check_point_side (ptc) != 
          self._DOWN_ptop.check_point_side (ptc)):
        if (self._DOWN_pback.check_point_side (ptc) !=
            self._DOWN_pfront.check_point_side (ptc)):
          return True

    return False


  def is_point_in_surface (self, p):

    ptc = point.point(p[0], p[1], p[2])

    return self._is_point_in_surface (ptc)


  def sphere_touch_me (self, s):

    mycenter = point.point(self._cx, self._cy, self._cz)

    dist = mycenter.get_distance_from(s.get_center())

    if (dist < s.get_radius()):
      return True

    #print "here"

    # in caso non si verificata questa condixione devo fare analisi piu'
    # accurata mediante punti generati all'inteno della sfera e controllo se
    # alcuni punti sono inclusi o meno
    # genero tante sfere con raggio a partire dal raggio della sfera stessa ed a
    # diminuire fino ad arrivare al centro della sfera ed ogni volta verifico
    # che se i punti in superficie sono o meno dentro la nanoparticella.

    surface_points = s.generate_surface_points(20)

    for p in surface_points:
      if (self.is_point_inside ([p.get_x(), 
        p.get_y(), p.get_z()])):
        return True

    return False


  def sphere_touch_me_surface_points (self, radius, center, 
      surface_points):

    mycenter = point.point(self._cx, self._cy, self._cz)

    dist = mycenter.get_distance_from(center)

    if (dist < radius):
      return True

    for p in surface_points:
      if (self.is_point_inside ([p.get_x(), 
        p.get_y(), p.get_z()])):
        return True


    return False


  def closest_point_outside (self, p):

    # si immagina di aver fatto' il check che il punto sia 
    # fuori dal poliedro, al;trimqnti questo test potrebbe non funzionare 

    closest_point = p

    best_sq_dist = float('inf')

    for p1, p2, p3 in self._triangles_points:
      q = triangle.closest_point_to_triangle(p, p1, p2, p2)
      sq_dist = triangle.dot(q - p, q - p)
      if (sq_dist < best_sq_dist): 
        best_sq_dist = sq_dist 
        closest_point = q

    return closest_point


  def closest_point_outside_list (self, p):

    # si immagina di aver fatto' il check che il punto sia 
    # fuori dal poliedro, al;trimqnti questo test potrebbe non funzionare 

    closest_point = []

    for p1, p2, p3 in self._triangles_points:
      q = triangle.closest_point_to_triangle(p, p1, p2, p2)
      closest_point.append(q)

    return closest_point


  def nanoparticle_touch_me (self, nanop):
  
    mycenter = point.point(self._cx, self._cy, self._cz)
    cx, cy, cz = nanop.get_center() 
    hiscenter = point.point(cx, cy, cz)
    sumr = self.get_max_sphere() + nanop.get_max_sphere()

    for p in nanop.inside_point_grid():
      if (p.get_distance_from(mycenter) <= sumr):
        if (self.is_point_inside([p.get_x(), p.get_y(), p.get_z()]) or \
            self.is_point_in_surface([p.get_x(), p.get_y(), p.get_z()])):
          return True

    for p in self.inside_point_grid():
      if (p.get_distance_from(hiscenter) <= sumr):
        if (nanop.is_point_inside([p.get_x(), p.get_y(), p.get_z()]) or \
            nanop.is_point_in_surface([p.get_x(), p.get_y(), p.get_z()])):
          return True
 
    return False


  def intersect_line (self, p, q):

    ipoints = []

    for tr in self._triangles_points:
      u = v = w = 0.0

      rval, ip = triangle.intersect_ray_triangle(p, q, tr[0], tr[1], tr[2])

      if (rval == 1):
        ipoints.append([ip.get_x(), ip.get_y(), ip.get_z()])

      #inters, u, v, w = \
      #    triangle.intersect_line_triangle(p, q, tr[0], tr[1], tr[2])
      #
      #if inters:
      #  ipoints.append([u, v, w])

    return ipoints

  def inside_point_grid (self):

    return self._pinside_list


  def get_surface_points (self):

    return self._psurface_list

  
###############################################################################
# PRIVATE
###############################################################################

  def __compute(self):

    self._x=[ \
       [self._cx-(self._B/2.0), self._cy-(self._B/2.0), self._cz], \
       [self._cx+(self._B/2.0), self._cy-(self._B/2.0), self._cz], \
       [self._cx-(self._B/2.0), self._cy+(self._B/2.0), self._cz], \
       [self._cx+(self._B/2.0), self._cy+(self._B/2.0), self._cz], \
       [self._cx-(self._A/2.0), self._cy-(self._A/2.0), self._cz+(self._H/2.0)], \
       [self._cx+(self._A/2.0), self._cy-(self._A/2.0), self._cz+(self._H/2.0)], \
       [self._cx-(self._A/2.0), self._cy+(self._A/2.0), self._cz+(self._H/2.0)], \
       [self._cx+(self._A/2.0), self._cy+(self._A/2.0), self._cz+(self._H/2.0)], \
       [self._cx-(self._A/2.0), self._cy-(self._A/2.0), self._cz-(self._H/2.0)], \
       [self._cx+(self._A/2.0), self._cy-(self._A/2.0), self._cz-(self._H/2.0)], \
       [self._cx-(self._A/2.0), self._cy+(self._A/2.0), self._cz-(self._H/2.0)], \
       [self._cx+(self._A/2.0), self._cy+(self._A/2.0), self._cz-(self._H/2.0)]]

    # scompongo in 20 triangoli
    self._triangles = [[0 , 6 , 4 ], \
                       [0 , 6 , 2 ], \
                       [2 , 7 , 6 ], \
                       [2 , 3 , 7 ], \
                       [3 , 5 , 1 ], \
                       [3 , 7 , 5 ], \
                       [0 , 5 , 4 ], \
                       [0 , 1 , 5 ], \
                       [4 , 7 , 6 ], \
                       [7 , 4 , 5 ], \
                       [0 , 10, 8 ], \
                       [0 , 10, 2 ], \
                       [2 , 11, 10], \
                       [2 , 11, 3 ], \
                       [1 , 3 , 9 ], \
                       [3 , 9 , 11], \
                       [0 , 1 , 9 ], \
                       [0 , 9 , 8 ], \
                       [8 , 9 , 10], \
                       [10, 9 , 11]]

    #10 poliedri i punti sono ordinati orario o antiorario
    self._polyhedra = [[0 ,  1,  5,  4],   # _UP_pright
                       [1 ,  3,  7,  5],   # _UP_pback
                       [3 ,  2,  6,  7],   # _UP_pleft
                       [2 ,  6,  4,  0],   # _UP_pfront
                       [4 ,  5,  7,  6],   # _UP_ptop
                       [0 ,  1,  9,  8],   # _DOWN_pright
                       [9 ,  1,  3, 11],   # _DOWN_pback
                       [11, 10,  2,  3],   # _DOWN_pleft 
                       [10,  2,  0,  8],   # _DOWN_pfront
                       [ 8,  9, 11, 10]]   # _DOWN_pbottom 


    self.__compute_triangles()
    self.__compute_polydata()
    self.__compute_plane()
    self.__compute_point_inside()
    self.__compute_point_in_surface()

  
  def __compute_point_in_surface(self):

    self._psurface_list = []

    if (POINTINSURFACESTEP != float('inf')) :
      # 10 poliedri in self._polyhedra
      for i in range(10):
        #print "Poly: ", i+1
        label = ""
        if ((i == 4) or (i == 9)):
          label = "001"
        else:
          label = "101"
     
        idx1 = self._polyhedra[i][0]
        p1 = point.point(self._x[idx1][0], self._x[idx1][1], self._x[idx1][2])
        idx2 = self._polyhedra[i][1]
        p2 = point.point(self._x[idx2][0], self._x[idx2][1], self._x[idx2][2])
        idx3 = self._polyhedra[i][2]
        p3 = point.point(self._x[idx3][0], self._x[idx3][1], self._x[idx3][2])
        idx4 = self._polyhedra[i][3]
        p4 = point.point(self._x[idx4][0], self._x[idx4][1], self._x[idx4][2])
     
        util.generate_point_inside_poly(p1, p2, p3, p4, POINTINSURFACESTEP, 
            self._psurface_list, label)
        #print "Compute: \"", self._psurface_list[-1].get_label(), "\""


  def __compute_triangles (self):

    NUMOFTRIANGLE = len(self._triangles)

    self._triangles_points = []

    for i in range(NUMOFTRIANGLE):
      p1 = point.point(self._x[self._triangles[i][0]][0], \
          self._x[self._triangles[i][0]][1], \
          self._x[self._triangles[i][0]][2])
      p2 = point.point(self._x[self._triangles[i][1]][0], \
          self._x[self._triangles[i][1]][1], \
          self._x[self._triangles[i][1]][2])
      p3 = point.point(self._x[self._triangles[i][2]][0], \
          self._x[self._triangles[i][2]][1], \
          self._x[self._triangles[i][2]][2])

      self._triangles_points.append([p1, p2, p3])


  def __compute_polydata(self, color = False):

    self._polydata = vtk.vtkPolyData()

    NUMOFP = len(self._x)
    NUMOFPTS = len(self.__pts)
    
    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()
    scalars = vtk.vtkFloatArray()
    
    for i in range(NUMOFP):
      points.InsertPoint(i,self._x[i])
      #if not color:
        #scalars.InsertTuple1(i,i)
        #scalars.InsertTuple1(1,1)
    
    if not color:
      if (NUMOFP == 12):
        scalars.InsertTuple1(0,0)
        scalars.InsertTuple1(1,0)
        scalars.InsertTuple1(2,0)
        scalars.InsertTuple1(3,0)

        scalars.InsertTuple1(4,1)
        scalars.InsertTuple1(5,1)
        scalars.InsertTuple1(6,1)
        scalars.InsertTuple1(7,1)
  
        scalars.InsertTuple1(8,1)
        scalars.InsertTuple1(9,1)
        scalars.InsertTuple1(10,1)
        scalars.InsertTuple1(11,1)
      else:
        for i in range(NUMOFP):
          scalars.InsertTuple1(i,i)


    for i in range(NUMOFPTS):
      ids = vtk.vtkIdList()
      ids.SetNumberOfIds(4)
      for j in range(4):
        ids.SetId(j, self.__pts[i][j])
    
      polys.InsertNextCell(ids)
    
    self._polydata.SetPoints(points)
    self._polydata.SetPolys(polys)
    if not color:
      self._polydata.GetPointData().SetScalars(scalars)

    #maskprop = vtk.vtkMassProperties()
    #maskprop.SetInput(self._polydata)
    #print maskprop.GetVolume()

    return self._polydata


  def __compute_plane(self): 

    # forse mi perdo i punti in superficie
    # molto liberamente ispirato a questo:
    # http://www.gamedev.net/topic/593430-finding-out-whether-a-point-is-in-a-frustum/
    # calcolo qui i piani che uso poi 

    h1_p1 = point.point(self._x[0][0], self._x[0][1], self._x[0][2])
    h1_p2 = point.point(self._x[1][0], self._x[1][1], self._x[1][2])
    h1_p3 = point.point(self._x[2][0], self._x[2][1], self._x[2][2])
    h1_p4 = point.point(self._x[3][0], self._x[3][1], self._x[3][2])
    h1_p5 = point.point(self._x[4][0], self._x[4][1], self._x[4][2])
    h1_p6 = point.point(self._x[5][0], self._x[5][1], self._x[5][2])
    h1_p7 = point.point(self._x[6][0], self._x[6][1], self._x[6][2])
    h1_p8 = point.point(self._x[7][0], self._x[7][1], self._x[7][2])

    self._UP_pright = plane.plane (h1_p1, h1_p2, h1_p5)
    self._UP_pleft = plane.plane (h1_p3, h1_p4, h1_p8)
    self._UP_pbottom = plane.plane (h1_p1, h1_p2, h1_p3)
    self._UP_ptop = plane.plane (h1_p8, h1_p5, h1_p6)
    self._UP_pback = plane.plane (h1_p2, h1_p4, h1_p8)
    self._UP_pfront = plane.plane (h1_p1, h1_p3, h1_p5)

    h2_p1 = point.point(self._x[0][0], self._x[0][1], self._x[0][2])
    h2_p2 = point.point(self._x[1][0], self._x[1][1], self._x[1][2])
    h2_p3 = point.point(self._x[2][0], self._x[2][1], self._x[2][2])
    h2_p4 = point.point(self._x[3][0], self._x[3][1], self._x[3][2])
    h2_p5 = point.point(self._x[8][0], self._x[8][1], self._x[8][2])
    h2_p6 = point.point(self._x[9][0], self._x[9][1], self._x[9][2])
    h2_p7 = point.point(self._x[10][0], self._x[10][1], self._x[10][2])
    h2_p8 = point.point(self._x[11][0], self._x[11][1], self._x[11][2])

    self._DOWN_pright = plane.plane (h2_p1, h2_p2, h2_p6)
    self._DOWN_pleft = plane.plane (h2_p7, h2_p3, h2_p8)
    self._DOWN_pbottom = plane.plane (h2_p5, h2_p6, h2_p7)
    self._DOWN_ptop = plane.plane (h2_p4, h2_p1, h2_p2)
    self._DOWN_pback = plane.plane (h2_p6, h2_p2, h2_p4)
    self._DOWN_pfront = plane.plane (h2_p7, h2_p5, h2_p1)

  def __compute_point_inside(self):

    dn = POINTINSIDEDIM
    dx = dy = self._B / float(dn+1)
    dz = self._H / float(dn+1) 

    self._pinside_list = []

    x1 = self._x[0][0]
    y1 = self._x[0][1]
    z1 = self._x[0][2] - self._H/2.0

    for i in range(dn+2):
      x = x1 + float(i) * dx
      for j in range(dn+2):
        y = y1 + float(j) * dy
        for k in range(dn+2):
          z = z1 + float(k) * dz
          p = point.point(x, y, z)
          if self.is_point_inside ([x, y, z]) or \
             self.is_point_in_surface ([x, y, z]):
            self._pinside_list.append(p)

    for i in range(len(self._x)):
      p = point.point(self._x[i][0], \
          self._x[i][1], self._x[i][2])
      self._pinside_list.append(p)

    return


  def __is_in_polyhedra (self, idx, ptc):
    
    ti = self._polyhedra[idx]

    polypoint = []
    polypoint.append(point.point(self._x[ti[0]][0], \
        self._x[ti[0]][1], self._x[ti[0]][2]))
    polypoint.append(point.point(self._x[ti[1]][0], \
        self._x[ti[1]][1], self._x[ti[1]][2]))
    polypoint.append(point.point(self._x[ti[2]][0], \
        self._x[ti[2]][1], self._x[ti[2]][2]))
    polypoint.append(point.point(self._x[ti[3]][0], \
        self._x[ti[3]][1], self._x[ti[3]][2]))

    diff = math.fabs(util.angle_sum_poly(polypoint, ptc) - util.TWOPI)
    if (diff < 1e-10):
      return True

    return False


  def __get_perimeter_point (self, idx, ptc):

    ti = self._polyhedra[idx]

    a = point.point(self._x[ti[0]][0], self._x[ti[0]][1], \
        self._x[ti[0]][2])
    b = point.point(self._x[ti[1]][0], self._x[ti[1]][1], \
        self._x[ti[1]][2])
    pret = util.closest_point_point_segment(a, b, ptc)
    dist = pret.get_distance_from(ptc)

    a = point.point(self._x[ti[2]][0], self._x[ti[2]][1], \
        self._x[ti[2]][2])
    d = util.closest_point_point_segment(a, b, ptc)
    nd = d.get_distance_from(ptc)
    if (nd < dist):
      pret = d
      dist = nd

    b = point.point(self._x[ti[3]][0], self._x[ti[3]][1], \
        self._x[ti[3]][2])
    d = util.closest_point_point_segment(a, b, ptc)
    nd = d.get_distance_from(ptc)
    if (nd < dist):
      pret = d
      dist = nd

    a = point.point(self._x[ti[0]][0], self._x[ti[0]][1], \
        self._x[ti[0]][2])
    d = util.closest_point_point_segment(a, b, ptc)
    nd = d.get_distance_from(ptc)
    if (nd < dist):
      pret = d
      dist = nd

    return pret


  def __get_perimeter_distance (self, idx, ptc):

    ti = self._polyhedra[idx]

    a = point.point(self._x[ti[0]][0], self._x[ti[0]][1], \
        self._x[ti[0]][2])
    b = point.point(self._x[ti[1]][0], self._x[ti[1]][1], \
        self._x[ti[1]][2])
    dist = util.get_dist_point_segment(a, b, ptc)

    a = point.point(self._x[ti[2]][0], self._x[ti[2]][1], \
        self._x[ti[2]][2])
    nd = util.get_dist_point_segment(a, b, ptc)
    if (nd < dist):
      dist = nd

    b = point.point(self._x[ti[3]][0], self._x[ti[3]][1], \
        self._x[ti[3]][2])
    nd = util.get_dist_point_segment(a, b, ptc)
    if (nd < dist):
      dist = nd

    a = point.point(self._x[ti[0]][0], self._x[ti[0]][1], \
        self._x[ti[0]][2])
    nd = util.get_dist_point_segment(a, b, ptc)
    if (nd < dist):
      dist = nd

    return dist


  def __compute_distance_from_perimeter (self, ptc):

    print "Chevk it "

    # 0 1
    a = point.point(self._x[0][0], self._x[0][1], self._x[0][2])
    b = point.point(self._x[1][0], self._x[1][1], self._x[1][2])
    dist = util.get_dist_point_segment(a, b, ptc)

    # 1 3 
    a = point.point(self._x[3][0], self._x[3][1], self._x[3][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 3 2
    b = point.point(self._x[2][0], self._x[2][1], self._x[2][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 2 0
    a = point.point(self._x[0][0], self._x[0][1], self._x[0][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 0 8
    b = point.point(self._x[8][0], self._x[8][1], self._x[8][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 8 9
    a = point.point(self._x[9][0], self._x[9][1], self._x[9][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 1 9
    b = point.point(self._x[1][0], self._x[1][1], self._x[1][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 1 5
    a = point.point(self._x[5][0], self._x[5][1], self._x[5][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 4 5
    b = point.point(self._x[4][0], self._x[4][1], self._x[4][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 6 4
    a = point.point(self._x[6][0], self._x[6][1], self._x[6][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 7 6
    b = point.point(self._x[7][0], self._x[7][1], self._x[7][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 3 7
    a = point.point(self._x[3][0], self._x[3][1], self._x[3][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 3 11
    b = point.point(self._x[11][0], self._x[11][1], self._x[11][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 11 10
    a = point.point(self._x[10][0], self._x[10][1], self._x[10][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 2 10
    b = point.point(self._x[2][0], self._x[2][1], self._x[2][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 2 6
    a = point.point(self._x[6][0], self._x[6][1], self._x[6][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    # 5 7
    a = point.point(self._x[5][0], self._x[5][1], self._x[5][2])
    b = point.point(self._x[7][0], self._x[7][1], self._x[7][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d
 
    # 0 4
    a = point.point(self._x[0][0], self._x[0][1], self._x[0][2])
    b = point.point(self._x[4][0], self._x[4][1], self._x[4][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d
 
    # 9 11
    a = point.point(self._x[9][0], self._x[9][1], self._x[9][2])
    b = point.point(self._x[11][0], self._x[11][1], self._x[11][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d
 
    # 10 8
    a = point.point(self._x[10][0], self._x[10][1], self._x[10][2])
    b = point.point(self._x[8][0], self._x[8][1], self._x[8][2])
    d = util.get_dist_point_segment(a, b, ptc)
    if (d < dist):
      dist = d

    return dist


  def _is_point_in_surface (self, ptc):

    for idx in range(len(self._polyhedra)):
      if (self.__is_in_polyhedra(idx, ptc)):
        return True
    
    #if (self._UP_pright.is_point_in (ptc) or \
    #    self._UP_pleft.is_point_in (ptc) or \
    #    self._UP_pbottom.is_point_in (ptc) or \
    #    self._UP_ptop.is_point_in (ptc) or \
    #    self._UP_pback.is_point_in (ptc) or \
    #    self._UP_pfront.is_point_in (ptc) or \
    #    self._DOWN_pright.is_point_in (ptc) or \
    #    self._DOWN_pleft.is_point_in (ptc) or \
    #    self._DOWN_pbottom.is_point_in (ptc) or \
    #    self._DOWN_ptop.is_point_in (ptc) or \
    #    self._DOWN_pback.is_point_in (ptc) or \
    #    self._DOWN_pfront.is_point_in (ptc) ):
    #  return True

    return False

###############################################################################
# free functions
###############################################################################

def nanoparticle_to_arrays (nanoparticles = []):

  scx = numpy.linspace( 0.0, 0.0, len(nanoparticles)) 
  scy = numpy.linspace( 0.0, 0.0, len(nanoparticles))
  scz = numpy.linspace( 0.0, 0.0, len(nanoparticles))

  i = 0
  for n in nanoparticles:
    scx[i], scy[i], scz[i] = n.get_center()
    i += 1

  return scx, scy, scz

###############################################################################

def file_to_nanoparticle_list(filename, nanaparticles):

  file = open(filename, "r")

  zmax = xmax = ymax = -10000.0
  zmin = xmin = ymin =  10000.0
 
  #i = 0
  for sp in file:

    #print "ID: ", i+1
    #i = i + 1

    x, y, z, sA, sB, sH, p2x, p2y, p2z, tetha \
        = sp.split(" ")
    
    A = float(sA)
    B = float(sB)
    H = float(sH)

    nanop = nanotio2(float(x), float(y), float(z), 
        A, B, H)

    p1 = point.point(float(x), float(y), float(z))

    p2 = point.point(float(p2x), float(p2y), float(p2z))

    nanop.rotate_nanoparticle(p1, p2, float(tetha))

    nanaparticles.append(nanop)

    dm = max(H, B, A) / 2.0

    if (zmax < (float(z) + dm)):
      zmax = (float(z) + dm)
    if (xmax < (float(x) + dm)):
      xmax = (float(x) + dm)
    if (ymax < (float(y) + dm)):
      ymax = (float(y) + dm)
  
    if (zmin > (float(z) - dm)):
      zmin = (float(z) - dm)
    if (xmin > (float(x) - dm)):
      xmin = (float(x) - dm)
    if (ymin > (float(y) - dm)):
      ymin = (float(y) - dm)
  
  file.close()

  return xmin, xmax, ymin, ymax, zmin, zmax

###############################################################################

def get_near_nanoparticle (nanoparticles, px, py, pz, distance):

  scx, scy, scz = nanoparticle_to_arrays (nanoparticles)

  distx = (scx - px)
  disty = (scy - py)
  distz = (scz - pz)

  distx2 = distx * distx
  disty2 = disty * disty
  distz2 = distz * distz

  dist = distx2 + disty2 + distz2

  d = numpy.sqrt(dist)

  bools1 = d <= distance

  indices, = numpy.where(bools1)

  toret = []
  toretdst = numpy.linspace( 0.0, 0.0, len(indices))

  for i in range(len(indices)):
    toret.append(nanoparticles[indices[i]])
    toretdst[i] = d[indices[i]]

  return toret, toretdst

###############################################################################

def file_to_nanoparticle_list_and_center(filename, nanaparticles):

  file = open(filename, "r")

  zmax = xmax = ymax = -10000.0
  zmin = xmin = ymin =  10000.0
  
  R = -1.0

  for sp in file:
    x, y, z, r, p2x, p2y, p2z, tetha \
        = sp.split(" ")
    
    if (R < 0.0):
      R = float(r)
    else:
      if (R != float(r)):
        print "Error R differ"
        exit()
 
    if (zmax < (float(z) + float(r))):
      zmax = (float(z) + float(r))
    if (xmax < (float(x) + float(r))):
      xmax = (float(x) + float(r))
    if (ymax < (float(y) + float(r))):
      ymax = (float(y) + float(r))
  
    if (zmin > (float(z) - float(r))):
      zmin = (float(z) - float(r))
    if (xmin > (float(x) - float(r))):
      xmin = (float(x) - float(r))
    if (ymin > (float(y) - float(r))):
      ymin = (float(y) - float(r))
  
  file.close()

  botx = xmin
  boty = ymin
  botz = zmin

  zmax = xmax = ymax = -10000.0
  zmin = xmin = ymin =  10000.0

  file = open(filename, "r")

  for sp in file:
    xs, ys, zs, r, p2x, p2y, p2z, tetha \
        = sp.split(" ")
    
    x = float(xs) - botx
    y = float(ys) - boty
    z = float(zs) - botz

    if (R < 0.0):
      R = float(r)
    else:
      if (R != float(r)):
        print "Error R differ"
        exit()
 
    H = float(r) * 2.52
    B = H*0.76
    A = B*0.32

    nanop = nanotio2(x, y, z, 
        A, B, H)

    p1 = point.point(x, y, z)

    p2 = point.point(float(p2x), float(p2y), float(p2z))

    nanop.rotate_nanoparticle(p1, p2, float(tetha))

    nanaparticles.append(nanop)

    if (zmax < (z + float(r))):
      zmax = (z + float(r))
    if (xmax < (x + float(r))):
      xmax = (x + float(r))
    if (ymax < (y + float(r))):
      ymax = (y + float(r))
  
    if (zmin > (z - float(r))):
      zmin = (z - float(r))
    if (xmin > (x - float(r))):
      xmin = (x - float(r))
    if (ymin > (y - float(r))):
      ymin = (y - float(r))

  file.close()

  return xmin, xmax, ymin, ymax, zmin, zmax, R

###############################################################################

def nanoparticle_list_to_arrays (nanoparticles):

  scx = numpy.linspace( 0.0, 0.0, len(nanoparticles)) 
  scy = numpy.linspace( 0.0, 0.0, len(nanoparticles))
  scz = numpy.linspace( 0.0, 0.0, len(nanoparticles))
  radius = numpy.linspace( 0.0, 0.0, len(nanoparticles))

  i = 0
  for n in nanoparticles:
    scx[i], scy[i], scz[i] = n.get_center()
    radius[i] = n.get_max_sphere()

    i = i + 1

  return scx, scy, scz, radius

###############################################################################

def get_near_nanoparticles_index_to (ith, scx, scy, scz, radius):

  x = scx[ith]
  y = scy[ith]
  z = scz[ith]
  r = radius[ith]

  rx = (scx - x) 
  ry = (scy - y)
  rz = (scz - z)

  dis = numpy.sqrt ((rx * rx) + (ry * ry) + (rz * rz))

  bools1 = (dis <= (radius + r))

  interior_indices, = numpy.where(bools1)

  return interior_indices

###############################################################################

def get_line_x_y (x1, y1, z1, x2, y2, z2, zin):

  x = x1 + (((zin - z1) * (x2 - x1))/(z2 - z1))
  y = y1 + (((x - x1) * (y2 - y1))/(x2 - x1))

  return x, y

###############################################################################

def get_near_nanoparticle_set_fixed (nanoparticles, px, py, pz, distance):

  scx, scy, scz = nanoparticle_to_arrays (nanoparticles)

  distx = (scx - px)
  disty = (scy - py)
  distz = (scz - pz)

  distx2 = distx * distx
  disty2 = disty * disty
  distz2 = distz * distz

  dist = distx2 + disty2 + distz2

  d = numpy.sqrt(dist)

  bools1 = d <= distance

  indices, = numpy.where(bools1)

  toret = []
  toretdst = numpy.linspace( 0.0, 0.0, len(indices))

  for i in range(len(indices)):
    nanoparticles[indices[i]].set_fixed()
    toret.append(nanoparticles[indices[i]])
    toretdst[i] = d[indices[i]]

  return toret, toretdst

###############################################################################
