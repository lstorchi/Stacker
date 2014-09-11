import vtk

def addcube_to_source (sources, botx, boty, botz, \
    topx, topy, topz):

  # draw box
  source = vtk.vtkLineSource()
  source.SetPoint1(botx, boty, botz)
  source.SetPoint2(topx, boty, botz)
  sources.append(source)
  
  source = vtk.vtkLineSource()
  source.SetPoint1(botx, boty, botz)
  source.SetPoint2(botx, topy, botz)
  sources.append(source)
  
  source = vtk.vtkLineSource()
  source.SetPoint1(topx, boty, botz)
  source.SetPoint2(topx, topy, botz)
  sources.append(source)
  
  source = vtk.vtkLineSource()
  source.SetPoint1(topx, topy, botz)
  source.SetPoint2(topx, topy, topz)
  sources.append(source)
  
  source = vtk.vtkLineSource()
  source.SetPoint1(topx, topy, topz)
  source.SetPoint2(topx, boty, topz)
  sources.append(source)

  source = vtk.vtkLineSource()
  source.SetPoint1(topx, boty, topz)
  source.SetPoint2(botx, boty, topz)
  sources.append(source)

  source = vtk.vtkLineSource()
  source.SetPoint1(botx, boty, topz)
  source.SetPoint2(botx, boty, botz)
  sources.append(source)

  source = vtk.vtkLineSource()
  source.SetPoint1(botx, boty, topz)
  source.SetPoint2(botx, topy, topz)
  sources.append(source)

  source = vtk.vtkLineSource()
  source.SetPoint1(botx, topy, topz)
  source.SetPoint2(botx, topy, botz)
  sources.append(source)

  source = vtk.vtkLineSource()
  source.SetPoint1(botx, topy, botz)
  source.SetPoint2(topx, topy, botz)
  sources.append(source)

  source = vtk.vtkLineSource()
  source.SetPoint1(topx, boty, botz)
  source.SetPoint2(topx, boty, topz)
  sources.append(source)

  source = vtk.vtkLineSource()
  source.SetPoint1(topx, topy, topz)
  source.SetPoint2(botx, topy, topz)
  sources.append(source)

  #print len(sources)

###############################################

def cube_to_actors (botx, boty, botz, \
    topx, topy, topz, r = 1.0, g = 1.0, \
    b = 1.0):

  sources = []
  addcube_to_source (sources, botx, boty, botz, \
      topx, topy, topz)

  mappers = []

  for s in sources:
    mapper = vtk.vtkPolyDataMapper()
    #mapper.SetInput(s.GetOutput())
    mapper.SetInputConnection(s.GetOutputPort())

    mappers.append(mapper)

  actors = []
  for m in mappers:

    actor = vtk.vtkActor()
    actor.SetMapper(m)
    actor.GetProperty().SetColor(r, g, b)

    actors.append(actor)

  return actors
