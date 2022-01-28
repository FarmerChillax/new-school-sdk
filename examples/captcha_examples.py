# -*- coding: utf-8 -*-
'''
    :file: use_verify.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2022/01/14 21:33:06
'''

from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
# 并根据验证码类型指定captcha_type为kap或者cap
# 使用Kaptcha(与旧版系统类似的验证码)
Gdust = SchoolClient("172.16.254.1", exist_verify=True, captcha_type="kaptcha")
# 使用captcha(滑块验证码)
Gdust = SchoolClient("172.16.254.1", exist_verify=True, captcha_type="captcha")


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