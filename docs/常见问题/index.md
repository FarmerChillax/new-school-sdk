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

### 教务系统有弹窗，导致登录失败 (LoginException)？

部分学校的教务系统会在以下情况弹出强制弹窗（必须阅读确认后才能进入主页）：

- 学生账号**未完善个人资料**（如联系电话为空）
- 学生账号**存在挂科**记录
- 教务系统发布的全局通知弹窗

弹窗会阻断正常的登录流程，导致 SDK 抛出 `LoginException`。

**处理建议：**

1. 先在浏览器手动登录，完善个人资料或确认弹窗内容
2. 若弹窗为一次性确认，确认后 SDK 即可正常使用
3. 若每次登录都出现弹窗，请提 [issue](https://github.com/FarmerChillax/new-school-sdk/issues) 并附上弹窗页面截图与教务系统地址

### 报 JSONDecodeError 登录失败？

```text
requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

通常是教务系统返回了非 JSON 响应（如 HTML 错误页或空响应），常见原因：

- **教务系统维护或宕机**：先在浏览器中确认教务系统能正常访问
- **接口路径变更**：教务系统升级后 URL 路径可能发生变化，需通过 `url_endpoints` 更新
- **网络拦截**：防火墙或 CDN 拦截了请求，返回了非预期内容

**排查步骤：**

```python
import requests

# 手动访问教务系统，确认返回状态
resp = requests.get("https://jw.example.edu.cn/xtgl/login_slogin.html")
print(resp.status_code)
print(resp.text[:500])  # 检查返回内容是否正常
```

### URL 路径和默认的不一致（如多了 `/jwglxt/` 前缀）？

不同正方部署的 URL 前缀可能不同（如 `/jwglxt/xtgl/...` 而非 `/xtgl/...`），
可通过 `url_endpoints` 整体覆盖端点表：

```python
from school_sdk.config import URL_ENDPOINT

# 基于默认端点表修改，只需覆盖有差异的部分
url_endpoints = {
    "HOME_URL": "/jwglxt/xtgl/login_slogin.html",
    "INDEX_URL": "/jwglxt/xtgl/index_initMenu.html",
    'LOGIN': {
        'INDEX': '/jwglxt/xtgl/login_slogin.html',
        'CAPTCHA': '/jwglxt/zfcaptchaLogin',
        'KCAPTCHA': '/jwglxt/kaptcha',
        'PUBLIC_KEY': '/jwglxt/xtgl/login_getPublicKey.html',
    },
    "SCORE_URL": "",
    "INFO_URL": "",
    "SCHEDULE": {
        "API": '/jwglxt/kbcx/xskbcx_cxXsKb.html',
    },
    'SCORE': {
        'API': '/jwglxt/cjcx/cjcx_cxDgXscj.html'
    },
    'INFO': {
        'API': '/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html'
    }
}

school = SchoolClient("jw.example.edu.cn", url_endpoints=url_endpoints)
```

!!! tip
    在浏览器打开教务系统，观察地址栏中的路径前缀，或使用浏览器开发者工具的 Network 面板抓包确认。

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
详细用法见[课表接口 - 自定义作息表](../接口方法/get_schedule.md#_2)。

### 接口路径和我们的学校不一致？

不同正方部署的 URL 前缀可能不同，可通过 `url_endpoints` 整体覆盖端点表（抓包获取实际路径）：

```python
from school_sdk.config import URL_ENDPOINT

url_endpoints = dict(URL_ENDPOINT)
url_endpoints["SCHEDULE"] = {"API": "/kbcx/actual_path.html"}

school = SchoolClient("jw.example.edu.cn", url_endpoints=url_endpoints)
```

完整示例见[学校参数](../快速开始/school_args.md)。

## 环境与部署

### 校外访问需要 VPN 怎么办？

部分学校的教务系统仅在校内网络可访问，校外需要通过 VPN。有两种方案：

**方案一：先连 VPN 再运行 SDK（推荐）**

在操作系统层面连接学校 VPN 后，SDK 可正常使用，无需额外配置。

**方案二：为 SDK 设置 HTTP 代理**

如果 VPN 提供了 HTTP 代理地址，可为 SDK 的 Session 配置代理：

```python
school = SchoolClient("jw.vpn.czjtu.edu.cn", ssl=True)
user = school.user_login("account", "password")

# 为已登录的用户 session 设置代理
user._http.proxies = {
    "http": "http://vpn-proxy:port",
    "https": "http://vpn-proxy:port",
}

# 后续请求将通过代理发出
course = user.get_schedule(year=2022, term=1)
```

**方案三：通过环境变量设置代理**

```bash
export HTTP_PROXY=http://vpn-proxy:port
export HTTPS_PROXY=http://vpn-proxy:port
python my_script.py
```

!!! note
    如果学校 VPN 地址与教务系统地址不同（如 `vpn.czjtu.edu.cn` vs `jw.czjtu.edu.cn`），
    `host` 应填写**通过 VPN 后实际访问的教务系统地址**。

### Linux 云服务器安装失败或依赖过大？

在存储空间受限的云服务器上安装时，`pip install school-sdk` 可能因磁盘空间不足而静默失败（无错误提示）。

**排查步骤：**

```bash
# 检查磁盘空间
df -h

# 确认是否安装成功
pip list | grep school-sdk
```

**轻量安装建议：**

SDK 的核心依赖（requests、pyquery、bs4、Pillow、fake-headers）总共约 10-20 MB，非常轻量。
占用空间大的是图形验证码的可选依赖 PyTorch（~700 MB+）。

如果你的学校**不需要图形验证码**（大多数学校属于此情况），直接安装即可：

```bash
pip install school-sdk
```

!!! warning
    不要安装 `school-sdk[kaptcha]`，除非确认你的学校使用图形验证码。
    PyTorch + torchvision 的体积较大，在 500MB 以下存储限制的服务器上可能无法安装。

### 正方教务 V-9.0 等新版本兼容吗？

SDK 基于新版正方教务系统（新正方）开发，兼容大多数部署版本。
如果你不确定学校的正方版本，可以观察登录页面的 URL 特征：

- 登录页包含 `/xtgl/login_slogin.html` → **新版正方**，本 SDK 支持
- 登录页为旧式表单提交 → **旧版正方**，不适用本 SDK

!!! tip
    V-9.0 及更新版本一般均兼容，如遇到具体问题请提 [issue](https://github.com/FarmerChillax/new-school-sdk/issues) 并附上教务系统地址。

### 从旧版本升级后报 AttributeError？

从 v1.6.x 升级到 v1.7.x+ 时，可能遇到类似错误：

```text
AttributeError: 'UserClient' object has no attribute '_http'
AttributeError: 'UserClient' object has no attribute 'score'
```

**原因**：v1.7.x 对内部结构做了重构，旧版本创建的 `UserClient` 实例不兼容新版本代码。

**解决方法**：

1. 升级到最新版本：`pip install --upgrade school-sdk`
2. **重新创建** `UserClient` 实例（不要复用旧进程中的对象）
3. 如果问题持续，尝试清除缓存：`pip cache purge && pip install --force-reinstall school-sdk`

## 扩展相关

### SDK 没有封装我要的接口怎么办？

用 `proxy_request()` 复用已登录会话，自行抓包并实现业务逻辑，详见[其他接口](../接口方法/others.md)。

### 抢课时太多人访问，如何优化？

选课高峰期教务系统响应慢甚至拒绝服务，可尝试以下策略：

```python
# 1. 增大请求超时时间，避免高峰期超时
school = SchoolClient("jw.example.edu.cn", timeout=30)

# 2. 登录后提前预热会话
user = school.user_login("account", "password")
user.get_info()  # 预热，确保后续请求更快

# 3. 选课高峰期，用 proxy_request 直接调用选课接口
#    先用浏览器开发者工具抓包获取选课 API 和参数
import time
while True:
    try:
        resp = user.proxy_request("POST", "/xkcx/xk_cxXkSave.html", data={
            # 选课参数，需自行抓包获取
        })
        result = resp.json()
        if result.get("status") == "success":
            print("选课成功！")
            break
    except Exception as e:
        print(f"请求失败: {e}, 1秒后重试...")
    time.sleep(1)
```

!!! warning
    过于频繁的请求可能触发教务系统风控（封 IP 或强制下线），建议请求间隔不低于 1 秒。

### 更多示例在哪里？

仓库 [examples](https://github.com/FarmerChillax/new-school-sdk/tree/master/examples) 目录提供了 Cookie 登录、验证码配置、代理请求等可运行示例；仍未解决的疑惑欢迎提 [issue](https://github.com/FarmerChillax/new-school-sdk/issues)。
