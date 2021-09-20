# -*- coding: utf-8 -*-
"""
Created on: 2019/9/30 17:37
Author    : zxt
File      : pyrng.py
Software  : PyCharm
"""

import time
import random
from .tools import unsigned_right_shift


class ArcFour:
    def __init__(self):
        self.i = 0
        self.j = 0
        self.S = {}

    def init(self, key):
        for i in range(256):
            self.S[i] = i
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) & 255
            self.S[i], self.S[j] = self.S[j], self.S[i]
        self.i = 0
        self.j = 0

    def next(self):
        self.i = (self.i + 1) & 255
        self.j = (self.j + self.S[self.i]) & 255
        t = self.S[self.i]
        self.S[self.i] = self.S[self.j]
        self.S[self.j] = t
        return self.S[(t + self.S[self.i]) & 255]


class SecureRandom:
    def __init__(self):
        self.rng_state = None
        self.rng_pool = None
        self.rng_pptr = None
        self.rng_psize = 256

        if self.rng_pool is None:
            self.rng_pool = {}
            self.rng_pptr = 0
            while self.rng_pptr < self.rng_psize:
                self.t = int(65536 * random.random())
                self.rng_pool[self.rng_pptr] = unsigned_right_shift(self.t, 8)
                self.rng_pptr += 1
                self.rng_pool[self.rng_pptr] = self.t & 255
                self.rng_pptr += 1
            self.rng_pptr = 0
            self.rng_seed_time()

    def rng_seed_int(self, x):
        self.rng_pool[self.rng_pptr] ^= x & 255
        self.rng_pptr += 1
        self.rng_pool[self.rng_pptr] ^= (x >> 8) & 255
        self.rng_pptr += 1
        self.rng_pool[self.rng_pptr] ^= (x >> 8) & 255
        self.rng_pptr += 1
        self.rng_pool[self.rng_pptr] ^= (x >> 24) & 255
        if self.rng_pptr >= self.rng_psize:
            self.rng_pptr -= self.rng_psize

    def rng_seed_time(self):
        self.rng_seed_int(int(time.time() * 1000))

    def rng_get_byte(self):
        if self.rng_state is None:
            self.rng_seed_time()
            self.rng_state = ArcFour()
            self.rng_state.init(self.rng_pool)
            for self.rng_ppt in range(len(self.rng_pool)):
                self.rng_pool[self.rng_pptr] = 0
            self.rng_pptr = 0
        return self.rng_state.next()

    def rng_get_bytes(self, ba):
        for i in range(len(ba)):
            ba[i] = self.rng_get_byte()

