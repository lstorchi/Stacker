import pyOpt
from pyOpt import SNOPT

def objfunc(x):

  f = (x[0]+x[1])

  g = [0.0]

  #print g

  g[0] = x[0]*x[0] + x[1]*x[1] 

  fail = 0
  return f,g, fail

opt_prob = pyOpt.Optimization('2-D example wiki Constrained Problem',objfunc)

opt_prob.addObj('f')

opt_prob.addVar('x1','c',lower=0.0,upper=float('inf'),value=2.0)
opt_prob.addVar('x2','c',lower=0.0,upper=float('inf'),value=2.0)

opt_prob.addCon('g', type='i', lower=1, upper=2)

solvopt = SNOPT()
[fstr, xstr, inform] = solvopt(opt_prob,sens_type='FD')

#print opt_prob
print opt_prob.solution(0)
