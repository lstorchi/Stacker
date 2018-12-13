import os
import sys
import math
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize, signal

from lmfit import models

################################################################################

def g(x, A, m, s):
    return A / (s * math.sqrt(2 * math.pi)) * np.exp(-(x-m)**2 / (2*s**2))

################################################################################

def cost(parameters):
    g_0 = parameters[:3]
    g_1 = parameters[3:6]
    
    return np.sum(np.power(g(x, *g_0) + g(x, *g_1) - y, 2)) / len(x)

################################################################################

def generate_model(spec):
    composite_model = None
    params = None
    x = spec['x']
    y = spec['y']
    x_min = np.min(x)
    x_max = np.max(x)
    x_range = x_max - x_min
    y_max = np.max(y)
    for i, basis_func in enumerate(spec['model']):
        prefix = f'm{i}_'
        model = getattr(models, basis_func['type'])(prefix=prefix)
        if basis_func['type'] in ['GaussianModel', 'LorentzianModel', 'VoigtModel']: # for now VoigtModel has gamma constrained to sigma
            model.set_param_hint('sigma', min=1e-6, max=x_range)
            model.set_param_hint('center', min=x_min, max=x_max)
            model.set_param_hint('height', min=1e-6, max=1.1*y_max)
            model.set_param_hint('amplitude', min=1e-6)
            # default guess is horrible!! do not use guess()
            default_params = {
                prefix+'center': x_min + x_range * random.random(),
                prefix+'height': y_max * random.random(),
                prefix+'sigma': x_range * random.random()
            }
        else:
            raise NotImplemented(f'model {basis_func["type"]} not implemented yet')
        if 'help' in basis_func:  # allow override of settings in parameter
            for param, options in basis_func['help'].items():
                model.set_param_hint(param, **options)
        model_params = model.make_params(**default_params, **basis_func.get('params', {}))
        if params is None:
            params = model_params
        else:
            params.update(model_params)
        if composite_model is None:
            composite_model = model
        else:
            composite_model = composite_model + model
    return composite_model, params


################################################################################

def update_spec_from_peaks(spec, model_indicies, peak_widths=(10, 25), **kwargs):
    x = spec['x']
    y = spec['y']
    x_range = np.max(x) - np.min(x)
    peak_indicies = signal.find_peaks_cwt(y, peak_widths)
    np.random.shuffle(peak_indicies)
    for peak_indicie, model_indicie in zip(peak_indicies.tolist(), model_indicies):
        model = spec['model'][model_indicie]
        if model['type'] in ['GaussianModel', 'LorentzianModel', 'VoigtModel']:
            params = {
                'height': y[peak_indicie],
                'sigma': x_range / len(x) * np.min(peak_widths),
                'center': x[peak_indicie]
            }
            if 'params' in model:
                model.update(params)
            else:
                model['params'] = params
        else:
            raise NotImplemented(f'model {basis_func["type"]} not implemented yet')
    return peak_indicies

################################################################################

x = []
y = []

fp = open(sys.argv[1])
for l in fp:
    sl = l.split()
    x.append(float(sl[0]))
    y.append(float(sl[1]))

initial_guess = [1, -5.3, 0.2, 1, -3.2, 0.2]
result = optimize.minimize(cost, initial_guess)

print("steps", result.nit, result.fun)
print("g_0: amplitude: %3.3f mean: %3.3f sigma:%3.3f "%(result.x[0], result.x[1], result.x[2]))
print("g_1: amplitude: %3.3f mean: %3.3f sigma:%3.3f "%(result.x[3], result.x[4], result.x[5]))

fig, ax = plt.subplots()
ax.scatter(x, y, s=1)
ax.plot(x, g(x, *result.x[:3]))
ax.plot(x, g(x, *result.x[3:6]))
ax.plot(x, g(x, *result.x[:3]) + g(x, *result.x[3:6]))

"""

spec = {
        'x': x,
        'y': y,
        'model': [
            {'type': 'GaussianModel'},
            {'type': 'GaussianModel'},
            {'type': 'GaussianModel'},
            {'type': 'GaussianModel'},
            {'type': 'GaussianModel'}
            ]
        }

#peaks_found = update_spec_from_peaks(spec, [0, 1, 2, 3, 4], peak_widths=(15,))

model, params = generate_model(spec)

#fig, ax = plt.subplots()
#ax.scatter(spec['x'], spec['y'], s=4)

output = model.fit(spec['y'], params, x=spec['x'])

#components = output.eval_components(x=spec['x'])
#print(len(spec['model']))
#for i, model in enumerate(spec['model']):
#        ax.plot(spec['x'], components[f'm{i}_'])

fig, gridspec = output.plot(data_kws={'markersize': 1})

"""

plt.show()
