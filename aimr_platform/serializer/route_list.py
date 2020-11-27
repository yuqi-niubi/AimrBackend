# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: route_list.py
@time: 2020/9/28 11:00
"""


from rest_framework import serializers
from aimr_platform.models import WaterModel_RouteList
from typing import Dict, Any

# # 用户数据format方法
# class WaterModel_RouteListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WaterModel_RouteList
#         fields = '__all__'
# 
# 


def WaterModel_RouteListSerializer(routelist: WaterModel_RouteList) -> Dict[str, Any]:
    return {
        'routelist_id': routelist.routelist_id,
        'res_name': routelist.res_name,
        'position': routelist.position,
        'meter_count': routelist.meter_count,
        'x_position': routelist.x_position,
        'y_position': routelist.y_position,
        'task_smooth': routelist.task_smooth,
        'route_id': routelist.route_id,
    }