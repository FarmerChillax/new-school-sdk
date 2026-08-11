# 常见问题

本页汇总使用 `school-sdk` 时的高频问题与排查思路。

## 登录相关

### 登录失败，如何定位原因？

`user_login()` 失败时会抛出 `LoginException`，异常信息来自教务系统页面的 `#tips` 提示文本，常见文案与含义：

| 异常信息 | 含义 | 处理建议 |
| :--- | :--- | :--- |
| 用户名或密码不正确 | 账号或密码错误 | 先在浏览器中确认账密可正常登录 |
| 验证码错误 | 验证码识别失败或已过期 | 适当调大 `retry`（默认 10），让 SDK 自动重试 |
| 登录失败 / 滑块登录失败 | 启发式判定未通过 | 检查 `exist_verify`、`captcha_type` 配置是否与学校实际一致 |

```python
from school_sdk import SchoolClient
from school_sdk.client.exceptions import LoginException

school = SchoolClient("jw.example.edu.cn")
try:
    user = school.user_login("account", "password")
except LoginException as e:
    print(f"登录失败: {e}")  # e 中带有教务系统的原始提示
```

### 验证码类型应该怎么选？

`SchoolClient` 的两个参数共同决定登录链路：

| 场景 | exist_verify | captcha_type | 额外依赖 |
| :--- | :--- | :--- | :--- |
| 登录页无验证码 | `False` | 任意（不参与） | 无 |
| 滑块验证码 | `True` | `"captcha"`（`cap` 开头即可） | 无 |
| 图形验证码（6 位字母数字） | `True` | `"kaptcha"`（`kap` 开头即可） | `pip install school-sdk[kaptcha]` |

!!! note
    不确定的话，先在浏览器打开登录页观察：拖动拼图选 `captcha`，输入图中字符选 `kaptcha`。

### 报 ImportError：图形验证码需要 PyTorch？

图形验证码识别依赖 PyTorch（自 v1.9.0 起为可选依赖），按需安装即可：

```Shell
$ pip install school-sdk[kaptcha]
```

滑块验证码与无验证码登录不需要该依赖。

## 会话相关

### 请求时提示「session 已失效」怎么办？

会话失效会抛出 `LoginException`。账密登录的用户可直接调用 `check_session()`，它会在检测到失效后自动重新登录：

```python
user.check_session()  # 失效时自动重登
course = user.get_schedule(year=2022, term=1)
```

!!! warning
    通过 `user_login_with_cookies()` / `init_dev_user()` 创建的会话缺少账密，**无法自动重登**，
    过期后需要重新获取 Cookie。

### 长时间运行的任务如何保活？

建议在每次发起业务请求前调用 `user.check_session()`；或者捕获 `LoginException` 后重建用户。避免每次都重新 `user_login()`，频繁登录容易触发教务系统风控。

## 数据查询相关

### get_score 报 ValueError？

查询成绩必须显式指定学年：

```python
# 错误: 缺少学年
user.get_score(year=None, term=1)  # ValueError: year ...

# 正确: 2021-2022 学年第一学期
user.get_score(year=2021, term=1)
```

### get_schedule 报 KeyError 且提示 schedule_time？

传入的自定义作息表缺少课表中出现的节次。补齐缺失节次即可：

```python
user.get_schedule(year=2022, term=1, schedule_time={
    "1": [8, 30], "2": [9, 30],
    # 按报错提示补充缺失的节次, 如 "3": [10, 30], ...
})
```

不传 `schedule_time` 时使用 SDK 内置作息表；各校作息不同时建议传入本校作息。

### 接口路径和我们的学校不一致？

不同正方部署的 URL 前缀可能不同，可通过 `url_endpoints` 整体覆盖端点表（抓包获取实际路径）：

```python
from school_sdk.config import URL_ENDPOINT

url_endpoints = dict(URL_ENDPOINT)
url_endpoints["SCHEDULE"] = {"API": "/kbcx/actual_path.html"}

school = SchoolClient("jw.example.edu.cn", url_endpoints=url_endpoints)
```

完整示例见[学校参数](../快速开始/school_args.md)。

## 扩展相关

### SDK 没有封装我要的接口怎么办？

用 `proxy_request()` 复用已登录会话，自行抓包并实现业务逻辑，详见[其他接口](../接口方法/others.md)。

### 更多示例在哪里？

仓库 [examples](https://github.com/FarmerChillax/new-school-sdk/tree/master/examples) 目录提供了 Cookie 登录、验证码配置、代理请求等可运行示例；仍未解决的疑惑欢迎提 [issue](https://github.com/FarmerChillax/new-school-sdk/issues)。
