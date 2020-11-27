# encoding: utf-8
"""
@author: hanjq
@software: PyCharm
@file: Map.py
@time: 2020/9/28 14:30
"""
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_platform.common.Error import Error
from aimr_platform.models import WaterModel_RouteList, WaterModel_Route, WaterModel_Work, WaterModel_Emp, \
    WaterModel_WorkList, WaterModel_Meter
from aimr_backend.settings import pro_logger, err_logger
from aimr_platform.serializer.emp import WaterModel_EmpSerializer
from aimr_platform.serializer.route import WaterModel_RouteSerializer
from aimr_platform.serializer.route_list import WaterModel_RouteListSerializer
from aimr_platform.serializer.work import WaterModel_WorkSerializer
from aimr_platform.status import Pc_status


# 地图相关
class MapAPI(APIView):
    def get(self, request):
        """
            エリア设定一览
            :param request:
            :return:
        """
        try:
            # 取得flg
            flg = request.GET.get('flg')
            # 初期进入エリア设定
            if flg == 'routes':
                # 获取路线信息
                ret = self.get_route_detail(request)
            # 路线编辑或者新规，下拉框的值
            elif flg == 'emps':
                emps = WaterModel_Emp.objects.filter().exclude(emp_role='01')
                emplist = []
                for emp in emps:
                    emplist.append(WaterModel_EmpSerializer(emp))
                ret = Pc_status.set_area_uccess
                ret['result_data'] = {
                    'emplist': emplist,
                }
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def post(self, request):
        """
        新建route
        :param request:
        :return:
        """
        try:
            # 开始事务
            with transaction.atomic():
                ret = self.create_route(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def put(self, request):
        """
           更新エリア设定
           :param request:
           :return:
       """
        try:
            # 开始事务
            with transaction.atomic():
                ret = self.update_route(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def delete(self, request):
        """
            删除oute
            :param request:
            :return:
        """
        try:
            # 开始事务
            with transaction.atomic():
                ret = self.delete_route(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    # 获取路线信息
    def get_route_detail(self, request):
        # 每页显示多少条数据
        page_data_count = request.GET.get('page_data_count')
        # 第几页
        page_count = request.GET.get('page_count')
        # 取得flg
        init_flg = request.GET.get('init_flg')

        pro_logger.info('エリア设定')
        _list = []
        # 循环下标
        count = 0
        # 路线列表取得,如果为初期化,则返回总条数,否则为0
        if init_flg == 'init':
            route_list = WaterModel_Route.objects.all()
            # 数据总条数
            _list_count = route_list.__len__()
            # 分页数据
            route_list = \
                route_list[
                    (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(page_data_count) + int(page_data_count)]
        else:
            # 分页数据
            route_list = WaterModel_Route.objects.all()[
                         (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(page_data_count) + int(page_data_count)]
            _list_count = 0

        count_meta = 0
        index_no = (int(page_count) - 1) * int(page_data_count) + 1
        # 循环所有路线
        for route_info in route_list:
            route_info = WaterModel_RouteSerializer(route_info)
            route_info.__setitem__('emp_name', '')
            route_info.__setitem__('route_name', '')
            _list.append(route_info)

            # 查询路线名
            route_name = WaterModel_Route.objects.get(route_id=route_info.get('route_id'))
            route_name = WaterModel_RouteSerializer(route_name).get('route_name')
            _list[count].__setitem__('route_name', route_name)

            # 查询员工名
            emp_id = WaterModel_Route.objects.get(route_id=route_info.get('route_id')).emp_id
            emp_name = WaterModel_Emp.objects.get(emp_id=emp_id)
            emp_name = WaterModel_EmpSerializer(emp_name).get('emp_name')

            # 查询所有路线详细
            routelists = WaterModel_RouteList.objects.filter(route_id=route_info.get('route_id'))
            # 计算水表数
            for routlist in routelists:
                count_meta += routlist.meter_count

            # 查询地址
            routeposition = WaterModel_RouteList.objects.filter(route_id=route_info.get('route_id'))[:1]
            if routeposition:
                _list[count].__setitem__('position',
                                         WaterModel_RouteListSerializer(routeposition[0]).get('position'))
            else:
                _list[count].__setitem__('position', '')

            # 员工id
            _list[count].__setitem__('emp_id', emp_id)
            # 员工名
            _list[count].__setitem__('emp_name', emp_name)
            # 水表数
            _list[count].__setitem__('count', count_meta)
            # 基准日
            _list[count].__setitem__('datum_date', route_info.get('datum_date'))
            # index_no
            _list[count].__setitem__('index_no', index_no)
            index_no = index_no + 1
            count_meta = 0
            count += 1
        ret = Pc_status.set_area_uccess
        ret['result_data'] = {
            'route_list': _list,
            '_list_count': _list_count,
        }
        return ret

    # 创建路线
    def create_route(self, request):
        # 路线名
        route_name = request.data['route_name']
        # 员工ID
        emp_id = request.data['emp_id']
        # 基准日
        datum_date = request.data['datum_date']
        # 奇偶区分
        parity = request.data['parity']
        # 写入数据库
        route = WaterModel_Route(
            route_name=route_name,
            emp_id=emp_id,
            datum_date=datum_date,
            parity_distinction=parity,
        )
        route.save()
        # 返回状态
        ret = Pc_status.create_route_success
        return ret

    # 更新路线
    def update_route(self, request):
        # 路线id
        route_id = request.data['route_id']
        # 路线名
        route_name = request.data['route_name']
        # 基准日
        datum_date = request.data['datum_date']
        # 奇偶区分
        parity = request.data['parity']
        # 获取员工id
        emp_id = request.data['emp_id']

        # 获取需要更新的路线
        route = WaterModel_Route.objects.get(route_id=route_id)
        route.datum_date = datum_date
        route.route_name = route_name
        route.parity_distinction = parity
        route.emp_id = emp_id
        route.save()

        # 取得该路线对应的任务
        works = WaterModel_Work.objects.filter(route_id=route_id)
        # 如果存在任务
        if works.__len__() > 0:
            # 循环任务
            for work in works:
                # 更新任务员工id
                work.emp_id = emp_id
                work.save()
                # 取得任务详细
                worklists = WaterModel_WorkList.objects.filter(work_id=work.work_id)
                for worklist in worklists:
                    # 更新任务详细员工id
                    worklist.emp_id = emp_id
                    worklist.save()
        ret = Pc_status.update_route_success
        return ret

    # 删除路线
    def delete_route(self, request):
        # 路线id
        route_id = request.data['route_id']

        # 取得对应路线详细
        routelists = WaterModel_RouteList.objects.filter(route_id=route_id)
        # 删除所有该路线id下的路线详细与水表信息
        for route in routelists:
            routelist_id = WaterModel_RouteListSerializer(route).get('routelist_id')
            # 删除水表信息
            WaterModel_Meter.objects.filter(routelist_id=routelist_id).delete()
        # 删除路线详细
        routelists.delete()

        # 删除所有改路线id下的任务与任务详细
        works = WaterModel_Work.objects.filter(route_id=route_id)
        for work in works:
            work_id = WaterModel_WorkSerializer(work).get('work_id')
            # 删除任务详细
            WaterModel_WorkList.objects.filter(work_id=work_id).delete()
        # 删除任务
        works.delete()
        # 删除路线
        WaterModel_Route.objects.get(route_id=route_id).delete()
        # 返回状态
        ret = Pc_status.delete_route_success
        return ret
