import vtk
import random

# http://www.vtk.org/pipermail/vtkusers/2011-March/115686.html

import sys
sys.path.append("./modules")

from sphere import *
from point import *
from cube import *

spheres = []

class vtkTimerCallback():
   def __init__(self):
       self.timer_count = 0
 
   def execute(self,obj,event):

       iren = obj
       wren = iren.GetRenderWindow()
       renderer = wren.GetRenderers().GetFirstRenderer()

       #print self.timer_count

       if (self.timer_count < len(spheres)):
       
         sphereSource = vtk.vtkSphereSource()

         c = spheres[self.timer_count].get_center()
         
         cx = c.get_x()
         cy = c.get_y()
         cz = c.get_z()
         R = spheres[self.timer_count].get_radius()
         
         sphereSource.SetCenter(cx, cy, cz)
         sphereSource.SetRadius(R)
         
         #Create a mapper and actor
         mapper = vtk.vtkPolyDataMapper()
         mapper.SetInputConnection(sphereSource.GetOutputPort())
         actor = vtk.vtkActor()
         actor.SetMapper(mapper)

         actor.GetProperty().SetOpacity(0.5)
        
         renderer.AddActor(actor)
 
       iren.GetRenderWindow().Render()
       self.timer_count += 1
 
 
def main():
   # Setup a renderer, render window, and interactor
   renderer = vtk.vtkRenderer()
   renderWindow = vtk.vtkRenderWindow()
   #renderWindow.SetWindowName("Test")
 
   renderWindow.AddRenderer(renderer);
   renderWindowInteractor = vtk.vtkRenderWindowInteractor()
   renderWindowInteractor.SetRenderWindow(renderWindow)

   # determino la box
   file = open("final_config.txt", "r")

   zmax = xmax = ymax = -10000.0
   zmin = xmin = ymin =  10000.0

   for sp in file:
     x, y, z, r = sp.split(" ")
     center = point(float(x), float(y), float(z))
     s = sphere(center, float(r))
     spheres.append(s)

     if (zmax < (float(z) + float(r))):
       zmax = (float(z) + float(r))
     if (xmax < (float(x) + float(r))):
       xmax = (float(x) + float(r))
     if (ymax < (float(y) + float(r))):
       ymax = (float(y) + float(r))
     
     if (zmin > (float(z) - float(r))):
       zmin = (float(z) - float(r))
     if (xmin > (float(x) - float(r))):
       xmin = (float(x) - float(r))
     if (ymin > (float(y) - float(r))):
       ymin = (float(y) - float(r))

   file.close()
 
   # add cube
   sources = []

   addcube_to_source (sources, zmin, ymin, zmin, \
       xmax, ymax, zmax)

   for s in sources:
     mapper = vtk.vtkPolyDataMapper()
     mapper.SetInputConnection(s.GetOutputPort())
     actor = vtk.vtkActor()
     actor.SetMapper(mapper)
     renderer.AddActor(actor)

   file = open("final_config.txt", "r")

   for sp in file:
     x, y, z, r = sp.split(" ")
     center = point(float(x), float(y), float(z))
     s = sphere(center, float(r))
     spheres.append(s)

   file.close()
 
   #Render and interact
   renderWindow.Render()
 
   # Initialize must be called prior to creating timer events.
   renderWindowInteractor.Initialize()
 
   # Sign up to receive TimerEvent
   cb = vtkTimerCallback()
   cb.actor = actor
   renderWindowInteractor.AddObserver('TimerEvent', cb.execute)
   timerId = renderWindowInteractor.CreateRepeatingTimer(100);
 
   #start the interaction and timer
   renderWindowInteractor.Start()
 
 
if __name__ == '__main__':
   main()
