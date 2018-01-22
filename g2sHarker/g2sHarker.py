# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""

import oct2py


# %%

octave = oct2py.Oct2Py()

octave.eval('pkg load signal')
octave.eval('pkg load image')

print('Octave Loaded')


# %%

def g2s(g_x, g_y, N=3):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)
    octave.eval("[H,W] = size(g_x);")
    octave.eval("x = linspace(1, W, W)';")
    octave.eval("y = linspace(1, H, H)';")
    octave.push('N', N)

    octave.eval('Z = g2s( g_x, g_y, x, y, N );')  # I

    return octave.pull('Z')


def g2sSpectral(g_x, g_y, N=3, mask=None, basisFns='cosine'):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)
    octave.eval("[H,W] = size(g_x);")
    octave.eval("x = linspace(1, W, W)';")
    octave.eval("y = linspace(1, H, H)';")
    octave.push('N', N)

    if mask is None:
        mask = [g_x.shape[1]//4, g_x.shape[0]//4]

    octave.push('Mask', mask)

    octave.push('basisFns', basisFns)

    octave.eval('Z = g2sSpectral( g_x, g_y, x, y, N, Mask, basisFns );')  # II

    return octave.pull('Z')


def g2sDirichlet(g_x, g_y, N=3, boundaryMatrix=None):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)
    octave.eval("[H,W] = size(g_x);")
    octave.eval("x = linspace(1, W, W)';")
    octave.eval("y = linspace(1, H, H)';")
    octave.push('N', N)

    if boundaryMatrix is None:
        octave.eval("ZB = zeros(H, W)';")
    else:
        octave.push('ZB', boundaryMatrix)

    octave.eval('Zdir = g2sDirichlet( g_x, g_y, x, y, N, ZB );')  # IV

    return octave.pull('Z')


def g2sTikhonov(g_x, g_y, N=3, lambdaPar=0.025, deg=0, Z0=None):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)
    octave.eval("[H,W] = size(g_x);")
    octave.eval("x = linspace(1, W, W)';")
    octave.eval("y = linspace(1, H, H)';")
    octave.push('N', N)
    octave.push('lambda', lambdaPar)
    octave.push('deg', deg)

    if Z0 is None:
        octave.eval("Z0 = zeros(H, W)';")
    else:
        octave.push('Z0', Z0)

    octave.eval('[ Z, Res ] = g2sTikhonov( g_x, g_y, x, y, N, lambda, deg, Z0);')  # V

    return octave.pull('Z')


def g2sTikhonovStd(g_x, g_y, N=3, noLambdas=100, Z0=None):

    octave.push('g_x', g_x)
    octave.push('g_y', g_y)
    octave.eval("[H,W] = size(g_x);")
    octave.eval("x = linspace(1, W, W)';")
    octave.eval("y = linspace(1, H, H)';")
    octave.push('N', N)
    octave.push('noLambdas', noLambdas)

    if Z0 is None:
        octave.eval("Z0 = zeros(H, W)';")
    else:
        octave.push('Z0', Z0)

    octave.eval('[ Z, lamOpt, RC, Theta ] = g2sTikhonovStd( g_x, g_y, x, y, N, noLambdas, Z0 );')  # VI

    return octave.pull('Z')

#
#Z = g2s( g_x, g_y, x, y, N ) ;
#Zpoly = g2sSpectral( g_x, g_y, x, y, N, Mask, basisFns ) ;
#Zdir = g2sDirichlet( g_x, g_y, x, y, 5, ZB ) ;
#[ Ztik, Res ] = g2sTikhonov( g_x, g_y, x, y, N, lambda, deg, Z0 ) ;
#[ ZtikL, lamOpt, RC, Theta ] = g2sTikhonovStd( g_x, g_y, x, y, N, noLambdas, Z0 ) ;
#


