# encoding: utf-8
"""
@author: hanjq
@software: PyCharm
@file: AndroidTask.py
@time: 2020/10/19 14:30
"""
import io
import os
import shutil
from os import listdir
from os.path import isfile, isdir, join
from datetime import datetime
from zipfile import ZipFile

from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_backend.settings import err_logger, zip_file_path, meter_file_path, meter_position_file_path
from aimr_platform.common.Error import Error
from aimr_platform.common.Fileoperate import Fileoperate
from aimr_platform.models import WaterModel_Work, WaterModel_WorkList, WaterModel_Meter, WaterModel_Route, \
    WaterMaster_MeterWork, WaterModel_MeterType, WaterModel_RouteList
from aimr_platform.serializer.meter import WaterModel_MeterSerializer
from aimr_platform.serializer.route import WaterModel_RouteSerializer
from aimr_platform.serializer.route_list import WaterModel_RouteListSerializer
from aimr_platform.serializer.work import WaterModel_WorkSerializer
from aimr_platform.serializer.worklist import WaterModel_WorkListSerializer
from aimr_platform.status import App_status


# 获取最新任务
class AndroidTaskAPI(APIView):
    # 获取任务
    def post(self, request):
        """
            获取最新任务
            :param request:
            :return:
        """
        try:
            flg = request.data['flg']
            # 获取最新任务
            if flg == 'accept':
                # 取得员工id
                emp_id = request.data['emp_id']
                # 取得该员工的任务
                works = WaterModel_Work.objects.filter(Q(emp_id=emp_id) & Q(work_accept_flag='01'))
                # 返回结果集
                result = []
                # 任务年月日
                work_batch_ym = ''
                # 路线名
                route_name = ''
                # 検針予定日
                datum_date = ''
                # 路线id
                route_id = ''
                # 検針状态
                meter_work_name = ''
                # 使用量
                meter_use_count = ''
                # 水表类型
                meter_type = ''
                # 水表使用期间from
                meter_use_during_from = ''
                # 水表使用期间to
                meter_use_during_to = ''
                # 路线详细id
                routelist_id = ''
                # 物件名
                res_name = ''
                # 位置
                position = ''
                # x坐标
                x_position = ''
                # y坐标
                y_position = ''
                # 任务顺
                task_smooth = ''
                # 识别方式
                recognition_id = ''
                if works.__len__() > 0:
                    _list = []
                    meter_count_average = 0
                    for work in works:
                        # →获取任务表数据：任务id，路线id，任务年月
                        work_data = WaterModel_WorkSerializer(work)
                        # 任务id
                        work_id = work_data.get('work_id')
                        # 路线id
                        route_id = work_data.get('route_id')
                        # 任务年月
                        work_batch_ym = work_data.get('work_batch_ym')

                        # →获取路线表数据：路线名，検針予定日
                        route_info = WaterModel_Route.objects.get(route_id=route_id)
                        # 路线名
                        route_name = WaterModel_RouteSerializer(route_info).get('route_name')
                        # 検針予定日
                        datum_date = work_batch_ym + WaterModel_RouteSerializer(route_info).get('datum_date')

                        # →获取任务详细表数据：路线名，検針予定日
                        # 获取单个任务
                        work_list = WaterModel_WorkList.objects.filter(
                            Q(work_id=work_id) &
                            Q(download_flg='0')).order_by('download_flg')[:1]
                        _list = work_list
                        # 検針状态
                        meter_work_name = \
                            WaterMaster_MeterWork.objects.get(meter_work_id=
                                                              _list[0].meter_reading_status).meter_work_name

                        # 识别方式
                        recognition_id = _list[0].recognition_type
                        # 使用量
                        if _list[0].meter_count.__len__() > 0 and _list[0].meter_count != '--':
                            meter_use_count = int(_list[0].meter_count) - int(_list[0].meter_count_last)
                        else:
                            meter_use_count = '--'

                        # 当前月的01号
                        date_to = datetime.now().strftime("%Y-%m-") + '01'
                        # 去年当前月的01号
                        date_from = str(int(date_to[0:4]) - 1) + date_to[4:]

                        # 根据这个区间作为抄表日期查询所有worklist并且按照时间排序，得出该区间总用水，然后根据worklist条数，得到平均用水
                        worklist_meter_average = WaterModel_WorkList.objects.filter(Q(meter_id=_list[0].meter_id) &
                                                                                    Q(meter_reading_date__range=[
                                                                                        date_from, date_to])). \
                            exclude(Q(meter_reading_date=None)).order_by('-meter_reading_date')
                        # 算平均用水的数组
                        meter_average_list = []

                        for work_info in worklist_meter_average:
                            # 数据format
                            work_single = WaterModel_WorkListSerializer(work_info)
                            # 追加到数组
                            meter_average_list.append(work_single)
                            # 得到数组长度
                            meter_count_average_len = len(meter_average_list)
                            # 如果大于1，用最后一个抄表数减去第一个抄表数，得到区间用水
                            if meter_count_average_len > 1:
                                meter_count_average = \
                                    int(meter_average_list[meter_count_average_len - 1].get('meter_count') - \
                                        meter_average_list[0].get('meter_count')) / worklist_meter_average.__len__()
                            # 如果长度等于1则直接计算
                            elif meter_count_average_len == 1:
                                meter_count_average = int(
                                    meter_average_list[0].get('meter_count')) / worklist_meter_average.__len__()
                            else:
                                meter_count_average = 0

                        # 取得上次抄表图片
                        meter_name_before = WaterModel_WorkList.objects.filter(meter_id=_list[0].meter_id) \
                                                .order_by('-meter_reading_date')[:1][0].img_name
                        # 取得上次抄表时间
                        meter_reading_date_before = WaterModel_WorkList.objects.filter(meter_id=_list[0].meter_id) \
                                                        .order_by('-meter_reading_date')[:1][0].meter_reading_date
                        # 取得物件位置图片
                        position_name = WaterModel_Meter.objects.filter(meter_id=_list[0].meter_id)[
                            0].img_position
                        # →获取水表表数据：路线详细id，水表类型，水表使用期间from，水表使用期间to
                        meter_info = WaterModel_Meter.objects.get(meter_id=_list[0].meter_id)
                        # 路线详细id
                        routelist_id = WaterModel_MeterSerializer(meter_info).get('routelist_id')
                        # 水表类型
                        meter_type_code = WaterModel_MeterSerializer(meter_info).get('meter_type')
                        meter_type = WaterModel_MeterType.objects.get(meter_type_id=meter_type_code).meter_caliber
                        # 水表使用期间from
                        meter_use_during_from = WaterModel_MeterSerializer(meter_info).get('meter_use_during_from')
                        # 水表使用期间to
                        meter_use_during_to = WaterModel_MeterSerializer(meter_info).get('meter_use_during_to')

                        # →获取路线详细数据：物件名，位置，x坐标，y坐标，任务顺
                        route_list_info = WaterModel_RouteList.objects.get(routelist_id=routelist_id)
                        route_list_ser = WaterModel_RouteListSerializer(route_list_info)
                        # 物件名
                        res_name = route_list_ser.get('res_name')
                        # 位置
                        position = route_list_ser.get('position')
                        # x坐标
                        x_position = route_list_ser.get('x_position')
                        # y坐标
                        y_position = route_list_ser.get('y_position')
                        # 任务顺
                        task_smooth = route_list_ser.get('task_smooth')

                    # 返回数据格式化
                    # 数组下标
                    count = 0
                    for work_info in _list:
                        result.append(WaterModel_WorkListSerializer(work_info))
                        # 返回数据追加:
                        # 任务年月日
                        result[count].__setitem__('work_batch_ym', work_batch_ym)
                        # 路线名
                        result[count].__setitem__('route_name', route_name)
                        # 検針予定日
                        result[count].__setitem__('datum_date', datum_date)
                        # 识别方式
                        result[count].__setitem__('recognition_id', recognition_id)
                        # 路线id
                        result[count].__setitem__('route_id', route_id)
                        # 検針状态
                        result[count].__setitem__('chk_meter_status', meter_work_name)
                        # 使用量
                        result[count].__setitem__('meter_use_count', meter_use_count)
                        # 平均使用量
                        if meter_count_average and meter_count_average > 0:
                            result[count].__setitem__('meter_count_average', int(meter_count_average))
                        else:
                            result[count].__setitem__('meter_count_average', 0)
                        # 水表类型
                        result[count].__setitem__('meter_type', meter_type)
                        # 水表使用期间from
                        result[count].__setitem__('meter_use_during_from', meter_use_during_from)
                        # 水表使用期间to
                        result[count].__setitem__('meter_use_during_to', meter_use_during_to)
                        # 路线详细id
                        result[count].__setitem__('routelist_id', routelist_id)
                        # 物件名
                        result[count].__setitem__('res_name', res_name)
                        # 持有人住址
                        result[count].__setitem__('meter_cust_add',
                                                  str(result[count].get('meter_cust_add')).split('丁目')[1])
                        # 位置
                        result[count].__setitem__('position', position)
                        # x坐标
                        result[count].__setitem__('x_position', x_position)
                        # y坐标
                        result[count].__setitem__('y_position', y_position)
                        # 任务顺
                        result[count].__setitem__('task_smooth', task_smooth)
                        # メーター取付位置
                        result[count].__setitem__('meter_name_before', meter_name_before)
                        # 検針写真
                        result[count].__setitem__('position_name', position_name)
                        # 前回抄表时间
                        result[count].__setitem__('meter_reading_date', meter_reading_date_before)

                        # 移除冗余值:
                        # # 抄表日期
                        # result[count].__delitem__('meter_reading_date')
                        # 抄表状态
                        result[count].__delitem__('meter_reading_status')
                        # 抄表图片
                        result[count].__delitem__('img_name')
                        # 异常报告日
                        result[count].__delitem__('unusual_report_date')
                        # 异常信息是否已读
                        result[count].__delitem__('unusual_report_read_status')
                        # お客様状態
                        result[count].__delitem__('meter_customer_status')
                        # 识别方式
                        result[count].__delitem__('recognition_type')
                        count += 1
                    # 返回状态以及数据
                    ret = App_status.have_task_success
                    ret['result_data'] = result[0]
                else:
                    ret = App_status.have_task_fail
            # 单个任务接受完毕
            elif flg == 'acceptsingle':
                with transaction.atomic():
                    # 取得员工id
                    emp_id = request.data['emp_id']
                    # 任务详细id
                    work_details_id = request.data['work_details_id']
                    # 任务id
                    work_id = request.data['work_id']
                    # 获取任务详细
                    work_list = WaterModel_WorkList.objects.filter(work_details_id=work_details_id)
                    # 单个任务下载状态更新
                    if work_list.__len__() > 0:
                        for work in work_list:
                            work.download_flg = '1'
                            work.save()
                        # 获取剩余任务个数
                        work_surplus = WaterModel_WorkList.objects.filter(Q(work_id=work_id)
                                                                          & Q(download_flg='0')).__len__()
                    # 剩余任务个数为0
                    if work_surplus == 0:
                        # 取得该员工的任务
                        works = WaterModel_Work.objects.filter(Q(emp_id=emp_id) & Q(work_accept_flag='01'))
                        # 所有任务下载完成，更新任务表数据
                        if works.__len__() > 0:
                            for work in works:
                                work.work_accept_flag = '02'
                                work.work_accept_date = datetime.now()
                                work.save()
                    # 返回数据格式化
                    ret = App_status.download_task_success
                    ret['result_data'] = {
                        'work_surplus': work_surplus
                    }
            # 更新任务
            elif flg == 'updatetask':
                with transaction.atomic():
                    # 任务详细表:
                    # 任务详细id
                    work_details_id = request.data['work_details_id']
                    # 抄表日期
                    meter_reading_date = request.data['meter_reading_date']
                    # meter_reading_date = \
                    #     meter_reading_date[:4] + '-' + meter_reading_date[4:6] + '-' + meter_reading_date[6:]
                    # 抄表数
                    meter_count = request.data['meter_count']
                    # 抄表状态
                    meter_reading_status = request.data['chk_meter_status']
                    # 识别方式
                    recognition_type = request.data['recognition_type']
                    # 抄表图片
                    img_name = request.data['img_name']

                    # 系统自动判断是否为异常数据
                    work_list = WaterModel_WorkList.objects.get(work_details_id=work_details_id)
                    # 如果上报为正常抄表数据
                    if meter_reading_status == '02':
                        use_count = int(meter_count) - int(work_list.meter_count_last)
                        # 如果与上次抄表数对比发现异常
                        if use_count > 20 or use_count < 0:
                            work_list.meter_reading_status = '81'
                        # 如果与上次抄表数对比无异常，、并且抄表方式为估表
                        elif recognition_type == '02':
                            work_list.meter_reading_status = '21'
                        # 否则为正常抄表数据
                        else:
                            work_list.meter_reading_status = '20'
                    # 如果上报为异常
                    elif meter_reading_status == '03':
                        # 取得err_flg
                        err_flg = request.data['err_flg']
                        # 抄表状态
                        work_list.meter_reading_status = err_flg
                        # 异常报告日
                        work_list.unusual_report_date = meter_reading_date
                        # 异常信息是否已读
                        work_list.unusual_report_read_status = '0'
                        work_list.unusual_status = '00'
                        # 取得对应水表
                        meter = WaterModel_Meter.objects.get(meter_id=work_list.meter_id)
                        # 更新异常对应状态 （未对应）
                        meter.unusual_status = '00'
                        meter.save()
                    # 抄表日
                    work_list.meter_reading_date = meter_reading_date
                    # 抄表数
                    work_list.meter_count = meter_count
                    # 识别方式
                    work_list.recognition_type = recognition_type
                    # 抄表图片
                    work_list.img_name = img_name
                    # 更新
                    work_list.save()

                # 返回状态
                ret = App_status.read_meter_success
            # 接受全部任务
            elif flg == 'acceptall':
                # 取得员工id
                emp_id = request.data['emp_id']
                # 取得该员工的任务
                works = WaterModel_Work.objects.filter(Q(emp_id=emp_id) & Q(work_accept_flag='01'))
                # 返回结果集
                result = []
                count = 0
                if works.__len__() > 0:
                    _list = []
                    meter_count_average = 0
                    work_id_array = []
                    # 需要压缩的文件名
                    meter_img = []
                    meter_position_img = []
                    for work in works:
                        # →获取任务表数据：任务id，路线id，任务年月
                        work_data = WaterModel_WorkSerializer(work)
                        # 任务id
                        work_id = work_data.get('work_id')
                        work_id_array.append(work_id)
                        # 路线id
                        route_id = work_data.get('route_id')
                        # 任务年月
                        work_batch_ym = work_data.get('work_batch_ym')
                        # →获取路线表数据：路线名，検針予定日
                        route_info = WaterModel_Route.objects.get(route_id=route_id)
                        # 路线名
                        route_name = WaterModel_RouteSerializer(route_info).get('route_name')
                        # 検針予定日
                        datum_date = work_batch_ym + WaterModel_RouteSerializer(route_info).get('datum_date')

                        # →获取任务详细表数据：路线名，検針予定日
                        # 获取单个任务
                        work_list = WaterModel_WorkList.objects.filter(
                            Q(work_id=work_id) &
                            Q(download_flg='0')).order_by('download_flg')
                        for _list in work_list:
                            # 検針状态
                            meter_work_name = \
                                WaterMaster_MeterWork.objects.get(meter_work_id=
                                                                  _list.meter_reading_status).meter_work_name

                            # 识别方式
                            recognition_id = _list.recognition_type
                            # 使用量
                            if _list.meter_count.__len__() > 0 and _list.meter_count != '--':
                                meter_use_count = int(_list.meter_count) - int(_list.meter_count_last)
                            else:
                                meter_use_count = 0

                            # 当前月的01号
                            date_to = datetime.now().strftime("%Y-%m-") + '01'
                            # 去年当前月的01号
                            date_from = str(int(date_to[0:4]) - 1) + date_to[4:]

                            # 根据这个区间作为抄表日期查询所有worklist并且按照时间排序，得出该区间总用水，然后根据worklist条数，得到平均用水
                            worklist_meter_average = WaterModel_WorkList.objects.filter(Q(meter_id=_list.meter_id) &
                                                                                        Q(meter_reading_date__range=[
                                                                                            date_from, date_to])). \
                                exclude(Q(meter_reading_date=None)).order_by('-meter_reading_date')
                            # 算平均用水的数组
                            meter_average_list = []

                            for work_info in worklist_meter_average:
                                # 数据format
                                work_single = WaterModel_WorkListSerializer(work_info)
                                # 追加到数组
                                meter_average_list.append(work_single)
                                # 得到数组长度
                                meter_count_average_len = len(meter_average_list)
                                # 如果大于1，用最后一个抄表数减去第一个抄表数，得到区间用水
                                if meter_count_average_len > 1:
                                    meter_count_average = \
                                        int(meter_average_list[meter_count_average_len - 1].get('meter_count') - \
                                            meter_average_list[0].get('meter_count')) / worklist_meter_average.__len__()
                                # 如果长度等于1则直接计算
                                elif meter_count_average_len == 1:
                                    meter_count_average = int(
                                        meter_average_list[0].get('meter_count')) / worklist_meter_average.__len__()
                                else:
                                    meter_count_average = 0

                            # 取得上次抄表图片
                            meter_name_before = WaterModel_WorkList.objects.filter(meter_id=_list.meter_id) \
                                                    .order_by('-meter_reading_date')[:1][0].img_name

                            if meter_name_before not in meter_img:
                                meter_img.append(meter_name_before)
                            # 取得上次抄表时间
                            meter_reading_date_before = WaterModel_WorkList.objects.filter(meter_id=_list.meter_id) \
                                                            .order_by('-meter_reading_date')[:1][0].meter_reading_date
                            # 取得物件位置图片
                            position_name = WaterModel_Meter.objects.filter(meter_id=_list.meter_id)[
                                0].img_position
                            if position_name not in meter_position_img:
                                meter_position_img.append(position_name)

                            # →获取水表表数据：路线详细id，水表类型，水表使用期间from，水表使用期间to
                            meter_info = WaterModel_Meter.objects.get(meter_id=_list.meter_id)
                            # 路线详细id
                            routelist_id = WaterModel_MeterSerializer(meter_info).get('routelist_id')

                            # 水表类型
                            meter_type_code = WaterModel_MeterSerializer(meter_info).get('meter_type')
                            meter_type = WaterModel_MeterType.objects.get(meter_type_id=meter_type_code).meter_caliber
                            # 水表使用期间from
                            meter_use_during_from = WaterModel_MeterSerializer(meter_info).get(
                                'meter_use_during_from')
                            # 水表使用期间to
                            meter_use_during_to = WaterModel_MeterSerializer(meter_info).get('meter_use_during_to')

                            # →获取路线详细数据：物件名，位置，x坐标，y坐标，任务顺
                            route_list_info = WaterModel_RouteList.objects.get(routelist_id=routelist_id)
                            route_list_ser = WaterModel_RouteListSerializer(route_list_info)
                            # 物件名
                            res_name = route_list_ser.get('res_name')
                            # 位置
                            position = route_list_ser.get('position')
                            # x坐标
                            x_position = route_list_ser.get('x_position')
                            # y坐标
                            y_position = route_list_ser.get('y_position')
                            # 任务顺
                            task_smooth = route_list_ser.get('task_smooth')

                            result.append(WaterModel_WorkListSerializer(_list))
                            # 返回数据追加:
                            # 任务年月日
                            result[count].__setitem__('work_batch_ym', work_batch_ym)
                            # 路线名
                            result[count].__setitem__('route_name', route_name)
                            # 検針予定日
                            result[count].__setitem__('datum_date', datum_date)
                            # 识别方式
                            result[count].__setitem__('recognition_id', recognition_id)
                            # 路线id
                            result[count].__setitem__('route_id', route_id)
                            # 検針状态
                            result[count].__setitem__('chk_meter_status', meter_work_name)
                            # 使用量
                            result[count].__setitem__('meter_use_count', meter_use_count)
                            # 平均使用量
                            if meter_count_average and meter_count_average > 0:
                                result[count].__setitem__('meter_count_average', int(meter_count_average))
                            else:
                                result[count].__setitem__('meter_count_average', 0)
                            # 水表类型
                            result[count].__setitem__('meter_type', meter_type)
                            # 水表使用期间from
                            result[count].__setitem__('meter_use_during_from', meter_use_during_from)
                            # 水表使用期间to
                            result[count].__setitem__('meter_use_during_to', meter_use_during_to)
                            # 路线详细id
                            result[count].__setitem__('routelist_id', routelist_id)
                            # 物件名
                            result[count].__setitem__('res_name', res_name)
                            # 持有人住址
                            result[count].__setitem__('meter_cust_add',
                                                      str(result[count].get('meter_cust_add')).split('丁目')[1])
                            # 位置
                            result[count].__setitem__('position', position)
                            # x坐标
                            result[count].__setitem__('x_position', x_position)
                            # y坐标
                            result[count].__setitem__('y_position', y_position)
                            # 任务顺
                            result[count].__setitem__('task_smooth', task_smooth)
                            # メーター取付位置
                            result[count].__setitem__('meter_name_before', meter_name_before)
                            # 検針写真
                            result[count].__setitem__('position_name', position_name)
                            # 前回抄表时间
                            result[count].__setitem__('meter_reading_date', meter_reading_date_before)

                            # 移除冗余值:
                            # # 抄表日期
                            # result[count].__delitem__('meter_reading_date')
                            # 抄表状态
                            result[count].__delitem__('meter_reading_status')
                            # 抄表图片
                            result[count].__delitem__('img_name')
                            # 异常报告日
                            result[count].__delitem__('unusual_report_date')
                            # 异常信息是否已读
                            result[count].__delitem__('unusual_report_read_status')
                            # お客様状態
                            result[count].__delitem__('meter_customer_status')
                            # 识别方式
                            result[count].__delitem__('recognition_type')
                            count += 1
                    # 设定压缩文件名
                    zip_name = datetime.now().strftime("%Y%m%d%H%M%S")
                    # 以追加模式打开或创建zip文件
                    fp = ZipFile(zip_file_path + zip_name + '.zip', mode='a')
                    # 循环需要压缩文件的数组
                    for i in range(len(meter_img)):
                        # 写入文件
                        fp.write(meter_file_path + meter_img[i])
                    for j in range(len(meter_position_img)):
                        # 写入文件
                        fp.write(meter_position_file_path + meter_position_img[j])
                    fp.close()
                    # 取到压缩文件的大小
                    size = os.path.getsize(zip_file_path + zip_name + '.zip')

                    # fs = Fileoperate.FileOperate()
                    # # 取得需要上传的文件
                    # file_zip = open('./file.zip', 'rb')
                    # # 上传到minio服务器
                    # fs.upload_singlefile('meter-zip', zip_name + '.zip', file_zip, int(size))
                    # file_zip.close()
                    # # 移除本地的压缩文件
                    # os.remove('./file.zip')
                    # # 移除本地的送信生成的文件
                    # shutil.rmtree('./file')

                    # 返回状态以及数据

                    ret = App_status.have_task_success
                    ret['result_data'] = result
                    ret['zip_name'] = zip_name + '.zip'
                    ret['file_size'] = size
                else:
                    ret = App_status.have_task_fail
            # 更新任务
            elif flg == 'acceptall_over':
                with transaction.atomic():
                    workids = request.data['workids']
                    workid_list = str(workids).split('_')

                    for i in range(len(workid_list)):
                        # 取得该员工的任务
                        work = WaterModel_Work.objects.get(work_id=workid_list[i])
                        # 取得所有任务详细
                        worklists = WaterModel_WorkList.objects.filter(work_id=work.work_id)
                        # 更新任务详细的下载flg
                        for worklist in worklists:
                            worklist.download_flg = '1'
                            worklist.save()
                        # 更新任务表是否被接收
                        work = WaterModel_Work.objects.get(work_id=work.work_id)
                        work.work_accept_flag = '02'
                        work.work_accept_date = datetime.now()
                        work.save()
                    # 返回数据格式化
                    ret = App_status.download_task_success
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)
