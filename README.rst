.. image:: https://coveralls.io/repos/github/oemof/cydets/badge.svg?branch=master
    :target: https://coveralls.io/github/oemof/cydets?branch=master
.. image:: https://travis-ci.org/oemof/cydets.svg?branch=master
    :target: https://travis-ci.org/oemof/cydets
.. image:: https://badge.fury.io/py/cydets.svg
    :target: https://badge.fury.io/py/cydets
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.2625698.svg
   :target: https://doi.org/10.5281/zenodo.2625698

This package implements an algorithm to detect cycles in a times series
along with their respective depth-of-cycle (DoC) and duration.
It is maintained as a standalone package within the
`Open Energy Modelling Framework <https://oemof.org/>`_.
The acronym *CyDeTS* stands for *(Cy)cle (De)tection in (T)ime (S)eries* and
is chosen to prevent confusions with cycle definitions from graph theory.

Algorithmic results have been tested against the well known rainflow cycle counting
(RFC) method from mechanical engineering and the equivalence of both counting methods
has been proved.
The original algorithm has been developed and proposed within the following publication:

*Dambrowski, Jonny; Pichlmaier, Simon & Jossen, Andreas.
Mathematical methods for classification of state-of-charge time series for cycle lifetime prediction.
Advanced Automotive Battery Conference. Mainz, Germany. 2012.*

Thanks again to Simon Pichlmaier for sharing his code and allowing us
to port and publish the algorithm under a free license.

Documentation
=============

The probably most extensive description of the algorithm can be found in the
abovementioned paper. In addition, we have tried to document the single parts of
the algorithm as docstrings within the code.

Installation
================

If you have a working Python3 environment, use can pypi to install the latest
version.

.. code:: bash

  pip install cydets

Usage
=====

The algorithm is implemented as a function which takes an array-like data
structure as argument.
Results are returned as a `pandas <https://pandas.pydata.org/>`_ dataframe.

.. code:: bash

    import pandas as pd
    from cydets.algorithm import detect_cycles

    # create sample data
    series = pd.Series([0, 1, 0, 0.5, 0, 1, 0, 0.5, 0, 1, 0])

    # detect cycles
    cycles = detect_cycles(series)

Citation
========

Please use our `entry on Zenodo <https://doi.org/10.5281/zenodo.2625698>`_ to refer a specific version

License
=======

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
