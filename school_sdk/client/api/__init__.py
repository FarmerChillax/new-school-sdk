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
from school_sdk.PyRsa.pyb64 import Base64


class BaseCrawler():

    BASE_URL = ''

    # def __init__(self, school, session: requests.Session) -> None:
    def __init__(self, user_client) -> None:
        print(user_client)
        self.user_client = user_client
        self.school = user_client.school or None
        self._http:requests.Session = user_client._http or requests.Session()
        self._b64 = Base64()
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
