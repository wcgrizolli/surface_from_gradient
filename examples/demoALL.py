# -*- coding: utf-8 -*-
"""

@author: Walan
"""

# %%
import matplotlib
matplotlib.use('Agg')
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

plotInputs = True
plotHist = False
noiseFlag = False
noiseLevel = 5.0  # in percents
plotSurfsFlag = True
plotErrorsFlag = True
plotErrorsGradFlag = True

from itertools import count
_count_fig = count()
next(_count_fig)


def unique_fname():
    fname = 'fig_' + str('{:02d}'.format(next(_count_fig))) + '.png'
    print('Saving ' + fname)
    return(fname)


def _grad(func):

    del_func_2d_x = np.diff(func, axis=1)
    del_func_2d_x = np.pad(del_func_2d_x, ((0, 0), (1, 0)), 'edge')

    del_func_2d_y = np.diff(func, axis=0)
    del_func_2d_y = np.pad(del_func_2d_y, ((1, 0), (0, 0)), 'edge')

    return del_func_2d_x, del_func_2d_y


def _err(res, model):

    res -= np.mean(res)
    model -= np.mean(model)

    array2plot = np.abs(model - res).flatten()

    if plotHist:

        plt.figure()
        plt.hist(array2plot, 51)
        plt.title(r'Err $=\| model - result \|$,' +
                  r' $\mu=${:.4f}'.format(np.mean(array2plot)))

        plt.savefig(unique_fname())
        plt.close()

    return np.mean(array2plot)


def _rerr(res, model):

    res -= np.mean(res)
    model -= np.mean(model)

    array2plot = np.abs((model - res)/np.ptp(model)).flatten()

    if plotHist:

        plt.figure()
        plt.hist(array2plot, 51)
        plt.title(r'Relative Err $=\| model - result\| / PV(model)$,' +
                  ' $\mu=${:.4f}'.format(np.mean(array2plot)))

        plt.savefig(unique_fname())
        plt.close()

    return np.mean(array2plot)

# %%

# some number nx and ny crash the program.
# test in newer octave. 200x200 works
# WG: I think it must be multiple of 4 to match the mask of g2s
nx = 500
ny = 500

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
    plt.tight_layout()
    plt.savefig(unique_fname())
    plt.close()

    for [plotThis, titleStr] in zip([im, g_x, g_y], ['im', 'g_x', 'g_y']):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.title(titleStr + ', No noise')
        ax.plot_surface(xx, yy, plotThis,
                        rstride=nx//100, cstride=ny//100,
                        cmap='jet', linewidth=0.1)
        plt.tight_layout()
        plt.savefig(unique_fname())
        plt.close()

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
    plt.close()

    for [plotThis, titleStr] in zip([g_x, g_y], ['g_x', 'g_y']):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, plotThis,
                        rstride=nx//100, cstride=ny//100,
                        cmap='jet', linewidth=0.1)
        plt.title('Noise added')
        plt.close()
        plt.tight_layout()
        plt.savefig(unique_fname())
        plt.close()


# plt.show(block=True)

# %%

all_res = []
all_toc = []
all_titles = []

list_of_algorithms = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#list_of_algorithms = [1, 2, 6, 7, 8, 9, 10]

if 1 in list_of_algorithms:
    tic = time.time()
    res = g2sAgrawal.poisson_solver_function_neumann(g_x, g_y)
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('I - poisson_solver_function_neumann')

if 2 in list_of_algorithms:
    tic = time.time()
    res = g2sAgrawal.frankotchellappa(g_x, g_y)
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('II - frankotchellappa')

if 3 in list_of_algorithms:
    tic = time.time()
    res = g2sAgrawal.M_estimator(g_x, g_y)
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('III - M_estimator')

if 4 in list_of_algorithms:
    tic = time.time()
    res = g2sAgrawal.halfquadractic(g_x, g_y)
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('IV - halfquadractic')

if 5 in list_of_algorithms:
    tic = time.time()
    res = g2sAgrawal.affineTransformation(g_x, g_y)
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('V - affineTransformation')

if 6 in list_of_algorithms:
    tic = time.time()
    res = g2sHarker.g2s(g_x, g_y)
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('VI - g2s')

if 7 in list_of_algorithms:
    tic = time.time()
    res = g2sHarker.g2sSpectral(g_x, g_y, basisFns='poly')
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('VII - g2sSpectral')

if 8 in list_of_algorithms:
    tic = time.time()
    res = g2sHarker.g2sDirichlet(g_x, g_y)
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('VIII - g2sDirichlet')

if 9 in list_of_algorithms:
    tic = time.time()
    res = g2sHarker.g2sTikhonov(g_x, g_y)
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('IX - g2sTikhonov')

if 10 in list_of_algorithms:
    tic = time.time()
    res = g2sHarker.g2sTikhonovStd(g_x, g_y)
    toc = time.time() - tic
    all_res.append(res)
    all_toc.append(toc)
    all_titles.append('X - g2sTikhonovStd')


# %%

if plotSurfsFlag:

    for i, res in enumerate(all_res):

        print('Plot results: ' + all_titles[i])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, res,
                        rstride=nx//100, cstride=ny//100,
                        cmap='jet', linewidth=0.1)
        plt.title(all_titles[i])
        plt.tight_layout()
        plt.savefig(unique_fname())
        plt.close()


# plt.show(block=True)

# %%

all_err = []
all_rerr = []

if plotErrorsFlag:

    for i, res in enumerate(all_res):

        print('Plot errors: ' + all_titles[i])

        err = _err(res, im)
        rerr = _rerr(res, im)
        all_err.append(err)
        all_rerr.append(rerr)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, im-res,
                        rstride=nx//100, cstride=ny//100,
                        cmap='jet', linewidth=0.1)

        str_err = '\nError = {:.4g}, Relative error = {:.4g}'.format(err, rerr)
        plt.title(all_titles[i] + str_err)
        plt.tight_layout()
        plt.savefig(unique_fname())
        plt.close()




# plt.show(block=True)

# %%


all_err_x = []
all_rerr_x = []
all_err_y = []
all_rerr_y = []


if plotErrorsGradFlag:

    print('Plot Gradient Errors')

    for i, res in enumerate(all_res):

        print('Plot Gradient Errors: ' + all_titles[i])

        res_g_x, res_g_y = _grad(res)

        err_x = _err(res_g_x, g_x)
        rerr_x = _rerr(res_g_x, g_x)
        err_y = _err(res_g_y, g_y)
        rerr_y = _rerr(res_g_y, g_y)

        all_err_x.append(err_x)
        all_rerr_x.append(rerr_x)
        all_err_y.append(err_y)
        all_rerr_y.append(rerr_y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, res_g_x - g_x,
                        rstride=nx//100, cstride=ny//100,
                        cmap='jet', linewidth=0.1)
        str_err_x = '\ng_x Error = {:.4g}, Rel error = {:.4g}'.format(err_x, rerr_x)
        plt.title(all_titles[i] + str_err_x)
        plt.tight_layout()
        plt.savefig(unique_fname())
        plt.close()

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xx, yy, res_g_y - g_y,
                        rstride=nx//100, cstride=ny//100,
                        cmap='jet', linewidth=0.1)
        str_err_y = '\ng_y Error = {:.4g}, Rel error = {:.4g}'.format(err_y, rerr_y)
        plt.title(all_titles[i] + str_err_y)
        plt.tight_layout()
        plt.savefig(unique_fname())
        plt.close()
        # plt.show(block=True)


# %%
print("--- RACE RESULTS")

for i, toc in enumerate(all_toc):
    print("--- Algorithm " +
          '{:<40}'.format(all_titles[i]) + ":{:5.4f} seconds ---".format(toc))


# %%
print("--- ERRORS RESULTS - Model")
for i, _ in enumerate(all_err):
    print("--- Algorithm " +
          '{:<40s}'.format(all_titles[i]) +
          ' errors:\t {:.4g},\t {:.4g}'.format(all_err[i], all_rerr[i]))


# %%

print("--- ERRORS RESULTS - GRADIENT")


for i, _ in enumerate(all_err_x):
    print("--- Algorithm " +
          '{:<35s}'.format(all_titles[i]) +
          ' errors x:\t {:.4g},\t {:.4g}'.format(all_err_x[i], all_rerr_x[i]))

    print("--- Algorithm " +
          '{:<35s}'.format(all_titles[i]) +
          ' errors y:\t {:.4g},\t {:.4g}'.format(all_err_y[i], all_rerr_y[i]))

print('Finished!')