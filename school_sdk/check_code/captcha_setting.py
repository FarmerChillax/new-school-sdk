# -*- coding: utf-8 -*-
'''
      :file: captcha_setting.py
      :author: -Farmer
      :url: https://blog.farmer233.top
      :date: 2022/01/14 21:30:22
'''
# 验证码中的字符
# string.digits + string.ascii_uppercase
NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
            'Z']+['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                  'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ALL_CHAR_SET = NUMBER + ALPHABET
ALL_CHAR_SET_LEN = len(ALL_CHAR_SET)
MAX_CAPTCHA = 6

# 图像大小
IMAGE_HEIGHT = 50
IMAGE_WIDTH = 200
