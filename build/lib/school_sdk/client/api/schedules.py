# -*- coding: utf-8 -*-
'''
    :file: schedules.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/08 11:16:22
'''


from school_sdk.client.api.schedule_parse import ScheduleParse
from school_sdk.client.api import BaseCrawler
from school_sdk.client.settings import PERSON_SCHEDULE_API


class Schedule(BaseCrawler):

    def __init__(self, user_client) -> None:
        super().__init__(school=user_client.school, session=user_client._http)
        self.user_client = user_client
        self.raw_schedule = None
        self.schedule = None
        self.schedule_parse:ScheduleParse = ScheduleParse()
    
    @property
    def account(self):
        return self.user_client.account
    
    def refresh_schedule(self):
        """刷新课表数据
        """
        self.raw_schedule = None
        self.schedule = None
        self.load_schedule()

    def get_schedule_dict(self, **kwargs):
        """获取解析后的课表数据

        Returns:
            dict: 解析后的课表数据
        """
        if not self.is_load_schedule():
            self.load_schedule()
        return self.schedule_parse.get_dict()

    def get_schedule_list(self, **kwargs):
        if not self.is_load_schedule():
            self.load_schedule()
        return self.schedule_parse.get_list()
        # schedule = ScheduleParse(self.raw_schedule).get_dict()
        return schedule

    def get_raw_schedule(self, **kwargs):
        """获取元素课表数据

        Returns:
            [json]: 原始课表数据
        """
        if self.raw_schedule is None:
            self.load_schedule()
        return self.raw_schedule

    def parse_ics(self):
        """解析成ics日历格式
        """
        pass
    
    def is_load_schedule(self):
        return False if self.raw_schedule is None else True

    def load_schedule(self, **kwargs):
        """加载课表
        """
        self.raw_schedule = self._get_student_schedule()
        self.schedule_parse.load(self.raw_schedule)

    def _get_student_schedule(self): 
        params = {
            "gnmkdm": "N2151",
            "su": self.account
        }

        data = {
            "xnm": 2021,
            "xqm": 3,
            "kzlx": "ck"
        }
        url = f'{PERSON_SCHEDULE_API}'

        res = self.post(url=url, params=params, data=data)
        return res.json()




