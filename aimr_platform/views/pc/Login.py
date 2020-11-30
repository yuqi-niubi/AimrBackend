# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: Login.py
@time: 2020/9/25 11:30
"""
import base64
import hashlib
import hmac
import json
from datetime import timedelta, datetime
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_backend.settings import pro_logger, err_logger, emp_avatar_file_path
from aimr_platform.common.Error import Error
from aimr_platform.models import WaterModel_Emp, WaterModel_WorkList
from aimr_platform.serializer.emp import WaterModel_EmpSerializer
from aimr_platform.status import Pc_status
from aimr_platform.status import App_status


# 员工操作API
class LoginAPI(APIView):
    # 员工登录
    def get(self, request):
        """
            员工登录
            :param request:
            emp_code: 员工账号
            emp_password: 员工密码
            :return:
        """
        try:
            pro_logger.info('开始登录')
            emp_code = request.GET.get('emp_code')
            emp_password = request.GET.get('emp_password')
            # 员工角色
            emp_role = '01'
            # 通过员工账号与员工密码查询对应数据
            pro_logger.info('校验账号与密码')
            emp_token = ''
            # web端登录
            ret = self.emp_login(emp_code, emp_password, emp_role, emp_token)
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    # 员工信息更新以及手机端登录
    def post(self, request):
        """
           员工信息更新以及手机端登录
           :param request:
           :return:
       """
        try:
            # 取得flg
            flg = request.data['flg']
            # 手机端登录
            if flg == 'mobile':
                # 员工账号
                emp_code = request.data['emp_code']
                # 员工密码
                emp_password = request.data['emp_password']
                # firebase token
                emp_token = request.data['emp_token']
                # 员工角色
                emp_role = '02'
                ret = self.emp_login(emp_code, emp_password, emp_role, emp_token)
            # 开始事务
            # 更新员工信息
            elif flg == 'update':
                with transaction.atomic():
                    # 员工id
                    emp_id = request.data['emp_id']
                    # 密码
                    emp_password = request.data['emp_password']
                    # 电话
                    emp_tel = request.data['emp_tel']
                    # 取得员工情报
                    emp_info = WaterModel_Emp.objects.get(emp_id=emp_id)
                    # 员工情报设定
                    emp_info.emp_password = emp_password
                    emp_info.emp_tel = emp_tel
                    # 更新
                    emp_info.save()
                    # 返回状态
                    ret = App_status.user_info_success
        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)

    # 员工登录
    def emp_login(self, emp_code, emp_password, emp_role, emp_token):
        emp = WaterModel_Emp.objects.filter(Q(emp_code=emp_code) &
                                            Q(emp_password=emp_password) &
                                            Q(emp_role=emp_role))

        # 如果数据条数等于1，遍历该条数据
        if emp.__len__() == 1:
            # 更新前回登陆时间
            emp[0].last_login_time = emp[0].login_time
            # 更新登录时间
            emp[0].login_time = datetime.now()
            # 如果是抄表员的话
            if emp_role == '02':
                emp[0].emp_token = emp_token
            # 保存到数据库
            emp[0].save()
            # 返回数据数组
            _list = [WaterModel_EmpSerializer(emp[0])]

            # 时间format
            last_login_time = str(_list[0].__getitem__('last_login_time')).replace('T', ' ')[:16]
            login_time = str(_list[0].__getitem__('login_time')).replace('T', ' ')[:16]

            # 设定返回数据中的相关时间
            _list[0].__setitem__('last_login_time', last_login_time)
            _list[0].__setitem__('login_time', login_time)
            if emp_role == '01':
                # 获取当前用户头像
                _name = _list[0].get('emp_img_name')
                # 获取员工头像
                with open(emp_avatar_file_path + _name, 'rb') as f:
                    image_data = f.read()
                    image_data = str(base64.b64encode(image_data), encoding='utf-8')
                # base64拼接
                imagedata = "data:image/png;base64," + str(image_data).replace('b\'', '').replace('\'', '')
            else:
                imagedata = ''
            # 返回状态以及数据
            ret = Pc_status.login_success
            ret['result_data'] = {
                'emp_list': _list[0],
                'imgdata': imagedata
            }
        else:
            ret = Pc_status.login_fail
        return ret

    # 生成token，暂时未使用
    def encode_token(self, emp={}):
        # 开始事务
        with transaction.atomic():
            header = {'typ': 'JWT', 'alg': 'HS256'}
            header = base64.b64encode(json.dumps(header).encode()).decode()

            payload_info = {
                'exp': str(datetime.now() + timedelta(days=0, seconds=30 * 6)),
                'iat': str(datetime.now()),
                'user_id': emp.get('emp_id'),
                'user_name': emp.get('emp_name')
            }

            payload = base64.b64encode(json.dumps(payload_info).encode()).decode()
            secret = 'dxw.com'
            message = header + '.' + payload
            h_obj = hmac.new(secret.encode(), message.encode(), hashlib.sha256)
            signature = h_obj.hexdigest()
            token = message + '.' + signature
            emp_id = emp.get('emp_id')
            emp = WaterModel_Emp.objects.get(emp_id=emp_id)
            emp.emp_token = token
            emp.token_create_time = payload_info.get('iat')
            emp.token_expired_time = payload_info.get('exp')
            emp.save()
        return token

    # 批量更改数据用，请勿删改
    # def delete(self, request):
    #
    #     # count_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    #     # works = WaterModel_WorkList.objects.filter(Q(work_id='107'))
    #     #
    #     # img_name = ['987.jpg', '789.jpg', '654.jpg', '456.jpg',
    #     #             '432.jpg', '543.jpg', '321.jpg', '123.jpg']
    #     # recognition_type = ['00', '01', '02']
    #     # for work in works:
    #     #     rand = random.randint(0, 10000)
    #     #     work.meter_reading_date = datetime.now()
    #     #     work.meter_reading_status = '20'
    #     #     work.meter_count = str(rand).rjust(4, '0')
    #     #     work.recognition_type = recognition_type[random.randint(0, 2)]
    #     #     work.img_name = img_name[random.randint(0, 7)]
    #     #     work.meter_count_last = str(rand - (count_list[random.randint(0, 19)] - 20)).rjust(4, '0')
    #     #     if int(work.meter_count) - int(work.meter_count_last) > 20 or int(work.meter_count) - int(work.meter_count_last) < 0:
    #     #         work.meter_reading_status = '81'
    #     #     work.save()
    #
    #     works = WaterModel_WorkList.objects.all()
    #     for work in works:
    #         if work.meter_count != '--':
    #             work.meter_count = str(work.meter_count).rjust(4, '0')
    #         if work.meter_count_last != '--':
    #             work.meter_count_last = str(work.meter_count_last).rjust(4, '0')
    #         work.save()
    #     return JsonResponse({'code': '200'})
