#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import exists, dirname, realpath
from setuptools import find_namespace_packages, setup
import sys


author = u"Mehrpad Monajem"
# authors in alphabetical order
description = 'A package for controlling APT experiment and calibrating the APT data'
name = 'PyCCAPT'
year = "2022"


# sys.path.insert(0, realpath(dirname(__file__))+"/"+name)

try:
    from pyccapt import version
except BaseException:
    version = "0.0.32"

setup(
    name=name,
    namespace_packages=['pyccapt'],
    author=author,
    author_email='mehrpad.monajem@fau.de',
    url='https://github.com/mmonajem/pyccapt',
    version=version,
    entry_points={
            'console_scripts': {
                'pyccapt=pyccapt.control.gui.__main__:main',
                }
    },
    data_files=[('my_data', ['./tests/data'])],

    packages=find_namespace_packages(include=['pyccapt.calibration.pyccapt.*', 'pyccapt.control.pyccapt.*']),
    include_package_data=True,
    license="GPL v3",
    description=description,
    long_description=open('README.md').read() if exists('README.md') else '',
    long_description_content_type="text/markdown",
    install_requires=[
                        "numpy",
                        "matplotlib",
                        "opencv-python",
                        "pandas",
                        "PyQt5",
                        "pyqtgraph",
                        "scikit_learn",
                        "ipywidgets",
                        "networkx",
                        "numba",
                        "requests",
                        "wget",
                        "h5py",
                        "nidaqmx",
                        "pypylon",
                        "tweepy",
                        "pyvisa",
                        "pyvisa-py",
                        "pyserial",
                        "tables",
                      ],
    # not to be confused with definitions in pyproject.toml [build-system]
    setup_requires=["pytest-runner"],
    python_requires=">=3.8",
    tests_require=["pytest", "pytest-mock"],
    keywords=[],
    classifiers=['Operating System :: Microsoft :: Windows',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering :: Visualization',
                 'Intended Audience :: Science/Research',
                 ],
    platforms=['ALL'],
)