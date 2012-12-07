import sys
sys.path.append("./modules")

import util
import line
import cube
import point
import sphere
import circle
import square
import triangle
import util_for_tr
import nanoparticle

import random
import numpy
import math
import sys
import vtk

###############################################################################

# non mi interessano le intersezioni
nanoparticle.POINTINSIDEDIM = 0

filename = "nanoparticle_final_config.txt"

if (len(sys.argv)) > 1:
  filename = sys.argv[1]

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

hw_many_planes = 100
hw_many_points = 1000

nanoparticles = []

zmax = xmax = ymax = -10000.0
zmin = xmin = ymin =  10000.0

xmin, xmax, ymin, ymax, zmin, zmax = \
    nanoparticle.file_to_nanoparticle_list(filename, nanoparticles)

cube_actors = cube.cube_to_actors(xmin, ymin, zmin, \
        xmax, ymax, zmax, 1.0, 1.0, 1.0)
for a in cube_actors:
  ren.AddActor(a)

Dz = (zmax-zmin)
Dy = (ymax-ymin)
Dx = (xmax-xmin)

scx, scy, scz, radius = nanoparticle.nanoparticle_list_to_arrays(nanoparticles)

meanr = radius.mean()
meand = 2.0 * meanr

# voglio fermarmi a circa 2 D dalla vetta visto che in cima avro' sempre una
# densita' minore(ricorda la prima sfera che supera zmax ferma la procedura.
dz = ((zmax - zmin) - (3.0 * meand)) / float(hw_many_planes+1)

poly_data_points = []
center = []

for iplane in range(hw_many_planes):

  zplane = zmin + meand + (iplane+1)*dz

  # seleziona le nanoparticelle che dovrebbero passare per il piano
  # usando le sfere per fare la selezione e' possibile io ottenga
  # dei falsi positivi

  bools1 = numpy.fabs(scz - zplane) < radius
  interior_indices, = numpy.where(bools1)

  for i in range(hw_many_points):

    x = random.uniform(xmin + meand, xmax - meand)
    y = random.uniform(ymin + meand, ymax - meand)

    is_inside = False

    for idx in interior_indices:
      cx, cy, cz = nanoparticles[idx].get_center()
      dist = util_for_tr.point_distance([x, y], [cx, cy])

      if (dist <= radius[idx]):
        if (nanoparticles[idx].is_point_inside([x, y, zplane])):
          is_inside = True
          break

    if not is_inside:

      p = point.point(x, y, zplane)
      ren.AddActor(p.get_actor(0.5, 1.0, 0.0, 0.0))

      # q lo genro fuori dalla box perche' cosi' sono certo attraversera 
      # tutte le nanoparticelle
      point_circle = circle.circle(x, y, 2.0 * max(Dx, Dy, Dz))
      second_points = point_circle.generate_circle_points(36)

      poly_data_points = []

      for sp in second_points:
        q = point.point(sp[0], sp[1], zplane)  

        #ren.AddActor(q.get_actor(1.0, 1.0, 0.0, 0.0))

        selected_point = []
        min_d = float("inf")
        for idx in interior_indices:
          intersect_points = nanoparticles[idx].intersect_line(p, q)

          if (len(intersect_points) != 0):

            if (len(intersect_points) != 2):
              print "Warning less than two point"

            #print len(intersect_points)
            for ip in intersect_points:
              #print ip[0], ip[1], ip[2]

              if (ip[2] != zplane):
                print "Error"
                exit()

              d = util_for_tr.point_distance([x, y], [ip[0], ip[1]])
              if (d < min_d):
                min_d = d
                selected_point = ip

        #ipp = point.point(selected_point[0], selected_point[1], selected_point[2])
        #ren.AddActor(ipp.get_actor(0.5))

        if (min_d != float("inf")):
          poly_data_points.append(selected_point)


      print util_for_tr.get_radius ([x, y], poly_data_points, zplane)

      for ip in poly_data_points:
        ipp = point.point(ip[0], ip[1], ip[2])
        ren.AddActor(ipp.get_actor(0.5))

      for idx in interior_indices:
        nanopactor = nanoparticles[idx].get_vtk_actor(False, opacity = 0.8)
        #nanopactor.GetProperty().SetRepresentationToWireframe()
        ren.AddActor(nanopactor)

      break
  
  break

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
papper.SetInput(polydata)
papper.SetScalarRange(0,0)

pactor = vtk.vtkActor()
pactor.SetMapper(papper)
#pactor.GetProperty().SetOpacity(opacity)
pactor.GetProperty().SetColor(1.0,1.0,1.0)
pactor.GetProperty().SetRepresentationToWireframe()

ren.AddActor(pactor)

ren.SetBackground(0,0,0)
ren.ResetCamera()
#renWin.SetSize(1024, 768)

renWin.SetSize(1024, 768)

renderLarge = vtk.vtkRenderLargeImage()
renderLarge.SetInput(ren)
renderLarge.SetMagnification(4)

writer = vtk.vtkTIFFWriter()
writer.SetInputConnection (renderLarge.GetOutputPort())
writer.SetFileName("largeImage.tif")
writer.Write()

renWin.Render()
iren.Start()
