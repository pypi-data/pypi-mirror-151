# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'


# 基础异常
class BaseError(Exception):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


# 数据库只读限制异常
class MySQLReadOnlyError(BaseError):
    pass


# 数据库客户端已销毁
class MySQLClientDestroyed(BaseError):
    pass


# 常量设置异常
class ConstError(BaseError):
    pass


# NTP校准异常
class NTPCalibrateError(BaseError):
    pass
