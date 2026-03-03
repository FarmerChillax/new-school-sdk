# 简单示例

## 安装模块
```Shell
$ pip install school-sdk
```

## 使用示例

```py
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")
```

## 获取【个人】课表

```py
# 获取课表
course = user.get_schedule(year=2021, term=1)
print(course)
```

## 获取成绩
```py
# 获取成绩, 2020-2021学年第一学期的成绩
score = user.get_score(year=2020, term=1)
print(score)
```

## 获取个人信息
```py
# 获取个人信息
info = user.get_info()
print(info)
```
