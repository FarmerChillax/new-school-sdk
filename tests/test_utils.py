# -*- coding: utf-8 -*-
'''
    :file: test_utils.py
    :brief: school_sdk/utils.py 工具方法离线测试: ObjectDict 属性式访问与 is_endpoint 端点判断
    :usage: pytest tests/test_utils.py
'''

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from school_sdk.utils import ObjectDict, is_endpoint


def test_objectdict_attr_read_hit():
    """已存在的键应支持属性式读取"""
    obj = ObjectDict(a=1)
    assert obj["a"] == 1
    assert obj.a == 1


def test_objectdict_attr_read_missing_returns_none():
    """访问不存在的属性应返回 None 而非抛 AttributeError"""
    obj = ObjectDict(a=1)
    assert obj.not_exist is None


def test_objectdict_attr_write():
    """属性赋值应写入底层字典"""
    obj = ObjectDict()
    obj.b = 2
    assert obj["b"] == 2
    assert obj.b == 2


def test_objectdict_dict_semantics():
    """常规字典语义不受影响"""
    obj = ObjectDict()
    obj["key"] = "value"
    assert "key" in obj
    assert "missing" not in obj
    assert len(obj) == 1


def test_objectdict_getstate_returns_none():
    """__getstate__ 按设计返回 None, 不向 pickle 提供序列化状态"""
    obj = ObjectDict(a=1)
    assert obj.__getstate__() is None


def test_is_endpoint_full_url():
    """完整 URL 不是端点"""
    assert is_endpoint("http://jw.example.edu.cn/xtgl/login_slogin.html") is False
    assert is_endpoint("https://jw.example.edu.cn/xtgl/login_slogin.html") is False


def test_is_endpoint_relative_path():
    """相对路径视为端点"""
    assert is_endpoint("/xtgl/login_slogin.html") is True
    assert is_endpoint("xtgl/login_slogin.html") is True


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, "-v"]))
