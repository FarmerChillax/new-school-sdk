# -*- coding: utf-8 -*-
'''
    :file: user_info.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/11/25 11:50:16
'''

from school_sdk.client.api import BaseCrawler
from pyquery import PyQuery as pq



class Info(BaseCrawler):

    def __init__(self, user_client) -> None:
        """获取用户信息类

        Args:
            user_client (UserClient): 已登录的用户实例
        """
        super().__init__(user_client)
        self.raw_info = None
        self.info = None

    def get_info(self, **kwargs):
        if self.raw_info is None:
            self.raw_info = self._get_raw_info(**kwargs)
            self.info = self._parse(self.raw_info)
        return self.info
    
    
    def _get_raw_info(self, **kwargs):
        """获取用户信息原始数据
        """

        params = {
            "gnmkdm": "N100801",
            "layout": "default",
            "su": self.account
        }
        url = self.school.config['url_endpoints']['INFO']['API']

        result = self.get(url=url, params=params, **kwargs)
        return result.content
    
    def _parse(self, html:str) -> dict:
        doc = pq(html)
        info = {
            'student_number': doc('#ajaxForm > div > div.panel-heading > div > div:nth-child(1) > div > div > p').text(),
            'name': doc('#ajaxForm > div > div.panel-heading > div > div:nth-child(2) > div > div > p').text(),
            'department_name': doc('#col_jg_id > p').text(),
            'class_name': doc('#col_bh_id > p').text(),
            'grade': doc('#col_njdm_id > p').text(),
            'graduation_school': doc('#col_byzx > p').text(),
        }
        
        return info
