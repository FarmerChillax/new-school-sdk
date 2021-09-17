# -*- coding: utf-8 -*-
"""
Created on: 2019/10/1 18:02
Author    : zxt
File      : tools.py
Software  : PyCharm
"""


import ctypes


def unsigned_right_shift(n, i):
    """
    无符号整数右移
    :param n:
    :param i:
    :return:
    """
    def int_overflow(val):
        maxint = 2147483647
        if not -maxint - 1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val

    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    # print(n)
    return int_overflow(n >> i)
