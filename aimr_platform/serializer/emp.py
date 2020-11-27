# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: emp.py
@time: 2020/9/28 11:00
"""


from rest_framework import serializers
from aimr_platform.models import WaterModel_Emp
from typing import Dict, Any

# 用户数据format方法
# class WaterModel_EmpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WaterModel_Emp
#         fields = '__all__'


def WaterModel_EmpSerializer(emp: WaterModel_Emp) -> Dict[str, Any]:
    return{
        'emp_id': emp.emp_id,
        'emp_name': emp.emp_name,
        'emp_code': emp.emp_code,
        'emp_img_name': emp.emp_img_name,
        'emp_email': emp.emp_email,
        'emp_tel': emp.emp_tel,
        'emp_role': emp.emp_role,
        'emp_token': emp.emp_token,
        'login_time': emp.login_time,
        'last_login_time': emp.last_login_time,
    }

