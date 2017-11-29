import sys
from setuptools import find_packages
# Python 2 install
if sys.version_info[0] >= 3:
    from distutils.core import setup
else:
    from setuptools import setup

setup(
    name='nbi',
    version='0.1.0',
    packages=find_packages(),
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)
