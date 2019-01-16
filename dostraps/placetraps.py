import re
import sys

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

