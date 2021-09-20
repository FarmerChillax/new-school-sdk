# -*- coding: utf-8 -*-
'''
    :file: score.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/20 20:06:29
'''
# cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005&su=2018133209

from school_sdk.client.api import BaseCrawler


class Score(BaseCrawler):

    def __init__(self, user_client) -> None:
        super().__init__(user_client)
        self.endpoints:dict = self.school.config['url_endpoints']
        self.raw_score = None
        self.score_dict = {}
        self.score_list = []

    def get_score(self, **kwargs):
        self.raw_score = self._get_score()
        self._parse(self.raw_score)
        return self.score_dict

    def _get_score(self, **kwargs):
        
        url = self.endpoints['SCORE']['API']
        
        params = {
            'doType': 'query',
            'gnmkdm': 'N305005',
            'su': self.account
        }

        data = {
            'xnm': 2020,
            'xqm': 3,
            '_search': False,
            'nd': self.t,
            'queryModel.showCount': 500,
            'queryModel.currentPage': 1,
            'queryModel.sortName': None,
            'queryModel.sortOrder': 'asc',
            'time': 4,
        }

        res = self.post(url=url, params=params, data=data, **kwargs)
        return res.json()
    
    def _parse(self, raw:dict):
        # kcmc -> 课程名称 # kcxzmc -> 课程性质名称 # kcbj -> 课程标记 # jsxm -> 教师姓名
        # khfsmc -> 考核方式 # ksxz -> 考试性质 # xf -> 学分 # kkbmmc -> 开课部门名称 # cj -> 成绩
        # njdm_id -> 年级代码
        items = raw.get('items')
        for item in items:
            format_item = {
                "course_name": item.get('kcmc'),
                'course_nature': item.get('kcxzmc'),
                'course_target': item.get('kcbj'),
                'teacher': item.get('jsxm'),
                'exam_method': item.get('khfsmc'),
                'exam_nature': item.get('ksxz'),
                'exam_result': item.get('cj'),
                'credit': item.get('xf'),
                'course_group': item.get('kkbmmc'),
                'grade': item.get('njdm_id')
            }
            self.score_list.append(format_item)
            self.score_dict.setdefault(item.get('kcmc'), format_item)
