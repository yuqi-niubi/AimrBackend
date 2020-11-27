# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: work.py
@time: 2020/9/28 11:00
"""

# from rest_framework import serializers
# from aimr_platform.models import WaterModel_Work
#
#
# # 用户数据format方法
# class WaterModel_WorkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WaterModel_Work
#         fields = '__all__'
from typing import Dict, Any
from aimr_platform.models import WaterModel_Work


def WaterModel_WorkSerializer(work: WaterModel_Work) -> Dict[str, Any]:
    return{
        'work_id': work.work_id,
        'work_batch_ym': work.work_batch_ym,
        'work_send_message_title': work.work_send_message_title,
        'work_send_message_date': work.work_send_message_date,
        'work_accept_flag': work.work_accept_flag,
        'work_accept_date': work.work_accept_date,
        'emp_id': work.emp_id,
        'route_id': work.route_id,
    }
