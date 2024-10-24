.. image:: https://img.shields.io/badge/sitcomtn--092-lsst.io-brightgreen.svg
   :target: https://sitcomtn-092.lsst.io/
.. image:: https://github.com/lsst-sitcom/sitcomtn-092/workflows/CI/badge.svg
   :target: https://github.com/lsst-sitcom/sitcomtn-092/actions/

################################################
M1M3 Force Balance System - Inertia Compensation
################################################

SITCOMTN-092
============

The M1M3 Force Balance System was engineered to mitigate the influence of gravity/elevation forces, thermal fluctuations, and inertia impacts. This technical note presents an initial analysis of the Force Balance System's performance when implementing corrections to account for inertia effects.

**Links:**

- Publication URL: https://sitcomtn-092.lsst.io/
- Alternative editions: https://sitcomtn-092.lsst.io/v
- GitHub repository: https://github.com/lsst-sitcom/sitcomtn-092
- Build system: https://github.com/lsst-sitcom/sitcomtn-092/actions/

Build this technical note
=========================

You can clone this repository and build the technote locally if your system has Python 3.11 or later:

.. code-block:: bash

   git clone https://github.com/lsst-sitcom/sitcomtn-092
   cd sitcomtn-092
   make init
   make html

Repeat the ``make html`` command to rebuild the technote after making changes.
If you need to delete any intermediate files for a clean build, run ``make clean``.

The built technote is located at ``_build/html/index.html``.

Publishing changes to the web
=============================

This technote is published to https://sitcomtn-092.lsst.io/ whenever you push changes to the ``main`` branch on GitHub.
When you push changes to a another branch, a preview of the technote is published to https://sitcomtn-092.lsst.io/v.

Editing this technical note
===========================

The main content of this technote is in ``index.rst`` (a reStructuredText file).
Metadata and configuration is in the ``technote.toml`` file.
For guidance on creating content and information about specifying metadata and configuration, see the Documenteer documentation: https://documenteer.lsst.io/technotes.
