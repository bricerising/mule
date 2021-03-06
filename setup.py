#!/usr/bin/env python

import setuptools
from mule import __version__

setuptools.setup(
    name='mule',
    version=__version__,
    scripts=['bin/mule'],
    description='Script for executing automated tasks',
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    include_package_data=True,
    install_requires=[
        'pystache',
        'gitpython',
        'pygithub',
        'pyyaml',
        'termcolor',
    ],
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
