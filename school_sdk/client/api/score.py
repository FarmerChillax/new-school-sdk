# -*- coding: utf-8 -*-
'''
    :file: score.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/20 20:06:29
'''
# cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005&su=2018133209

import requests
from school_sdk.client.api import BaseCrawler


class Score(BaseCrawler):

    def __init__(self, school, session: requests.Session) -> None:
        """获取成绩

        Args:
            school ([type]): [description]
            session (requests.Session): [description]
        """
        super().__init__(school, session)
        pass
    pass