import re
import sys
import math

import numpy
import scipy.ndimage
import scipy.optimize
import scipy.interpolate

import matplotlib.pyplot as plt

from scipy import interpolate

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

#f = interpolate.interp1d(x, y)
f = numpy.polyfit(x, y, 1)
m, b = f


plt.plot(x, y,'ro',label = 'data')
x_range = numpy.linspace(x[0],x[-1],1000)
for i in range(len(x_range)):
        plt.plot(x_range[i], x_range[i] * m + b, 'go')

print -b/m

plt.show()
