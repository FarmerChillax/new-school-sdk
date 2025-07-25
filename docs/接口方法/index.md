# 概览


| Api                                        | Description                                                     | Argument          |
| :----------------------------------------- | :-------------------------------------------------------------- | :---------------- |
| [user_login](./user_login.md)              | 登陆函数                                                        | account, password |
| [user_login_with_cookies](./user_login.md) | cookie 登陆函数                                                 | cookies, account  |
| [init_dev_user](./user_login.md)           | 开发测试函数，主要用于开发者调试使用，传入 cookie，无需频繁登录          | cookies           |
| [get_schedule](./get_schedule.md)          | 课表查询                                                        | year, term        |
| [get_score](./get_score.md)                | 成绩查询                                                        | year, term        |
| [get_info](./get_info.md)                  | 获取个人信息                                                    | None              |
| [refresh_info](./others.md)                | 刷新个人信息                                                    | None              |
| [check_session](./others.md)               | 检查session并其失效后重登录                                     | None              |
| [proxy_request](./others.md)               | 补充 sdk 未实现的业务功能，以支持各种登录后的教务系统操作             | method, url_or_endpoint, **kwargs   |

