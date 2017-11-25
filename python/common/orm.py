#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import traceback
from common import mysql

'''
mysql orm
class User(Model):
    __table__ = 'users'
    __primary_key__ = dict(
        id = '',
    )
    __fields__ = dict(
        email = '',
        passwd = '',
        admin = 0,
        name = '',
        image = '',
        created_at = '',
    )

'''

__author__ = 'Sola'

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        tableName = attrs.get('__table__', None) or name
        if not attrs.get('__primary_key__', None):
            raise RuntimeError('table[%s] Primary key not found' % tableName)
        if '__fields__' not in attrs:
            raise RuntimeError('table[%s] fields not found' % tableName)

        attrs['__table__'] = tableName

        escaped_fields = list(map(lambda f: '`%s`' % f, attrs.get('__fields__')))
        escaped_keys = list(map(lambda f: '`%s`' % f, attrs.get('__primary_key__')))
        attrs['__select__'] = 'select %s, %s from `%s`' % (', ' . join(escaped_keys), ', ' . join(escaped_fields), tableName)
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, insert=None, **kw):
        self._dirty = dict()
        self._insert = insert
        #default value
        for k, v in self.__primary_key__.items():
            if k not in kw:
                kw[k] = v
        for k, v in self.__fields__.items():
            if k not in kw:
                kw[k] = v
            elif not self._insert:
                self._dirty[k] = True
        dict.__init__(self, **kw)


    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"Model[%s] object has no attribute '%s'" % (self.__class__.__name__, key))

    def __setattr__(self, key, value):
        self[key] = value

    def __setitem__(self, key, value):
        if key in self.__primary_key__:
            raise RuntimeError('some one try change table[%s] primary key' % self.__table__)

        if key in self.__fields__:
            self._dirty[key] = True

        dict.__setitem__(self, key, value)

    @classmethod
    async def find(self, where=None, **kw):
        if where:
            sql = self.__select__ + where
        else:
            param = ''
            for k, v in kw.items():
                param += '`%s`' % k + ' = ' + str(v)
            if len(param) == 0:
                sql = self.__select__
            else:
                sql = '%s where %s' % (self.__select__, param)
        rs, _ = await mysql.execute(sql)
        if len(rs) == 0:
            return []
        return list(map(lambda f: self(**f, insert=True), rs))

    async def save(self):
        if self._insert:
            print(self._dirty)
            if len(self._dirty) == 0:
                return
            temp_keys = []
            temp_values = []
            for k in self.__primary_key__.keys():
                temp_keys.append("`%s`='%s'" % (k, str(self[k])))

            for k in self._dirty.keys():
                temp_values.append("`%s`='%s'" % (k, str(self[k])))

            sql = 'update `%s` set %s where %s' % (self.__table__, ', ' . join(temp_values), 'and '. join(temp_keys))
        else:
            temp_keys = []
            temp_values = []
            for k in self.__primary_key__.keys():
                temp_keys.append(k)
                temp_values.append(str(self[k]))
            for k in self._dirty.keys():
                temp_keys.append(k)
                temp_values.append(str(self[k]))

            escaped_keys = list(map(lambda f: '`%s`' % f, temp_keys))
            escaped_values = list(map(lambda f: "'%s'" % f, temp_values))
            sql = 'insert into `%s` (%s) values (%s)' % (self.__table__, ', ' . join(escaped_keys), ', ' . join(escaped_values))
            self._insert = True

        self._dirty.clear()
        return await mysql.execute(sql)

