# 用户登录

| 字段       | 默认值  | 类型     | 描述   |
| -------- | ---- | ------ | ---- |
| account  | None | String | 用户账号 |
| password | None | String | 用户密码 |

## 示例
```python
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")
```

## 其他登录方式
更多登录 demo 详见仓库 [examples](https://github.com/FarmerChillax/new-school-sdk/tree/master/examples) 目录