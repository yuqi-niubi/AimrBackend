# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: meter_typetype.py
@time: 2020/10/19 16:30
"""


from rest_framework import serializers
from aimr_platform.models import WaterModel_MeterType
from typing import Dict, Any

# 水表信息format方法
# class WaterModel_MeterTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WaterModel_meter_typeType
#         fields = '__all__'


def WaterModel_MeterTypeSerializer(meter_type: WaterModel_MeterType) -> Dict[str, Any]:
    return {
        'id': meter_type.id,
        'meter_type_id': meter_type.meter_type_id,
        'meter_caliber': meter_type.meter_caliber,
    }

