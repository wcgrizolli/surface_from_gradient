

# Surface from Gradient scripts for Python

[surface_from_gradient] is Python library to calculate a surface from the
gradient data. It relies in [octave] and [oct2py] library to run codes
originally written in `MATLAB`©

## Documentation

The original `MATLAB` codes are described here:

1) [Agrawal, A., Raskar, R., & Chellappa, R. (2006). What Is the Range of Surface Reconstructions from a Gradient Field?](https://doi.org/10.1007/11744023_45)

- [Package's author web page](http://www.cs.cmu.edu/~ILIM/projects/IM/aagrawal/)

- [MATLAB codes](http://www.cs.cmu.edu/~ILIM/projects/IM/aagrawal/eccv06/RangeofSurfaceReconstructions.html)

2) [Harker, M., & O’Leary, P. (2015). MATLAB toolbox for the regularized surface reconstruction from gradients.](https://doi.org/10.1117/12.2182827)

- [MATLAB codes](https://www.mathworks.com/matlabcentral/fileexchange/43149-surface-reconstruction-from-gradient-fieldsgrad2surf-version-1-0?s_tid=prof_contriblnk)

- Additional toolbox required: [Discrete Orthogonal Polynomial Toolbox](http://docutils.sourceforge.net/docs/user/rst/quickref.html)


# Installation

:warning: **Attention**: Only tested in Linux

Experient users can simply download the zip file from github and use it as any `python` library. Please have a look at the examples.

Below is described the step to use git and conda to properly setup an enviroment and solve dependencies

### Step 1 - Syncing with github


**Requirements**: [git], [conda], [octave]


#### Clone

```shell
git clone https://github.com/wcgrizolli/pythonWorkspace.git
```
 
:exclamation: **NOTE**: This is a private project. Your need to have a user at github.com and to be added to the project to have access.


#### Update your local installation


```shell
git pull
```

#### Make git to store your credentials


```shell
git config credential.helper store
```



### Step 2 - Installing dependencies with conda



#### Creating conda enviroment


:exclamation: **NOTE**: You need to have [conda] or [miniconda] installed

:exclamation: **NOTE**: You only need to do this whe installing the first time.

```shell
conda create -n ENV_NAME python=3.5 numpy=1.11  scipy=0.17 matplotlib=1.5 spyder=2.3.9 --yes
```

:warning: **Attention**: Edit ``ENV_NAME``


#### Soving dependencies with conda



```shell
source activate `ENV_NAME`
conda install -c conda-forge oct2py
```

#### Running `spyder` insider conda enviroment

In order to use the correct version of `python`, `numpy`, etc, you need to run `spyder` inside a `conda` enviroment


```shell
source activate `ENV_NAME`
spyder
```

### Step 3 - Installing the `MATLAB` files


The `MATLAB` scripts must be downloaded, unzipe and properly
placed at the directory tree. The script [install_mfiles.sh](install_mfiles.sh)
is supposed to take care of that (LINUX only). You must run:


```shell
chmod +x install_mfiles.sh
./install_mfiles.sh
```



By the end of the script, the directory tree should looks like::


```
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

```


### Step 4 - Testing that you can run Octave


:exclamation: Read octave/README.rst


### Step 5 - Running

Load the `ENV_NAME` conda enviroment, open `spyder`, load one of the examples, run.

#### Formating README.md


* https://guides.github.com/features/mastering-markdown/





[surface_from_gradient]: https://gitlab.com/wcgrizolli/surface_from_gradient "surface_from_gradient"
[octave]: https://www.gnu.org/software/octave/ "GNU Octave"
[oct2py]: http://blink1073.github.io/oct2py/ "oct2py"
[conda]: https://conda.io/docs/index.html "conda"
[git]: https://git-scm.com "git"
[miniconda]: https://conda.io/miniconda.html "miniconda"
