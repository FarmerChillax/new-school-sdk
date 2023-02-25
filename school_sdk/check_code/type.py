# -*- coding: utf-8 -*-
'''
    :file: type.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2022/01/14 17:28:49
'''
from ast import Bytes
from io import BytesIO
from typing import Tuple
from PIL import Image

scan_height = 50

def captcha_func(image:Image) -> Tuple[int, int]:
    """滑块验证码回调函数
    """

    def _is_continuity_in_y(image:Image, x, y, height) -> int:
        count = 0
        img = image.load()
        for i in range(height):
            if img[x+1, y+i] > img[x, y + i]:
                count += 1
        return count

    img = image.convert("L")
    img_x, img_y = img.size
    for y in range(0, img_y - scan_height):
        for x in range(1, img_x - 1):
            pixel_shallow_count = _is_continuity_in_y(img, x, y, scan_height)
            if pixel_shallow_count == scan_height:
                return x, y

    return 0, 0


def kaptcha_func(image:Image) -> str:
    """图片验证码回调函数
    """
    from school_sdk.check_code.predict import check

    code = check(image)
    # print(code)
    return code
