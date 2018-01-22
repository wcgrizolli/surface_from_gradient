# -*- coding: utf-8 -*-
"""

This scripts shows how oct2py is used to run matlab code in python.

The goal is only to ilustrate. Do not use this method for your calculations


@author: Walan
"""


# %%% imports cell
import numpy as np
import matplotlib.pyplot as plt


import time


# %%
import oct2py

octave = oct2py.Oct2Py()

# %%

octave.eval("addpath(genpath('../g2sAgrawal/AgrawalECCV06CodeMFiles/'));")
octave.eval("addpath(genpath('../octave/'));")
octave.eval("addpath(genpath('../utils/'));")

octave.eval('pkg load signal')
octave.eval('pkg load image')

# %%

octave.push('H', 201.0)
octave.push('W', 201.0)
octave.push('radius', 201.0//15)

octave.eval('im = sample_fermi_diracs(H, W, radius);')

# %%
octave.eval('[g_x,g_y] = calculate_gradients(im,0,0);')

octave.eval('[H,W] = size(g_x)')

# %%

tic = time.time()
octave.eval('r_ls = poisson_solver_function_neumann(g_x, g_y);')  # I
toc1 = time.time() - tic

tic = time.time()
octave.eval('fc = frankotchellappa(g_x, g_y);')  # II
toc2 = time.time() - tic

tic = time.time()
octave.eval('r_M = M_estimator(g_x, g_y, 0); r_M = r_M - min(r_M(:));')  # IV
toc4 = time.time() - tic

tic = time.time()
octave.eval('rr = halfquadractic(g_x, g_y);')  # V
toc5 = time.time() - tic

tic = time.time()
octave.eval('[x,D11,D12,D22] = AffineTransformation(g_x,g_y);')  # VI
toc6 = time.time() - tic


# %%


im = octave.pull('im')
g_x = octave.pull('g_x')
g_y = octave.pull('g_y')

r_ls = octave.pull('r_ls');
fc = octave.pull('fc');
r_M = octave.pull('r_M');
rr = octave.pull('rr');
x = octave.pull('x');

octave.eval('whos')


# %%
print("--- RACE RESULTS")
print("--- Algorithm 1:  %.4f seconds ---" % (toc1))
print("--- Algorithm 2:  %.4f seconds ---" % (toc2))
print("--- Algorithm 4:  %.4f seconds ---" % (toc4))
print("--- Algorithm 5:  %.4f seconds ---" % (toc5))
print("--- Algorithm 6:  %.4f seconds ---" % (toc6))



