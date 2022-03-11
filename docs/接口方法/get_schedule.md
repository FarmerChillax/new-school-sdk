# 课表接口

| 字段 | 默认值 | 类型 | 描述                   |
| ---- | ------ | ---- | ---------------------- |
| year | None   | int  | 查询学年               |
| term | 1      | int  | 查询学期，默认第一学期 |

## 示例
```py
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

user:UserClient = Gdust.user_login("account", "password")

# 获取课表
course = user_1.get_schedule(year=2020, term=1)
print(course)
```

