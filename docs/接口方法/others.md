# 其他接口

## proxy_request (通用代理请求接口)

| 字段       | 默认值  | 类型     | 描述   |
| -------- | ---- | ------ | ---- |
| method  | None | String | HTTP Method |
| url_or_endpoint | None | String | 请求的完整 URL 或者具体的请求 HTTP Path |
| **kwargs | None | Any | 这些参数将会透传到 requests 网络请求库的 request 方法中，具体参数请查阅其文档: https://docs.python-requests.org/en/latest/api/#requests.request |

## 示例
```python
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
```

## 其他登录方式
更多 demo 详见仓库 [examples](https://github.com/FarmerChillax/new-school-sdk/tree/master/examples) 目录
