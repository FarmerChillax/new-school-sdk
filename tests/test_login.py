# -*- coding: utf-8 -*-
'''
    :file: test_login.py
    :brief: ZFLogin 登录编排离线测试: mock CSRF 页面/公钥/登录与验证码响应, 覆盖三类登录分支
    :usage: pytest tests/test_login.py
'''

import io
import os
import sys
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image
import pytest

from school_sdk import SchoolClient
from school_sdk.client import UserClient
from school_sdk.client.api import login as login_module
from school_sdk.client.api.login import ZFLogin
from school_sdk.client.exceptions import LoginException, RTKException

ACCOUNT = "2018133209"
PASSWORD = "pwd123"

# 真实正方公钥样例(见 PyRsa/pyrsa.py __main__), 可跑通完整 RSA 加密链路
MODULUS_B64 = ("AKRB6FwmOe0hE9Uo6LMKoDE5U9JU9lH1v8Uv7ATjRj2W+aTPlR9Hfm8fR782pzGwDsTD4Yr7t"
               "BHQ1cuEnGrqrJn5HuPiLqmSg4Z/AwS+Rq8eE7T+ZaGoUtpqvcoSffSJOW29RNVMwT391ona/+eK5"
               "B3RkC9WaJFYiZai7FiQDeXT")
EXPONENT_B64 = "AQAB"

LOGIN_PAGE_HTML = '<html><body><input id="csrftoken" value="csrf-token-123"></body></html>'
SUCCESS_HTML = f'<html><body><input value="{ACCOUNT}"></body></html>'
CRED_FAIL_HTML = '<div id="tips">用户名或密码不正确</div>'
# 注意: 文案不能包含「请」字, 否则 _is_login 会将其误判为已登录页面
CAPTCHA_FAIL_HTML = '<div id="tips">验证码错误, 账号或密码不正确</div>'
CAPTCHA_JS = "var captcha = {tk:'mock-rtk-001', check:function(){}};"


def _tiny_png() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (300, 150), (10, 20, 30)).save(buf, format="PNG")
    return buf.getvalue()


TINY_PNG = _tiny_png()


class FakeResponse:
    """最小可用的 requests.Response 替身"""

    def __init__(self, text="", payload=None, content=None, status_code=200):
        self.status_code = status_code
        self.text = text
        self._payload = payload
        self.content = content if content is not None else text.encode()

    def json(self):
        return self._payload


class LoginEnv:
    """按 URL 路由分发假响应的登录测试环境, 并记录全部请求"""

    def __init__(self, exist_verify=False, captcha_type="captcha", retry=2,
                 login_html=SUCCESS_HTML, captcha_verify_payload=None,
                 captcha_js=CAPTCHA_JS):
        self.state = {
            "login_html": login_html,
            "captcha_verify_payload": captcha_verify_payload or {"status": "success"},
            "captcha_js": captcha_js,
        }
        self.calls = []
        school = SchoolClient("127.0.0.1", exist_verify=exist_verify,
                              captcha_type=captcha_type, retry=retry)
        self.user = UserClient(school, ACCOUNT, PASSWORD)
        self.user._http.request = self._fake_request
        self.login = ZFLogin(user_client=self.user)

    def _fake_request(self, method=None, url=None, **kwargs):
        path = urlparse(url).path
        self.calls.append({"method": method, "path": path,
                           "params": kwargs.get("params"), "data": kwargs.get("data")})
        return self._handle(method, path, kwargs)

    def _handle(self, method, path, kwargs):
        if path == "/xtgl/login_slogin.html":
            if method == "GET":
                return FakeResponse(text=LOGIN_PAGE_HTML)
            return FakeResponse(text=self.state["login_html"])
        if path == "/xtgl/login_getPublicKey.html":
            return FakeResponse(payload={"modulus": MODULUS_B64, "exponent": EXPONENT_B64})
        if path == "/zfcaptchaLogin":
            if method == "POST":
                return FakeResponse(payload=self.state["captcha_verify_payload"])
            ptype = (kwargs.get("params") or {}).get("type")
            if ptype == "resource":
                return FakeResponse(text=self.state["captcha_js"])
            if ptype == "refresh":
                return FakeResponse(payload={"imtk": "imtk-1", "si": "si-1"})
            if ptype == "image":
                return FakeResponse(content=TINY_PNG)
        if path == "/kaptcha":
            return FakeResponse(content=TINY_PNG)
        raise AssertionError(f"unexpected request: {method} {path}")

    def posts(self, path):
        return [c for c in self.calls if c["method"] == "POST" and c["path"] == path]


def test_get_raw_csrf_and_cookie():
    """登录页应能解析出 csrf token"""
    env = LoginEnv()
    env.login.get_raw_csrf_and_cookie()
    assert env.login._csrf == "csrf-token-123"


def test_get_rsa_publick_key():
    """公钥接口返回的 modulus/exponent 应原样透传"""
    env = LoginEnv()
    modulus, exponent = env.login.get_rsa_publick_key()
    assert modulus == MODULUS_B64
    assert exponent == EXPONENT_B64


def test_post_login_success_without_captcha():
    """无验证码登录: 走通 RSA 加密并成功提交"""
    env = LoginEnv(exist_verify=False)
    assert env.login.get_login() is True

    login_posts = env.posts("/xtgl/login_slogin.html")
    assert len(login_posts) == 1
    data = login_posts[0]["data"]
    assert data["csrftoken"] == "csrf-token-123"
    assert data["yhm"] == ACCOUNT
    # mm 为 RSA 加密后的 base64 密文, 每次随机填充但不应为空
    assert data["mm"] and data["mm"] != PASSWORD


def test_user_client_login_entry():
    """UserClient.login 成功后应返回用户自身"""
    env = LoginEnv(exist_verify=False)
    assert env.user.login() is env.user


def test_is_login_branches():
    """_is_login 的四种判定分支"""
    env = LoginEnv()
    assert env.login._is_login(f'<input value="{ACCOUNT}">') is True
    assert env.login._is_login('<div>请选择学期</div>') is True
    assert env.login._is_login(CAPTCHA_FAIL_HTML) is False
    with pytest.raises(LoginException) as ei:
        env.login._is_login(CRED_FAIL_HTML)
    assert "用户名或密码不正确" in str(ei.value)


def test_login_failure_with_server_error_msg():
    """服务端返回明确错误时应抛出带原文案的 LoginException"""
    env = LoginEnv(exist_verify=False, login_html=CRED_FAIL_HTML)
    with pytest.raises(LoginException) as ei:
        env.login.get_login()
    assert "用户名或密码不正确" in str(ei.value)


def test_login_failure_with_captcha_hint():
    """验证码类提示不算致命错误, 但最终应落到 '登录失败'"""
    env = LoginEnv(exist_verify=False, login_html=CAPTCHA_FAIL_HTML)
    with pytest.raises(LoginException) as ei:
        env.login.get_login()
    assert "登录失败" in str(ei.value)


def test_slider_login_success(monkeypatch):
    """滑块验证码分支: 取 rtk/图片 -> 识别 -> 校验通过后登录"""
    monkeypatch.setattr(login_module, "captcha_func", lambda image: (120, 30))
    env = LoginEnv(exist_verify=True, captcha_type="captcha")
    assert env.login.get_login() is True

    # 验证 POST 应携带 rtk 且类型为 verify
    verify_posts = env.posts("/zfcaptchaLogin")
    assert len(verify_posts) == 1
    assert verify_posts[0]["data"]["rtk"] == "mock-rtk-001"
    assert verify_posts[0]["data"]["type"] == "verify"
    # 最终仍要提交账密登录
    assert len(env.posts("/xtgl/login_slogin.html")) == 1


def test_slider_verify_failed_then_login_failed():
    """滑块校验失败且账密登录也被拒时应抛 '滑块登录失败'"""
    env = LoginEnv(exist_verify=True, captcha_type="captcha",
                   login_html=CAPTCHA_FAIL_HTML,
                   captcha_verify_payload={"status": "failed"})
    with pytest.raises(LoginException) as ei:
        env.login.get_login()
    assert "滑块登录失败" in str(ei.value)


def test_get_rtk_parse_error():
    """captcha js 中缺少 tk 时应抛 RTKException"""
    env = LoginEnv(exist_verify=True, captcha_type="captcha",
                   captcha_js="var captcha = {};")
    with pytest.raises(RTKException):
        env.login._get_rtk()


def test_get_track_reaches_distance():
    """模拟轨迹应单调前进并到达目标距离, Y 轴保持不变"""
    env = LoginEnv()
    track = env.login._get_track(100, 25)
    assert len(track) > 1
    xs = [point["x"] for point in track]
    assert xs == sorted(xs)
    assert all(point["y"] == 25 for point in track)
    assert xs[-1] >= 1200 + 100


def test_kaptcha_login_success(monkeypatch):
    """图形验证码分支: 识别结果应随 yzm 字段提交"""
    monkeypatch.setattr(login_module, "kaptcha_func", lambda image: "abc123")
    env = LoginEnv(exist_verify=True, captcha_type="kaptcha")
    assert env.login.get_login() is True

    login_posts = env.posts("/xtgl/login_slogin.html")
    assert len(login_posts) == 1
    assert login_posts[0]["data"]["yzm"] == "abc123"


def test_kaptcha_retry_exhausted(monkeypatch):
    """识别持续失败时按 retry 次数重试后抛出 '验证码登录失败'"""
    monkeypatch.setattr(login_module, "kaptcha_func", lambda image: "wrong!")
    env = LoginEnv(exist_verify=True, captcha_type="kaptcha",
                   retry=2, login_html=CAPTCHA_FAIL_HTML)
    with pytest.raises(LoginException) as ei:
        env.login.get_login()
    assert "验证码登录失败" in str(ei.value)
    assert len(env.posts("/xtgl/login_slogin.html")) == 2


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, "-v"]))
