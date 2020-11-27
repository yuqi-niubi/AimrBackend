# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: meter.py
@time: 2020/9/28 11:00
"""


from rest_framework import serializers
from aimr_platform.models import WaterModel_Meter
from typing import Dict, Any

# 水表信息format方法
# class WaterModel_MeterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WaterModel_Meter
#         fields = '__all__'


def WaterModel_MeterSerializer(meter: WaterModel_Meter) -> Dict[str, Any]:
    return{
        'meter_id': meter.meter_id,
        'meter_customer_no': meter.meter_customer_no,
        'meter_no': meter.meter_no,
        'meter_qr_code': meter.meter_qr_code,
        'unusual_status': meter.unusual_status,
        'img_position': meter.img_position,
        'meter_customer_name': meter.meter_customer_name,
        'meter_customer_address': meter.meter_customer_address,
        'meter_customer_tel': meter.meter_customer_tel,
        'meter_type': meter.meter_type,
        'meter_use_during_from': meter.meter_use_during_from,
        'meter_use_during_to': meter.meter_use_during_to,
        'routelist_id': meter.routelist_id,
    }
