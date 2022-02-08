# -*- coding: utf-8 -*-
'''
    :file: check.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2022/02/04 17:42:44
'''
from school_sdk.client.api import BaseCrawler
class CheckSession(BaseCrawler):

    def __init__(self, user_client) -> None:
        super().__init__(user_client)
    
    # def check