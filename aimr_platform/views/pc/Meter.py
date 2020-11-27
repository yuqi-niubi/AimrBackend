# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: Meter.py
@time: 2020/9/28 14:30
"""
import base64
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_platform.common.Error import Error
from aimr_platform.models import WaterModel_Route, WaterModel_Work, WaterModel_Emp, WaterModel_RouteList, \
    WaterModel_WorkList, WaterModel_Meter, WaterMaster_MeterWork, WaterMaster_WorkRecognition, \
    WaterMaster_UnusualStatus, WaterModel_MeterType
from aimr_backend.settings import pro_logger, err_logger, meter_file_path
from aimr_platform.serializer.emp import WaterModel_EmpSerializer
from aimr_platform.serializer.meter import WaterModel_MeterSerializer
from aimr_platform.serializer.metertype import WaterModel_MeterTypeSerializer
from aimr_platform.serializer.route import WaterModel_RouteSerializer
from aimr_platform.serializer.worklist import WaterModel_WorkListSerializer
from aimr_platform.status import Pc_status


# 検針データ相关
class MeterAPI(APIView):

    def get(self, request):
        """
            検針データ下拉框与検針データ检索
            :param request:
            :return:
        """
        try:
            # 取得flg
            flg = request.GET.get('flg')
            # 获取所有抄表员以及路线信息
            if flg == 'selemproute':
                ret = self.search_emp_route()
            # 获取对应抄表员的路线
            elif flg == 'selroutes':
                emp_id = request.GET.get('emp_id')
                ret = self.search_route(emp_id)
            # 获取当前路线下抄表员信息(当前未利用)
            elif flg == 'selemps':
                route_id = request.GET.get('route_id')
                ret = self.search_emps(route_id)
            # 取得照会图片
            elif flg == 'imgopen':
                imgname = request.GET.get('imgname')
                ret = self.open_image(imgname)
            # システムアラート一覧
            elif flg == 'alert':
                # 每页显示多少条数据
                page_data_count = request.GET.get('page_data_count')
                # 第几页
                page_count = request.GET.get('page_count')
                # 取得init_flg
                init_flg = request.GET.get('init_flg')
                ret = self.alert(int(page_data_count), int(page_count), init_flg)
            # 検針員異常報告
            elif flg == 'anomaly':
                # 每页显示多少条数据
                page_data_count = request.GET.get('page_data_count')
                # 第几页
                page_count = request.GET.get('page_count')
                # 取得init_flg
                init_flg = request.GET.get('init_flg')
                ret = self.anomaly(int(page_data_count), int(page_count), init_flg)
            # 获得水表类型
            elif flg == 'metertype':
                ret = self.get_metertype()
            else:
                ret = Pc_status.get_meter_reading_data_fail
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def post(self, request):
        """
            検針データ检索与お客様新規
            :param request:
            :return:
        """
        try:
            flg = request.data['flg']
            # 検針データ检索
            if flg == 'search':
                # 每页显示多少条数据
                page_data_count = request.data['page_data_count']
                # 第几页
                page_count = request.data['page_count']
                # 当期检索
                thisym = request.data['thisym']
                # 区间检索
                fromym = request.data['fromym']
                todate = request.data['todate']
                # 抄表状态
                read_status = request.data['read_status']
                # 识别方式
                recognition_type = request.data['recognition_type']
                # 抄表员id
                emp_id = request.data['emp_id']
                # 路线id
                route_id = request.data['route_id']
                # 关键字
                key_word = request.data['key_word']
                # 关键字对应字段
                key_word_val = request.data['key_word_val']

                # 检索条件字典
                search_dict = dict()
                # 如果read_status存在，放入到检索条件字典里
                if len(read_status) > 0:
                    search_dict['meter_reading_status'] = read_status
                # 如果recognition_type存在，放入到检索条件字典里
                if len(recognition_type) > 0:
                    search_dict['recognition_type'] = recognition_type
                # 如果emp_id存在，放入到检索条件字典里
                if len(str(emp_id)) > 0:
                    search_dict['emp_id'] = emp_id

                # 如果关键字为None,则给初始值
                if key_word is None:
                    # 关键字类型(姓名，地址，电话。。。)
                    key_word = ''
                    # 关键字是什么
                    key_word_val = ''
                # 如果当前年月存在则查询当期
                if thisym is not None and len(thisym) > 0:
                    ret = self.search_list(thisym, None,
                                           search_dict, key_word, key_word_val, int(page_data_count),
                                           int(page_count), route_id)
                # 如果fromym与todate存在，则查询区间
                elif fromym is not None and todate is not None and len(fromym) > 0 and len(todate) > 0:
                    ret = self.search_list(fromym, todate,
                                           search_dict, key_word, key_word_val, int(page_data_count),
                                           int(page_count), route_id)
                # 否则查询关键字
                else:
                    ret = self.search_list(None, None,
                                           search_dict, key_word, key_word_val, int(page_data_count),
                                           int(page_count), route_id)
            # お客様新規
            elif flg == 'create':
                # 开始事务
                with transaction.atomic():
                    ret = self.create_meter(request)
            # 其他场合
            else:
                ret = Pc_status.get_meter_reading_data_fail

        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def put(self, request):
        """
            お客様更新
            :param request:
            :return:
        """
        try:
            # 开始事务
            with transaction.atomic():
                ret = self.update_meter(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    def delete(self, request):
        """
            お客様削除
            :param request:
            :return:
        """
        try:
            # 开始事务
            with transaction.atomic():
                ret = self.delete_meter(request)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    # 検針データ検索結果
    def search_list(self, begym, endym, search_dict, key_word, key_word_val, page_data_count, page_count, route_id):
        # 选择为すべて
        if begym is None and endym is None:
            # 如果画面未指定ルート
            if route_id == '' or route_id is None:
                works = WaterModel_Work.objects.all().order_by('emp_id')
            else:
                works = WaterModel_Work.objects.filter(route_id=route_id).order_by('emp_id')
        # 当期或前期
        elif endym is None:
            # 如果画面未指定ルート
            if route_id == '' or route_id is None:
                works = WaterModel_Work.objects.filter(Q(work_batch_ym=begym)).order_by('emp_id')
            else:
                works = WaterModel_Work.objects.filter(Q(work_batch_ym=begym) & Q(route_id=route_id)).order_by('emp_id')
        # 区间检索
        else:
            # 如果画面未指定ルート
            if route_id == '' or route_id is None:
                works = WaterModel_Work.objects.filter(Q(work_batch_ym__range=[begym, endym])).order_by('emp_id')
            else:
                works = WaterModel_Work.objects.filter(
                    Q(work_batch_ym__range=[begym, endym]) & Q(route_id=route_id)).order_by('emp_id')
        datalistAll = []
        for work in works:

            # 关键字为お客様番号
            if key_word == 'meter_customer_no':
                work_lists = WaterModel_WorkList.objects.filter(Q(work_id=work.work_id) &
                                                                Q(**search_dict) &
                                                                Q(meter_cust_no__contains=key_word_val)
                                                                )
            # 关键字为お客様名
            elif key_word == 'meter_customer_name':
                work_lists = WaterModel_WorkList.objects.filter(Q(work_id=work.work_id) &
                                                                Q(**search_dict) &
                                                                Q(meter_cust_name__contains=key_word_val)
                                                                )
            # 关键字为住所
            elif key_word == 'meter_customer_address':
                work_lists = WaterModel_WorkList.objects.filter(Q(work_id=work.work_id) &
                                                                Q(**search_dict) &
                                                                Q(meter_cust_add__contains=key_word_val)
                                                                )
            # 关键字为電話
            elif key_word == 'meter_customer_tel':
                work_lists = WaterModel_WorkList.objects.filter(Q(work_id=work.work_id) &
                                                                Q(**search_dict) &
                                                                Q(meter_cust_tel__contains=key_word_val)
                                                                )
            # 未选择关键字
            else:
                work_lists = WaterModel_WorkList.objects.filter(Q(work_id=work.work_id) &
                                                                Q(**search_dict)
                                                                )
            if len(work_lists) > 0:
                for worklist in work_lists:
                    work_arr = WaterModel_WorkListSerializer(worklist)
                    # 如果抄表日为None，设为空字符串
                    if work_arr.get('meter_reading_date') is None:
                        work_arr.__setitem__('meter_reading_date', '')
                    else:
                        work_arr.__setitem__('meter_reading_date', str(work_arr.get('meter_reading_date')))
                    datalistAll.append(work_arr)
        # 分页起止点
        data_from = (int(page_count) - 1) * int(page_data_count)
        data_to = (int(page_count) - 1) * int(page_data_count) + int(page_data_count)
        # 分页数据
        datalistAll = sorted(datalistAll, key=lambda keys: keys['meter_reading_date'], reverse=True)
        datalist = datalistAll[data_from:data_to]
        for i in range(len(datalist)):
            datalist[i].__setitem__('index_no', data_from + 1)
            data_from += 1
            # 判断抄表状态
            if datalist[i].get('meter_reading_status'):
                meter_work_name = \
                    WaterMaster_MeterWork.objects.get(meter_work_id=
                                                      datalist[i].get('meter_reading_status')).meter_work_name
                # 将code转为汉字
                datalist[i].__setitem__('meter_reading_status', meter_work_name)
            # 判断抄表方式
            if datalist[i].get('recognition_type'):
                recognition_work_name = WaterMaster_WorkRecognition.objects.get(recognition_work_id=
                                                                                datalist[i].get(
                                                                                    'recognition_type')).recognition_work_name
                # 将code转为汉字
                datalist[i].__setitem__('recognition_type', recognition_work_name)
            # 取得员工名
            emp_name = WaterModel_Emp.objects.get(emp_id=datalist[i].get('emp_id')).emp_name
            # 设定员工名
            datalist[i].__setitem__('emp_id', emp_name)
            # 判断抄表数
            if datalist[i].get('meter_count') != '--' and int(datalist[i].get('meter_count')) > 0:
                # 设定用水量
                datalist[i].__setitem__('use_water',
                                        int(datalist[i].get('meter_count')) - int(datalist[i].get('meter_count_last')))
            else:
                datalist[i].__setitem__('use_water', '--')

        # 返回状态及数据
        ret = Pc_status.get_meter_reading_data_success
        ret['result_data'] = {
            'datalist': datalist,
            'datalist_count': datalistAll.__len__(),
        }
        return ret

    # システムアラート一覧
    def alert(self, page_data_count, page_count, init_flg):
        # 取得所有任务详细按照时间倒序,如果为初期化,则返回总条数,否则为0
        if init_flg == 'init':
            worklists = WaterModel_WorkList.objects.filter(meter_reading_status=81).order_by('-meter_reading_date')
            # 数据总条数
            _list_count = worklists.__len__()
            # 分页数据
            worklists = \
                worklists[
                (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(page_data_count) + int(
                    page_data_count)]
        else:
            # 分页数据
            worklists = WaterModel_WorkList.objects.filter(meter_reading_status=81).order_by('-meter_reading_date')[
                        (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(page_data_count) + int(
                            page_data_count)]
            _list_count = 0

        datalist = []
        # 数组下标
        i = 0
        index_no = (int(page_count) - 1) * int(page_data_count) + 1
        for worklist in worklists:
            worklist = WaterModel_WorkListSerializer(worklist)
            datalist.append(worklist)
            # 判断抄表状态
            if datalist[i].get('meter_reading_status'):
                # 修改对应code为汉字
                meter_reading_name = \
                    WaterMaster_MeterWork.objects.get(meter_work_id=
                                                      datalist[i].get('meter_reading_status')).meter_work_name
                datalist[i].__setitem__('meter_reading_status', meter_reading_name)
            # 判断抄表方式
            if datalist[i].get('recognition_type'):
                recognition_work_name = WaterMaster_WorkRecognition.objects.get(recognition_work_id=
                                                                                datalist[i].get(
                                                                                    'recognition_type')).recognition_work_name
                # 修改对应code为汉字
                datalist[i].__setitem__('recognition_type', recognition_work_name)

            emp_name = WaterModel_Emp.objects.get(emp_id=datalist[i].get('emp_id')).emp_name
            # 更新emp_id为员工名
            datalist[i].__setitem__('emp_id', emp_name)

            # index_no
            datalist[i].__setitem__('index_no', index_no)
            index_no = index_no + 1

            # 判断当期用水量
            if datalist[i].get('meter_count') != '--' and int(datalist[i].get('meter_count')) > 0:
                datalist[i].__setitem__('use',
                                        int(datalist[i].get('meter_count')) - int(datalist[i].get('meter_count_last')))
            else:
                datalist[i].__setitem__('use', '--')
            i += 1

        # 返回状态以及数据
        ret = Pc_status.get_meter_reading_data_success
        ret['result_data'] = {
            'datalist': datalist,
            'datalist_count': _list_count,
        }
        return ret

    # 検針員異常報告
    def anomaly(self, page_data_count, page_count, init_flg):
        # 查询符合条件的任务详细数据,如果为初期化,则返回总条数,否则为0
        if init_flg == 'init':
            worklists = WaterModel_WorkList.objects.filter(Q(meter_reading_status='91') |
                                                           Q(meter_reading_status='92') |
                                                           Q(meter_reading_status='93')).order_by(
                'unusual_status', '-unusual_report_date')
            # 数据总条数
            _list_count = worklists.__len__()
            # 分页数据
            worklists = \
                worklists[
                (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(
                    page_data_count) + int(page_data_count)]
        else:
            # 分页数据
            worklists = WaterModel_WorkList.objects.filter(Q(meter_reading_status='91') |
                                                           Q(meter_reading_status='92') |
                                                           Q(meter_reading_status='93')).order_by(
                'unusual_status', '-unusual_report_date')[
                        (int(page_count) - 1) * int(page_data_count):(int(page_count) - 1) * int(
                            page_data_count) + int(page_data_count)]
            _list_count = 0

        datalist = []
        for worklist in worklists:
            worklist = WaterModel_WorkListSerializer(worklist)
            datalist.append(worklist)

        index_no = (int(page_count) - 1) * int(page_data_count) + 1

        for i in range(0, len(datalist)):
            # 判断抄表状态
            if datalist[i].get('meter_reading_status'):
                meter_work_name = WaterMaster_MeterWork.objects.get(meter_work_id=
                datalist[i].get(
                    'meter_reading_status')).meter_work_name
                # 修改对应code为汉字
                datalist[i].__setitem__('meter_reading_status', meter_work_name)
            # 判断抄表方式
            if datalist[i].get('recognition_type'):
                recognition_work_name = WaterMaster_WorkRecognition.objects.get(recognition_work_id=
                datalist[i].get(
                    'recognition_type')).recognition_work_name
                # 修改对应code为汉字
                datalist[i].__setitem__('recognition_type', recognition_work_name)
            # 判断异常状态
            if datalist[i].get('unusual_status'):
                unusual_status_name = WaterMaster_UnusualStatus.objects.get(unusual_status_id=
                datalist[i].get(
                    'unusual_status')).unusual_status_name
                # 修改对应code为汉字
                datalist[i].__setitem__('unusual_status_name', unusual_status_name)
            # 修改emp_id为对应员工名
            emp_name = WaterModel_Emp.objects.get(emp_id=datalist[i].get('emp_id')).emp_name
            datalist[i].__setitem__('emp_id', emp_name)

            # index_no
            datalist[i].__setitem__('index_no', index_no)
            index_no = index_no + 1

        # 返回状态以及数据
        ret = Pc_status.get_meter_reading_data_success
        ret['result_data'] = {
            'datalist': datalist,
            'datalist_count': _list_count,
        }
        return ret

    # 获取对应抄表员的路线
    def search_route(self, _eid):
        routelist = []
        # 取得抄表员对应的所有路线
        routes = WaterModel_Route.objects.filter(emp_id=_eid)
        for route in routes:
            routelist.append(WaterModel_RouteSerializer(route))
        # 返回状态以及数据
        ret = Pc_status.get_meter_reading_data_success
        ret['result_data'] = {
            'routelist': routelist,
        }
        return ret

    # 获取当前路线下抄表员信息，未利用
    def search_emps(self, _rid):
        emplist = []
        # 取得路线
        route = WaterModel_Route.objects.get(route_id=_rid)
        # 取得抄表员
        emp = WaterModel_Emp.objects.get(emp_id=route.emp_id)
        emplist.append(WaterModel_EmpSerializer(emp))
        # 返回状态以及数据
        ret = Pc_status.get_meter_reading_data_success
        ret['result_data'] = {
            'emps': emplist
        }
        return ret

    # 获取所有抄表员以及路线信息
    def search_emp_route(self):
        # 返回数组初期化
        emplist = []
        routelist = []

        # 取得所有抄表员
        emps = WaterModel_Emp.objects.all().exclude(emp_role='01')
        # 循环追加到数组
        for emp in emps:
            emplist.append(WaterModel_EmpSerializer(emp))
        # 取得所有route
        routes = WaterModel_Route.objects.all()
        # 循环追加到数组
        for route in routes:
            routelist.append(WaterModel_RouteSerializer(route))
        # 返回状态以及数据
        ret = Pc_status.get_meter_reading_data_success
        ret['result_data'] = {
            'emps': emplist,
            'routes': routelist
        }
        return ret

    # 取得照会图片
    def open_image(self, _name):
        # 从服务器取得数据,暂时未利用
        # fs = Fileoperate.FileOperate()
        # res = fs.readfile('meter', _name)
        # # 将数据转码
        # image_data = base64.b64encode(res.read())

        # 取得对应抄表图片
        with open(meter_file_path + _name, 'rb') as f:
            image_data = f.read()
            image_data = str(base64.b64encode(image_data), encoding='utf-8')
        # 拼接base64
        imagedata = "data:image/png;base64," + str(image_data).replace('b\'', '').replace('\'', '')
        # 返回状态以及数据
        ret = Pc_status.get_meter_reading_data_success
        ret['result_data'] = imagedata
        return ret

    # 获得水表类型
    def get_metertype(self):
        # 获取所有水表类型
        types = WaterModel_MeterType.objects.all()
        # 返回数据数组
        list_type = []
        # 循环并追加到数组
        for _type in types:
            _type = WaterModel_MeterTypeSerializer(_type)
            list_type.append(_type)
        # 返回状态以及数据
        ret = Pc_status.get_meter_reading_data_success
        ret['result_data'] = {
            'list_type': list_type
        }
        return ret

    # お客様新規
    def create_meter(self, request):
        # 路线详细id
        routelist_id = request.data['routelist_id']
        # お客様番号
        meter_customer_no = request.data['customer_no']
        # 水表号
        meter_no = request.data['meter_no']
        # お客様名
        meter_customer_name = request.data['customer_name']
        # お客様地址
        meter_customer_address = request.data['customer_address']
        # お客様电话
        meter_customer_tel = request.data['customer_tel']
        # 水表类型
        metertype = request.data['metertype']
        # 使用期间
        meter_use_during_from = request.data['during_from']
        meter_use_during_to = request.data['during_to']
        # 判断お客様与メーター番号是否存在
        meter_exist = WaterModel_Meter.objects.filter(Q(meter_no=meter_no) |
                                                      Q(meter_customer_no=meter_customer_no))
        # 如果存在，则创建失败，否则保存到数据库
        if meter_exist.__len__() > 0:
            meter_no_exist = WaterModel_MeterSerializer(meter_exist).get('meter_no')
            meter_customer_no_exist = WaterModel_MeterSerializer(meter_exist).get('meter_customer_no')
            # 如果お客様存在
            if meter_no_exist == meter_no:
                ret = Pc_status.create_meter_fail_customer
            # 如果メーター番号是否存在
            elif meter_customer_no_exist == meter_customer_no:
                ret = Pc_status.create_meter_fail_meter
            # 如果お客様与メーター番号都存在
            else:
                ret = Pc_status.create_meter_fail
        else:
            # 写入数据库
            meter = WaterModel_Meter(
                meter_customer_no=meter_customer_no,
                meter_no=meter_no,
                meter_qr_code=meter_no,
                meter_customer_name=meter_customer_name,
                meter_customer_address=meter_customer_address,
                meter_customer_tel=meter_customer_tel,
                meter_type=metertype,
                meter_use_during_from=meter_use_during_from,
                meter_use_during_to=meter_use_during_to,
                routelist_id=routelist_id
            )
            meter.save()
            # 取得路线详细
            routelist = WaterModel_RouteList.objects.get(routelist_id=routelist_id)
            # 当前路线详细水表数+1
            routelist.meter_count = int(routelist.meter_count) + 1
            routelist.save()
            # 返回状态
            ret = Pc_status.create_meter_success
        return ret

    # お客様更新
    def update_meter(self, request):
        # 水表id
        meter_id = request.data['meter_id']
        # お客様名
        meter_customer_name = request.data['customer_name']
        # お客様地址
        meter_customer_address = request.data['customer_address']
        # お客様电话
        meter_customer_tel = request.data['customer_tel']
        # 水表类型
        metertype = request.data['metertype']
        # 使用期间
        meter_use_during_from = request.data['during_from']
        meter_use_during_to = request.data['during_to']

        # 更新数据库
        meter = WaterModel_Meter.objects.get(meter_id=meter_id)
        meter.meter_customer_name = meter_customer_name
        meter.meter_customer_address = meter_customer_address
        meter.meter_customer_tel = meter_customer_tel
        meter.meter_use_during_from = meter_use_during_from
        meter.meter_use_during_to = meter_use_during_to
        meter.meter_type = metertype
        meter.save()
        # 返回状态
        ret = Pc_status.update_meter_success
        return ret

    # お客様削除
    def delete_meter(self, request):
        # 水表id
        meter_id = request.data['meter_id']
        # 水表信息
        meter = WaterModel_Meter.objects.get(meter_id=meter_id)
        # 获取路线详细id
        routelist_id = WaterModel_MeterSerializer(meter).get('routelist_id')
        # 取得路线详细
        routelist = WaterModel_RouteList.objects.get(routelist_id=routelist_id)
        # 更新该路线水表数
        routelist.meter_count = int(routelist.meter_count) - 1
        # 保存到数据库
        routelist.save()
        # 删除水表
        meter.delete()
        # 返回状态
        ret = Pc_status.delete_meter_success
        return ret
