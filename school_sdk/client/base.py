# -*- coding: utf-8 -*-
'''
    :file: base.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/08 00:17:24
'''
from school_sdk.utils import is_endpoint
import requests
from fake_headers import Headers


class BaseUserClient():
    BASE_URL = ""
    _http = None

    def __init__(self) -> None:
        self._http = requests.Session()
        self._http.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.89 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        })

    def _generate_headers(self, **kwargs):
        headers = Headers(browser="chrome", os="win", headers=True).generate()
        return headers
    
    def _request(self, method, url_or_endpoint, **kwargs) -> requests.models.Response:
        if is_endpoint(url_or_endpoint=url_or_endpoint):
            url = f'{self.BASE_URL}{url_or_endpoint}'
        else:
            url = url_or_endpoint
        res = self._http.request(
            method=method,
            url = url,
            **kwargs
        )
        return res
    
    def get(self, url, **kwargs):
        return self._request(method='GET', url_or_endpoint=url, **kwargs)
    
    def post(self, url, **kwargs):
        return self._request(method='POST', url_or_endpoint=url, **kwargs)

    def _update_headers(self, headers_dict):
        self._http.headers.update(headers_dict)
    

