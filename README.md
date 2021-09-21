正方系统 Python SDK。

<!-- [![Build Status](https://travis-ci.org/dairoot/school-api.svg?branch=master)](https://travis-ci.org/dairoot/school-api)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/dairoot/school-api/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/dairoot/school-api/?branch=master)
[![codecov](https://codecov.io/gh/dairoot/school-api/branch/master/graph/badge.svg)](https://codecov.io/gh/dairoot/school-api)
[![pypi](https://img.shields.io/pypi/v/school-api.svg)](https://pypi.org/project/school-api/)
[![Downloads](https://pepy.tech/badge/school-sdk)](https://pepy.tech/project/school-api) -->

## Usage
```Shell
$ pip install school-sdk
# or
$ pip install zf-school-sdk
```

```Python
from school_sdk import SchoolClient

# 先实例化一个学校，再实例化用户
school = SchoolClient("172.16.254.1", exist_verify=True)
user:UserClient = school.user_login("2018xxxxx", "xxxxxxxx")
cours = user.get_schedule()
print(cours)
```

## Api Function

| Api          | Description | Argument          |
| :----------- | :---------- | :---------------- |
| user_login   | 登陆函数    | account, password |
| get_schedule | 课表查询    | year, term        |
| get_score    | 成绩查询    | year, term        |



## School-SDK Options

| Option        | Default      | Description           |
| :------------ | :----------- | :-------------------- |
| host          | 不存在默认值 | 教务系统地址(`必填`)  |
| port          | 80           | 端口号                |
| ssl           | http         | 教务系统是否使用https |
| name          | None         | 学校名称              |
| exist_verify  | False        | 是否存在验证码        |
| lan_host      | None         | 内网地址              |
| lan_port      | 80           | 内网地址端口          |
| timeout       | 10           | 全局请求延时          |
| url_endpoints | None         | 地址配置              |



<!-- | <!--            | url_path_list | `略`                    | 学校接口地址列表 |
| class_time_list | `略`          | 上课时间列表            |
| timeout         | 10            | 全局请求延时            |
| session         | MemoryStorage | 缓存工具(推荐使用redis) |              | --> 
