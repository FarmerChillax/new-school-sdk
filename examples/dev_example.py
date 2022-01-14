# -*- coding: utf-8 -*-
'''
    :file: dev_example.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2022/01/06 20:34:12
'''
from school_sdk import SchoolClient
from school_sdk.client import UserClient

# 实例化学校
Gdust = SchoolClient("farmer2333.top", port=7899)

# 实例化用户
cookies_str = "<Your cookies string>" # e.g JSESSIONID=E738AE92B3CF133171F5B8E3E4643A5E
user: UserClient = Gdust.init_dev_user(cookies_str)

# 获取课表
course = user.get_schedule(year=2020, term=2)
print(course)

# 获取成绩, 2020-2021学年第一学期的成绩
score = user.get_score(year=2020, term=1)
print(score)

# 获取个人信息
info = user.get_info()
print(info)
