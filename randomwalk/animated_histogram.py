import sys
import argparse
import collections

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.path as path
import matplotlib.patches as patches
import matplotlib.animation as animation


#####################################################################

def file_len(fname):
    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass

    return i + 1

#####################################################################

def counter_hist(data):

    counter = {}
    for v in data:

        if v in counter:
            counter[v] += 1
        else:
            counter[v] = 1

    for k, v in collections.OrderedDict(sorted(counter.items())).items():
        if v != 0:
            print(k, ":", v)


#####################################################################

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filename", help="Traps filename", \
        type=str, required=True, dest="filename")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()
filename = args.filename

numoflines = file_len(filename)

fp = open(filename, "r")

data = []

l = fp.readline()
data.append(list(map(int, l.split())))

n, bins = np.histogram(data[-1], 100)

left = np.array(bins[:-1])
right = np.array(bins[1:])
bottom = np.zeros(len(left))
top = bottom + n
nrects = len(left)

nverts = nrects * (1 + 3 + 1)
verts = np.zeros((nverts, 2))
codes = np.ones(nverts, int) * path.Path.LINETO
codes[0::5] = path.Path.MOVETO
codes[4::5] = path.Path.CLOSEPOLY
verts[0::5, 0] = left
verts[0::5, 1] = bottom
verts[1::5, 0] = left
verts[1::5, 1] = top
verts[2::5, 0] = right
verts[2::5, 1] = top
verts[3::5, 0] = right
verts[3::5, 1] = bottom

numid = 2
patch = None

def animate(i):
    l = fp.readline()
    data.append(list(map(int, l.split())))
    n, bins = np.histogram(data[-1], 100)

    print(i)
    counter_hist(data[-1])
    print()

    top = bottom + n
    verts[1::5, 1] = top
    verts[2::5, 1] = top
    return [patch, ]

fig, ax = plt.subplots()
barpath = path.Path(verts, codes)
patch = patches.PathPatch(
            barpath, facecolor='green', edgecolor='yellow', alpha=0.5)
ax.add_patch(patch)

ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max())

ani = animation.FuncAnimation(fig, animate, numoflines-4, interval=10, repeat=False, blit=True)
plt.show()
