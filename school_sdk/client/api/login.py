# -*- coding: utf-8 -*-
'''
    :file: login.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/02 22:12:00
'''
from school_sdk.client.exceptions import LoginException, RTKException
from school_sdk.check_code import ZFCaptchaDistinguish
from school_sdk.client.api import BaseCrawler

from school_sdk.PyRsa import RsaKey
from pyquery import PyQuery as pq
import time
import re
import json
import base64

class ZFLogin(BaseCrawler):

    LOGIN_EXTEND = b'{"appName":"Netscape","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36","appVersion":"5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}'

    def get_login(self, **kwargs):
        self.get_raw_csrf_and_cookie()
        self.get_rsa_publick_key()
        for _ in range(3):
            if self.verification_captcha():
                break
        if not self._post_login():
            raise LoginException("xxx", "登录失败")
        

    def __init__(self, school, account, password, session=None) -> None:
        super().__init__(school, session)
        self.account = account
        self.password = password
        self._csrf = None
        self.t = int(time.time() * 1000)
        self._image = None
        self.path = self.school.config["url_endpoints"]['LOGIN']

    def get_raw_csrf_and_cookie(self):
        """获取CSRF令牌
        """
        url = self.path['INDEX']
        res = self.get(url)
        doc = pq(res.text)
        csrf = doc("#csrftoken").attr("value")
        self._csrf = csrf

    def get_rsa_publick_key(self):
        """获取RSA公钥信息

        Returns:
            str: return RSA moduls and exponent
        """
        url = self.path["PUBLIC_KEY"]
        params = {"time": self.t, "_": self.t}
        headers = self.generate_headers()
        # headers.setdefault("X-Requested-With", "XMLHttpRequest")
        res = self.get(url=url, params=params, headers=headers)
        result_json = res.json()
        return result_json.get("modulus"), result_json.get('exponent')

    def verification_captcha(self) -> bool:
        """滑块验证
            1. 获取图片
            2. 获取验证偏移量
            3. 发起验证请求
        """
        rtk = self._get_rtk()
        self._image = self._get_captcha_image()
        cap = ZFCaptchaDistinguish(self._image)
        x, y = cap.verify()
        track = self._get_track(x, y)
        captcha_verify_result = json.dumps(track).encode('utf-8')
        url = self.path["CAPTCHA"]
        data = {
            "instanceId": "zfcaptchaLogin",
            "rtk": rtk,
            "time": int(time.time() * 1000),
            "mt": base64.b64encode(captcha_verify_result),
            "extend": base64.b64encode(self.LOGIN_EXTEND),
            "type": "verify"
        }
        res = self.post(url=url, data=data)
        if res.status_code == 200 and res.json().get("status") == "success":
            return True
        return False

    def _post_login(self) -> bool:
        rsa_key = RsaKey()
        m, e = self.get_rsa_publick_key()
        rsa_key.set_public(self._b64.b64tohex(m), self._b64.b64tohex(e))
        rr = rsa_key.rsa_encrypt(self.password)
        data = {
            'csrftoken': self._csrf,
            'yhm': self.account,
            'mm': self._b64.hex2b64(rr)
        }
        params = {"time": self.t}
        url =  self.path['INDEX']
        res = self.post(url, params=params, data=data)
        return self._is_login(res.text)


    def _is_login(self, html) -> bool:
        re_str = f'value="{self.account}"'
        result = re.search(re_str, html)
        return True if result else False

    def _get_captcha_image(self):
        """获取验证码
        1. 获取rtk、si、imtk等信息
        2. 下载图片
        """
        params = {
            "type": "refresh",
            "time": {self.t},
            "instanceId": "zfcaptchaLogin"
        }
        url = self.path["CAPTCHA"]
        res = self.get(url, params=params)
        captcha_data = res.json()
        params.update({
            "type": "image",
            "imtk": captcha_data.get("imtk"),
            "id": captcha_data.get("si")
        })
        url = self.path["CAPTCHA"]
        res = self.get(url=url, params=params)
        if res.status_code == 200:
            return res.content

    def _get_rtk(self) -> str:
        """获取rtk
        从JavaScript文件中提前rtk
        """
        url = self.path['CAPTCHA']
        params = {
            "type": "resource",
            "instanceId": "zfcaptchaLogin",
            "name": "zfdun_captcha.js"
        }
        res = self.get(url, params=params)
        result = re.search("tk:'(.*)',", res.text)
        try:
            return result.group(1)
        except:
            raise RTKException("rtk解析错误")

    def _get_track(self, distance, y) -> list:
        """模拟人手滑动
        通过设置前快后慢的加速度，模拟人手滑动

        Args:
            distance ([int]): [移动距离]
            y ([int]): [滑块Y值]

        Returns:
            [list]: [坐标数组]
        """
        start = 1200
        current = 0
        track = []
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0
        while current < distance:
            # 加速->加速度为 2; 减速->加速度为-3
            a = 2 if current < mid else -3
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            # 移动距离 x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移量
            current += move
            # 加入轨迹
            track.append({"x": start + int(current), "y": y,
                         "t": int(time.time() * 1000)})
            time.sleep(0.01)
        return track



