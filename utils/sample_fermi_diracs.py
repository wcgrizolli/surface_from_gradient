# -*- coding: utf-8 -*-
"""

@author: Walan
"""

import numpy as np

def sample_fermi_diracs(m, n, radius=10):

    np.seterr(over='ignore')


    xo_vec = [3*m//4, 2*m//4, m//4]
    yo_vec = [3*n//4, 2*n//4, n//4]
    yy, xx = np.mgrid[0:n, 0:m]

    sigma_list = [.01, .025, .05, .1, .25, .5, 1., 2.5, 5.]

#    sigma_list = [1., 2.5, 5., 1., 2.5, 5., 1., 2.5, 5.]
    zz = np.zeros((n, m))

    counter = 0
    for xo in xo_vec:
        for yo in yo_vec:
            zz += 1.0/(1 + np.exp((np.sqrt((xx-xo)**2+(yy-yo)**2)-radius) / sigma_list[counter]))
            counter += 1

    return zz

