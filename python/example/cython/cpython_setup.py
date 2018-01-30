#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' run as #python cpython_setup.py build '

__author__ = 'Sola'

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
#from common.globals import *

setup(
    name = 'example',
    version = '1.0',
    description= 'simple cython example',
    author = 'sola',
    author_email = '530830311@qq.com',
#    py_modules = ['example'],
#    packages = list_package('../common'),
    ext_modules = cythonize([
        Extension('cpython', ['cpython.pyx']),
    ])
)