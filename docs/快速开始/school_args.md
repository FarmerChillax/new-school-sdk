# 学校参数

| Option        | Default      | Description              |
| :------------ | :----------- | :----------------------- |
| host          | 不存在默认值 | 教务系统地址(`必填`)     |
| port          | 80           | 端口号                   |
| ssl           | False        | 教务系统是否使用https    |
| name          | None         | 学校名称                 |
| exist_verify  | False        | 是否存在验证码           |
| captcha_type  | captcha      | 验证码类型(常规 或 滑块) |
| retry         | 10           | 登录重试次数             |
| lan_host      | None         | 内网地址                 |
| lan_port      | 80           | 内网地址端口             |
| timeout       | 10           | 全局请求延时             |
| url_endpoints | None         | 地址配置                 |

## 示例

### 使用验证码
```python
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
# 并根据验证码类型指定captcha_type为kap或者cap
# 使用Kaptcha(与旧版系统类似的验证码)
Gdust = SchoolClient("172.16.254.1", exist_verify=True, captcha_type="kaptcha")
# 使用captcha(滑块验证码)
Gdust = SchoolClient("172.16.254.1", exist_verify=True, captcha_type="captcha")
```

### 使用自定义路径
```python
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 通过抓包填写以下路径，如有迷惑或错误烦请提issue并提供地址测试
url_endpoints = {
    'HOME_URL': "/xtgl/login_slogin.html", # 首页url
    'LOGIN': {
        # 该模块表示登录使用到的端点
        'INDEX': '/xtgl/login_slogin.html', # 首页，一般和上面保持一致
        'CAPTCHA': '/zfcaptchaLogin', # 验证码url，貌似都一样
        'PUBLIC_KEY': '/xtgl/login_getPublicKey.html', # RSA密钥端点
    },
    "SCORE_URL": "", # 未使用
    "INFO_URL": "", # 未使用
    # 课表页面的api
    "SCHEDULE": {
        "API": '/kbcx/xskbcx_cxXsKb.html',
    },
    # 成绩页面的api
    'SCORE': {
        'API': '/cjcx/cjcx_cxDgXscj.html'
    }
}

# 使用自定义的endpoints，实例化学校
# exist_verify: 是否有验证码
Gdust = SchoolClient("172.16.254.1", exist_verify=True, url_endpoints=url_endpoints)
```

