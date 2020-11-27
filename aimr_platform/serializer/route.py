# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: route.py
@time: 2020/9/28 11:00
"""


from rest_framework import serializers
from aimr_platform.models import WaterModel_Route
from typing import Dict, Any

# # 用户数据format方法
# class WaterModel_RouteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WaterModel_Route
#         fields = '__all__'


def WaterModel_RouteSerializer(route: WaterModel_Route) -> Dict[str, Any]:
    return {
        'route_id': route.route_id,
        'route_name': route.route_name,
        'datum_date': route.datum_date,
        'parity_distinction': route.parity_distinction,
        'emp_id': route.emp_id,
    }
