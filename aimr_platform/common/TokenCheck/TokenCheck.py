# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: TokenCheck.py
@time: 2020/9/08 09:30
"""
import base64
import json
from datetime import datetime
from aimr_platform.models import WaterModel_Emp


# 验证token
def token_check(token):

    header, payload, old_signature = token.rsplit('.')
    message = str(base64.b64decode(payload))
    emp_id = json.loads(message.replace('b\'', '').replace('\'', '')).get('user_id')
    emp = WaterModel_Emp.objects.get(emp_id=emp_id)
    # emp = {}
    if datetime.now() <= emp.token_expired_time:
        if token == emp.token:
            obj = True
        else:
            obj = False
    else:
        obj = False
    return obj

