# -*- coding: utf-8 -*-
'''
    :file: __init__.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/02 22:19:19
'''

# from school_sdk.client.api.login_manage import LoginManagement
# from school_sdk.client.settings import HOST
import requests
from fake_headers import Headers
import time

class BaseCrawler():

    BASE_URL = ''
    TERM = {1: 3, 2: 12, 3: 16}
    def __init__(self, user_client) -> None:
        self.user_client = user_client
        self.school = user_client.school or None
        self._http:requests.Session = user_client._http or requests.Session()
        self.t = int(time.time() * 1000)
        self.BASE_URL = user_client.school.base_url

    @property
    def account(self):
        return self.user_client.account

    def generate_headers(self, **kwargs):
        headers = Headers(browser="chrome", os="win", headers=True).generate()
        return headers

    def _requests(self, method: str, url_or_endpoint: str, **kwargs) -> requests.Response:
        if not url_or_endpoint.startswith(('http://', 'https://')):
            url = f'{self.BASE_URL}{url_or_endpoint}'
        else:
            url = url_or_endpoint
        res = self._http.request(method=method, url=url, **kwargs)
        return res

    def get(self, url, **kwargs) -> requests.Response:
        return self._requests(method='GET', url_or_endpoint=url, **kwargs)

    def post(self, url, **kwargs) -> requests.Response:
        return self._requests(method='POST', url_or_endpoint=url, **kwargs)

    def update_headers(self, headers: dict):
        self._client.headers.update(headers)
