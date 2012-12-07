import vtk
import sys

filename = "final_config.txt"

####################################################################

def sphere_to_point ():
  points = vtk.vtkPoints()

  file = open(filename, "r")

  for sp in file:
    x, y, z, r = sp.split(" ")
    points.InsertNextPoint(float(x), float(y), float(z))

  file.close()

  return points

####################################################################

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

# parto dal presupposto che hanno lo stesso raggio
file = open(filename, "r")

R = -1.0
for sp in file:
  x, y, z, r = sp.split(" ")
  if R < 0.0:
    R = r
  else:
    if R != r:
      print "Error "
      exit()

file.close()

sphere = vtk.vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(float(R))
sphere.SetThetaResolution(10)
sphere.SetPhiResolution(10)

model_points = sphere_to_point()

model_polydata = vtk.vtkPolyData()
model_polydata.SetPoints(model_points)

model_glyph = vtk.vtkGlyph3D()
model_glyph.SetInput( model_polydata )
model_glyph.SetScaleModeToDataScalingOff()
#model_glyph.SetScaleFactor(0.25)
#model_glyph.SetScaling(1)
model_glyph.SetSourceConnection(sphere.GetOutputPort())

model_mapper = vtk.vtkPolyDataMapper()
model_mapper.SetInputConnection(model_glyph.GetOutputPort())
model_mapper.ScalarVisibilityOff()
 
model = vtk.vtkActor()
model.SetMapper(model_mapper)
model.GetProperty().SetRepresentationToSurface()
model.GetProperty().SetInterpolationToGouraud() # behaves like Flat
model.GetProperty().SetAmbient(0.15)
model.GetProperty().SetDiffuse(0.85)
model.GetProperty().SetSpecular(0.1)
model.GetProperty().SetSpecularPower(30)
#model.GetProperty().SetColor(1, 0, 0)

model.GetProperty().SetOpacity(1.0)


ren = vtk.vtkRenderer()
ren.AddActor(model)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(model_glyph.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(mapOutline)
outlineActor.GetProperty().SetColor(.6, .6, .6)

ren.AddActor(outlineActor)

# Create a text property for the cube axes
tprop = vtk.vtkTextProperty()
tprop.SetColor(1, 1, 1)
tprop.ShadowOn()

axes = vtk.vtkCubeAxesActor2D()
axes.SetInput(model_glyph.GetOutput())
axes.SetCamera(ren.GetActiveCamera())
axes.SetLabelFormat("%6.1g")
axes.SetFlyModeToOuterEdges()
axes.SetFontFactor(1.0)
axes.SetAxisTitleTextProperty(tprop)
axes.SetAxisLabelTextProperty(tprop)

ren.AddViewProp(axes)

#########################################################

camera = vtk.vtkCamera()
camera.SetPosition(1,1,1)
camera.SetFocalPoint(0,0,0)


renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

renWin.SetSize(1024, 768)


ren.SetActiveCamera(camera)
ren.ResetCamera()
ren.ResetCamera()

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()

renderLarge = vtk.vtkRenderLargeImage()
renderLarge.SetInput(ren)
renderLarge.SetMagnification(4)

writer = vtk.vtkTIFFWriter()
writer.SetInputConnection (renderLarge.GetOutputPort())
writer.SetFileName("largeImage.tif")
writer.Write()


renWin.Render()
iren.Start()
