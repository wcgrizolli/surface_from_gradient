# -*- coding: utf-8 -*-
"""

@author: Walan
"""

# %%

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np


import time
import sys

#global octave

sys.path.append('../g2sAgrawal')
import g2sAgrawal
# In the following line you need to add the MATLAB folder to the octave path
# Because it has nothing to do with the PYTHONPATH, you better add the absolute path
g2sAgrawal.octave.eval("addpath(genpath('../g2sAgrawal/AgrawalECCV06CodeMFiles/'));")



sys.path.append('../g2sHarker')
import g2sHarker
# In the following line you need to add the MATLAB folder to the octave path
# Because it has nothing to do with the PYTHONPATH, you better add the absolute path
g2sHarker.octave.eval("addpath(genpath('../g2sHarker/grad2Surf/'));")
g2sHarker.octave.eval("addpath(genpath('../g2sHarker/DOPBox/'));")

sys.path.append('../utils') # I only need this to generate the source
from sample_fermi_diracs import *


# %%

plotInputs = False
noiseFlag = False
noiseLevel = 5.0  # in percents
plotSurfsFlag = False
plotErrorsFlag = False
plotErrorsGradFlag = False


def _grad(func):

    del_func_2d_x = np.diff(func, axis=1)
    del_func_2d_x = np.pad(del_func_2d_x, ((0, 0), (1, 0)), 'edge')

    del_func_2d_y = np.diff(func, axis=0)
    del_func_2d_y = np.pad(del_func_2d_y, ((1, 0), (0, 0)), 'edge')

    return del_func_2d_x, del_func_2d_y


def _err(res, model, plotHist=False):

    res -= np.mean(res)
    model -= np.mean(model)

    array2plot = np.abs(model - res).flatten()

    if plotHist:

        plt.figure()
        plt.hist(array2plot, 51)
        plt.title(r'Err $=\| model - result \|$,' +
                  r' $\mu=${:.4f}'.format(np.mean(array2plot)))
        plt.show()

    return np.mean(array2plot)


def _rerr(res, model, plotHist=False):

    res -= np.mean(res)
    model -= np.mean(model)

    array2plot = np.abs((model - res)/np.ptp(model)).flatten()

    if plotHist:

        plt.figure()
        plt.hist(array2plot, 51)
        plt.title(r'Relative Err $=\| model - result\| / PV(model)$,' +
                  ' $\mu=${:.4f}'.format(np.mean(array2plot)))
        plt.show()

    return np.mean(array2plot)

# %%

nx = 101
ny = 101  # some number here crash the program. test in newer octave. 200x200 works
radius = nx // 15
im = sample_fermi_diracs(nx, ny, radius)
yy, xx = np.mgrid[0:ny, 0:nx]
g_x, g_y = _grad(im)

if plotInputs:
    plt.figure(figsize=(14, 6))
    plt.subplot(121)
    plt.imshow(g_x, cmap='RdGy')
    plt.colorbar(shrink=0.5)
    plt.title('g_x', fontsize=18, weight='bold')

    plt.subplot(122)
    plt.imshow(g_y, cmap='RdGy')
    plt.colorbar(shrink=0.5)
    plt.title('g_y', fontsize=18, weight='bold')

    plt.suptitle('Gradients, No noise',
                 fontsize=18, weight='bold')
    plt.show()

    for [plotThis, titleStr] in zip([im, g_x, g_y], ['im', 'g_x', 'g_y']):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.title(titleStr + ', No noise')
        ax.plot_surface(xx, yy, plotThis, rstride=nx//100, cstride=ny//100, cmap='jet', linewidth=0.1)
        plt.show()

if noiseFlag:
    np.random.seed(23153493)
    g_x += noiseLevel*np.ptp(g_x)/100*np.random.randn(ny, nx)
    np.random.seed(64709745)
    g_y += noiseLevel*np.ptp(g_y)/100*np.random.randn(ny, nx)

if (noiseFlag and plotInputs):
    plt.figure(figsize=(14, 6))
    plt.subplot(121)
    plt.imshow(g_x, cmap='RdGy')
    plt.colorbar(shrink=0.5)
    plt.title('g_x', fontsize=18, weight='bold')

    plt.subplot(122)
    plt.imshow(g_y, cmap='RdGy')
    plt.colorbar(shrink=0.5)
    plt.title('g_y', fontsize=18, weight='bold')

    plt.suptitle('Gradients, {:.1f} % noise'.format(noiseLevel),
                 fontsize=18, weight='bold')
    plt.show()

    for [plotThis, titleStr] in zip([g_x, g_y], ['g_x', 'g_y']):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, plotThis, rstride=nx//100, cstride=ny//100, cmap='jet', linewidth=0.1)
        plt.title('Noise added')
        plt.show()




plt.show(block=True)

# %%
tic = time.time()
res1 = g2sAgrawal.poisson_solver_function_neumann(g_x, g_y)
toc1 = time.time() - tic

tic = time.time()
res2 = g2sAgrawal.frankotchellappa(g_x, g_y)
toc2 = time.time() - tic

tic = time.time()
res4 = g2sAgrawal.M_estimator(g_x, g_y)
toc4 = time.time() - tic

tic = time.time()
res5 = g2sAgrawal.halfquadractic(g_x, g_y)
toc5 = time.time() - tic

tic = time.time()
res6 = g2sAgrawal.affineTransformation(g_x, g_y)
toc6 = time.time() - tic


tic = time.time()
res7 = g2sHarker.g2s(g_x, g_y)
toc7 = time.time() - tic

tic = time.time()
res8 = g2sHarker.g2sSpectral(g_x, g_y, basisFns='poly')
toc8 = time.time() - tic

tic = time.time()
res9 = g2sHarker.g2sDirichlet(g_x, g_y)
toc9 = time.time() - tic

tic = time.time()
res10 = g2sHarker.g2sTikhonov(g_x, g_y)
toc10 = time.time() - tic

tic = time.time()
res11 = g2sHarker.g2sTikhonovStd(g_x, g_y)
toc11 = time.time() - tic


# %% List with all results
all_res = [im, res1, res2, res2*0.0, res4, res5, res6, res7, res8, res9, res10, res11]
all_toc = [toc1, toc2, np.nan, toc4, toc5, toc6, toc7, toc8, toc9, toc10, toc11]

# %%
print("--- RACE RESULTS")

for i,toc in enumerate(all_toc):
    print("--- Algorithm %d:  %.4f seconds ---" % (i + 1, toc))

# %%

if plotSurfsFlag:

    for res in all_res:

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, res, rstride=nx//100, cstride=ny//100, cmap='jet', linewidth=0.1)
        plt.show()


plt.show(block=True)

# %%

if plotErrorsFlag:

    for res in all_res:

        err = _err(res, im, plotHist=False)
        rerr = _rerr(res, im, plotHist=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, im-res,
                        rstride=nx//100, cstride=ny//100,
                        cmap='jet', linewidth=0.1)

        str_err = 'Error = {:.4g}, Rel error = {:.4g}'.format(err, rerr)
        plt.title(str_err)
        plt.show()
        print(str_err)

plt.show(block=True)

# %%

if plotErrorsGradFlag:

    for res in all_res:

        res_g_x, res_g_y = _grad(res)

        err_x = _err(res_g_x, g_x, plotHist=False)
        rerr_x = _rerr(res_g_x, g_x, plotHist=False)
        err_y = _err(res_g_y, g_y, plotHist=False)
        rerr_y = _rerr(res_g_y, g_y, plotHist=False)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, res_g_x - g_x, rstride=nx//100, cstride=ny//100, cmap='jet', linewidth=0.1)
        str_err_x = 'g_x Error = {:.4g}, Rel error = {:.4g}'.format(err_x, rerr_x)
        plt.title(str_err_x)
        plt.show()


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, res_g_y - g_y, rstride=nx//100, cstride=ny//100, cmap='jet', linewidth=0.1)
        str_err_y = 'g_y Error = {:.4g}, Rel error = {:.4g}'.format(err_y, rerr_y)
        plt.title(str_err_y)
        plt.show(block=True)

        print(str_err_x + ',\t' + str_err_y)


