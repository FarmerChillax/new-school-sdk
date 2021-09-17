# -*- coding: utf-8 -*-
'''
    :file: schedule_parse.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/14 13:03:36
'''
import re


class ScheduleParse():

    __TIME_LIST = {
        "1": [8, 30],
        "2": [9, 20],
        "3": [10, 25],
        "4": [11, 15],
        "5": [14, 40],
        "6": [15, 30],
        "7": [16, 30],
        "8": [17, 20],
        "9": [19, 30],
        "10": [20, 20]
    }

    def __init__(self, content=None) -> None:
        self.raw = content
        self.parse_list:list = []
        self.parse_dict:dict = {}
        self.parse_ics = None

    def get_dict(self):
        return self.parse_dict

    def get_list(self):
        return self.parse_list

    def load(self, content):
        self.raw = content
        self._parse()

    def _parse(self):
        """解析课表
            姓名、班级、课程、时间、地点、校区、节数、周数等详细信息
        Args:
            content ([type]): [description]
        """
        user_message: dict = self.raw.get("xsxx")
        schedule_list: list = self.raw.get("kbList")
        # 用户基本信息
        user_class_name = user_message.get("BJMC")
        username = user_message.get("XM")

        # get schedule items
        for course in schedule_list:
            weeks_arr = self.get_course_week(course.get('zcd'))
            time_text = f"{course.get('xqjmc')} {course.get('jc')}"

            self.parse_list.append({
                "course": course.get('kcmc', "找不到课程名"),
                "place": course.get('cdmc', "找不到上课地点"),
                "campus": course.get('xqmc', "南城"),
                "teacher": course.get('xm'),
                "weeks_text": course.get('zcd'),
                "week_day": course.get('xqj'),
                "week_day_text": course.get('xqjmc'),
                "time_text": time_text,
                "weeks_arr": weeks_arr,
                "time": self.get_class_time(course.get('jcs'))
            })
        
        self.parse_dict.setdefault("class_name", user_class_name)
        self.parse_dict.setdefault("username", username)
        self.parse_dict.setdefault("course_list", self.parse_list)

    def get_class_time(self, b2e:str):
        start, end = b2e.split('-')
        start_time = self.__TIME_LIST[start]
        end_time = self.__TIME_LIST[end]
        return {"start": start_time, "last": end_time}

    def get_course_week(self, week_text: str) -> list:
        """获得这门课程一共要上的详细周数

        Args:
            zcd (str): zcd正方原始数据对应的key名

        Returns:
            list: 要上该门课的星期
        """
        interval = week_text.split(",")
        weeks = []

        for week in interval:
            leap = 1
            if "(单)" in week or "(双)" in week:
                week = week.replace("(双)", "")
                week = week.replace("(单)", "")
                leap = 2
            re_result = re.search("(\d+).?(\d*).*", week)
            real = re_result.groups()
            if real[-1] == '':
                weeks += [int(real[0])]
            else:
                # for start to end week
                weeks += [i for i in range(
                    int(real[0]), int(real[1]) + 1, leap)]

        return weeks
