import re
import sys
import vtk
import math
import numpy

from scipy.interpolate import interp1d

import argparse

sys.path.append("../modules")

import nanoparticle
import xyznanop
import sphere
import traps
import point
import util
import cube

CONVERTFCT = 1.889725989
# if not needed 
# CONVERTFCT = 1.0

#######################################################################`

def rototranslate_traps (intraps, cx, cy, cz, p1, p2, tetha, npid):
  
    trap_centerx = numpy.mean([t.get_x() for t in intraps])
    trap_centery = numpy.mean([t.get_y() for t in intraps])
    trap_centerz = numpy.mean([t.get_z() for t in intraps])
    
    distx = trap_centerx-cx
    disty = trap_centery-cy
    distz = trap_centerz-cz

    vals = [point.point(t.get_x()-distx, t.get_y()-disty, \
        t.get_z()-distz) for t in intraps]
    rotvals = [util.point_rotate(p1, p2, p, tetha) for p in vals]
    rettraps = [traps.trap(p.get_x(), p.get_y(), p.get_z()) \
        for p in rotvals]

    # should be Vectorized
    for i in range(len(rettraps)):
        rettraps[i].set_id(intraps[i].get_id())
        rettraps[i].set_npid(npid)
        rettraps[i].set_atomid(intraps[i].get_atomid())

    return rettraps

#######################################################################`

def visualize_all_sources (renWin, iren, sources):

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
    
      actors.append(actor)
      
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

#######################################################################`

def read_filecurve (fname):
    fp = open(fname)
    
    x = []
    xval = []

    y = []
    yval = []
 
    z = []
    zval = []
 
    for l in fp:
        p = re.compile(r'\s+')
        line = p.sub(' ', l)
        line = line.lstrip()
        line = line.rstrip()
        linelist = line.split(" ")
    
        if len(linelist) != 6:
            print "Error in file format"
            exit(1)
    
        if (util.is_a_float(linelist[0]) and \
                util.is_a_float(linelist[1])):
            x.append(float(linelist[0]))
            xval.append(float(linelist[1]))

        if (util.is_a_float(linelist[2]) and \
                util.is_a_float(linelist[3])):
            y.append(float(linelist[2]))
            yval.append(float(linelist[3]))

        if (util.is_a_float(linelist[4]) and \
                util.is_a_float(linelist[5])):
            z.append(float(linelist[4]))
            zval.append(float(linelist[5]))
    
    fp.close()
    
    sumx = numpy.sum(xval)
    xval[:] = [xv / sumx for xv in xval]

    sumy = numpy.sum(yval)
    yval[:] = [yv / sumy for yv in yval]

    sumz = numpy.sum(zval)
    zval[:] = [zv / sumz for zv in zval]

    return x, xval, sumx,  \
            y, yval, sumy,  \
            z, zval, sumz,

#######################################################################

def generate_traps (x, xval, sumx, y, yval, sumy, \
        z, zval, sumz, xlist, ylist, zlist, atoms,\
        plt, numoftotaltraps, verbose = False):

    activatevtk = False
    showalsomainspheres = True

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
    
    if verbose:
        print >> sys.stderr, "Curves limits: "
        print >> sys.stderr, "%10.5f %10.5f"%(min(x), max(x))
        print >> sys.stderr, "%10.5f %10.5f"%(min(y), max(y))
        print >> sys.stderr, "%10.5f %10.5f"%(min(z), max(z))
    
    fx = interp1d(x, xval, kind='cubic')
    fy = interp1d(y, yval, kind='cubic')
    fz = interp1d(z, zval, kind='cubic')
    
    plt.subplot(3, 1, 1)
    xnew = numpy.linspace(min(x), max(x), num=10000, endpoint=True)
    xvalnew = fx(xnew)
    plt.title('X values')
    plt.plot(x, xval, 'o', xnew, xvalnew, '-')

    plt.subplot(3, 1, 2)
    ynew = numpy.linspace(min(y), max(y), num=10000, endpoint=True)
    yvalnew = fy(ynew)
    plt.title('Y values')
    plt.plot(y, yval, 'o', ynew, yvalnew, '-')
 
    plt.subplot(3, 1, 3)
    znew = numpy.linspace(min(z), max(z), num=10000, endpoint=True)
    zvalnew = fz(znew)
    plt.title('Z values')
    plt.plot(z, zval, 'o', znew, zvalnew, '-')
 
    np_centerx = numpy.mean(xlist)
    np_centery = numpy.mean(ylist)
    np_centerz = numpy.mean(zlist)
    
    xlist -= np_centerx
    ylist -= np_centery
    zlist -= np_centerz
    
    if verbose:
        print >> sys.stderr, "Nanoparticle limits: "
        print >> sys.stderr, "%10.5f %10.5f"%(min(xlist), max(xlist))
        print >> sys.stderr, "%10.5f %10.5f"%(min(ylist), max(ylist))
        print >> sys.stderr, "%10.5f %10.5f"%(min(zlist), max(zlist))
    
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
            traps_xyz_pdf.append([xlist[i], ylist[i], zlist[i], p, i])
    
    for i in range(len(traps_xyz_pdf)):
        traps_xyz_pdf[i][3] = 100.0 * (traps_xyz_pdf[i][3] / totp )
        #print traps_xyz_pdf[i][0], \
        #        traps_xyz_pdf[i][1], \
        #        traps_xyz_pdf[i][2], \
        #        traps_xyz_pdf[i][3]
    
    # create a rendering window and renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
     
    # create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    sources = []
    
    #print min(x), max(x) 
    #print min(y), max(y) 
    #print min(z), max(z)
    
    if (activatevtk):
        cube.addcube_to_source (sources, curveminx, curveminy, curveminz, \
                curvemaxx, curvemaxy, curvemaxz)
    
    if (activatevtk):
        for trap in traps_xyz_pdf:
            source = vtk.vtkSphereSource()
            source.SetCenter(trap[0], trap[1], trap[2])
            source.SetRadius(trap[3])
            
        if showalsomainspheres:
            sources.append(source)

    totalsum = 0.0
    for trap in traps_xyz_pdf:
        totalsum += trap[3]

    if verbose:
        print >> sys.stderr, "Check number of traps and sum: ", \
                len(traps_xyz_pdf), totalsum

    totalnumoft = 0
    placedpoints = 0
    realtraps = []
    for trap in traps_xyz_pdf:
        numoftraps_per_atom = int(numoftotaltraps*trap[3]/totalsum)
    
        totalnumoft += numoftraps_per_atom
    
        r = trap[3]
        cx = trap[0]
        cy = trap[1]
        cz = trap[2]
        atomid = trap[4]

        trapcounter = 0

        # do not place point if estimation is equal to zero
        todo = (numoftraps_per_atom != 0)
        while todo:
            theta = 2.0 * math.pi * numpy.random.uniform(0.0, 1.0)
            phi = math.pi * numpy.random.uniform(0.0, 1.0)
            xt = cx + r * math.sin(phi) * math.cos(theta)
            yt = cy + r * math.sin(phi) * math.sin(theta)
            zt = cz + r * math.cos(phi)
           
            t = traps.trap(xt, yt, zt)
            t.set_atomid(atomid)
    
            realtraps.append(t)
            trapcounter += 1
            placedpoints += 1
            
            if (activatevtk):
                source = vtk.vtkSphereSource()
                source.SetCenter(xt, yt, zt)
                source.SetRadius(0.1)
                sources.append(source)
    
            if trapcounter >= numoftraps_per_atom:
                todo = False
    

    if verbose:
        print >> sys.stderr, \
                "Check totalnumoft vs numoftotaltraps and placedpoints : ", \
                totalnumoft, numoftotaltraps, placedpoints

    if (activatevtk):
        visualize_all_sources (renWin, iren, sources)

    return realtraps
    
#######################################################################

if __name__ == "__main__":

   xcurvefname = ""
   ycurvefname = "" 
   zcurvefname = ""
   xyzfname = ""

   main_activatevtk = False
   
   parser = argparse.ArgumentParser()
   
   parser.add_argument("-i", "--input-files", \
           help="input files \"id1:file1xyz;id2:file2xyz;...;idN:fileNxyz\"  ", \
           type=str, required=True, default="", dest="curvefiles")
   parser.add_argument("-I", "--input-xyz", help="input XYZ file", \
           type=str, required=True, default="", dest="xyzfile")
   parser.add_argument("-N", "--numof-point-per-state", help="number of points per each trap state", \
           type=int, required=True, default=0, dest="numofpointperstate")
 
   parser.add_argument("-f", "--input-film", help="input the film file if needed", \
           type=str, required=False, default="", dest="filmfile")
   parser.add_argument("-v", "--verbose", help="increase output verbosity", \
           default=False, action="store_true")
   
   if len(sys.argv) == 1:
       parser.print_help()
       exit(1)
   
   args = parser.parse_args()
   
   verbose = args.verbose
   xyzfname = args.xyzfile
   
   xlist, ylist, zlist, atoms = xyznanop.read_ncxyz (xyzfname)

   xlist = numpy.divide(xlist, CONVERTFCT)
   ylist = numpy.divide(ylist, CONVERTFCT)
   zlist = numpy.divide(zlist, CONVERTFCT)

   alltraps = []

   for pair in args.curvefiles.split(";"):
       id, fname = pair.split(":")
   
       print >> sys.stderr, id, fname
   
       x, xval, sumx, \
               y, yval, sumy, \
               z, zval, sumz = read_filecurve (fname)

       x = numpy.divide(x, CONVERTFCT)
       y = numpy.divide(y, CONVERTFCT)
       z = numpy.divide(z, CONVERTFCT)
   
       import matplotlib.pyplot as plt

       plt.clf() 
       plt.cla()

       # in case of a different generation for each NP just move this 
       realtraps = generate_traps (x, xval, sumx, y, yval, sumy, \
               z, zval, sumz, xlist, ylist, zlist, atoms, plt, \
               args.numofpointperstate, verbose)

       realtraps[:] = [ t for t in realtraps if t.set_id(int(id)) ]

       alltraps.extend(realtraps)

       plt.savefig("curve_" + id + ".png", bbox_inches='tight')

   # too big in case of many traps
   #fullsetoftraps = []

   if args.filmfile != "":
       # non mi inter)essano le intersezioni
       nanoparticle.POINTINSIDEDIM = 0

       nanoparticles = []

       print >> sys.stderr, "Reading nanoparticles file"

       botx, topx, boty, topy, botz, topz = \
               nanoparticle.file_to_nanoparticle_list(args.filmfile, \
               nanoparticles) 

       if (botx >= topx) or (boty >= topy) or (boty >= topy):
          print "Error Invalid BOX"
          exit()

       sources = []

       counter = 0

       for nanop in nanoparticles:
         p1, p2, tetha = nanop.get_rotation_info ()

         cx, cy, cz = nanop.get_center()

         counter = counter + 1

         print >> sys.stderr, counter , "of ", len(nanoparticles)

         if main_activatevtk:
             source = vtk.vtkSphereSource()
             source.SetCenter(cx, cy, cz)
             source.SetRadius(1.0)
             sources.append(source)

         centerdtraps = rototranslate_traps (alltraps, cx, cy, cz, \
             p1, p2, tetha, counter)
         
         #fullsetoftraps.extend(centerdtraps)
         
         if verbose:
             for t in centerdtraps:
                 print "%10d %10.5f %10.5f %10.5f %10d %10d"%(t.get_id(), t.get_x(), \
                         t.get_y(), t.get_z(), t.get_npid(), t.get_atomid())

         
         if main_activatevtk:
             for c in centerdtraps:
                 source = vtk.vtkSphereSource()
                 source.SetCenter(c.get_x(), c.get_y(), c.get_z())
                 source.SetRadius(0.5)
                 sources.append(source)
                 
             cube.addcube_to_source(sources, botx, boty, botz, \
                     topx, topy, topz)

       if main_activatevtk:
           # create a rendering window and renderer
           ren = vtk.vtkRenderer()
           renWin = vtk.vtkRenderWindow()
           renWin.AddRenderer(ren)
           
           # create a renderwindowinteractor
           iren = vtk.vtkRenderWindowInteractor()
           iren.SetRenderWindow(renWin)
           
           visualize_all_sources (renWin, iren, sources)

   #if verbose:
   #    for t in fullsetoftraps:
   #        print "%10d %10.5f %10.5f %10.5f %10d %10d"%(t.get_id(), t.get_x(), \
   #                t.get_y(), t.get_z(), t.get_npid(), t.get_atomid())

