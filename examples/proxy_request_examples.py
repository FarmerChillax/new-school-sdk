# -*- coding: utf-8 -*-
'''
    :file: proxy_request_examples.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2025/07/25 14:21:07
'''
import requests
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.1.1")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")

# 如果有某个 sdk 未实现的接口，如获取考试成绩接口
# 用户想自行抓包后复用本 SDK 的登录能力，可以这么实现：

# 1. 填写抓包获取的 http body
request_body = {
    "kcxx_example": "test-data"
}
# 2. 发起网络请求
resp:requests.Response = user.proxy_request("POST", "/cjcx/cjcx_cxDgXscj.html", data=request_body)

# 3. 获取响应体内容
print(f"response body: {resp.json()}")
