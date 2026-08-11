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

## 配置验证码

登录页存在验证码时, 需要开启 `exist_verify` 并按验证码形态选择 `captcha_type`：

```py
# 滑块验证码(拖动拼图): cap 开头
Gdust = SchoolClient("172.16.254.1", exist_verify=True, captcha_type="captcha")

# 图形验证码(输入图中字符): kap 开头, 需安装 pip install school-sdk[kaptcha]
Gdust = SchoolClient("172.16.254.1", exist_verify=True, captcha_type="kaptcha")
```

!!! note
    登录页没有验证码时保持默认配置即可（`exist_verify=False`）。
    全部学校参数说明见[学校参数](./school_args.md)。

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

## 处理常见异常

登录与会话相关的失败以 `LoginException` 抛出, 异常信息带有教务系统的原始提示：

```py
from school_sdk import SchoolClient
from school_sdk.client.exceptions import LoginException

Gdust = SchoolClient("172.16.254.1")
try:
    user = Gdust.user_login("account", "password")
except LoginException as e:
    print(f"登录失败: {e}")
```

!!! tip
    一次登录后可反复调用 `get_schedule` / `get_score` / `get_info`, 无需重复登录；
    会话失效时可调用 `user.check_session()` 自动重登。

## 下一步

- [学校参数](./school_args.md): `SchoolClient` 全部配置项与自定义端点示例
- [接口方法](../接口方法/index.md): 各 API 的参数与返回说明
- [最佳实践](../最佳实践.md): 会话复用、Cookie 调试、异常处理等推荐做法
- [常见问题](../常见问题/index.md): 高频报错的排查思路
