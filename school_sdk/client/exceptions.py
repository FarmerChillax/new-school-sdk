# -*- coding: utf-8 -*-
'''
    :file: exceptions.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/02 23:49:32
'''

class SchoolException(Exception):
    """Base exception for school-api"""

    def __init__(self, name, school_code, errmsg):
        self.name = name
        self.errmsg = errmsg
        self.school_code = school_code

    def __str__(self):
        msg = f'{self.errmsg}'
        return msg

class LoginException(SchoolException):

    def __init__(self, school_code, errmsg):
        super(LoginException, self).__init__('登录错误', school_code, errmsg)


class RTKException(ValueError):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)