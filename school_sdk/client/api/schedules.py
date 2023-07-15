# -*- coding: utf-8 -*-
'''
    :file: schedules.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/08 11:16:22
'''


from school_sdk.client.api.schedule_parse import ScheduleParse
from school_sdk.client.api import BaseCrawler
from school_sdk.client.exceptions import LoginException
from school_sdk.client.utils import user_is_login


class Schedule(BaseCrawler):
    year = None
    term = None
    def __init__(self, user_client, schedule_time:dict = None) -> None:
        """课表类

        Args:
            user_client (UserClient): 已登录用户实例
        """
        super().__init__(user_client=user_client)
        self.raw_schedule = None
        self.schedule = None
        self.schedule_parse: ScheduleParse = ScheduleParse(schedule_time=schedule_time)

    def refresh_schedule(self):
        """刷新课表数据
        """
        self.raw_schedule = None
        self.schedule = None
        self.load_schedule()

    def get_schedule_dict(self, **kwargs) -> dict:
        """获取解析后的课表数据

        Returns:
            dict: 解析后的课表数据
        """
        if not self.is_load_schedule():
            self.load_schedule(**kwargs)
        if kwargs.get("year") != self.year or kwargs.get("term") != self.term:
            self.load_schedule(**kwargs)
        return self.schedule_parse.get_dict()

    def get_schedule_list(self, **kwargs):
        """获取解析后的课表列表
            仅课表列表
        Returns:
            list: 仅课表列表
        """
        if not self.is_load_schedule():
            self.load_schedule()
        return self.schedule_parse.get_list()

    def get_raw_schedule(self, **kwargs):
        """获取原始课表数据

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
        self.raw_schedule = self._get_student_schedule(**kwargs)
        self.schedule_parse.load(self.raw_schedule)

    def _get_student_schedule(self, year, term, **kwargs):
        self.year = year
        self.term = term
        params = {
            "gnmkdm": "N2151",
            "su": self.account
        }

        data = {
            "xnm": year,
            "xqm": self.TERM.get(term, 1),
            "kzlx": "ck"
        }
        url = self.school.config['url_endpoints']['SCHEDULE']['API']

        res = self.post(url=url, params=params, data=data, **kwargs)
        # print(res.text, res, res.status_code)
        if user_is_login(self.account, res.text):
            return res.json()
        raise LoginException()
