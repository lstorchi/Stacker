import vtk
import sys 
import re
import numpy

sys.path.append("../modules")

import nanoparticle


#####################################################################

def get_color (atom):

  if (atom == 'O'):
    return 0.0, 0.0, 1.0
  elif (atom == 'Ti'):
    return 1.0, 0.0, 0.0

  return 0.0, 0.0, 0.0

#####################################################################

filename = ""

# in A
radius = {'O':0.60, 'Ti':1.40}

if (len(sys.argv)) == 2:
  filename = sys.argv[1]
else:
  print "usage :", sys.argv[0] , " xyzfile"
  exit(1)

filep = open(filename, "r")

filep.readline()
filep.readline()

actors = []
xlist = []
ylist = []
zlist = []

for line in filep:
  p = re.compile(r'\s+')
  line = p.sub(' ', line)
  line = line.lstrip()
  line = line.rstrip()

  plist =  line.split(" ")

  if (len(plist) == 4):
   atomname = plist[0]
   x = plist[1]
   y = plist[2]
   z = plist[3]

   xlist.append(float(x))
   ylist.append(float(y))
   zlist.append(float(z))

   if atomname in radius:
     print atomname, " has ", radius[atomname], x, y, z

     source = vtk.vtkSphereSource()
     source.SetCenter(float(x),float(y),float(z))
     source.SetRadius(radius[atomname])

     mapper = vtk.vtkPolyDataMapper()
     if vtk.VTK_MAJOR_VERSION <= 5:
       mapper.SetInput(source.GetOutput())
     else:
       mapper.SetInputConnection(source.GetOutputPort())
                 
     actor = vtk.vtkActor()
     actor.SetMapper(mapper)
     actor.GetProperty().SetColor(get_color(atomname)); #(R,G,B)
     actors.append(actor)


filep.close()

nanop = nanoparticle.nanotio2(numpy.mean(xlist), \
    numpy.mean(ylist), numpy.mean(zlist), \
    14.44, 23.56, 28.99)

sphere = vtk.vtkSphereSource()
sphere.SetCenter(numpy.mean(xlist), \
        numpy.mean(ylist), numpy.mean(zlist))
sphere.SetRadius(float(28.909/2.11799999999941388495))

mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
  mapper.SetInput(sphere.GetOutput())
else:
  mapper.SetInputConnection(sphere.GetOutputPort())
 
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetOpacity(1.0)

actors.append(nanop.get_vtk_actor(True, 0.8))
actors.append(actor)

print "X ", min(xlist), " " , max(xlist), " ", max(xlist)-min(xlist)
print "Y ", min(ylist), " " , max(ylist), " ", max(ylist)-min(ylist)
print "Z ", min(zlist), " " , max(zlist), " ", max(zlist)-min(zlist)

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
for actor in actors :
  ren.AddActor(actor)
                
iren.Initialize()
renWin.Render()
iren.Start()
