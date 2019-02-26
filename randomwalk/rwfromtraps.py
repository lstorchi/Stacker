import sys
import math
import numpy
import random

from operator import attrgetter

import sys
sys.path.append("../modules")

from cube import *
from traps import *
from point import * 
from sphere import *

###############################################################################

def progress_bar (count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 

###############################################################################

def distance(x0, x1, dimensions):
    delta = numpy.abs(x0 - x1)
    delta = numpy.where(delta > 0.5 * dimensions, delta - dimensions, delta)
    return numpy.sqrt((delta ** 2).sum(axis=-1))

###############################################################################

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-f","--filename", help="Traps filename", \
        type=str, required=True, dest="filename")
parser.add_argument("-v", "--verbose", help="increase output verbosity", \
        default=False, action="store_true")
parser.add_argument("--checksingleelectron", help="use a single electron for debugging", \
        default=False, action="store_true")
parser.add_argument("-n", "--num-of-iter", help="Number of iterations ", \
        type=int, required=False, default=100, dest="numofiter")
parser.add_argument("--v0", help="v0 value ", \
        type=float, required=False, default=2.5)
parser.add_argument("--Ec", help="Ec value ", \
        type=float, required=False, default=10.0)
parser.add_argument("--Ei", help="Ei value ", \
        type=float, required=False, default=11.0)
parser.add_argument("-T", help="T value ", \
        type=float, required=False, default=298.0)
parser.add_argument("--min-dist", help="Cut-off radius to neighboured traps ", \
        type=float, required=False, default=20.0, dest="mindist")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

filename = args.filename

checksingle = args.checksingleelectron

# need to set proper values
numofiter = args.numofiter
v0 = args.v0
t0 = 1.0 / v0
Ec = args.Ec
Ei = args.Ei
T = args.T
mindist = args.mindist # radius of the traps where to jump

kB = 1.0

verbose = args.verbose

file = open(filename, "r")

for line in file:
  id, x, y, z, npnum = sp.split(" ")

file.close()
