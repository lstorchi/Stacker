import vtk

class cube:

  def __init__(self, x = 0.0, y = 0.0, z = 0.0, dim = 0.0):
    self.x = x
    self.y = y
    self.z = z
    self.dim = dim


  def get_borders (self):

    return self.x, self.y, self.z, self.x+self.dim,  self.z+self.dim, self.z+self.dim,

  def get_center (self):

    return self.x+(self.dim/2.0), self.y+(self.dim/2.0), self.z+(self.dim/2.0)


  def get_actor (self, rc = 1.0, gc = 1.0, bc = 1.0):

    source = vtk.vtkCubeSource()
    source.SetCenter(self.get_center())

    source.SetXLength(self.dim)
    source.SetYLength(self.dim)
    source.SetZLength(self.dim)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(rc, gc, bc)

    return actor

