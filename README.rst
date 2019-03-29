SPACE FOR BADGES (DOI, PIP VERSION, BUILD, COVERAGE)

This package implements a generic algorithm to detect cycles along with their
respective amplitude and and duration in a times series.
It is maintained as a standalone package within the
`Open Energy System Modeling Framework <https://oemof.org/>`_.

Algorithmic results have been tested against the well known rainflow cycle counting
(RFC) method from mechanical engineering and the equivalence of both counting methods
has been proved.
The original algorithm has been developed and proposed within the following publication.

*Dambrowski, Jonny; Pichlmaier, Simon & Jossen, Andreas.
Mathematical methods for classification of state-of-charge time series for cycle lifetime prediction.
Advanced Automotive Battery Conference. Orlando, Florida. 2012.*

Thanks again to Simon Pichlmaier for sharing his MATLAB Code and allowing us
to port and publish the algorithm under a free license.

Documentation
=============

The probably most extensive description of the algorithm can be found in the
abovementioned paper. In addition, we have tried to document the single parts of
the algorithm as docstrings within the code.

Installation
================

If you have a working Python3 environment, use can pypi to install the latest
version:

.. code:: bash

  pip install cycle_detecttion

Citation
========

Please use our entry on Zenodo to refer to you used version including a DOI: ENTRY

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
