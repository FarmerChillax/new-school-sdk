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
        self.endpoints: dict = self.school.config['url_endpoints']
        self.raw_score = None
        self.score_dict:dict = {}
        self.score_list:list = []

    def get_score(self, **kwargs):
        return self.get_score_dict(**kwargs)

    def get_score_list(self, **kwargs):
        """获取成绩清单-列表

        Returns:
            list: 成绩列表
        """
        if not self.score_list:
            self.parse(**kwargs)
        return self.score_list

    def get_score_dict(self, **kwargs):
        """获取成绩清单-字典

        Returns:
            dict: 成绩字典清单
        """
        if not self.score_dict:
            self.parse(**kwargs)
        return self.score_dict

    def parse(self, **kwargs):
        """解析数据
        """
        if self.raw_score is None:
            self.load_score(**kwargs)
        self._parse(self.raw_score)

    def load_score(self, **kwargs) -> None:
        """加载课表
        """
        self.raw_score = self._get_score(**kwargs)

    def _get_score(self, year: int, term: int = 1, **kwargs):
        """获取教务系统成绩

        Args:
            year (int): 学年
            term (int, optional): 学期. Defaults to 1.

        Returns:
            json: json数据
        """
        url = self.endpoints['SCORE']['API']

        params = {
            'doType': 'query',
            'gnmkdm': 'N305005',
            'su': self.account
        }

        data = {
            'xnm': year,
            'xqm': self.TERM.get(term, 3),
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

    def _parse(self, raw: dict):
        # kcmc -> 课程名称 # kcxzmc -> 课程性质名称 # kcbj -> 课程标记 # jsxm -> 教师姓名
        # khfsmc -> 考核方式 # ksxz -> 考试性质 # xf -> 学分 # kkbmmc -> 开课部门名称 # cj -> 成绩
        # njdm_id -> 年级代码
        """解析教务系统成绩

        Args:
            raw (dict): 教务系统的原始数据
        """
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
