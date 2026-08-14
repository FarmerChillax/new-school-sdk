# 其他接口

## check_session (检查会话)

检查当前会话是否有效，失效时自动重新登录。

```python
# 在每次业务请求前检查会话
user.check_session()  # 失效时自动重登
course = user.get_schedule(year=2022, term=1)
```

!!! warning
    通过 `user_login_with_cookies()` / `init_dev_user()` 创建的会话缺少账密，无法自动重登。

## refresh_info (刷新个人信息)

丢弃缓存的个人信息，重新从教务系统获取。

```python
# 第一次调用会缓存
info = user.get_info()

# 强制重新获取
info = user.refresh_info()
```

## proxy_request (通用代理请求接口)

| 字段       | 默认值  | 类型     | 描述   |
| -------- | ---- | ------ | ---- |
| method  | None | String | HTTP Method |
| url_or_endpoint | None | String | 请求的完整 URL 或者具体的请求 HTTP Path |
| **kwargs | None | Any | 这些参数将会透传到 requests 网络请求库的 request 方法中，具体参数请查阅其文档: https://docs.python-requests.org/en/latest/api/#requests.request |

`proxy_request` 复用已登录的 Session，可调用教务系统任意接口。先用浏览器开发者工具抓包，然后构造请求即可。

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

## 扩展场景示例

### 查询考试安排

考试安排接口通常位于 `/kwgl/kscx_cxXsksxxIndex.html`，具体路径因学校而异：

```python
# 查询考试安排（具体参数需抓包确认）
resp = user.proxy_request("POST", "/kwgl/kscx_cxXsksxxIndex.html", data={
    "xnm": "2022",       # 学年
    "xqm": "3",           # 学期编码: 1=3, 2=12, 3=16
    "ksmcdmb_id": "",     # 考试场次，留空表示全部
    "kch": "",            # 课程代码，留空表示全部
})

exam_list = resp.json().get("items", [])
for exam in exam_list:
    print(f"科目: {exam.get('kcmc')}")
    print(f"时间: {exam.get('kssj')}")
    print(f"地点: {exam.get('cdmc')}")
    print("---")
```

### 查询空教室

```python
# 查询空教室（具体参数需抓包确认）
resp = user.proxy_request("POST", "/jsjy/jsjy_cxKjsjsxx.html", data={
    "xnm": "2022",
    "xqm": "3",
    "xqj": "1",           # 星期几
    "jcd": "1-2",        # 节次范围
})

rooms = resp.json().get("items", [])
for room in rooms:
    print(f"教室: {room.get('jsmc')} 容量: {room.get('zws')}")
```

### 查询绩点与学分汇总

```python
# 查询所有学年成绩（具体参数需抓包确认）
resp = user.proxy_request("POST", "/cjcx/cjcx_cxDgXscj.html", data={
    "xnm": "",            # 留空表示所有学年
    "xqm": "",            # 留空表示所有学期
    "_search": "false",
    "queryModel.showCount": "5000",  # 获取所有记录
})

scores = resp.json().get("items", [])
total_credit = sum(float(s.get("xf", 0)) for s in scores)
print(f"总学分: {total_credit}")
```

!!! tip
    以上示例中的接口路径和参数因学校而异，请用浏览器开发者工具（F12 → Network）抓包确认实际值。

## 其他登录方式
更多 demo 详见仓库 [examples](https://github.com/FarmerChillax/new-school-sdk/tree/master/examples) 目录
