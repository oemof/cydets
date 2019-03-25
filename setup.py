from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='cycle detection',
      version='0.0.1 dev',
      description='',
      url='',
      author='',
      author_email='',
      long_description=read('README.rst'),
      license='',
      packages=['cycle_detection'],
      python_requires='>=3',
      install_requires=['numpy >= 1.14.3',
                        'pandas >= 0.22.0'])
