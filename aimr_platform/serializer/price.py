# encoding: utf-8
"""
@author: hanjq
@software: PyCharm
@file: price.py
@time: 2020/9/28 16:00
"""


from rest_framework import serializers
from aimr_platform.models import WaterMaster_Price_General
from aimr_platform.models import WaterMaster_Price_Sewage
from typing import Dict, Any

# 一般水价数据格式化方法
# class WaterModel_GeneralSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WaterMaster_Price_General
#         fields = '__all__'


def WaterModel_GeneralSerializer(price_general: WaterMaster_Price_General) -> Dict[str, Any]:
    return{
        'id': price_general.id,
        'meter_base_size': price_general.meter_base_size,
        'meter_base_price': price_general.meter_base_price,
        'onetothree': price_general.onetothree,
        'sixtoten': price_general.sixtoten,
        'eletotwenty': price_general.eletotwenty,
        'twonetothirty': price_general.twonetothirty,
        'thonetofifty': price_general.thonetofifty,
        'fifonetohun': price_general.fifonetohun,
        'hunonetotwohun': price_general.hunonetotwohun,
        'twohunonetohus': price_general.twohunonetohus,
        'husoneabove': price_general.husoneabove,
        'meter_usetype': price_general.meter_usetype,
    }


#
# # 污水水价数据格式化方法
# class WaterModel_SewageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WaterMaster_Price_Sewage
#         fields = '__all__'


def WaterModel_SewageSerializer(price_sewage: WaterMaster_Price_Sewage) -> Dict[str, Any]:
    return{
        'id': price_sewage.id,
        'otoeight': price_sewage.otoeight,
        'ninetotwenty': price_sewage.ninetotwenty,
        'twonetofifty': price_sewage.twonetofifty,
        'fifonetohun': price_sewage.fifonetohun,
        'hunonetotwohun': price_sewage.hunonetotwohun,
        'twohunonetofihun': price_sewage.twohunonetofihun,
        'fihunonetohus': price_sewage.fihunonetohus,
        'husoneabove': price_sewage.husoneabove,
        'meter_usetype': price_sewage.meter_usetype,
    }