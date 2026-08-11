# New-School-SDK

---

新版正方系统爬虫--Python SDK


[![pypi](https://img.shields.io/pypi/v/school-sdk.svg)](https://pypi.org/project/school-sdk/)
[![Downloads](https://pepy.tech/badge/school-sdk)](https://pepy.tech/project/school-sdk)


new-school-sdk 是一个新版正方系统接口的第三方 Python SDK, 实现了用户成绩查询、课表查询以及用户信息查询。

## 架构概览

SDK 采用「学校配置 + 用户会话」的两层客户端模型：

- **`SchoolClient`（学校级门面）**：持有教务系统地址、验证码类型、重试次数、端点表等学校级配置；无状态、可复用，一个实例可为多个用户签发会话
- **`UserClient`（用户级会话）**：持有 `requests.Session` 与账号凭据，对外提供 `get_schedule` / `get_score` / `get_info` 三类查询 API，以及用于扩展任意业务的 `proxy_request`

内部分层如下：

```
门面层  SchoolClient ──factory──▶ UserClient
业务层  ZFLogin(登录编排) │ Schedule(课表) │ Score(成绩) │ Info(个人信息)
解析层  ScheduleParse │ 各业务类内的 _parse
HTTP 层 共享同一个 requests.Session, 自动拼接 BASE_URL
支撑层  PyRsa(纯 Python RSA) │ check_code(验证码识别) │ URL_ENDPOINT 端点表
```

关键流程与机制：

- **登录流程**：获取 CSRF 令牌 → 获取 RSA 公钥 → 按学校配置自动识别验证码（滑块启发式 / 图形 CNN）→ 提交 RSA 加密后的密码
- **验证码识别**：滑块验证码基于像素列扫描启发式（仅依赖 Pillow）；图形验证码基于 CNN 推理（需安装 `[kaptcha]` 可选依赖）
- **跨校适配**：`url_endpoints` 端点表可整体覆盖，适配不同 URL 前缀的正方部署；学期编码由 SDK 内部映射
- **异常体系**：登录失败与会话失效统一抛出 `LoginException`，异常信息携带教务系统原始提示

详细的模块职责、登录时序与已知约束见仓库根目录 `design_doc/` 下的项目设计文档（`架构设计.md`、`Codecov接入设计.md`）。


## 安装模块

### uv (推荐)
```Shell
$ uv add school-sdk
```

### pip
```Shell
$ pip install school-sdk
```

## 快速使用

1. 按需创建虚拟环境
2. 通过 `from school_sdk import SchoolClient, UserClient` 导入依赖包
3. 通过 `my_school = SchoolClient("<此处填写教务系统地址>")` 创建学校
4. 通过`user = my_school.user_login("account", "password")` 获取一个登录的用户

以下是完整的例子：
```py
from school_sdk import SchoolClient, UserClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")
```
