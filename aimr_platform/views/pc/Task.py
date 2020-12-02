# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: Task.py
@time: 2020/9/28 14:30
"""
import datetime
import os
import threading

from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_platform.common.Error import Error
from aimr_platform.common.Firebase.fire_base import send_message
from aimr_platform.models import WaterModel_Work, WaterModel_Emp, WaterModel_Route, WaterMaster_SendWork, \
    WaterModel_RouteList, WaterModel_Meter, WaterModel_WorkList
from aimr_backend.settings import pro_logger, err_logger
from aimr_platform.serializer.emp import WaterModel_EmpSerializer
from aimr_platform.serializer.route import WaterModel_RouteSerializer
from aimr_platform.serializer.route_list import WaterModel_RouteListSerializer
from aimr_platform.serializer.work import WaterModel_WorkSerializer
from aimr_platform.serializer.worklist import WaterModel_WorkListSerializer
from aimr_platform.status import Pc_status


# タスク相关
class TaskAPI(APIView):
    # 获取タスク更新確認
    def get(self, request):
        """
            获取タスク更新確認状态
            :param request:
            :return:
        """
        try:
            # 获取タスク更新確認状态
            ret = self.get_task_status(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def post(self, request):
        """
           单个送信
           :param request:
           :return:
        """
        try:
            # 开始事务
            emp_id = request.data['emp_id']
            pro_logger.info('emp_id:' + str(emp_id))
            with transaction.atomic():
                ret = self.send_msg(request)
            emp = WaterModel_Emp.objects.get(emp_id=emp_id)
            emp_data = WaterModel_EmpSerializer(emp)
            token = {
                'token': emp_data.get('emp_token')
            }
            pro_logger.info('token:' + str(token))
            t = threading.Thread(target=send_message,
                                 kwargs=token)
            t.start()
            # ret = Pc_status.send_message_success
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    # 获取タスク更新確認状态
    def get_task_status(self, request):
        # 每页显示多少条数据
        page_data_count = request.GET.get('page_data_count')
        # 第几页
        page_count = request.GET.get('page_count')
        # 取得flg
        init_flg = request.GET.get('init_flg')

        pro_logger.info('タスク列表取得')
        # 返回数据数组初期化
        _list = []
        # 数组下标
        count = 0
        # タスク列表取得,如果为初期化,则返回总条数,否则为0
        if init_flg == 'init':
            task_list = WaterModel_Work.objects.filter().order_by('-work_send_message_date', 'work_accept_flag')
            # 数据总条数
            _list_count = task_list.__len__()
            # 分页数据
            task_list = \
                task_list[(int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(page_data_count) + int(page_data_count)]
        else:
            # 分页数据
            task_list = WaterModel_Work.objects.filter().order_by(
                '-work_send_message_date', 'work_accept_flag')[
                        (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(page_data_count) + int(page_data_count)]
            _list_count = 0
        # 循环タスク列表
        index_no = (int(page_count) - 1) * int(page_data_count) + 1
        for task_info in task_list:
            # 时间format
            if task_info.work_send_message_date:
                task_info.work_send_message_date = task_info.work_send_message_date.strftime("%Y-%m-%d %H:%M")
            # 序列化
            task_info = WaterModel_WorkSerializer(task_info)
            # 设定初期值
            task_info.__setitem__('emp_name', '')
            task_info.__setitem__('route_name', '')
            task_info.__setitem__('flag_name', '')

            # 查询员工并确定员工名
            emp_name = WaterModel_Emp.objects.get(emp_id=task_info.get('emp_id'))
            emp_name = WaterModel_EmpSerializer(emp_name).get('emp_name')

            # 查询路线并确定路线名
            route_name = WaterModel_Route.objects.get(route_id=task_info.get('route_id'))
            route_name = WaterModel_RouteSerializer(route_name).get('route_name')

            # 接受标识名
            flag_name = WaterMaster_SendWork.objects.get(send_work_id=task_info.get('work_accept_flag')).send_work_name

            _list.append(task_info)
            # 设定员工名
            _list[count].__setitem__('emp_name', emp_name)
            # 设定路线名
            _list[count].__setitem__('route_name', route_name)
            # 设定接受标识名
            _list[count].__setitem__('flag_name', flag_name)

            # index_no
            _list[count].__setitem__('index_no', index_no)
            index_no = index_no + 1

            # 取得接收日期
            work_accept_date = _list[count].get('work_accept_date')
            # 如果存在则进行format
            if work_accept_date:
                work_accept_date = str(work_accept_date).replace('T', ' ')[:16]
                _list[count].__setitem__('work_accept_date', work_accept_date)
            count += 1
        # 返回状态及数据
        ret = Pc_status.get_task_success
        ret['result_data'] = {
            '_list': _list,
            '_list_count': _list_count,
        }
        return ret

    # 单个送信
    def send_msg(self, request):
        # 任务年月
        work_batch_ym = request.data['work_batch_ym']
        # 员工id
        emp_id = request.data['emp_id']
        # 路线id
        route_id = request.data['route_id']
        # 发送任务标题
        work_send_message_title = str(work_batch_ym[0:4]) + '年' + str(work_batch_ym[4:6]) + '月検針タスク'
        # 根据当前条件查询数据库
        works = WaterModel_Work.objects.filter(Q(work_batch_ym=work_batch_ym) &
                                               Q(route_id=route_id))
        # 如果此批任务不存在,则新建
        if works.__len__() == 0:
            work = WaterModel_Work(
                work_batch_ym=work_batch_ym,
                work_send_message_title=work_send_message_title,
                work_send_message_date=datetime.datetime.now(),
                work_accept_flag='01',
                work_accept_date=None,
                emp_id=emp_id,
                route_id=route_id
            )
            work.save()
        else:
            work = works[0]
            work.work_accept_flag = '01'
            work.work_accept_date = None
            work.work_send_message_date = datetime.datetime.now()
            work.save()
            # 删除以前送信做成的任务详细
            WaterModel_WorkList.objects.filter(work_id=work.work_id).delete()

        # 查询对应路线详细
        routelists = WaterModel_RouteList.objects.filter(route_id=route_id)
        # 水表数组
        _meters_format = []
        # 循环路线详细取得水表
        for routelist in routelists:
            routelist_id = WaterModel_RouteListSerializer(routelist).get('routelist_id')
            meters = WaterModel_Meter.objects.filter(routelist_id=routelist_id)
            # 如果水表存在则追加到数组
            if len(meters) > 0:
                for meter in meters:
                    # 从任务详细取得上次抄表数据
                    meter_before = WaterModel_WorkList.objects.filter(meter_id=meter.meter_id).order_by(
                        '-meter_reading_date')
                    # 取得上次抄表数,如果没有则设为空
                    if meter_before:
                        meter_count_last = WaterModel_WorkListSerializer(meter_before[0]).get('meter_count_last')
                    else:
                        meter_count_last = '--'
                    # 保存到数据库
                    worklist = WaterModel_WorkList(
                        meter_reading_date=None,
                        meter_count='--',
                        meter_count_last=meter_count_last,
                        meter_reading_status='00',
                        meter_cust_no=meter.meter_customer_no,
                        meter_cust_name=meter.meter_customer_name,
                        meter_cust_add=meter.meter_customer_address,
                        meter_cust_tel=meter.meter_customer_tel,
                        recognition_type=None,
                        img_name='',
                        unusual_report_date=None,
                        unusual_report_read_status=None,
                        meter_customer_status='0',
                        emp_id=emp_id,
                        message_id=None,
                        work_id=work.work_id,
                        meter_id=meter.meter_id
                    )
                    worklist.save()

        # 返回消息
        ret = Pc_status.send_message_success
        return ret
