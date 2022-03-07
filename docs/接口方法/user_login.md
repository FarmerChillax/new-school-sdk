# user_login接口

| 字段       | 默认值  | 类型     | 描述   |
| -------- | ---- | ------ | ---- |
| account  | None | String | 用户账号 |
| password | None | String | 用户密码 |

## 示例
```py

from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")
```