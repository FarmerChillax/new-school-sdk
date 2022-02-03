# -*- coding: utf-8 -*-
'''
    :file: config.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/04 23:39:20
'''

# INDEX http://192.168.2.123:7899/xtgl/index_initMenu.html?jsdm=xs&_t=1643879775142

URL_ENDPOINT = {
    "HOME_URL": "/xtgl/login_slogin.html",
    "INDEX_URL": "/xtgl/index_initMenu.html",
    'LOGIN': {
        'INDEX': '/xtgl/login_slogin.html',
        'CAPTCHA': '/zfcaptchaLogin',
        'KCAPTCHA': '/kaptcha',
        'PUBLIC_KEY': '/xtgl/login_getPublicKey.html',
    },
    "SCORE_URL": "",
    "INFO_URL": "",
    "SCHEDULE": {
        "API": '/kbcx/xskbcx_cxXsKb.html',
    },
    'SCORE': {
        'API': '/cjcx/cjcx_cxDgXscj.html'
    },
    'INFO': {
        'API': '/xsxxxggl/xsgrxxwh_cxXsgrxx.html'
    }
}
