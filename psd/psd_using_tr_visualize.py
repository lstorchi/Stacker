import sys
sys.path.append("../modules")

import util
import line
import point
import sphere
import circle
import square
import triangle

import util_for_tr

import random
import math
import sys
import vtk

###############################################################################

util_for_tr.NUMOFCIRCLEPOINTS = 72

filename = "final_config.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

hw_many_planes = 100
hw_many_points = 1000

spheres = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    util.file_to_sphere_diffr_list(filename, spheres)

totr = 0.0
for s in spheres:
  totr += s.get_radius()
  
meanr = totr / float(len(spheres))
meand = 2.0 * meanr

# voglio fermarmi a circa 2 D dalla vetta visto che in cima avro' sempre una
# densita' minore(ricorda la prima sfera che supera zmax ferma la procedura.
dz = ((zmax - zmin) - (3.0 * meand)) / float(hw_many_planes+1)

#print "xmax: ", xmax, "xmin: ",xmin, "ymax: ", ymax, \
#    "ymin: ", ymin, "zmx: ", zmax, "zmin: ", zmin

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

zplane = (zmax - zmin) / 2.0

for ac in square.square_to_actors(xmin, ymin, xmax, ymax, zplane):
  ren.AddActor(ac)

circles = util_for_tr.get_circle_in_plane (spheres, zplane)

for cir in circles:
  circleactor = cir.get_actor(zplane)
  #circleactor.GetProperty().SetRepresentationToWireframe()
  ren.AddActor(circleactor)

poly_data_points = []

for i in range(hw_many_points):

  x = random.uniform(xmin + meand, xmax - meand)
  y = random.uniform(ymin + meand, ymax - meand)

  if not util_for_tr.is_inside_circles (x, y, circles):

    poly_data_points = util_for_tr.get_circle_points_list(x, y, circles)

    print x, y

    break;

polydata = vtk.vtkPolyData()
points = vtk.vtkPoints()
polys = vtk.vtkCellArray()
scalars = vtk.vtkFloatArray()

i = 0

for p in poly_data_points:
  #pp = point.point(p[0], p[1], zplane)
  #ren.AddActor(pp.get_actor(0.2))

  points.InsertPoint(i, [p[0], p[1], zplane])

  #scalars.InsertTuple1(i,0)

  i += 1 

center = i
points.InsertPoint(center, [x, y, zplane])

pp = point.point(x, y, zplane)
centerpointactor = pp.get_actor(0.5)

centerpointactor.GetProperty().SetColor(0.0, 0.0, 1.0)

ren.AddActor(centerpointactor)

"""
for i in range(len(poly_data_points)-1):
  j = i + 1

  print i, j

  p0 = poly_data_points[i]
  p = poly_data_points[j]

  print p0
  print p

  l = line.line2d()
  l.set_two_point(p0, p)
  ren.AddActor(l.get_actor(zplane))

l = line.line2d()
l.set_two_point(poly_data_points[0], \
    poly_data_points[len(poly_data_points)-1])
ren.AddActor(l.get_actor(zplane))
"""

for i in range(len(poly_data_points)-1):

  j = i + 1

  ids = vtk.vtkIdList()
  ids.SetNumberOfIds(3)
  
  ids.SetId(0, j)
  ids.SetId(1, i)
  ids.SetId(2, center)

  polys.InsertNextCell(ids)

# ultimo triangolo
ids = vtk.vtkIdList()
ids.SetNumberOfIds(3)
ids.SetId(0, 0)
ids.SetId(1, len(poly_data_points)-1)
ids.SetId(2, center)
polys.InsertNextCell(ids)

polydata.SetPoints(points)
polydata.SetPolys(polys)
#polydata.GetPointData().SetScalars(scalars)

papper = vtk.vtkPolyDataMapper()
#papper.SetInput(polydata)
papper.SetInputData(polydata)
papper.SetScalarRange(0,0)

pactor = vtk.vtkActor()
pactor.SetMapper(papper)
#pactor.GetProperty().SetOpacity(opacity)
pactor.GetProperty().SetRepresentationToWireframe()
pactor.GetProperty().SetColor(1.0,1.0,1.0)

ren.AddActor(pactor)

ren.SetBackground(0,0,0)
ren.ResetCamera()
#renWin.SetSize(1024, 768)

renWin.SetSize(1024, 768)

#renderLarge = vtk.vtkRenderLargeImage()
#renderLarge.SetInput(ren)
#renderLarge.SetMagnification(4)

writer = vtk.vtkGL2PSExporter()
writer.SetRenderWindow(renWin)
writer.SetFileFormatToPDF ()
writer.SetFilePrefix("largeImage")
writer.Write()
 
#writer = vtk.vtkTIFFWriter()
#writer.SetInputConnection (renderLarge.GetOutputPort())
#writer.SetFileName("largeImage.tif")
#writer.Write()

renWin.Render()
iren.Start()

