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
        """初始化

        Args:
            content (string): 课表原始数据
        """
        self.raw = content
        self._parse()

    def _parse(self):
        """解析课表
            姓名、班级、课程、时间、地点、校区、节数、周数等详细信息
        """
        self.parse_list:list = []
        self.parse_dict:dict = {}
        self.parse_ics = None
        
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
        """获取课程的开始和结束的上课时间
            如某课程为早上一二节(1-2), 则开始时间为第一节的时间, 结束时间为第二节课的上课时间。
            注意：是开始和结束的`上课时间`
            e.g: 第一二节为8.30-9.15, 中间休息5分钟, 9.20-10.05
                    返回: {
                        'start': [8, 30],
                        'last': [9, 20]
                    }
        Args:
            b2e (str): 原始范围字符串, 如`1-2`

        Returns:
            [type]: 课程开始和课程结束的时间
        """
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
