新版正方系统 Python SDK。(支持自动识别、处理滑块验证码与常规验证码，如果觉得还不错,给个小星星趴~⭐)

> 这是全网唯一一个自动处理新版教务系统验证码的 SDK :p

<!-- [![Build Status](https://travis-ci.org/dairoot/school-api.svg?branch=master)](https://travis-ci.org/dairoot/school-api)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/dairoot/school-api/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/dairoot/school-api/?branch=master)
[![codecov](https://codecov.io/gh/dairoot/school-api/branch/master/graph/badge.svg)](https://codecov.io/gh/dairoot/school-api)
[![pypi](https://img.shields.io/pypi/v/school-api.svg)](https://pypi.org/project/school-api/)
[![Downloads](https://pepy.tech/badge/school-sdk)](https://pepy.tech/project/school-api) -->


<!-- <p align = "center"> -->
  [![Downloads](https://pepy.tech/badge/school-sdk)](https://pepy.tech/project/school-sdk)
    <a href = "https://www.python.org">
        <img alt = "python3" src = "https://img.shields.io/badge/language-python3-brightgreen" />
    </a>
    <a href = "LICENSE">
        <img alt = "license" src = "https://img.shields.io/badge/license-MIT-blue.svg" />
    </a>
    <a href = "https://github.com/FarmerChillax/new-school-sdk/stargazers/">
        <img alt = "stars" src = "https://badgen.net/github/stars/FarmerChillax/new-school-sdk/" />
    </a>
    <a href = "https://github.com/FarmerChillax/new-school-sdk/network/members/">
        <img alt = "forks" src = "https://badgen.net/github/forks/FarmerChillax/new-school-sdk/" />
    </a>
    [![PyPI Version](http://img.shields.io/pypi/v/school-sdk.svg)](https://pypi.python.org/pypi/school-sdk)

<!-- </p> -->

[在线文档](https://farmerChillax.github.io/new-school-sdk/)

[Roadmap](https://github.com/FarmerChillax/new-school-sdk/milestone/1)

## 支持的登录/验证码方式
- 帐号密码登录
- 滑块验证码登录
- 图形验证码登录
- cookie 登录（用于扫码登录、OIDC 等场景）


## 测试环境
- Python == 3.8 
- 默认验证码识别方式: CPU

## Usage
```Shell
$ pip install school-sdk
# or
$ pip install zf-school-sdk
```

> 如果机器内存不足，可以使用 pip `--no-cache-dir` 选项来安装
> e.g: `pip --no-cache-dir install school-sdk`

```Python
from school_sdk import SchoolClient
from school_sdk.client import UserClient

# 先实例化一个学校，再实例化用户
school = SchoolClient("172.16.254.1")
user:UserClient = school.user_login("2018xxxxx", "xxxxxxxx")

# 获取 2020 学年第二学期的课程
course = user.get_schedule(year=2020, term=2)
print(course)
```

使用示例参见 [examples](examples/)

## Api Function

| Api           | Description                 | Argument          |
| :------------ | :-------------------------- | :---------------- |
| user_login    | 登陆函数                    | account, password |
| get_schedule  | 课表查询                    | year, term        |
| get_score     | 成绩查询                    | year, term        |
| get_info      | 获取个人信息                | None              |
| refresh_info  | 刷新个人信息                | None              |
| check_session | 检查session并其失效后重登录 | None              |



## School-SDK Options

| Option        | Default      | Description              |
| :------------ | :----------- | :----------------------- |
| host          | 不存在默认值 | 教务系统地址(`必填`)     |
| port          | 80           | 端口号                   |
| ssl           | False        | 教务系统是否使用https    |
| name          | None         | 学校名称                 |
| exist_verify  | False        | 是否存在验证码           |
| captcha_type  | captcha      | 验证码类型(常规 或 滑块) |
| retry         | 10           | 登录重试次数             |
| lan_host      | None         | 内网地址（暂不可用）                 |
| lan_port      | 80           | 内网地址端口（暂不可用）             |
| timeout       | 10           | 全局请求延时             |
| url_endpoints | None         | 地址配置                 |

## 相关项目
> 帮教务系统做负载均衡：https://github.com/FarmerChillax/school-load-balance
> 
> (如果你们学校教务系统抢课经常崩溃，可以考虑看看这个 repo)


- 新版正方教务系统: https://github.com/FarmerChillax/new-school-sdk
- 旧版正方教务系统: https://github.com/dairoot/school-api
- SDK的Flask扩展: https://github.com/FarmerChillax/flask-school
- 验证码识别: https://github.com/FarmerChillax/new-zfxfzb-code

<!-- | <!--            | url_path_list | `略`                    | 学校接口地址列表 |
| class_time_list | `略`          | 上课时间列表            |
| timeout         | 10            | 全局请求延时            |
| session         | MemoryStorage | 缓存工具(推荐使用redis) |              | --> 
