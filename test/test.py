# -*- coding: utf-8 -*-
'''
    :file: test.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/02 23:09:54
'''

def gen(**kwargs):
    print(kwargs, type(kwargs))
    for key in kwargs:
        print(key, kwargs[key])

gen(x=1, y = 2, z = 3)
