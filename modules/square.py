import vtk

def addsquare_to_source (sources, botx, boty, \
    topx, topy, zplane):

  # draw box
  source = vtk.vtkLineSource()
  source.SetPoint1(botx, boty, zplane)
  source.SetPoint2(topx, boty, zplane)
  sources.append(source)
  
  source = vtk.vtkLineSource()
  source.SetPoint1(botx, boty, zplane)
  source.SetPoint2(botx, topy, zplane)
  sources.append(source)
  
  source = vtk.vtkLineSource()
  source.SetPoint1(topx, boty, zplane)
  source.SetPoint2(topx, topy, zplane)
  sources.append(source)
  
  source = vtk.vtkLineSource()
  source.SetPoint1(topx, topy, zplane)
  source.SetPoint2(botx, topy, zplane)
  sources.append(source)
  
  #print len(sources)

###############################################

def square_to_actors (botx, boty, \
    topx, topy, zplane, r = 1.0, g = 0.0, \
    b = 0.0):

  sources = []
  addsquare_to_source (sources, botx, boty, \
      topx, topy, zplane)

  mappers = []

  for s in sources:
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(s.GetOutput())

    mappers.append(mapper)

  actors = []
  for m in mappers:

    actor = vtk.vtkActor()
    actor.SetMapper(m)
    actor.GetProperty().SetColor(r, g, b)

    actors.append(actor)

  return actors
