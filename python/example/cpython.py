#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' ... '

__author__ = 'Sola'

import ctypes

lib = ctypes.cdll.LoadLibrary('./libpycall.so')
lib.foo(1, 3)