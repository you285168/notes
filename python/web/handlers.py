#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' ... '

__author__ = 'Sola'

from model import *
from coroweb import *

@get('/')
async def index(request):
    users = await User.find()
    return {
        '__template__': 'test.html',
        'users': users,
    }
