# -*- coding: utf-8 -*-
'''
    :file: test_check_code.py
    :brief: check_code 验证码识别离线测试: 滑块启发式/识别调度器/缺依赖提示, torch 相关用例按需跳过
    :usage: pytest tests/test_check_code.py
'''

import io
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from PIL import Image

from school_sdk.check_code import ZFCaptchaDistinguish
from school_sdk.check_code.type import captcha_func, kaptcha_func

SCAN_HEIGHT = 50


def make_gap_image(width=200, height=100, gap_x=100, band_top=0, band_bottom=None):
    """合成带垂直亮带的灰度图: x > gap_x 的列变亮, 模拟滑块缺口边缘"""
    band_bottom = height if band_bottom is None else band_bottom
    img = Image.new("L", (width, height), 0)
    px = img.load()
    for y in range(band_top, band_bottom):
        for x in range(gap_x + 1, width):
            px[x, y] = 255
    return img


def to_png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_captcha_func_finds_gap():
    """全高亮带应被定位到缺口列"""
    img = make_gap_image(gap_x=100)
    assert captcha_func(img) == (100, 0)


def test_captcha_func_gap_offset_in_y():
    """亮带不从顶部开始时, 应返回亮带起始行"""
    img = make_gap_image(gap_x=80, band_top=10, band_bottom=90)
    assert captcha_func(img) == (80, 10)


def test_captcha_func_no_gap_returns_zero():
    """无缺口的纯色图应返回 (0, 0)"""
    img = Image.new("L", (200, 100), 0)
    assert captcha_func(img) == (0, 0)


def test_captcha_func_short_band_not_matched():
    """亮带高度不足 scan_height 时不应命中"""
    img = make_gap_image(gap_x=100, band_top=0, band_bottom=SCAN_HEIGHT - 1)
    assert captcha_func(img) == (0, 0)


def test_zfcaptcha_distinguish_verify_delegates():
    """verify() 应委托给传入的回调函数"""
    png = to_png_bytes(make_gap_image())
    cap = ZFCaptchaDistinguish(png, verify_func=lambda image: (1, 2))
    assert cap.verify() == (1, 2)


def test_zfcaptcha_distinguish_verify_with_slide():
    """内置滑块扫描应能定位缺口并记录坐标"""
    png = to_png_bytes(make_gap_image(gap_x=100))
    cap = ZFCaptchaDistinguish(png)
    assert cap.verify_with_slide() == (100, 0)
    assert cap.X == 100 and cap.Y == 0


def test_kaptcha_func_missing_torch_hint(monkeypatch):
    """predict 模块不可导入时应提示安装 [kaptcha] extra"""
    monkeypatch.delitem(sys.modules, "school_sdk.check_code.predict", raising=False)
    monkeypatch.setitem(sys.modules, "school_sdk.check_code.predict", None)
    with pytest.raises(ImportError) as ei:
        kaptcha_func(Image.new("RGB", (200, 50)))
    assert "school-sdk[kaptcha]" in str(ei.value)


# ---- 以下用例依赖可选的 torch, 未安装 [kaptcha] 的环境(含 CI 矩阵)自动跳过 ----

def test_dataset_predict_loader_shape():
    pytest.importorskip("torch")
    from school_sdk.check_code.dataset import get_predict_data_loader

    img = Image.new("RGB", (200, 50), (128, 128, 128))
    batch = next(iter(get_predict_data_loader(img)))
    assert tuple(batch.shape) == (1, 1, 50, 200)


def test_cnn_output_shape():
    torch = pytest.importorskip("torch")
    from school_sdk.check_code import captcha_setting
    from school_sdk.check_code.model import CNN

    model = CNN()
    model.eval()
    out = model(torch.rand(1, 1, captcha_setting.IMAGE_HEIGHT, captcha_setting.IMAGE_WIDTH))
    assert tuple(out.shape) == (1, captcha_setting.MAX_CAPTCHA * captcha_setting.ALL_CHAR_SET_LEN)


def test_predict_check_returns_six_chars():
    pytest.importorskip("torch")
    from school_sdk.check_code.captcha_setting import ALL_CHAR_SET
    from school_sdk.check_code.predict import check

    img = Image.new("RGB", (200, 50), (200, 180, 160))
    code = check(img)
    assert isinstance(code, str)
    assert len(code) == 6
    assert all(c in ALL_CHAR_SET for c in code)


if __name__ == '__main__':
    sys.exit(pytest.main([__file__, "-v"]))
