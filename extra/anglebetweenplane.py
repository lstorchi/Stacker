import sys
sys.path.append("../modules")

import plane
import point

import math

p1 = point.point(  0.060167 , -0.267595 , -0.094069)
p2 = point.point( -0.029163 , -0.510884 ,  1.967362)
p3 = point.point( -1.836883 ,  0.380311 ,  0.286389)

pA = plane.plane(p1, p2, p3)

p4 = point.point(  0.060167 , -0.267595 , -0.094069) 
p5 = point.point(  2.036123 , -0.514122 ,  0.052635)
p6 = point.point( -0.129902 , -0.189737 , -1.927521 )

pB = plane.plane(p4, p5, p6)

angle = pA.return_angle(pB)
print angle ,  "rad " , 360.0 * (angle/math.pi), " grad"
