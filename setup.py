#!/usr/bin/env python

import sys, os
import a301

__version__ = a301.__version__

from setuptools import setup, find_packages

#version_file = open(os.path.join('e340py', 'version'))
#version = version_file.read().strip()

setup(
    name = "a301",
    packages=find_packages(),
    version=__version__,
    include_package_data=True,
    package_data={'a301': ['VERSION']},
    entry_points={
          'console_scripts': [
              'pytree = a301.scripts.pytree:main',
              'hdf4ls = a301.scripts.hdf4ls:main',
              'modisheader = a301.scripts.modismeta_read:main'
          ]
    },
)
