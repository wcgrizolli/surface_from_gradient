
============================================
**surface_from_gradient**
============================================


============================================
**Surface from Gradient scripts for Python**
============================================

surface_from_gradient_ is Python library to calculate a surface from the
gradient data. It relies in `GNU Octave`_ and oct2py_ library to run codes
originally written in MATLAB©

.. _surface_from_gradient: https://gitlab.com/wcgrizolli/surface_from_gradient
.. _GNU Octave: https://www.gnu.org/software/octave/
.. _oct2py: http://blink1073.github.io/oct2py/


-----------------
**Documentation**
-----------------
The original MATLAB codes are described here:

1) Agrawal, A., Raskar, R., & Chellappa, R. (2006). What Is the Range of Surface
Reconstructions from a Gradient
Field? `LINK <https://doi.org/10.1007/11744023_45>`_.

- `Package's author web page <http://www.cs.cmu.edu/~ILIM/projects/IM/aagrawal/>`_,

- `MATLAB codes <http://www.cs.cmu.edu/~ILIM/projects/IM/aagrawal/eccv06/RangeofSurfaceReconstructions.html>`_

2) Harker, M., & O’Leary, P. (2015). MATLAB toolbox for the regularized surface reconstruction from gradients. `LINK <https://doi.org/10.1117/12.2182827>`_.

- `MATLAB codes <https://www.mathworks.com/matlabcentral/fileexchange/43149-surface-reconstruction-from-gradient-fields--grad2surf-version-1-0?s_tid=prof_contriblnk>`_

- Additional toolbox used: `Discrete Orthogonal Polynomial Toolbox <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_.



======================================
**Step 1 Syncing with gitlab**
======================================

*Requirements*: git, `GNU Octave`_, conda


**NOTE**: You need to have ``git`` installed


**Clone**
----------

::

 $> git clone https://gitlab.com/wcgrizolli/pythonWorkspace.git

 
**NOTE**: This is a private project. Your need to have a user at gitlab.com and to be added to the project to have access.


**Update your local installation**
----------------------------------

::

 $> git pull


**To make git to store your credentials**
-----------------------------------------

::

 $> git config credential.helper store

