from setuptools import setup
import os


def read(fname):
    """Auxiliary function to read file from current folder."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='cycle_detection',
      version='0.0.1',
      description=(
              'Cycle detetction software. Detect detphs of cycle and cycle '
              'frequency in time series.'),
      url='https://github.com/oemof/cycle_detection',
      author='Cord Kaldemeyer, Francesco Witte',
      author_email='francesco.witte@hs-flensburg.de',
      long_description=read('README.rst'),
      license='GPL-3.0',
      packages=['cycle_detection'],
      python_requires='>=3',
      install_requires=['numpy >= 1.14.3',
                        'pandas >= 0.22.0'])
