# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: Error.py
@time: 2020/9/08 09:30
"""


# 异常format
def catchError(code, _str):
    ret = dict()
    # 异常code
    ret['code'] = code
    # 异常message
    ret['message'] = _str
    ret['result_data'] = ''
    return ret
