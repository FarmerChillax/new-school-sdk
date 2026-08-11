# -*- coding: utf-8 -*-
'''
    :file: test_info.py
    :brief: Info 模块离线测试: 基于 HTML 快照 fixture 校验个人信息解析与缓存行为
    :usage: pytest tests/test_info.py
'''

import os
import sys
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from school_sdk import SchoolClient, UserClient

FIXTURE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "fixtures", "info_page.html")

EXPECTED_INFO = {
    "student_number": "2018133209",
    "name": "张三",
    "department_name": "计算机与软件学院",
    "class_name": "软件1802班",
    "grade": "2018",
    "graduation_school": "示例中学",
    "major": "软件工程",
    "gender": "男",
}

INFO_API_PATH = "/xsxxxggl/xsgrxxwh_cxXsgrxx.html"


class FakeResponse:
    def __init__(self, content: bytes):
        self.status_code = 200
        self.content = content
        self.text = content.decode("utf-8")


def build_user(html_content: bytes):
    """构造一个网络层被 mock 的 UserClient, 并记录请求次数"""
    counter = {"requests": 0}

    def fake_request(method=None, url=None, **kwargs):
        assert urlparse(url).path == INFO_API_PATH
        counter["requests"] += 1
        return FakeResponse(html_content)

    school = SchoolClient("127.0.0.1", exist_verify=False)
    user = UserClient(school, "2018133209", "pwd")
    user._http.request = fake_request
    return user, counter


def test_parse_info_from_html_snapshot():
    """HTML 快照应能完整解析出 8 个个人信息字段"""
    with open(FIXTURE_PATH, "rb") as f:
        html = f.read()
    user, counter = build_user(html)

    info = user.get_info()
    assert info == EXPECTED_INFO
    assert counter["requests"] == 1


def test_get_info_uses_cache():
    """二次调用应命中缓存, 不再发起请求"""
    with open(FIXTURE_PATH, "rb") as f:
        html = f.read()
    user, counter = build_user(html)

    user.get_info()
    user.get_info()
    assert counter["requests"] == 1


def test_refresh_info_refetches():
    """refresh_info 应丢弃缓存并重新请求"""
    with open(FIXTURE_PATH, "rb") as f:
        html = f.read()
    user, counter = build_user(html)

    user.get_info()
    refreshed = user.refresh_info()
    assert counter["requests"] == 2
    assert refreshed == EXPECTED_INFO


if __name__ == '__main__':
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
