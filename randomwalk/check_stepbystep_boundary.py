from os import listdir
from os.path import isfile, join

import argparse
import math
import sys

import convert_boundary_cond

#####################################################################

def is_an_int(s):
    
    try: 
        int(s)
        return True
    except ValueError:
        return False

#####################################################################

mypath = "/pub3/redo/"

parser = argparse.ArgumentParser()

parser.add_argument("-p","--filepath", help="Electron filename root path", \
                    type=str, required=True)
parser.add_argument("-d","--dimensions", help="dimension \"xdim:ydim:zdim\"", \
                    type=str, required=True)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()
mypath = args.filepath
sxdim, sydim, szdim = args.dimensions.split(":")

xdim = float(sxdim)
ydim = float(sydim)
zdim = float(szdim)

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

num_of_ele = 0
steps = set()
for f in onlyfiles:
    if f.find("electrons_") >= 0 and f.find("_at_step_") >= 0:
        val = f[f.find("at_step")+8:-4]
        
        if is_an_int(val):
            steps.add(int(val))
        else:
            print("check name: ", f)

        val = f[f.find("_of_")+4:f.find("_at_step_")]

        if is_an_int(val):
            if num_of_ele < int(val):
                num_of_ele = int(val)

for s in sorted(steps):
    print("need to check at steps %6d"%(s), " for %5d"%(num_of_ele), " electrons ")

    fulldist = 0.0
    for i in range(1, num_of_ele+1):
        filename = mypath+"electrons_%d_of_%d_at_step_%d.txt"%(i, num_of_ele, s)
        #print(filename)

        file = open(filename, "r")

        coordinates = []
        for line in file:
            mergedline = ' '.join(line.split())
            sx, sy, sz, snpnum, stpidx, strapid = mergedline.split(" ")

            x = float(sx)
            y = float(sy)
            z = float(sz)

            coordinates.append([x, y, z, int(snpnum), int(stpidx), int(strapid)])

        file.close()
        final = convert_boundary_cond.resort_boundary (xdim, ydim, zdim, coordinates)
        
        #for f in final:
        #    print("%10.5f %10.5f %10.5f %10d %10d"%(f[0], f[1], f[2], f[3], f[4]))

        start = final[0]
        end = final[-1]

        dist = math.sqrt((start[0]-end[0])**2 + \
                (start[1]-end[1])**2 + \
                (start[2]-end[2])**2)

        fulldist += dist

    print("    AVG D: %10.5f"%(fulldist/float(num_of_ele)))

