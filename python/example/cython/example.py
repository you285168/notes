#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' ... '

__author__ = 'Sola'


import ctypes

lib = ctypes.cdll.LoadLibrary('./libcpython.so')

lib.SayHello()
