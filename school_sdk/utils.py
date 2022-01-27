# -*- coding: utf-8 -*-
'''
    :file: utils.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/04 23:45:40
'''

class ObjectDict(dict):
    """:copyright: (c) 2014 by messense.
    Makes a dictionary behave like an object, with attribute-style access.
    """

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value

    def __getstate__(self):
        return None


def is_endpoint(url_or_endpoint:str) -> bool:
    """判断是不是端点

    Args:
        url_or_endpoint (str): url 或 端点字符串

    Returns:
        bool: 不是http则返回False
    """
    if url_or_endpoint.startswith(('http://', 'https://')):
        return False
    return True

