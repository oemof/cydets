from setuptools import setup
import os


def read(fname):
    """Auxiliary function to read file from current folder."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='cydets',
      version='1.1',
      description=(
              'Cycle Detection in Time Series (CyDeTS). An algorithm to '
              'detect cycles in times series along with their respective '
              'depth of cycle and duration.'),
      url='https://github.com/oemof/cydets',
      author='Cord Kaldemeyer, Francesco Witte',
      author_email='francesco.witte@hs-flensburg.de',
      long_description=read('README.rst'),
      license='GPL-3.0',
      packages=['cydets'],
      python_requires='>=3',
      install_requires=['numpy >= 1.14.3',
                        'pandas >= 0.22.0'])
