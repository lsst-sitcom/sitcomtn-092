[![sitcomtn-092](https://img.shields.io/badge/sitcomtn--092-lsst.io-brightgreen.svg)](https://sitcomtn-092.lsst.io/) 
[![CI](https://github.com/lsst-sitcom/sitcomtn-092/workflows/CI/badge.svg)](https://github.com/lsst-sitcom/sitcomtn-092/actions/)

# SITCOMTN-092 - M1M3 Force Balance System - Inertia Compensation

The M1M3 Force Balance System was engineered to mitigate the influence of gravity/elevation forces, thermal fluctuations, and inertia impacts. This technical note presents an initial analysis of the Force Balance System's performance when implementing corrections to account for inertia effects. 

This technote, in particular, contains also a set of notebooks and can be used as a python package. See more details below.

**Links:**

- Publication URL: https://sitcomtn-092.lsst.io/
- Alternative editions: https://sitcomtn-092.lsst.io/v
- GitHub repository: https://github.com/lsst-sitcom/sitcomtn-092
- Build system: https://github.com/lsst-sitcom/sitcomtn-092/actions/

## Build this technical note

You can clone this repository and build the technote locally if your system has Python 3.11 or later:

```bash
git clone https://github.com/lsst-sitcom/sitcomtn-092
cd sitcomtn-092
make init
make html
```

Repeat the `make html` command to rebuild the technote after making changes.
If you need to delete any intermediate files for a clean build, run `make clean`.

The built technote is located at `_build/html/index.html`.

## Publishing changes to the web

This technote is published to https://sitcomtn-092.lsst.io/ whenever you push changes to the `main` branch on GitHub.
When you push changes to a another branch, a preview of the technote is published to https://sitcomtn-092.lsst.io/v.

## Editing this technical note

The main content of this technote is in `index.md` (a reStructuredText file).
Metadata and configuration is in the `technote.toml` file.
For guidance on creating content and information about specifying metadata and configuration, see the Documenteer documentation: https://documenteer.lsst.io/technotes.


## Using as a python package

You can install this repository to use the modules inside the `python/lsst/sitcom/sitcomtn092` folder. 

### On a terminal

If you are using Python or iPython on a terminal, you can:

  0. Make sure you have loaded the LSST Stack.
  ``
  
  1. Ensure you are inside this repository.  
  `cd $PATH_TO_SITCOMTN092/`

  2. Install this repository using EUPS.
  `setup -r .`


### Make it available in Nublado

If you want these modules available in notebooks running in Nublado, you will have to add the following line to your `$HOME/notebooks/.user_setups`.

```
setup -r $HOME/notebooks/lsst-sitcom/sitcomtn-092
```

Open a notebook and try to run the import below to confirm it is working properly:

```
from lsst.sitcom.sitcomtn092 import query
```