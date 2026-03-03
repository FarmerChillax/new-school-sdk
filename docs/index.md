# New-School-SDK

---

新版正方系统爬虫--Python SDK


[![pypi](https://img.shields.io/pypi/v/school-sdk.svg)](https://pypi.org/project/school-sdk/)
[![Downloads](https://pepy.tech/badge/school-sdk)](https://pepy.tech/project/school-sdk)


new-school-sdk 是一个新版正方系统接口的第三方 Python SDK, 实现了用户成绩查询、课表查询以及用户信息查询。


## 安装模块
```Shell
$ pip install school-sdk
```

## 快速使用

1. 按需创建虚拟环境
2. 通过 `pip install school-sdk` 安装依赖
3. 通过 `from school_sdk import SchoolClient, UserClient` 导入依赖包
4. 通过 `MySchool = SchoolClient("<此处填写教务系统地址>")` 创建学校
5. 通过`user = MySchool.user_login("account", "password")` 获取一个登录的用户

以下是完整的例子：
```py
from school_sdk import SchoolClient, UserClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")
```