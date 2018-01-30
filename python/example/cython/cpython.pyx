#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' ... '

__author__ = 'Sola'

cdef extern from "stdio.h":
    extern int printf(const char * format, ...)

cdef public SayHello():
    printf("hello world\n")
