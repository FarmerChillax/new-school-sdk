# -*- coding: utf-8 -*-
"""
Created on: 2019/9/29 11:17
Author    : zxt
File      : pyjsbn.py
Software  : PyCharm
"""

import math
from .tools import unsigned_right_shift


class Classic:
    def __init__(self, m):
        self.m = m

    def convert(self, x):
        if x.int_dict['s'] < 0 or x.compare2(self.m) >= 0:
            return x.mod(self.m)
        else:
            return x

    def revert(self, x):
        return x

    def reduce(self, x):
        x.rem2(self.m, None, x)

    def mul2(self, x, y, r):
        x.multiply2(y, r)
        self.reduce(r)

    def sqr2(self, x, r):
        x.square2(r)
        self.reduce(r)


class Montgomery:
    def __init__(self, m):
        self.m = m
        self.mp = m.inv_digit()
        self.mpl = self.mp & 0x7fff
        self.mph = self.mp >> 15
        self.um = (1 << (m.DB - 15)) - 1
        self.mt2 = 2 * m.int_dict['t']

    def convert(self, x):
        r = BigInteger(None)
        x.abs().dl_shift2(self.m.int_dict['t'], r)
        r.rem2(self.m, None, r)
        if x.int_dict['s'] < 0 < r.compare2(ZERO):
            self.m.sub2(r, r)
        return r

    def reduce(self, x):
        while x.int_dict['t'] <= self.mt2:
            x.int_dict[x.int_dict['t']] = 0
            x.int_dict['t'] += 1
        for i in range(self.m.int_dict['t']):
            j = x.int_dict[i] & 0x7fff
            u0 = (j * self.mpl + (((j * self.mph + (x.int_dict[i] >> 15) * self.mpl) & self.um) << 15)) & x.DM
            j = i + self.m.int_dict['t']
            x.int_dict[j] += self.m.am(0, u0, x, i, 0, self.m.int_dict['t'])
            while x.int_dict[j] >= x.DV:
                x.int_dict[j] -= x.DV
                j += 1
                x.int_dict[j] += 1
        x.clamp()
        x.dr_shift2(self.m.int_dict['t'], x)  # x.dr_shift2() 执行后数据与浏览器一致
        if x.compare2(self.m) >= 0:
            x.sub2(self.m, x)

    def sqr2(self, x, r):
        x.square2(r)
        self.reduce(r)

    def revert(self, x):
        r = BigInteger(None)
        x.copy2(r)
        self.reduce(r)
        return r

    def mul2(self, x, y, r):
        x.multiply2(y, r)
        self.reduce(r)


class BigInteger:
    def __init__(self, a, b=None, c=None):
        self.int_dict = dict({i: None for i in range(37)}, **{'s': 0, 't': 0})
        self.BI_RM = "0123456789abcdefghijklmnopqrstuvwxyz"
        self.BI_RC = self.bi_rc()
        self.DB = 28
        self.DM = 268435455
        self.DV = 268435456
        self.F1 = 24
        self.F2 = 4
        self.FV = 4503599627370496

        if a is not None:
            if b is None and type(a) != str:
                self.from_string(a, 256)
            else:
                self.from_string(a, b)
        else:
            self.int_dict = {'s': 0, 't': 0}

    def __getitem__(self, item):
        return self.int_dict

    def int2char(self, n):
        return self.BI_RM[n]

    def am1(self, i, x, w, j, c, n):
        n -= 1
        while n >= 0:
            v = x * self.int_dict[i] + w.int_dict[j] + c
            i += 1
            c = int(v / 0x4000000)
            w.int_dict[j] = v & 0x3ffffff
            j += 1
            n -= 1
        return c

    def am2(self, i, x, w, j, c, n):
        xl = x & 0x7fff
        xh = x >> 15
        n -= 1
        while n >= 0:
            l = self.int_dict[i] & 0x7fff
            h = self.int_dict[i] >> 15
            i += 1
            m = xh * l + h * xl
            l = xl * l + ((m & 0x7fff) << 15) + w.int_dict[j] + (c & 0x3fffffff)
            c = unsigned_right_shift(l, 30) + unsigned_right_shift(m, 15) + xh * h + unsigned_right_shift(c, 30)
            w[j] = l & 0x3fffffff
            j += 1
            n -= 1
        return c

    def am(self, i, x, w, j, c, n):
        xl = x & 0x3fff
        xh = x >> 14
        for k in range(n - 1, -1, -1):
            ll = self.int_dict[i] & 0x3fff
            h = self.int_dict[i] >> 14
            i += 1
            m = xh * ll + h * xl
            ll = xl * ll + ((m & 0x3fff) << 14) + w.int_dict[j] + c
            c = (ll >> 28) + (m >> 14) + xh * h
            w.int_dict[j] = ll & 0xfffffff
            j += 1
        return c

    def nbv(self, i):
        r = BigInteger(None)
        r.from_int(i)
        return r

    def bi_rc(self):
        birc = {}
        rr = ord('0')
        for vv in range(10):
            birc[rr] = vv
            rr += 1
        rr = ord('a')
        for vv in range(10, 36):
            birc[rr] = vv
            rr += 1
        rr = ord('A')
        for vv in range(10, 36):
            birc[rr] = vv
            rr += 1
        return birc

    def from_int(self, x):
        self.int_dict['t'] = 1
        self.int_dict['s'] = -1 if x < 0 else 0
        if x > 0:
            self.int_dict[0] = x
        elif x < -1:
            self.int_dict[0] = x + self.DV
        else:
            self.int_dict['t'] = 0

    def from_string(self, s, b):
        k = int(math.log(b, 2))
        i = len(s)
        mi = False
        sh = 0
        i -= 1
        while i > 0:
            x = s[i] & 0xff if k == 8 else self.intat(s, i)
            if x < 0:
                if s[i] == '-':
                    mi = True
                continue
            mi = False
            if sh == 0:
                self.int_dict[self.int_dict['t']] = x
                self.int_dict['t'] += 1
            elif sh + k > self.DB:
                self.int_dict[self.int_dict['t'] - 1] |= (x & ((1 << (self.DB - sh)) - 1)) << sh
                self.int_dict[self.int_dict['t']] = (x >> (self.DB - sh))
                self.int_dict['t'] += 1
            else:
                self.int_dict[self.int_dict['t'] - 1] |= x << sh
            sh += k
            if sh >= self.DB:
                sh -= self.DB
            i -= 1
        if k == 8 and (s[0] & 0x80) != 0:
            self.int_dict['s'] = -1
            if sh > 0:
                self.int_dict[self.int_dict['t'] - 1] |= ((1 << (self.DB - sh)) - 1) << sh
        self.clamp()
        if mi:
            self.sub2(self, self)

    def intat(self, s, i):
        try:
            c = self.BI_RC[ord(s[i])]
        except:
            return -1
        return c

    def clamp(self):
        c = self.int_dict['s'] & self.DM
        while self.int_dict['t'] > 0 and self.int_dict[self.int_dict['t'] - 1] == c:
            self.int_dict['t'] -= 1

    def to_string(self, b):
        if self.int_dict['s'] < 0:
            return '-' + self.negate().to_string(b)
        k = int(math.log(b, 2))
        km = (1 << k) - 1
        m = False
        r = ''
        i = self.int_dict['t']
        p = self.DB - (i * self.DB) % k
        if i > 0:
            i -= 1
            d = self.int_dict[i] >> p
            if p < self.DB and d > 0:
                m = True
                r = self.int2char(d)
            while i >= 0:
                if p < k:
                    d = (self.int_dict[i] & ((1 << p) - 1)) << (k - p)
                    i -= 1
                    p += self.DB - k
                    d |= self.int_dict[i] >> p
                else:
                    p -= k
                    d = (self.int_dict[i] >> p) & km
                    if p <= 0:
                        p += self.DB
                        i -= 1
                if d > 0:
                    m = True
                if m:
                    r += self.int2char(d)
        return r if m else '0'

    def sub2(self, a, r):
        i = 0
        c = 0
        m = min(a.int_dict['t'], self.int_dict['t'])
        while i < m:
            c += self.int_dict[i] - a.int_dict[i]
            r.int_dict[i] = c & self.DM
            i += 1
            c >>= self.DB
        if a.int_dict['t'] < self.int_dict['t']:
            c -= a.int_dict['s']
            while i < self.int_dict['t']:
                c += self.int_dict[i]
                r.int_dict[i] = c & self.DM
                i += 1
                c >>= self.DB
            c += self.int_dict['s']
        else:
            c += self.int_dict['s']
            while i < a.int_dict['t']:
                c -= a.int_dict[i]
                r.int_dict[i] = c & self.DM
                i += 1
                c >>= self.DB
            c -= a.int_dict['s']
        r.int_dict['s'] = -1 if c < 0 else 0
        if c < -1:
            r.int_dict[i] = self.DV
            i += 1
        elif c > 0:
            r.int_dict[i] = c
            i += 1
        r.int_dict['t'] = i
        r.clamp()

    def copy2(self, r):
        for i in range(self.int_dict['t'] - 1, -1, -1):
            r.int_dict[i] = self.int_dict[i]
        r.int_dict['t'] = self.int_dict['t']
        r.int_dict['s'] = self.int_dict['s']

    def nbits(self, x):
        r = 1
        t = unsigned_right_shift(x, 16)
        if t != 0:
            x = t
            r += 16
        t = x >> 8
        if t != 0:
            x = t
            r += 8
        t = x >> 4
        if t != 0:
            x = t
            r += 4
        t = x >> 2
        if t != 0:
            x = t
            r += 2
        t = x >> 1
        if t != 0:
            x = t
            r += 1
        return r

    def negate(self):
        r = BigInteger(None)
        ZERO.sub2(self, r)
        return r

    def abs(self):
        return self.negate() if self.int_dict['s'] < 0 else self

    def compare2(self, a):
        r = self.int_dict['s'] - a.int_dict['s']
        if r != 0:
            return r
        i = self.int_dict['t']
        r = i - a.int_dict['t']
        if r != 0:
            return -r if self.int_dict['s'] < 0 else r
        for k in range(i - 1, -1, -1):
            r = self.int_dict[k] - a.int_dict[k]
            if r != 0:
                return r
        return 0

    def bit_length(self):
        if self.int_dict['t'] <= 0:
            return 0
        return self.DB * (self.int_dict['t'] - 1) + self.nbits(
            self.int_dict[self.int_dict['t'] - 1] ^ (self.int_dict['s'] & self.DM)
        )

    def dl_shift2(self, n, r):
        for i in range(self.int_dict['t'] - 1, -1, -1):
            r.int_dict[i + n] = self.int_dict[i]
        for i in range(n - 1, -1, -1):
            r.int_dict[i] = 0
        r.int_dict['t'] = self.int_dict['t'] + n
        r.int_dict['s'] = self.int_dict['s']

    def l_shift2(self, n, r):
        bs = n % self.DB
        cbs = self.DB - bs
        bm = (1 << cbs) - 1
        ds = int(n / self.DB)
        c = (self.int_dict['s'] << bs) & self.DM
        for i in range(self.int_dict['t'] - 1, -1, -1):
            r.int_dict[i + ds + 1] = (self.int_dict[i] >> cbs) | c
            c = (self.int_dict[i] & bm) << bs
        for i in range(ds - 1, -1, -1):
            r.int_dict[i] = 0
        r.int_dict[ds] = c
        r.int_dict['t'] = self.int_dict['t'] + ds + 1
        r.int_dict['s'] = self.int_dict['s']
        r.clamp()

    def dr_shift2(self, n, r):
        for i in range(n, self.int_dict['t']):
            r.int_dict[i - n] = self.int_dict[i]
        r.int_dict['t'] = max(self.int_dict['t'] - n, 0)
        r.int_dict['s'] = self.int_dict['s']

    def r_shift2(self, n, r):
        r.int_dict['s'] = self.int_dict['s']
        ds = int(n / self.DB)
        if ds >= self.int_dict['t']:
            r.int_dict['t'] = 0
            return
        bs = n % self.DB
        cbs = self.DB - bs
        bm = (1 << bs) - 1
        r.int_dict[0] = self.int_dict[ds] >> bs
        for i in range(ds + 1, self.int_dict['t']):
            r.int_dict[i - ds - 1] |= (self.int_dict[i] & bm) << cbs
            r.int_dict[i - ds] = self.int_dict[i] >> bs
        if bs > 0:
            r.int_dict[self.int_dict['t'] - ds - 1] |= (self.int_dict['s'] & bm) << cbs
        r.int_dict['t'] = self.int_dict['t'] - ds
        r.clamp()

    def multiply2(self, a, r):
        x = self.abs()
        y = a.abs()
        i = x.int_dict['t']
        r.int_dict['t'] = i + y.int_dict['t']
        i -= 1
        while i >= 0:
            r.int_dict[i] = 0
            i -= 1
        for i in range(y.int_dict['t']):
            r.int_dict[i + x.int_dict['t']] = x.am(0, y.int_dict[i], r, i, 0, x.int_dict['t'])
        r.int_dict['s'] = 0
        r.clamp()
        if self.int_dict['s'] != a.int_dict['s']:
            ZERO.sub2(r, r)

    def square2(self, r):
        x = self.abs()
        i = r.int_dict['t'] = 2 * x.int_dict['t']
        for k in range(i - 1, -1, -1):
            r.int_dict[k] = 0
        ii = 0
        for i in range(x.int_dict['t'] - 1):
            c = x.am(i, x.int_dict[i], r, 2 * i, 0, 1)
            r.int_dict[i + x.int_dict['t']] += x.am(i + 1, 2 * x.int_dict[i], r, 2 * i + 1, c, x.int_dict['t'] - i - 1)
            if r.int_dict[i + x.int_dict['t']] >= x.DV:
                r.int_dict[i + x.int_dict['t']] -= x.DV
                r.int_dict[i + x.int_dict['t'] + 1] = 1
            ii = i
        ii += 1
        if r.int_dict['t'] > 0:
            r.int_dict[r.int_dict['t'] - 1] += x.am(ii, x.int_dict[ii], r, 2 * ii, 0, 1)
        r.int_dict['s'] = 0
        r.clamp()

    def rem2(self, m, q=None, r=None):
        pm = m.abs()
        if pm.int_dict['t'] <= 0:
            return
        pt = self.abs()
        if pt.int_dict['t'] < pm.int_dict['t']:
            if q is not None:
                q.from_int(0)
            if r is not None:
                self.copy2(r)
            return
        if r is None:
            r = BigInteger(None)
        y = BigInteger(None)
        ts = self.int_dict['s']
        ms = m.int_dict['s']
        nsh = self.DB - self.nbits(pm.int_dict[pm.int_dict['t'] - 1])
        if nsh > 0:
            pm.l_shift2(nsh, y)
            pt.l_shift2(nsh, r)
        else:
            pm.copy2(y)
            pt.copy2(r)
        ys = y.int_dict['t']
        y0 = y.int_dict[ys - 1]
        if y0 == 0:
            return
        yt = y0 * (1 << self.F1) + (y.int_dict[ys - 2] >> self.F2 if ys > 1 else 0)
        d1 = self.FV / yt
        d2 = (1 << self.F1) / yt
        e = 1 << self.F2
        i = r.int_dict['t']
        j = i - ys
        t = BigInteger(None) if q is None else q
        y.dl_shift2(j, t)
        if r.compare2(t) >= 0:
            r.int_dict[r.int_dict['t']] = 1
            r.int_dict['t'] += 1
            r.sub2(t, r)
        ONE.dl_shift2(ys, t)
        t.sub2(y, y)
        while y.int_dict['t'] < ys:
            y.int_dict[y.int_dict['t']] = 0
            y.int_dict['t'] += 1
        for k in range(j - 1, -1, -1):
            i -= 1
            qd = self.DM if r.int_dict[i] == y0 else \
                int(r.int_dict[i] * d1 + (r.int_dict[i-1] + e) * d2)
            r.int_dict[i] += y.am(0, qd, r, k, 0, ys)
            if r.int_dict[i] < qd:
                y.dl_shift2(k, t)
                r.sub2(t, r)
                qd -= 1
                while r.int_dict[i] < qd:
                    r.sub2(t, r)
                    qd -= 1
        if q is not None:
            r.dr_shift2(ys, q)
            if ts != ms:
                ZERO.sub2(q, q)
        r.int_dict['t'] = ys
        r.clamp()
        if nsh > 0:
            r.r_shift2(nsh, r)
        if ts < 0:
            ZERO.sub2(r, r)

    def pow_int(self, e, m):
        if e < 256 or m.is_even():
            z = Classic(m)
        else:
            z = Montgomery(m)
        return self.exp(e, z)

    def is_even(self):
        return (self.int_dict[0] & 1 if self.int_dict['t'] > 0 else self.int_dict['s']) == 0

    def inv_digit(self):
        if self.int_dict['t'] < 1:
            return 0
        x = self.int_dict[0]
        if (x & 1) == 0:
            return 0
        y = x & 3
        y = (y * (2 - (x & 0xf) * y)) & 0xf
        y = (y * (2 - (x & 0xff) * y)) & 0xff
        y = (y * (2 - (((x & 0xffff) * y) & 0xffff))) & 0xffff
        y = (y * (2 - x * y % self.DV)) % self.DV
        return self.DV - y if y > 0 else -y

    def exp(self, e, z):
        if e > 0xffffffff or e < 1:
            return ONE
        r = BigInteger(None)
        r2 = BigInteger(None)
        g = z.convert(self)
        i = self.nbits(e) - 1
        g.copy2(r)  # g.copy() 方法前数据与浏览器一致
        for k in range(i - 1, -1, -1):
            z.sqr2(r, r2)
            if e & (1 << k) > 0:
                z.mul2(r2, g, r)
            else:
                r, r2 = r2, r
        return z.revert(r)  # 循环后参数 g, r2, self, z 与浏览器数据一致，r 数据不同

    def mod(self, a):
        r = BigInteger(None)
        self.abs().rem2(a, None, r)
        if self.int_dict['s'] < 0 < r.compare2(ZERO):
            a.sub2(r, r)
        return r
    
    
ZERO = BigInteger(None).nbv(0)
ONE = BigInteger(None).nbv(1)
