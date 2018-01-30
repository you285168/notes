#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' ... '

__author__ = 'Sola'

import inspect, os, re

def inspect_parameter(obj, kind = None, nodefault = None):
    '''
    get function/class args name

    :param obj: function/class

    :param kind:
    inspect.Parameter.POSITIONAL_ONLY	值必须作为位置参数提供。 Python没有明确的定义位置参数的语法，但许多内建和扩展模块函数（特别是那些只接受一个或两个参数的函数）接受它们。
    inspect.Parameter.POSITIONAL_OR_KEYWORD	值可以作为关键字或位置参数提供（这是在Python中实现的函数的标准绑定行为。）
    inspect.Parameter.VAR_POSITIONAL	没有绑定到任何其他参数的位置参数的元组。这对应于Python函数定义中的*args参数。
    inspect.Parameter.KEYWORD_ONLY	值必须作为关键字参数提供。仅限关键字的参数是在Python函数定义中的*或*args条目后出现的参数。
    inspect.Parameter.VAR_KEYWORD	未绑定到任何其他参数的关键字参数的dict。这对应于Python函数定义中的**kwargs参数。

    :param nodefault: not default param

    :return: tuple()
    '''
    args = []
    params = inspect.signature(obj).parameters
    for name, param in params.items():
        if not kind:
            args.append(name)
        elif param.kind == kind:
            if not nodefault or param.default == inspect.Parameter.empty:
                args.append(name)

    return tuple(args)


def _list_path(path, temp):
    li = os.listdir(path)
    if '__init__.py' not in li:
        return
    temp.append(path)
    for name in li:
        address = os.path.join(path, name)
        if os.path.isdir(address):
            _list_path(address, temp)

def list_package(path):
    temp = []
    _list_path(path, temp)
    return temp