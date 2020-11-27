# encoding: utf-8
"""
@author: hanjq
@software: PyCharm
@file: DataCreate.py
@time: 2020/11/12 11:30
"""

import random
from django.db import transaction
from django.db.models import Max
from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_platform.models import WaterModel_Route, WaterModel_RouteList, WaterModel_Meter


# 测试数据作成
class DataCreateAPI(APIView):
    # 测试数据作成
    def post(self, request):
        """
            :说明:执行一次，作成1个路线，100(可变)个路线详细，每个路线详细下8(可变)块表，一次增加800条数据
            :return:数据作成是否成功或者失败
        """
        with transaction.atomic():
            # 路线表数据作成
            route = WaterModel_Route(
                # 路线名
                route_name='テストルート',
                # 基准日
                datum_date='10',
                # 奇偶区分 1:奇数 2：偶数
                parity_distinction='1',
                # 分配员工 3：検針 井路
                emp_id_id='3'
            )
            route.save()
            # 最大路线id取得
            route_dict = WaterModel_Route.objects.all().aggregate(Max('route_id'))
            route_id = route_dict['route_id__max']

            for i in range(100):
                # 路线详细表数据作成
                position_tmp = 'テスト県テスト区' + str(i) + '丁目' + str(i) + '番地' + str(i) + '号'
                route_list = WaterModel_RouteList(
                    # 物件名
                    res_name='テスト物件' + str(i),
                    # 地址
                    address='テスト県テスト区テスト',
                    # 当前路线水表数
                    meter_count='8',
                    # 路线id
                    route_id_id=route_id,
                    # 位置
                    position=position_tmp,
                    # X坐标
                    x_position='35.663006',
                    # y坐标
                    y_position='139.673355',
                    # 任务顺
                    task_smooth=i + 1
                )
                route_list.save()
                # 水表表数据作成
                for j in range(8):
                    # 随机6位生成
                    random_num = random.randint(0, 999999)
                    alphabet = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
                    characters = random.sample(alphabet, 2)
                    # 最大路线详细id取得
                    route_list_dict = WaterModel_RouteList.objects.all().aggregate(Max('routelist_id'))
                    route_id_list = route_list_dict['routelist_id__max']
                    meter = WaterModel_Meter(
                        # お客様番号
                        meter_customer_no='01-' + str(random_num) + '-01',
                        # 水表号
                        meter_no=str(random_num),
                        # 二维码
                        meter_qr_code=str(random_num),
                        # 异常状态
                        unusual_status='',
                        # 持有人
                        meter_customer_name='テスト' + ' ' + characters[0] + characters[1] + str(i),
                        # 持有人住址
                        meter_customer_address=position_tmp + str(j) + '0' + str(j) + '室',
                        # 持有人电话
                        meter_customer_tel='09021232323',
                        # 水表型号
                        meter_type='01',
                        # 路线详细id
                        routelist_id_id=route_id_list,
                        # 水表所在位置图片
                        img_position='03.png',
                        # 水表使用期间from
                        meter_use_during_from='2020-09-15',
                        # 水表使用期间to
                        meter_use_during_to='2020-11-27',
                    )
                    meter.save()
        return JsonResponse('OK', safe=False)

