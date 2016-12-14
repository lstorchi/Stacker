import re
import sys
import math

import numpy
import scipy.ndimage
import scipy.optimize
import scipy.interpolate

import matplotlib.pyplot as plt

###############################################################################

def funcg2(x, a, b, c, d, e, f):
    return a*numpy.exp(-1.0 * (((x - b)**2)/(2*c**2))) + \
           d*numpy.exp(-1.0 * (((x - e)**2)/(2*f**2)))

###############################################################################

if (len(sys.argv)) == 2: 
    filename = sys.argv[1]
else:
    print "usage :", sys.argv[0] , " filename"
    exit(1)

fp = open(filename)

e = []
values = []

em = []
valuesm = []

#em.append(-3.0)
#valuesm.append(0.0)

MIN = -2.0
MAX = 2.5

for l in fp:
    p = re.compile(r'\s+')
    line = p.sub(' ', l)
    line = line.lstrip()
    line = line.rstrip()
    linelist = line.split(" ")

    e.append(float(linelist[0]))
    values.append(float(linelist[1]))

    if (float(linelist[0]) > MIN) and (float(linelist[0]) < MAX):
      em.append(float(linelist[0]))
      valuesm.append(float(linelist[1]))


fp.close()

# gaussina 

gfit = scipy.ndimage.filters.gaussian_filter1d (values, sigma=2.0, 
        cval=40.0, truncate=10.0)

# gaussina 

# minimi quadrati gaussian

params, cmtx = scipy.optimize.curve_fit (funcg2, em, valuesm, maxfev=20000)
cgfitm = []
for i in e:
    cgfitm.append(funcg2(i, params[0], params[1], params[2], 
        params[3], params[4], params[5]))

y1 = params[0]
y1 = 0.0
x1 = params[1] + 2.0 * params[2]
y2 = params[3]
y2 = 0.0
x2 = params[4] - 2.0 * params[5]

print " 2 sigma distance: ", x2-x1

plt.clf()

plt.plot([x1,x2], [y1,y2], 'ro')

plt.plot(e, values, '.')
plt.plot(em, valuesm, '.')
plt.plot(e, gfit)   
plt.plot(e, cgfitm)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
