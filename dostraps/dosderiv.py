import re
import sys
import math

import numpy
import scipy.ndimage
import scipy.optimize
import scipy.interpolate

import matplotlib.pyplot as plt

from scipy.interpolate import UnivariateSpline

if (len(sys.argv)) == 2: 
    filename = sys.argv[1]
else:
    print "usage :", sys.argv[0] , " filename"
    exit(1)

fp = open(filename)

x = []
y = []

for l in fp:
    p = re.compile(r'\s+')
    line = p.sub(' ', l)
    line = line.lstrip()
    line = line.rstrip()
    linelist = line.split(" ")

    x.append(float(linelist[0]))
    y.append(float(linelist[1]))

fp.close()

y_spl = UnivariateSpline(x,y,s=0,k=4)

plt.plot(x,y,'go',label = 'data')
#x_range = numpy.linspace(x[0],x[int(float(len(x))/2.0)],1000)
#plt.plot(x_range,y_spl(x_range))

x1 = -5.418
x2 = -3.139

y1 = y_spl(x1)
y2 = y_spl(x2)

y_spl_1d = y_spl.derivative(n=1)
m1 = y_spl_1d(-5.418)
m2 = y_spl_1d(-3.139)

q1 = y1 - m1*x1
q2 = y2 - m2*x2

x_range = numpy.linspace(x[0],x[int(float(len(x))/2.0)],1000)
for i in range(len(x_range)):
    plt.plot(x_range[i], x_range[i] * m1 + q1, 'go--')

x_range = numpy.linspace(x[int(float(len(x))/2.0)], x[-1], 1000)
for i in range(len(x_range)):
    plt.plot(x_range[i], x_range[i] * m2 + q2, 'go--')


print m1, q1, -q1/m1
print m2, q2, -q2/m2

plt.show()
