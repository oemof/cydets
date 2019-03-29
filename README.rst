SPACE FOR BADGES (DOI, PIP VERSION, BUILD, COVERAGE)

This package implements an algorithm to detect cycles in a times series
along with their respective amplitude and and duration.
It is maintained as a standalone package within the
`Open Energy System Modeling Framework <https://oemof.org/>`_.

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

  pip install cycle_detecttion

Usage
=====

The function can be imported and applied to an array-like data structure.
Results are returned as a `pandas <https://pandas.pydata.org/>`_ dataframe.

.. code:: bash

    import numpy as np
    import pandas as pd
    from cycle_detection import detect_cycles

    # create sample data
    arr = np.random.randint(10, size=50)
    series = pd.Series(arr.tolist())

    # detect cycles
    cycles = detect_cycles(series)

Citation
========

Please use our entry on Zenodo to refer a specific version: ENTRY

License
=======

Copyright (C) 2019 oemof developing group

This program is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see http://www.gnu.org/licenses/.
