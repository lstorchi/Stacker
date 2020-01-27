from os import listdir
from os.path import isfile, join

#####################################################################

def is_an_int(s):
    
    try: 
        int(s)
        return True
    except ValueError:
        return False

#####################################################################

mypath = "/pub3/redo/"

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
    print("need to check at steps ", s, " for ", num_of_ele, " electrons ")
