





====================================================
**Step 2 - Installing dependencies with conda**
====================================================

**Creating conda enviroment**
------------------------------

**NOTE**: You need to have ``anaconda`` or ``miniconda`` installed

::

 $> conda create -n ENV_NAME python=3.5 numpy=1.11  scipy=0.17 matplotlib=1.5 spyder=2.3.9 --yes

.. WARNING:: edit ``ENV_NAME``


**Soving dependencies with conda**
----------------------------------

::

 $> conda install -c conda-forge oct2py


=========================================
**Step 3 - Installing the MATLAB files**
=========================================

The MATLAB scripts must be downloaded, unzipe and properly
placed at the directory tree. The script ``install_mfiles.sh`` is supposed to
take care of that (LINUX only). You must run::

 $> chmod +x install_mfiles.sh
 $> ./install_mfiles.sh



By the end of the script, the directory tree should looks like::

	surface_from_gradient
	├── g2sAgrawal
	│   └── AgrawalECCV06CodeMFiles
	├── g2sHarker
	│   ├── DOPBox
	│   │   └── DOPBoxV1-8
	│   │       ├── Documentation
	│   │       ├── DOPbox
	│   │       └── SupportFns
	│   └── grad2Surf
	│       └── grad2SurfV1-0
	│           ├── Documentation
	│           └── grad2Surf
	└── octave
		└── output


================================
**Step 4 - Running test files**
================================

**NOTE** octave/README.rst

--------------------
Formating README.rst
--------------------

* `cheat-sheet for reStructuredText <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_