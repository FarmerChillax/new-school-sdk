# -*- coding: utf-8 -*-
'''
    :file: config.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/10/17 16:54:09
'''
# 使用自定义路径
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 通过抓包填写以下路径，如有迷惑或错误烦请提issue并提供地址测试
url_endpoints = {
    'HOME_URL': "/xtgl/login_slogin.html", # 首页url
    'LOGIN': {
        # 该模块表示登录使用到的端点
        'INDEX': '/xtgl/login_slogin.html', # 首页，一般和上面保持一致
        'CAPTCHA': '/zfcaptchaLogin', # 验证码url，貌似都一样
        'PUBLIC_KEY': '/xtgl/login_getPublicKey.html', # RSA密钥端点
    },
    "SCORE_URL": "", # 未使用
    "INFO_URL": "", # 未使用
    # 课表页面的api
    "SCHEDULE": {
        "API": '/kbcx/xskbcx_cxXsKb.html',
    },
    # 成绩页面的api
    'SCORE': {
        'API': '/cjcx/cjcx_cxDgXscj.html'
    }
}

# 使用自定义的endpoints，实例化学校
# exist_verify: 是否有验证码
Gdust = SchoolClient("172.16.254.1", exist_verify=True, url_endpoints=url_endpoints)

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