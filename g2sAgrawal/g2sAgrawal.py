# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""

import oct2py


# %%

global octave

octave = oct2py.Oct2Py()

octave.eval('pkg load signal')
octave.eval('pkg load image')

print('Octave Loaded')


# %%

def poisson_solver_function_neumann(g_x, g_y):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)

    octave.eval('r_ls = poisson_solver_function_neumann(g_x, g_y);')  # I

    return octave.pull('r_ls')


def frankotchellappa(g_x, g_y):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)

    octave.eval('fc = frankotchellappa(g_x, g_y);')  # II

    return octave.pull('fc')


def M_estimator(g_x, g_y):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)

    octave.eval('r_M = M_estimator(g_x, g_y); r_M = r_M - min(r_M(:));')  # IV

    return octave.pull('r_M')


def halfquadractic(g_x, g_y):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)

    octave.eval('rr = halfquadractic(g_x, g_y);')  # V

    return octave.pull('rr')


def affineTransformation(g_x, g_y):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)

    octave.eval('[x,D11,D12,D22] = AffineTransformation(g_x,g_y);')  # VI

    return octave.pull('x')






