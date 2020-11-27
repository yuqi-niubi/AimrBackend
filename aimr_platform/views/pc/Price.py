# encoding: utf-8
"""
@author: hanjq
@software: PyCharm
@file: price.py
@time: 2020/9/28 16:30
"""
from datetime import datetime

from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_platform.common.Error import Error
from aimr_platform.models import WaterMaster_Price_General
from aimr_platform.models import WaterMaster_Price_Sewage
from django.db import transaction
from aimr_platform.serializer.price import WaterModel_GeneralSerializer, WaterModel_SewageSerializer
from aimr_backend.settings import pro_logger, err_logger
from aimr_platform.status import Pc_status


# 水道料金設定
class PriceAPI(APIView):
    # 获取水道料金設定
    def get(self, request):
        """
            获取水道料金設定
            :param request:
            :return:
        """
        try:
            pro_logger.info('一般用水料金取得')
            general = []
            sewage = []
            # 一般用水料金取得
            general_lists = WaterMaster_Price_General.objects.filter()
            # 污水料金取得
            pro_logger.info('污水料金取得')
            sewage_lists = WaterMaster_Price_Sewage.objects.filter()
            for general_list in general_lists:
                general.append(WaterModel_GeneralSerializer(general_list))
            for sewage_list in sewage_lists:
                sewage.append(WaterModel_SewageSerializer(sewage_list))
            # 返回状态及数据
            ret = Pc_status.get_price_success
            ret['result_data'] = {
                'general_list': general,
                'sewage_list': sewage,
            }
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    # 設定水道料金
    def put(self, request):
        """
            設定水道料金
            :param request:
            :return:
        """
        try:
            with transaction.atomic():
                # token暂时不用
                # token = request.META.get("HTTP_AUTHORIZATION")
                # obj = TokenCheck.token_check(TokenCheck, token)
                obj = True
                if obj:
                    # 一般料金取得
                    general_list_update = request.data['general_list']
                    # 更新对应数据库的值
                    pro_logger.info('一般料金更新开始')
                    # 循环前台数据并更新
                    for i in range(0, len(general_list_update)):
                        # 取得数据库中对应数据然后进行更新
                        general = WaterMaster_Price_General.objects.get(id=general_list_update[i].get('id'))
                        # 基本水价
                        general.meter_base_price = general_list_update[i].get('meter_base_price')
                        # 1m³~5m³
                        general.onetothree = general_list_update[i].get('onetothree')
                        # 6m³~10m³
                        general.sixtoten = general_list_update[i].get('sixtoten')
                        # 11m³~20m³
                        general.eletotwenty = general_list_update[i].get('eletotwenty')
                        # 21m³~30m³
                        general.twonetothirty = general_list_update[i].get('twonetothirty')
                        # 31m³~50m³
                        general.thonetofifty = general_list_update[i].get('thonetofifty')
                        # 51m³~100m³
                        general.fifonetohun = general_list_update[i].get('fifonetohun')
                        # 101m³~200m³
                        general.hunonetotwohun = general_list_update[i].get('hunonetotwohun')
                        # 201m³~1000m³
                        general.twohunonetohus = general_list_update[i].get('twohunonetohus')
                        # 1001m³以上
                        general.husoneabove = general_list_update[i].get('husoneabove')
                        # 保存到数据库
                        general.save()
                    pro_logger.info('一般料金更新结束')

                    # 污水料金取得
                    sewage_list_update = request.data['sewage_list']
                    # 循环前台数据并更新
                    pro_logger.info('污水料金更新开始')
                    for i in range(0, len(sewage_list_update)):
                        # 取得数据库中对应数据然后进行更新
                        sewage = WaterMaster_Price_Sewage.objects.get(id=sewage_list_update[i].get('id'))
                        # 0m³~8m³
                        sewage.otoeight = sewage_list_update[i].get('otoeight')
                        # 9m³~20m³
                        sewage.ninetotwenty = sewage_list_update[i].get('ninetotwenty')
                        # 21m³~50m³
                        sewage.twonetofifty = sewage_list_update[i].get('twonetofifty')
                        # 51m³~100m³
                        sewage.fifonetohun = sewage_list_update[i].get('fifonetohun')
                        # 101m³~200m³
                        sewage.hunonetotwohun = sewage_list_update[i].get('hunonetotwohun')
                        # 201m³~500m³
                        sewage.twohunonetofihun = sewage_list_update[i].get('twohunonetofihun')
                        # 501m³~1000m³
                        sewage.fihunonetohus = sewage_list_update[i].get('fihunonetohus')
                        # 1001m³以上
                        sewage.husoneabove = sewage_list_update[i].get('husoneabove')
                        # 更新数据库
                        sewage.save()
                    pro_logger.info('污水料金更新结束')
                    ret = Pc_status.set_price_success
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

