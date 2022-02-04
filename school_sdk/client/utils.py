# -*- coding: utf-8 -*-
'''
    :file: utils.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2022/02/04 01:39:51
'''
import re
from pyquery import PyQuery as pq
from school_sdk.client.exceptions import LoginException

def user_is_login(account, html) -> bool:
    """工具函数，判断是否登录成功

    Args:
        account (str): 教务系统账号.
        html (str): html string.

    Raises:
        LoginException: 教务系统错误信息

    Returns:
        bool: html string 是否存在用户
    """

    re_str = f'value="{account}"'
    result = re.search(re_str, html)
    if result:
        return True
    doc = pq(html)
    err_msg = doc('#tips').text()
    if err_msg == "":
        return True
    # 错误流程
    if '验证码' in err_msg:
        return False
    raise LoginException(400, err_msg)