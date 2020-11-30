# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: Portal.py
@time: 2020/9/28 15:30
"""
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_platform.common.Error import Error
from aimr_platform.models import WaterModel_Route, WaterModel_Work, WaterModel_Emp, WaterModel_RouteList, \
    WaterModel_WorkList
from aimr_backend.settings import err_logger
from aimr_platform.serializer.emp import WaterModel_EmpSerializer
from aimr_platform.serializer.route import WaterModel_RouteSerializer
from aimr_platform.serializer.work import WaterModel_WorkSerializer
from aimr_platform.status import Pc_status


# ポータル初期化
class PortalAPI(APIView):

    # 「ポータル」页面初期化
    def get(self, request):
        """
            「ポータル」页面初期化
            :param request:
            :return:
        """
        try:
            # token暂时未利用
            # token = request.META.get("HTTP_AUTHORIZATION")
            # obj = TokenCheck.token_check(token)
            obj = True
            if obj:
                # 当期年月
                date_ym = request.GET.get('date_ym')

                # 前年年月取得
                date_ym_last = str(int(date_ym[0:4]) - 1) + str(date_ym[4:])
                # 今年数据
                this_year = self.exception_summary(date_ym)
                # 前年数据
                last_year = self.exception_summary(date_ym_last)
                # meters = self.layout_init_meter(date_ym)

                # 返回状态及数据
                ret = Pc_status.get_portal_data_success
                ret['result_data'] = {
                    'this_year': this_year,
                    'last_year': last_year
                }
            else:
                ret = Pc_status.emp_expired_status
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret, safe=False)

    # 「ポータル」页面初期化
    def exception_summary(self, date_ym):
        # 年月
        thismon = date_ym
        # 判断前月月份
        if thismon[4:] == '01':
            lastmon = str(int(thismon[0:4]) - 1) + '12'
        else:
            lastmon = int(thismon) - 1

        # 满足条件则正常查询
        workerrs = WaterModel_Work.objects.filter(Q(work_batch_ym=thismon) |
                                                  Q(work_batch_ym=lastmon))
        # 三种状态单一计数
        work_met_c = 0
        work_mis_c = 0
        work_wat_c = 0

        # 当前月三种状态计数
        work_thismon_met_c = 0
        work_thismon_mis_c = 0
        work_thismon_wat_c = 0

        # 前月三种状态计数
        work_lastmon_met_c = 0
        work_lastmon_mis_c = 0
        work_lastmon_wat_c = 0

        # 默认为空
        data = {
            'data_list': '',
            'sum_undone': 0,
            'sum_finish': 0,
        }
        # 如果查询到数据
        if workerrs.__len__() > 0:
            # 根据任务表查询数据
            _list = []
            for work in workerrs:
                # メーター故障 数
                work_lists_met = WaterModel_WorkList.objects.filter(
                    Q(work_id=work.work_id) & Q(meter_reading_status='91'))
                if work_lists_met.__len__() > 0:
                    work_met_c += work_lists_met.__len__()
                # 誤検針可能 数
                work_lists_mis = WaterModel_WorkList.objects.filter(
                    Q(work_id=work.work_id) & Q(meter_reading_status='92'))
                if work_lists_mis.__len__() > 0:
                    work_mis_c += work_lists_mis.__len__()

                # 漏水可能 数
                work_lists_wat = WaterModel_WorkList.objects.filter(
                    Q(work_id=work.work_id) & Q(meter_reading_status='93'))
                if work_lists_wat.__len__() > 0:
                    work_wat_c += work_lists_wat.__len__()

                # 如果为当期
                if work.work_batch_ym == thismon:

                    work = WaterModel_WorkSerializer(work)
                    # 查询路线
                    route = WaterModel_Route.objects.get(route_id=work.get('route_id'))

                    # 查询员工
                    emp = WaterModel_Emp.objects.get(emp_id=route.emp_id)

                    # 查询该任务下总任务详细条数
                    count_route = WaterModel_WorkList.objects.filter(work_id=work.get('work_id')).__len__()

                    # 查询已完成抄表水表数
                    finish = WaterModel_WorkList.objects.filter(work_id=work.get('work_id')). \
                        exclude(Q(recognition_type=None) |
                                Q(recognition_type='')).__len__()

                    # 返回数据
                    retdata = {
                        'route': WaterModel_RouteSerializer(route).get('route_name'),
                        'emp': WaterModel_EmpSerializer(emp).get('emp_name'),
                        'count': count_route,
                        'finish': finish,
                        'fail': count_route - finish
                    }
                    # 追加到数组
                    _list.append(retdata)
                    # 未完成件数
                    sum_undone = 0
                    # 完成件数
                    sum_finish = 0
                    # 循环并统计件数
                    for i in range(_list.__len__()):
                        sum_undone += _list[i].get('fail')
                        sum_finish += _list[i].get('finish')
                    data = {
                        'data_list': _list,
                        'sum_undone': sum_undone,
                        'sum_finish': sum_finish,
                    }
                    # 当月メーター故障 数
                    work_thismon_met_c += work_met_c
                    # 当月誤検針可能 数
                    work_thismon_mis_c += work_mis_c
                    # 当月漏水可能 数
                    work_thismon_wat_c += work_wat_c
                    # 清空
                    work_met_c = 0
                    work_mis_c = 0
                    work_wat_c = 0
                else:
                    # 前月メーター故障 数
                    work_lastmon_met_c += work_met_c
                    # 前月誤検針可能 数
                    work_lastmon_mis_c += work_mis_c
                    # 前月漏水可能 数
                    work_lastmon_wat_c += work_wat_c
                    # 清空
                    work_met_c = 0
                    work_mis_c = 0
                    work_wat_c = 0
        # 数据放入字典
        datalist = {
            'data': data,
            'err_list': {
                'month_scale': {
                    '91': {
                        'this_month_count': work_thismon_met_c,
                        'last_month_count': work_lastmon_met_c
                    },
                    '92': {
                        'this_month_count': work_thismon_mis_c,
                        'last_month_count': work_lastmon_mis_c
                    },
                    '93': {
                        'this_month_count': work_thismon_wat_c,
                        'last_month_count': work_lastmon_wat_c
                    }
                },
            }
        }
        # 返回数据
        return datalist
