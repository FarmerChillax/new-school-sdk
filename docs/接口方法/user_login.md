# 用户登录

| 字段       | 默认值  | 类型     | 描述   |
| -------- | ---- | ------ | ---- |
| account  | None | String | 用户账号 |
| password | None | String | 用户密码 |

## 示例
```python
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
Gdust = SchoolClient("172.16.254.1")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")
```

## 图形验证码登录

如果需要以「图形验证码」的方式登录，则需要在初始化 SchoolClient 时设置 exist_verify 参数的值为 true （开启验证码登录）
与 captcha_type 参数的值设为 kaptcha （登录验证码类型为图形验证码）

```python
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
# 使用 kaptcha (与旧版系统类似的验证码)
Gdust = SchoolClient("172.16.254.1", exist_verify=True, captcha_type="kaptcha")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")

# 获取个人信息
info = user.get_info()
print(info)
```

## 滑块验证码登录

与「图形验证码」的差异点在于“初始化 SchoolClient 时 captcha_type 参数的值为 captcha”

```python
from school_sdk.client import UserClient
from school_sdk import SchoolClient

# 实例化学校
# 使用captcha(滑块验证码)
Gdust = SchoolClient("172.16.254.1", exist_verify=True, captcha_type="captcha")

# 实例化用户
user:UserClient = Gdust.user_login("account", "password")

# 获取个人信息
info = user.get_info()
print(info)
```


## 其他登录方式
更多登录 demo 详见仓库 [examples](https://github.com/FarmerChillax/new-school-sdk/tree/master/examples) 目录
