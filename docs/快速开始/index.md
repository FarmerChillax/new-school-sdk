# 简单示例

## 安装模块
```Shell
$ pip install school-sdk
```

如果你的学校启用了图形验证码（`captcha_type="kap"` 开头），还需要安装深度学习依赖：
```Shell
$ pip install school-sdk[kaptcha]
```

!!! note
    无验证码与滑块验证码（`captcha_type="captcha"`）不需要额外依赖。

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
