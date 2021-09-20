# -*- coding: utf-8 -*-
"""
Created on: 2019/9/29 11:21
Author    : zxt
File      : pyb64.py
Software  : PyCharm
"""

import binascii


class Base64:
    def __init__(self):

        self.b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        self.b64pad = "="
        
        self.idx = "0123456789abcdefghijklmnopqrstuvwxyz"

    def hex2b64(self, h):
        ret = ''
        ii = 0
        for i in range(0, len(h) - 2, 3):
            c = int(h[i:i+3], 16)
            ret += self.b64map[c >> 6] + self.b64map[c & 63]
            ii = i
        ii += 3
        if ii + 1 == len(h):
            c = int(h[ii:ii+1], 16)
            ret += self.b64map[c << 2]
        elif ii + 2 == len(h):
            c = int(h[ii:ii + 2], 16)
            ret += self.b64map[c >> 2] + self.b64map[(c & 3) << 4]
        while (len(ret) & 3) > 0:
            ret += self.b64pad
        return ret

    def b64tohex(self, s):
        ret = ''
        k = 0
        slop = 0
        for i in range(len(s)):
            if s[i] == self.b64pad:
                break
            v = self.b64map.index(s[i])
            if v < 0:
                continue
            if k == 0:
                ret += self.idx[v >> 2]
                slop = v & 3
                k = 1
            elif k == 1:
                ret += self.idx[(v >> 4) | (slop << 2)]
                slop = v & 0xf
                k = 2
            elif k == 2:
                ret += self.idx[slop]
                ret += self.idx[v >> 2]
                slop = v & 3
                k = 3
            else:
                ret += self.idx[(slop << 2) | (v >> 4)]
                ret += self.idx[v & 0xf]
                k = 0
        if k == 1:
            ret += self.idx[slop << 2]
        return ret

    def b64toBA(self, s):
        h = self.b64tohex(s)
        a = []
        r = int(len(s) / 2) + 1
        for i in range(r):
            a.append(binascii.b2a_hex(h[2*i:2*i+2].encode('utf-8')))
        return a


if __name__ == '__main__':
    h = "9134d5d73ad3c7e4224e47068308ea8a54f8bd9067aff8c1016c3809a652be529c03059366780c55496352eed46d632ebabedf05038f" \
        "123d124baf3f2cb1cbea6ff12e1a76023b7398dab734cad33f67aab2f36a3a592776aea30bfbb151db14c618fba3df8ef595a251270" \
        "858997a323ef743b83b19b89b74848a03737007e9"
    b = Base64()
    bh = b.hex2b64(h)
    ret = "kTTV1zrTx+QiTkcGgwjqilT4vZBnr/jBAWw4CaZSvlKcAwWTZngMVUljUu7UbWMuur7fBQOPEj0SS68/LLHL6m/xLhp2AjtzmNq3NMr" \
          "TP2eqsvNqOlkndq6jC/uxUdsUxhj7o9+O9ZWiUScIWJl6Mj73Q7g7GbibdISKA3NwB+k="
    print(bh == ret)
