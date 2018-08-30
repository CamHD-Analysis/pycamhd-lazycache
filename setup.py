from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import os
from codecs import open

import versioneer

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Dependencies.
with open('requirements.txt') as f:
    requirements = f.readlines()
install_requires = [t.strip() for t in requirements]
print(install_requires)

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='pycamhd-lazycache',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Module for retrieving CamHD data through a LazyCache server',
      long_description=long_description,
      url='https://github.com/CamHD-Analysis/pycamhd-lazycache',
      author='Aaron Marburg',
      author_email='amarburg@apl.washington.edu',
      license='MIT',
      python_requires='>=3',
      packages=['pycamhd.lazycache'],
      install_requires=install_requires,
      tests_require=['tox', 'pytest', 'numpy'])
