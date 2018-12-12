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

plt.plot(x,y,'ro',label = 'data')
x_range = numpy.linspace(x[0],x[-1],1000)
plt.plot(x_range,y_spl(x_range))

y_spl_2d = y_spl.derivative(n=2)
y_dev = y_spl_2d(x_range)

minmax = numpy.r_[True, y_dev[1:] < y_dev[:-1]] & numpy.r_[y_dev[:-1] < y_dev[1:], True]

for i in range(minmax.size):
    if minmax[i]:
        print x_range[i], y_dev[i]
        plt.plot(x_range[i], y_dev[i], 'rv',label = 'data')

plt.plot(x_range,y_dev)

# dal plot delle derivate secone e dal grafico vedo il flesso 
# piu' ragionevole

plt.show()
