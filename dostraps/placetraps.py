import re
import sys
import vtk
import numpy

from scipy.interpolate import interp1d

sys.path.append("../modules")

import xyznanop
import sphere
import point
import util
import cube

#######################################################################`

def read_filecurve (fname):
    fp = open(fname)
    
    x = []
    xval = []
    
    for l in fp:
        p = re.compile(r'\s+')
        line = p.sub(' ', l)
        line = line.lstrip()
        line = line.rstrip()
        linelist = line.split(" ")
    
        if len(linelist) != 3:
            print "Error in file format"
            exit(1)
    
        x.append(float(linelist[0]))
        xval.append(float(linelist[2]))
    
    fp.close()
    
    sumx = 0.0
    for v in xval:
        sumx += v

    for i in range(len(xval)):
        xval[i] /= sumx

    return x, xval, sumx

#######################################################################

xcurvefname = ""
ycurvefname = "" 
zcurvefname = ""
xyzfname = ""

if (len(sys.argv)) == 5:
    xcurvefname = sys.argv[1]
    ycurvefname = sys.argv[2]
    zcurvefname = sys.argv[3]
    xyzfname = sys.argv[4]
else:
    print "usage :", sys.argv[0] , " xcurve ycurve zcurve file.xyz"
    exit(1)

x, xval, sumx = read_filecurve (xcurvefname)
y, yval, sumy = read_filecurve (ycurvefname)
z, zval, sumz = read_filecurve (zcurvefname)

centerx = numpy.mean(x)
centery = numpy.mean(y)
centerz = numpy.mean(z)

x -= centerx
y -= centery
z -= centerz

curveminx = min(x)
curvemaxx = max(x)
curveminy = min(y)
curvemaxy = max(y)
curveminz = min(z)
curvemaxz = max(z)


print "Curves limits: "
print min(x), max(x) 
print min(y), max(y) 
print min(z), max(z)

fx = interp1d(x, xval, kind='cubic')
fy = interp1d(y, yval, kind='cubic')
fz = interp1d(z, zval, kind='cubic')

"""
xnew = numpy.linspace(min(x), max(x), num=10000, endpoint=True)
ynew = fx(xnew)
import matplotlib.pyplot as plt
plt.plot(x, xval, 'o', xnew, ynew, '-')
plt.show()
"""

xlist, ylist, zlist, atoms = xyznanop.read_ncxyz (xyzfname)

np_centerx = numpy.mean(xlist)
np_centery = numpy.mean(ylist)
np_centerz = numpy.mean(zlist)

xlist -= np_centerx
ylist -= np_centery
zlist -= np_centerz

print "Nanoparticle limits: "
print min(xlist), max(xlist)
print min(ylist), max(ylist)
print min(zlist), max(zlist)

traps_xyz_pdf = []
totp = 0.0
for i in range(len(atoms)):
    #print atoms[i]
    if atoms[i] == "Ti":
        xv = xlist[i]
        yv = ylist[i]
        zv = zlist[i]

        if xv < min(x):
            print "out of range"
            xv = min(x)
        if xv > max(x):
            print "out of range"
            xv = max(x)

        if yv < min(y):
            print "out of range"
            yv = min(y)
        if yv > max(y):
            print "out of range"
            yv = max(y)

        if zv < min(z):
            print "out of range"
            zv = min(z)
        if zv > max(z):
            print "out of range"
            zv = max(z)

        p = fx(xv) * fy(yv) * fz(zv)
        totp += p
        traps_xyz_pdf.append([xlist[i], ylist[i], zlist[i], p])

for i in range(len(traps_xyz_pdf)):
    traps_xyz_pdf[i][3] = 100.0 * (traps_xyz_pdf[i][3] / totp )
    print traps_xyz_pdf[i][0], \
            traps_xyz_pdf[i][1], \
            traps_xyz_pdf[i][2], \
            traps_xyz_pdf[i][3]

# create a rendering window and renderer
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
# create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

sources = []

print min(x), max(x) 
print min(y), max(y) 
print min(z), max(z)

cube.addcube_to_source (sources, curveminx, curveminy, curveminz, \
     curvemaxx, curvemaxy, curvemaxz)

for trap in traps_xyz_pdf:
  source = vtk.vtkSphereSource()
  source.SetCenter(trap[0], trap[1], trap[2])
  source.SetRadius(trap[3])

  sources.append(source)

# mapper
mappers = []

for source in sources:
  mapper = vtk.vtkPolyDataMapper()
  #mapper.SetInput(source.GetOutput())
  mapper.SetInputConnection(source.GetOutputPort())
  
  mappers.append(mapper)

# actor
actors = []

for mapper in mappers:
  actor = vtk.vtkActor()
  #actor.GetProperty().SetOpacity(0.9)
  actor.SetMapper(mapper)

  actors.append(actor);
 
# assign actor to the renderer

for actor in actors:
  ren.AddActor(actor)

# enable user interface interactor
try:
  iren.Initialize()
  renWin.Render()
  #writer = vtk.vtkGL2PSExporter()
  #writer.SetRenderWindow(renWin)
  #writer.SetFileFormatToSVG ()
  #writer.SetFilePrefix("largeImage")
  #writer.Write()
  iren.Start()
except Exception as e:
  print e

#for trap in traps_xyz_pdf:
#    print trap[0], trap[1], trap[2], trap[3]

numoftraps = 10000
random_array = numpy.random.uniform(0.0, 1.0, numoftraps)

