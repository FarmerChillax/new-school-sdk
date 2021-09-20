# -*- coding: utf-8 -*-
'''
    :file: __init__.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/02 22:20:52
'''

from school_sdk.client.api.score import Score
from school_sdk.config import URL_ENDPOINT
from school_sdk.client.api.schedules import Schedule
from school_sdk.client.exceptions import LoginException
import time
from school_sdk.client.api.login import ZFLogin
from school_sdk.client.base import BaseSchoolClient


class SchoolClient():

    def __init__(self, host, port:int=80, ssl:bool=False, name=None, exist_verify:bool=False,
                lan_host=None, lan_port=80, timeout=10,
                login_url_path=None, url_endpoints=None) -> None:
        """初始化学校配置

        Args:
            host (str): 主机地址
            port (int, optional): 端口号. Defaults to 80.
            ssl (bool, optional): 是否启用HTTPS. Defaults to False.
            name (str, optional): 学校名称. Defaults to None.
            exist_verify (bool, optional): 是否有验证码. Defaults to False.
            lan_host (str, optional): 内网主机地址. Defaults to None.
            lan_port (int, optional): 内网主机端口号. Defaults to 80.
            timeout (int, optional): 请求超时时间. Defaults to 10.
            login_url_path ([type], optional): 登录地址. Defaults to None.
            url_endpoints ([dict], optional): 地址列表. Defaults to None.
        """
        school = {
            "name": name,
            "exist_verify": exist_verify,
            "lan_host": lan_host,
            "lan_port": lan_port,
            "timeout": timeout,
            "login_url_path": login_url_path,
            "url_endpoints": url_endpoints or URL_ENDPOINT
        }

        self.base_url = f'https://{host}:{port}' if ssl else f'http://{host}:{port}'
        self.config = school
    
    def user_login(self, account:str, password:str, **kwargs):
        """用户登录

        Args:
            account (str): 用户账号
            password (str): 用户密码
        """
        user = UserClient(self, account=account, password=password, **kwargs)
        return user.login()


class UserClient(BaseSchoolClient):
    schedule:Schedule = None
    score: Score = None
    def __init__(self, school, account, password) -> None:
        """初始化用户类
        用户类继承自学校

        Args:
            school (SchoolClient): 学校实例
            account (str): 账号
            password (str): 密码
        """
        self.account = account
        self.password = password
        self.school = school
        self._csrf = None
        self.t = int(time.time())
        self._image = None

    def login(self):
        """用户登录，通过SchoolClient调用
        """
        user = ZFLogin(user_client=self)
        user.get_raw_csrf_and_cookie()
        user.get_rsa_publick_key()
        try:
            user.get_login()
            self._http = user._http
            return self
        except LoginException as login_err:
            print(login_err)

    def init_schedule(self):
        if self.schedule is None:
            self.schedule = Schedule(self)

    def get_schedule(self, **kwargs):
        if self.schedule is None:
            self.schedule = Schedule(self)
        return self.schedule.get_schedule_dict(**kwargs)
    
    def get_score(self, **kwargs):
        if self.score is None:
            self.score = Score(self)
        return self.score.get_score()