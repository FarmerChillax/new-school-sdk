# -*- coding: utf-8 -*-
'''
    :file: __intit__.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/02 19:19:08
'''
from PIL import Image
from io import BytesIO
scan_height = 50

class ZFCaptchaDistinguish():

    def __init__(self, image_stream) -> None:
        stream = BytesIO(image_stream)
        self.image = Image.open(stream)
        self.X = -1
        self.Y = -1
    
    def _is_continuity_in_y(self, image:Image, x, y, height) -> int:
        count = 0
        img = image.load()
        for i in range(height):
            if img[x+1, y+i] > img[x, y + i]:
                count += 1
        return count

    def verify(self):
        img = self.image.convert("L")
        img_x, img_y = img.size
        for y in range(0, img_y - scan_height):
            for x in range(1, img_x - 1):
                pixel_shallow_count = self._is_continuity_in_y(img, x, y, scan_height)
                if pixel_shallow_count == scan_height:
                    self.X = x
                    self.Y = y
                    # self.image.crop((x, y, img_x, img_y)).show()
                    return x, y
    
    # def verify(self)


