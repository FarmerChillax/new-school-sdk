# -*- coding: utf-8 -*-
'''
    :file: base_sample.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/18 00:31:02
'''

from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")

# 获取课表
course = user.get_schedule(year=2021, term=1)
print(course)

# 获取成绩, 2020-2021学年第一学期的成绩
score = user.get_score(year=2020, term=1)
print(score)

# 获取个人信息
info = user.get_info()
print(info)