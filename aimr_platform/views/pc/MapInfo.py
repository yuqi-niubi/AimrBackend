# encoding: utf-8
"""
@author: hanjq
@software: PyCharm
@file: MapInfo.py
@time: 2020/9/28 14:30
"""
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_platform.common.Error import Error
from aimr_platform.models import WaterModel_RouteList, WaterModel_Route, WaterModel_Emp, \
    WaterModel_Meter, WaterModel_WorkList
from aimr_backend.settings import pro_logger, err_logger
from aimr_platform.serializer.meter import WaterModel_MeterSerializer
from aimr_platform.serializer.route_list import WaterModel_RouteListSerializer
from aimr_platform.status import Pc_status


# エリア相关
class MapInfoAPI(APIView):
    def get(self, request):
        """
            获取エリア详细信息
            :param request:
            :return:
        """
        try:
            ret = self.get_routelist_detail(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def post(self, request):
        """
            创建物件
            :param request:
            :return:
        """
        try:
            # 开始事务
            with transaction.atomic():
                ret = self.create_route_list(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def put(self, request):
        """
            更新物件
            :param request:
            :return:
        """
        try:
            # 开始事务
            with transaction.atomic():
                ret = self.update_route_list(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def delete(self, request):
        """
            删除物件
            :param request:
            :return:
        """
        try:
            # 开始事务
            with transaction.atomic():
                ret = self.delete_route_list(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    # 获取エリア详细信息
    def get_routelist_detail(self, request):
        # 每页显示多少条数据
        page_data_count = request.GET.get('page_data_count')
        # 第几页
        page_count = request.GET.get('page_count')

        pro_logger.info('获取エリア详细信息')
        # 返回数据数组
        _list = []
        # 取得flag
        flag = request.GET.get('flag')
        # 点击路线名
        if flag == 'route':
            # 路线id
            route_id = request.GET.get('route_id')
            # 总数据
            _list_all = []
            # エリア列表取得
            route_lists = WaterModel_RouteList.objects.filter(route_id=route_id).order_by('task_smooth')
            _list_count = route_lists.__len__()
            index_no = 1
            for route_info in route_lists:
                route_info = WaterModel_RouteListSerializer(route_info)
                route_info.__setitem__('index_no', index_no)
                _list_all.append(route_info)
                index_no += 1

            _list = _list_all[
                    (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(page_data_count) + int(
                        page_data_count)]

            # 返回状态及数据
            ret = Pc_status.set_area_uccess
            ret['result_data'] = {
                'route_list': _list,
                '_list_count': _list_count,
                '_list_all': _list_all
            }
        # # 点击送信，暂时未利用
        # elif flag == 'emp':
        #     emp_id = request.GET.get('emp_id')
        #     # 任务列表取得
        #     # works = WaterModel_Work.objects.filter(emp_id=emp_id)
        #
        #     route_list_ids = []
        #     _list = []
        #     # for work in works:
        #     # 路线列表取得
        #     routes = WaterModel_Route.objects.filter(emp_id=emp_id)
        #     # 循环所有路线
        #     for route_info in routes:
        #         # 取得路线详细id
        #         route_list_id = WaterModel_RouteSerializer(route_info).data.get('route_id')
        #         # 将所有路线详细id追加到数组
        #         route_list_ids.append(route_list_id)
        #     # 水表总数初期化
        #     count_all = 0
        #     # 循环下标
        #     j = 0
        #     # 循环所有路线详细id
        #     for i in range(0, len(route_list_ids)):
        #         # 路线详细取得
        #         routelists = WaterModel_RouteList.objects.filter(route_id=route_list_ids[i])
        #         for routelist in routelists:
        #             route_list = WaterModel_RouteListSerializer(routelist).data
        #             _list.append(route_list)
        #             # 员工名取得
        #             emp_name = WaterModel_Emp.objects.get(emp_id=emp_id).emp_name
        #             _list[j].__setitem__('emp_name', emp_name)
        #             # 基准日取得
        #             route_datum = WaterModel_Route.objects.get(route_id=_list[j].__getitem__('route_id')).datum_date
        #             _list[j].__setitem__('route_datum', route_datum)
        #             # 奇偶区分
        #             route_parity = WaterModel_Route.objects.get(route_id=
        #                                                         _list[j].__getitem__('route_id')).parity_distinction
        #             _list[j].__setitem__('route_parity', route_parity)
        #             # 路线名取得
        #             route_name = WaterModel_Route.objects.get(route_id=_list[j].__getitem__('route_id')).route_name
        #             _list[j].__setitem__('route_name', route_name)
        #             j += 1
        #     # 循环_list
        #     for index in (0, len(_list) - 1):
        #         # 计算水表总数
        #         count_all += _list[index].__getitem__('meter_count')
        #     # 分页
        #     _list = Paginator(_list, page_data_count)
        #     # 返回状态以及数据
        #     ret = Pc_status.set_area_uccess
        #     ret['result_data'] = {
        #         'route_list': _list.get_page(page_count).object_list,
        #         '_list_count': _list.count,
        #         'page_count': _list.num_pages,
        #         'count_all': count_all
        #     }
        # 点击物件名
        elif flag == 'meter':
            # 返回数据数组
            _list = []
            # 取得路线详细id
            routelist_id = request.GET.get('routelist_id')
            # 取得路线详细
            routelist = WaterModel_RouteList.objects.get(routelist_id=routelist_id)
            # 取得物件名
            resname = routelist.res_name
            # 取得路线
            route = WaterModel_Route.objects.get(route_id=routelist.route_id)
            # 取得员工名
            emp_name = WaterModel_Emp.objects.get(emp_id=route.emp_id).emp_name
            # 取得flg
            init_flg = request.GET.get('init_flg')

            # 取得符合条件水表追加到数组,如果为初期化,则返回总条数,否则为0
            if init_flg == 'init':
                meters = WaterModel_Meter.objects.filter(routelist_id=routelist_id)
                # 数据总条数
                _list_count = meters.__len__()
                # 分页数据
                meters = \
                    meters[
                    (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(page_data_count) + int(
                        page_data_count)]
            else:
                # 分页数据
                meters = WaterModel_Meter.objects.filter(routelist_id=routelist_id)[
                         (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(
                             page_data_count) + int(page_data_count)]
                _list_count = 0

            for meter in meters:
                _list.append(WaterModel_MeterSerializer(meter))
            # 如果_list长度达于0
            index_no = (int(page_count) - 1) * int(page_data_count) + 1
            if _list.__len__() > 0:
                # 循环_list
                for i in range(_list.__len__()):
                    # 设定物件名
                    _list[i].__setitem__('resname', resname)
                    # 设定员工名
                    _list[i].__setitem__('emp_name', emp_name)
                    # 设定水表数
                    _list[i].__setitem__('metacount', 1)
                    # index_no
                    _list[i].__setitem__('index_no', index_no)
                    index_no = index_no + 1

            # 返回状态以及数据
            ret = Pc_status.set_area_uccess
            ret['result_data'] = {
                'route_list': _list,
                '_list_count': _list_count,
            }
        else:
            ret = Pc_status.set_area_fail
        return ret

    # 创建物件
    def create_route_list(self, request):
        # 取得物件数组
        routelist_arr = request.data['routelist_arr']
        # 循环
        for i in range(0, routelist_arr.__len__()):
            # 如果该条数据为新规数据
            if routelist_arr[i].get('routelist_id') == '':
                # 路线id
                route_id = routelist_arr[i].get('route_id')
                # 物件名
                res_name = routelist_arr[i].get('res_name')
                # 位置
                position = routelist_arr[i].get('position')
                # x坐标
                x_position = routelist_arr[i].get('x_position')
                # y坐标
                y_position = routelist_arr[i].get('y_position')

                # 写入数据库
                routelist = WaterModel_RouteList(
                    res_name=res_name,
                    route_id=route_id,
                    position=position,
                    x_position=x_position,
                    y_position=y_position,
                    task_smooth=i + 1
                )
                routelist.save()
            # 如果该条数据为现有数据
            else:
                # 路线详细id
                routelist_id = routelist_arr[i].get('routelist_id')
                # 物件名
                res_name = routelist_arr[i].get('res_name')
                # 位置
                position = routelist_arr[i].get('position')
                # x坐标
                x_position = routelist_arr[i].get('x_position')
                # y坐标
                y_position = routelist_arr[i].get('y_position')

                # 写入数据库
                routelist = WaterModel_RouteList.objects.get(routelist_id=routelist_id)
                routelist.res_name = res_name
                routelist.position = position
                routelist.x_position = x_position
                routelist.y_position = y_position
                routelist.task_smooth = i + 1
                routelist.save()
        ret = Pc_status.create_routelist_success
        return ret

    # 更新物件
    def update_route_list(self, request):
        # 路线详细id
        routelist_id = request.data['routelist_id']
        # 物件名
        res_name = request.data['res_name']
        # 位置
        position = request.data['position']
        # x坐标
        x_position = request.data['x_position']
        # y坐标
        y_position = request.data['y_position']

        # 写入数据库
        routelist = WaterModel_RouteList.objects.get(routelist_id=routelist_id)
        routelist.res_name = res_name
        routelist.position = position
        routelist.x_position = x_position
        routelist.y_position = y_position
        routelist.save()

        ret = Pc_status.update_routelist_success
        return ret

    # 删除物件
    def delete_route_list(self, request):
        # 路线详细id
        routelist_id = request.data['routelist_id']
        # 获取该路线详细下水表
        meters = WaterModel_Meter.objects.filter(routelist_id=routelist_id)
        if meters:
            # 删除该路线详细下所有水表对应的任务详细
            for meter in meters:
                meter_id = WaterModel_MeterSerializer(meter).get('meter_id')
                # 删除任务详细
                WaterModel_WorkList.objects.filter(meter_id=meter_id).delete()
            # 删除该路线详细下水表
            meters.delete()
        # 删除该路线详细
        WaterModel_RouteList.objects.get(routelist_id=routelist_id).delete()

        routelist_arr = request.data['routelist_arr']
        for i in range(0, routelist_arr.__len__()):
            # 路线详细id
            routelist_id = routelist_arr[i].get('routelist_id')
            # 物件名
            res_name = routelist_arr[i].get('res_name')
            # 位置
            position = routelist_arr[i].get('position')
            # x坐标
            x_position = routelist_arr[i].get('x_position')
            # y坐标
            y_position = routelist_arr[i].get('y_position')

            # 写入数据库
            routelist = WaterModel_RouteList.objects.get(routelist_id=routelist_id)
            routelist.res_name = res_name
            routelist.position = position
            routelist.x_position = x_position
            routelist.y_position = y_position
            routelist.task_smooth = i + 1
            routelist.save()
        ret = Pc_status.delete_routelist_success
        return ret
