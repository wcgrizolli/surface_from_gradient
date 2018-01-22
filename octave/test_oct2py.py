# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""

# %%% imports cell
import numpy as np
#from oct2py import octave
import oct2py

octave = oct2py.Oct2Py()

# %%

octave.run('test_script_for_octave.m')

#%%
octave.exit()

# %%

im = np.loadtxt('output/fermidirac_5pct_noise_algorithm_0.txt')