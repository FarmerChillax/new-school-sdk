# 课表接口

| 字段 | 默认值 | 类型 | 描述                   |
| ---- | ------ | ---- | ---------------------- |
| year | None   | int  | 查询学年               |
| term | 1      | int  | 查询学期，默认第一学期 |
| schedule_time | None | dict | 自定义作息表，格式见下方说明 |

## 示例
```py
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

user:UserClient = Gdust.user_login("account", "password")

# 获取课表
course = user.get_schedule(year=2020, term=1)
print(course)
```

## 自定义作息表

不同学校的上课时间不同，SDK 内置了一套默认作息表。如果课表中的 `time` 字段与实际不符，可以传入本校的作息表：

```py
# 自定义作息表，键为节次序号（字符串），值为 [时, 分]
schedule_time = {
    "1": [8, 0],    # 第一节 8:00
    "2": [8, 50],   # 第二节 8:50
    "3": [10, 0],   # 第三节 10:00
    "4": [10, 50],  # 第四节 10:50
    "5": [14, 0],   # 第五节 14:00
    "6": [14, 50],  # 第六节 14:50
    "7": [16, 0],   # 第七节 16:00
    "8": [16, 50],  # 第八节 16:50
    "9": [19, 0],   # 第九节 19:00
    "10": [19, 50], # 第十节 19:50
}

course = user.get_schedule(year=2022, term=1, schedule_time=schedule_time)
print(course)
```

!!! warning
    作息表必须覆盖课表中出现的**所有节次**，否则会抛出 `KeyError` 并提示缺少的节次。

### 返回结果中的 time 字段

课表中每门课程的 `time` 字段包含开始和结束的**上课时间**：

```json
{
    "start": [8, 0],   // 第一节的上课时间
    "last": [8, 50]    // 最后一节的上课时间
}
```

!!! note
    `last` 是末节的**上课时间**而非下课时间。如果某课程为 1-2 节，则 `start` 是第 1 节的上课时间，`last` 是第 2 节的上课时间。

