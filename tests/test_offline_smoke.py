# -*- coding: utf-8 -*-
'''
    :file: test_offline_smoke.py
    :brief: 离线冒烟测试, 用 mock 响应覆盖课表/成绩/会话等易崩路径, 无需真实教务系统
    :usage: python tests/test_offline_smoke.py  或  pytest tests/test_offline_smoke.py
'''

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from school_sdk import SchoolClient, UserClient
from school_sdk.client.api.schedules import Schedule
from school_sdk.client.exceptions import LoginException

SCHEDULE_JSON = {
    "xsxx": {"BJMC": "18软件本科2班", "XM": "张三"},
    "kbList": [
        {"zcd": "1-16(单)", "xqjmc": "星期一", "jc": "1-2节", "jcs": "1-2",
         "kcmc": "高等数学", "cdmc": "A101", "xqmc": "南城", "xm": "李老师", "xqj": "1"},
        {"zcd": "3,5-8", "xqjmc": "星期三", "jc": "5-6节", "jcs": "5-6",
         "kcmc": "软件工程", "cdmc": "B202", "xqmc": "南城", "xm": "王老师", "xqj": "3"},
    ],
}

SCORE_JSON = {"items": [
    {"kcmc": "高等数学", "kch": "0001", "cj": "88", "xf": "4", "jd": "3.7"},
]}


class FakeResponse():
    """最小可用的 requests.Response 替身"""

    def __init__(self, payload, account="2018133209", logged_in=True) -> None:
        self._payload = payload
        self.status_code = 200
        self.text = f'<input value="{account}">' if logged_in \
            else '<div id="tips">您的会话已失效</div>'
        self.content = self.text.encode()

    def json(self):
        return self._payload


def build_user(payload, logged_in=True) -> UserClient:
    """构造一个跳过登录、网络层被 mock 的 UserClient"""
    school = SchoolClient("127.0.0.1", exist_verify=False)
    # 额外 kwargs 应被 UserClient 接受(SchoolClient.user_login 会透传)
    user = UserClient(school, "2018133209", "pwd", unexpected_kwarg=True)
    user._http.request = lambda *args, **kwargs: FakeResponse(payload, logged_in=logged_in)
    return user


def test_default_schedule():
    """不传 schedule_time 时应使用内置作息表, 且默认请求头已生效"""
    user = build_user(SCHEDULE_JSON)
    assert user._http.headers.get("Content-Type") == "application/x-www-form-urlencoded"

    result = user.get_schedule(year=2022, term=1)
    assert result["class_name"] == "18软件本科2班"
    assert result["username"] == "张三"

    first, second = result["course_list"]
    assert first["course"] == "高等数学"
    assert first["time"] == {"start": [8, 30], "last": [9, 20]}
    # 单周区间与逗号分隔混合表达式
    assert first["weeks_arr"] == [1, 3, 5, 7, 9, 11, 13, 15]
    assert second["weeks_arr"] == [3, 5, 6, 7, 8]


def test_custom_schedule_time():
    """自定义作息表可覆盖内置作息表"""
    user = build_user(SCHEDULE_JSON)
    result = user.get_schedule(year=2022, term=1, schedule_time={
        "1": [9, 0], "2": [10, 0], "5": [14, 0], "6": [15, 0],
    })
    assert result["course_list"][0]["time"] == {"start": [9, 0], "last": [10, 0]}


def test_incomplete_schedule_time():
    """自定义作息表缺节次时应给出可读报错"""
    user = build_user(SCHEDULE_JSON)
    try:
        user.get_schedule(year=2022, term=1, schedule_time={"1": [9, 0], "2": [10, 0]})
    except KeyError as e:
        assert "schedule_time" in str(e)
        return
    raise AssertionError("作息表缺失节次时未报错")


def test_schedule_helper_methods():
    """get_schedule_list / get_raw_schedule / refresh_schedule 可复用已缓存的学年学期"""
    user = build_user(SCHEDULE_JSON)
    user.get_schedule(year=2022, term=1)

    assert len(user.schedule.get_schedule_list()) == 2
    assert user.schedule.get_raw_schedule()["xsxx"]["XM"] == "张三"
    user.schedule.refresh_schedule()
    assert user.schedule.raw_schedule is not None


def test_expired_session_raises_login_exception():
    """会话失效应抛 LoginException 并带上可读信息"""
    user = build_user(SCHEDULE_JSON, logged_in=False)
    try:
        user.get_schedule(year=2022, term=1)
    except LoginException as e:
        assert "session 已失效" in str(e)
        return
    raise AssertionError("会话失效时未抛出 LoginException")


def test_score():
    """成绩解析, 以及 get_score_list 复用已缓存的学年学期"""
    user = build_user(SCORE_JSON)
    result = user.get_score(year=2022, term=1)
    assert result["高等数学"]["exam_result"] == "88"
    assert result["高等数学"]["grade_point"] == "3.7"

    user.score.raw_score = None
    user.score.score_list = []
    assert user.score.get_score_list()[0]["credit"] == "4"


def test_missing_year_raises_value_error():
    """未指定学年时应抛出明确的 ValueError"""
    user = build_user(SCORE_JSON)
    try:
        user.get_score(year=None, term=1)
    except ValueError as e:
        assert "year" in str(e)
        return
    raise AssertionError("缺少学年时未抛出 ValueError")


def test_set_cookies():
    """cookies 字符串支持多键值对, 且值中允许包含 '='"""
    user = build_user({}).get_dev_user("JSESSIONID=abc==; route=node1")
    assert user._http.cookies.get("JSESSIONID") == "abc=="
    assert user._http.cookies.get("route") == "node1"
    assert user._http.headers.get("Content-Type") == "application/x-www-form-urlencoded"


def test_update_headers():
    """BaseCrawler.update_headers 应作用于共享 session"""
    user = build_user(SCHEDULE_JSON)
    Schedule(user).update_headers({"X-Test": "1"})
    assert user._http.headers.get("X-Test") == "1"


def test_cookie_login_entry():
    """cookie 登录入口可透传 account 等参数"""
    user = SchoolClient("127.0.0.1").user_login_with_cookies("JSESSIONID=abc", account="tester")
    assert user.account == "tester"


if __name__ == '__main__':
    failed = 0
    for name, func in sorted(globals().items()):
        if not name.startswith("test_"):
            continue
        try:
            func()
            print(f"PASS  {name}")
        except Exception as e:
            failed += 1
            print(f"FAIL  {name}: {type(e).__name__}: {e}")
    print("\nALL PASS" if not failed else f"\n{failed} case(s) failed")
    sys.exit(1 if failed else 0)
