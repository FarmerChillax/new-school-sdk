# -*- coding: utf-8 -*-
"""
Created on: 2019/9/29 11:04
Author    : zxt
File      : PyRsa.py
Software  : PyCharm
"""


import binascii
from .pyrng import SecureRandom
from .pyjsbn import BigInteger
from .pyb64 import Base64


class RsaKey:
    def __init__(self):
        self.n = None
        self.e = 0
        self.d = None
        self.p = None
        self.q = None
        self.dmp1 = None
        self.dmq1 = None
        self.coeff = None

    def set_public(self, n, e):
        if n is not None and e is not None and len(n) > 0 and len(e) > 0:
            self.n = BigInteger(n, 16)
            self.e = int(e, 16)
        else:
            raise ValueError("Invalid RSA public key")

    def linkbrk(self, s, n):
        ret = ''
        i = 0
        while i + n < len(s):
            ret += s[i, i + n] + '\n'
            i += n
        return ret + s[i, len(s)]

    def byte2hex(self, b):
        if b < 0x10:
            return '0' + binascii.b2a_hex(b)
        else:
            return binascii.b2a_hex(b)

    def pkcs1pad2(self, s, n):
        if n < len(s) + 11:
            print("Message too long for RSA")
            exit()
        ba = {}
        i = len(s) - 1
        while i >= 0 and n > 0:
            c = ord(s[i])
            i -= 1
            if c < 128:
                n -= 1
                ba[n] = c
            elif 127 < c < 2048:
                n -= 1
                ba[n] = (c & 63) | 128
                n -= 1
                ba[n] = (c >> 6) | 192
            else:
                n -= 1
                ba[n] = (c & 63) | 128
                n -= 1
                ba[n] = ((c >> 6) & 63) | 128
                n -= 1
                ba[n] = (c >> 12) | 224
        n -= 1
        ba[n] = 0
        rng = SecureRandom()
        x = {}
        while n > 2:
            """
            产生与时间相关的随机阵列对按字符解析后的 ba 进行填充
            """
            x[0] = 0
            while x[0] == 0:
                rng.rng_get_bytes(x)
            n -= 1
            ba[n] = x[0]
        n -= 1
        ba[n] = 2
        n -= 1
        ba[n] = 0
        # print()
        bi = BigInteger(ba)
        # print()
        return BigInteger(ba)

    def do_public(self, x):
        return x.pow_int(self.e, self.n)

    def rsa_encrypt(self, text):
        m = self.pkcs1pad2(text, (self.n.bit_length() + 7) >> 3)
        if m is None:
            return None
        c = self.do_public(m)
        if c is None:
            return None
        h = c.to_string(16)
        if len(h) & 1 == 0:
            return h
        else:
            return '0' + h


if __name__ == '__main__':
    rsa = RsaKey()
    m = "AKRB6FwmOe0hE9Uo6LMKoDE5U9JU9lH1v8Uv7ATjRj2W+aTPlR9Hfm8fR782pzGwDsTD4Yr7tBHQ1cuEnGrqrJn5HuPiLqmSg4Z/AwS+Rq8eE7T+ZaGoUtpqvcoSffSJOW29RNVMwT391ona/+eK5B3RkC9WaJFYiZai7FiQDeXT"
    e = 'AQAB'
    rsa.set_public(Base64().b64tohex(m), Base64().b64tohex(e))
    rr = rsa.rsa_encrypt('1234567890')
    enpsw = Base64().hex2b64(rr)
    print(enpsw)
