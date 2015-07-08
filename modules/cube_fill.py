import vtk

class cube:

  def __init__(self, cx = 0.0, cy = 0.0, cz = 0.0, dim = 0.0):
    self.face1_free = True
    self.face2_free = True
    self.face3_free = True
    self.face4_free = True
    self.face5_free = True
    self.face6_free = True

    self._pts = [[0,1,2,3], \
                 [4,7,6,5], \
                 [0,1,5,4], \
                 [1,2,6,5], \
                 [3,7,6,2], \
                 [0,3,7,4]]

    self.dim = dim

    self.cx = cx
    self.cy = cy
    self.cz = cz

    dimmez = self.dim/2.0

    x1 = self.cx - dimmez
    y1 = self.cy - dimmez
    z1 = self.cz - dimmez

    self.p1 = [x1, y1, z1]

    x2 = self.cx - dimmez
    y2 = self.cy + dimmez
    z2 = self.cz - dimmez

    self.p2 = [x2, y2, z2]

    x3 = self.cx + dimmez
    y3 = self.cy + dimmez
    z3 = self.cz - dimmez

    self.p3 = [x3, y3, z3]
    
    x4 = self.cx + dimmez
    y4 = self.cy - dimmez
    z4 = self.cz - dimmez

    self.p4 = [x4, y4, z4]

    x5 = x1 
    y5 = y1
    z5 = self.cz + dimmez

    self.p5 = [x5, y5, z5]

    x6 = x2
    y6 = y2
    z6 = self.cz + dimmez

    self.p6 = [x6, y6, z6]

    x7 = x3
    y7 = y3
    z7 = self.cz + dimmez

    self.p7 = [x7, y7, z7]

    x8 = x4
    y8 = y4
    z8 = self.cz + dimmez

    self.p8 = [x8, y8, z8]

  def has_free_face (self):

    return (self.face1_free or \
        self.face2_free or \
        self.face3_free or \
        self.face4_free or \
        self.face5_free or \
        self.face6_free)

  def is_face_free (self, iface):

    if (iface == 1):
      return self.face1_free
    elif (iface == 2):
      return self.face2_free
    elif (iface == 3):
      return self.face3_free
    elif (iface == 4):
      return self.face4_free
    elif (iface == 5):
      return self.face5_free
    elif (iface == 6):
      return self.face6_free
    else:
      return False

  def set_iface (self, iface):

    if (iface == 1):
      self.face1_free = False
    elif (iface == 2):
      self.face2_free = False
    elif (iface == 3):
      self.face3_free = False
    elif (iface == 4):
      self.face4_free = False
    elif (iface == 5):
      self.face5_free = False
    elif (iface == 6):
      self.face6_free = False

  def get_center (self):

    return self.cx, self.cy, self.cz

  def get_dim (self):

    return self.dim

  def get_cube_coordintes (self):

    return [self.p1, self.p2, self.p3, self.p4, \
        self.p5, self.p6, self.p7, self.p8]

  def get_face_coords (self, iface):

    if (iface == 1):
      return self.p1, self.p2, self.p3, self.p4
    elif (iface == 2):
      return self.p5, self.p8, self.p7, self.p6
    elif (iface == 3):
      return self.p1, self.p2, self.p6, self.p5
    elif (iface == 4):
      return self.p2, self.p3, self.p7, self.p6
    elif (iface == 5):
      return self.p4, self.p8, self.p7, self.p3
    elif (iface == 6):
      return self.p1, self.p4, self.p8, self.p5
    else:
      # add an error code
      exit(1)

  def get_vtk_actor (self, rc = 1.0, gc = 1.0, bc = 1.0, opacity = 1.0):

    self._compute_polydata()

    nanopMapper = vtk.vtkPolyDataMapper()
    nanopMapper.SetInputData(self._polydata)

    nanopActor = vtk.vtkActor()
    nanopActor.SetMapper(nanopMapper)
    nanopActor.GetProperty().SetOpacity(opacity)

    nanopActor.GetProperty().SetColor(rc, gc, bc)

    return nanopActor

###################################################################3
# PRIVATE 
###################################################################3

  def _compute_polydata(self):

    self._polydata = vtk.vtkPolyData()

    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()
    
    points.InsertPoint(0,self.p1)
    points.InsertPoint(1,self.p2)
    points.InsertPoint(2,self.p3)
    points.InsertPoint(3,self.p4)
    points.InsertPoint(4,self.p5)
    points.InsertPoint(5,self.p6)
    points.InsertPoint(6,self.p7)
    points.InsertPoint(7,self.p8)
    
    for i in range(len(self._pts)):
      ids = vtk.vtkIdList()
      ids.SetNumberOfIds(4)
      for j in range(4):
        ids.SetId(j, self._pts[i][j])
    
      polys.InsertNextCell(ids)
    
    self._polydata.SetPoints(points)
    self._polydata.SetPolys(polys)

    return self._polydata
