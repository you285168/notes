#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#自定义枚举，检查重复值，不支持动态改变枚举中的值
class CEnum(dict):
    def __init__(self, **kw):
        temp = set()
        for v in kw.values():
            if v in temp:
                raise AttributeError(r"Enum value repeat")
            else:
                temp.add(v)
        dict.__init__(self, **kw)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        raise AttributeError(r"set Enum error")

    def __setitem__(self, key, value):
        raise AttributeError(r"set Enum error")


class Dict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value
