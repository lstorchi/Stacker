import re
import sys
import math

import numpy
import scipy.ndimage
import scipy.optimize
import scipy.interpolate

import matplotlib.pyplot as plt

###############################################################################

def funcg(x, a, b, c, d, e, f, g, h, i, l, m, n):
    return a*numpy.sin(x)*numpy.exp(-1.0 * (((x - b)**2)/(2*c**2))) + \
            d*numpy.cos(x)*numpy.exp(-1.0 * (((x - e)**2)/(2*f**2))) + \
            g*numpy.sin(x)*numpy.exp(-1.0 * (((x - h)**2)/(2*i**2))) + \
            l*numpy.cos(x)*numpy.exp(-1.0 * (((x - m)**2)/(2*n**2)))

###############################################################################

def funcg1(x, a, b, c, d, e, f, g, h, i):
    return a*numpy.sin(x)*numpy.exp(-1.0 * (((x - b)**2)/(2*c**2))) + \
            d*numpy.cos(x)*numpy.exp(-1.0 * (((x - e)**2)/(2*f**2))) + \
            g*numpy.sin(x)*numpy.exp(-1.0 * (((x - h)**2)/(2*i**2)))

###############################################################################

def funcg2(x, a, b, c, d, e, f):
    return a*numpy.exp(-1.0 * (((x - b)**2)/(2*c**2))) + \
           d*numpy.exp(-1.0 * (((x - e)**2)/(2*f**2)))

###############################################################################

def funcg3(x, a, b, c, d, e, f):
    return a*numpy.sin(x)*numpy.exp(-1.0 * (((x - b)**2)/(2*c**2))) + \
           d*numpy.cos(x)*numpy.exp(-1.0 * (((x - e)**2)/(2*f**2)))

###############################################################################

def func(x, a, b, c, d, e, f):
    return a + b*x + c*x*x + d*x*x*x + e*numpy.cos(x) + f*numpy.sin(x)

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

for l in fp:
    p = re.compile(r'\s+')
    line = p.sub(' ', l)
    line = line.lstrip()
    line = line.rstrip()
    linelist = line.split(" ")

    e.append(float(linelist[0]))
    values.append(float(linelist[1]))

    if (float(linelist[0]) > -2.0) and (float(linelist[0]) < 2.0):
      em.append(float(linelist[0]))
      valuesm.append(float(linelist[1]))


fp.close()

# gaussina 

gfit = scipy.ndimage.filters.gaussian_filter1d (values, sigma=2.0, 
        cval=40.0, truncate=10.0)


# gaussina 

#newvalues = [] 
#for v in values:
#    if v > 40 :
#        newvalues.append(v)
#    else:
#        newvalues.append(0.0)

#ngfit = scipy.ndimage.filters.gaussian_filter1d (newvalues, sigma=2.0, 
#        cval=40.0, truncate=10.0)

# minimi quadrati 

#params, cmtx = scipy.optimize.curve_fit (func, e, values)

#cfit = []
#for i in e:
#    cfit.append(func(i, params[0], params[1], params[2], 
#        params[3], params[4], params[5]))

# minimi quadrati gaussian

#params, cmtx = scipy.optimize.curve_fit (funcg, e, values, maxfev=20000)
#cgfit = []
#for i in e:
#    cgfit.append(funcg(i, params[0], params[1], params[2], 
#        params[3], params[4], params[5], 
#        params[6], params[7], params[8],
#        params[9], params[10], params[11]))

#params, cmtx = scipy.optimize.curve_fit (funcg, em, valuesm, maxfev=20000)
#cgfitm = []
#for i in e:
#    cgfitm.append(funcg(i, params[0], params[1], params[2], 
#        params[3], params[4], params[5], 
#        params[6], params[7], params[8],
#        params[9], params[10], params[11]))

#params, cmtx = scipy.optimize.curve_fit (funcg1, em, valuesm, maxfev=20000)
#cgfitm = []
#for i in e:
#    cgfitm.append(funcg1(i, params[0], params[1], params[2], 
#        params[3], params[4], params[5], 
#        params[6], params[7], params[8]))

params, cmtx = scipy.optimize.curve_fit (funcg2, em, valuesm, maxfev=20000)
cgfitm = []
for i in e:
    cgfitm.append(funcg2(i, params[0], params[1], params[2], 
        params[3], params[4], params[5]))

# interpolate

#ffit = scipy.interpolate.interp1d(e, values, kind='cubic')
#ifit = ffit(e) 
#s = scipy.interpolate.InterpolatedUnivariateSpline(e, values)
#ifit = s(e)
#tck = scipy.interpolate.splrep(e, values, s = 0.0)
#ifit = scipy.interpolate.splev(e, tck, der=0)

plt.clf()
plt.plot(e, values, '.')
#plt.plot(em, valuesm, '.')

#plt.plot(e, gfit)   
#plt.plot(e, ngfit)   
#plt.plot(e, cfit)
#plt.plot(e, cgfit)
#plt.plot(e, ifit)

plt.plot(e, cgfitm)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

#for i in range(len(r)):
#    print e[i] , r[i]
