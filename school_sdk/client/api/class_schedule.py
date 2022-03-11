# -*- coding: utf-8 -*-
'''
    :file: class_schedule.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2022/02/15 13:15:14
'''

import re
from school_sdk.client.api import BaseCrawler


url = '/kbdy/bjkbdy_cxBjKb.html?gnmkdm=N214505&su=2018133209'

payload = {
    'xnm': 2021,
    'xqm': 3,
    'xnmc': '2021-2022',
    'xqmmc': 1,
    'xqh_id': '1, 1',
    'njdm_id': 2018,
    'zyh_id': 1008,
    'bh_id': 10081802,
    'tjkbzdm': 1,
    'tjkbzxsdm': 0,
    'zymc': '软件工程',
    'jgmc': '计算机学院',
    'bj': '18软件本科2班',
    'xkrs': 34,
    'zxszjjs': False,
    'kzlx': 'ck'
}


class ScheduleClass(BaseCrawler):
    year = None
    term = None

    def __init__(self, user_client) -> None:
        super().__init__(user_client)
        self.raw_schedule = None
        self.class_schedule = None

    def _get_raw(self, year, term=1, grade=None, user_info=None, **kwargs):
        self.year = year
        self.term = term
        params = {
            'gnmkdm': 'N214505',
            'su': self.account
        }
        data = {
            'xnm': self.year,
            'xqm': self.TERM.get(term, 1),
            # 'xnmc': f'{self.year}-{self.year + 1}',
            # 'xqmmc': self.term,
            # 'xqh_id': '4,4',
            'njdm_id': 2019,
            'zyh_id': 1008,
            'bh_id': 10081910,
            # 'tjkbzdm': 1,
            # 'tjkbzxsdm': 0,
            # 'zymc': '软件工程',
            # 'jgmc': '计算机学院',
            # 'bj': '19软件本科10班',
            # 'xkrs': 51,
            # 'zxszjjs': False,
            'kzlx': 'ck'
        }

        url = self.school.config['url_endpoints']['CLASS_SCHEDULE']['API']
        
        res = self.post(url=url, params=params, data=data, **kwargs)
        print(res.json(), res.status_code)
        import json
        
        with open("test.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(res.json(), ensure_ascii=False))