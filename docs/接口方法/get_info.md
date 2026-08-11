# 获取个人信息

| 字段 | 默认值 | 类型 | 描述 |
| -------- | ---- | ------ | ---- |
| 无 | - | - | 使用已登录会话获取当前用户的个人信息 |

## 示例

```python
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")

# 获取个人信息
info = user.get_info()
print(info)
```

返回示例：

```python
{
    'student_number': '2018133209',
    'name': '张三',
    'department_name': '计算机与软件学院',
    'class_name': '软件1802班',
    'grade': '2018',
    'graduation_school': '示例中学',
    'major': '软件工程',
    'gender': '男'
}
```

## 返回字段

| 字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| student_number | String | 学号 |
| name | String | 姓名 |
| department_name | String | 学院（系）名称 |
| class_name | String | 班级名称 |
| grade | String | 年级 |
| graduation_school | String | 毕业中学 |
| major | String | 专业方向 |
| gender | String | 性别 |

!!! note
    个人信息基于页面 CSS 选择器解析，是三类数据中最依赖页面结构的一处；
    若某字段返回空字符串，通常是教务系统页面改版导致选择器失效，欢迎提 issue 并附上页面结构。

## 缓存与刷新

`get_info()` 的结果会被缓存，重复调用不会再次发起请求；需要强制重新获取时使用 `refresh_info()`：

```python
# 命中缓存, 不会发起新请求
info = user.get_info()

# 丢弃缓存并重新请求
info = user.refresh_info()
```
