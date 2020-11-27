# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: Status.py
@time: 2020/8/11 15:00
"""


def status_join(module: str, code: int, result: str) -> dict:
    result_code = {
        "code": module + str(code),
        "message": result,
    }
    return result_code

