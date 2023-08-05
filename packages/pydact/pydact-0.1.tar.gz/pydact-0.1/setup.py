#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


# Meta-data
NAME = 'pydact'
DESCRIPTION = 'Redact information'
URL = 'https://github.com/kind-lab/pydact'
AUTHOR = 'Alistair Johnson'

def readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
    name=NAME,
    version='0.1',
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
)
