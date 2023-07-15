# -*- coding: utf-8 -*-
'''
    :file: test.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/02 23:09:54
'''


import sys
import os

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

import ssl
ssl.OPENSSL_VERSION = ssl.OPENSSL_VERSION.replace("LibreSSL", "OpenSSL")
from school_sdk.client import UserClient
from school_sdk import SchoolClient

SCHOOL_HOST = os.getenv("SCHOOL_HOST")
SCHOOL_ACCOUNT = os.getenv("SCHOOL_ACCOUNT")
SCHOOL_PASSWORD = os.getenv("SCHOOL_PASSWORD")

# 实例化学校
Gdust = SchoolClient(host=SCHOOL_HOST, port=443,ssl=True, exist_verify=False)

# 实例化用户
user:UserClient = Gdust.user_login(SCHOOL_ACCOUNT, SCHOOL_PASSWORD)
print(user.check_session())

# 获取课表
course = user.get_schedule(year=2022, term=2, schedule_time={
        "1": [8, 30],
        "2": [9, 20],
        "3": [10, 10],
        "4": [11, 00],
        "5": [13, 30],
        "6": [14, 20],
        "7": [15, 10],
        "8": [16, 00],
        "9": [18, 30],
        "10": [19, 20],
        "11": [20, 10],
    })
# user.get_schedule()
print(course)

# 获取成绩, 2020-2021学年第一学期的成绩
score = user.get_score(year=2022, term=1)
print(score)

# 获取个人信息
info = user.get_info()
print(info)