from setuptools import find_packages
from distutils.core import setup

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
