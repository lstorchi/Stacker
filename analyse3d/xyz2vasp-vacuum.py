import sys
from ase.io.vasp import *
from ase.io.xyz import *
from ase.io import *

# python xyz2vasp.py file.xyz vacuumvalue

#system = read_xyz(sys.argv[1])
system = read(sys.argv[1], 0, "xyz")
output = 'POSCAR' + sys.argv[1]

defaultvacuum=10

if len(sys.argv) > 2:
    vacuumvalue = float(sys.argv[2])
else:
    vacuumvalue = float(defaultvacuum)

system.center(vacuum=vacuumvalue)

print 'value of vacuum: ', vacuumvalue

write_vasp(output,system, label='xyz2vasp',direct=True,sort=True,vasp5=True)
