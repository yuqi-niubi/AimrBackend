# encoding: utf-8
"""
@author: hanjq
@software: PyCharm
@file: TaskConfirm.py
@time: 2020/10/19 14:30
"""
from django.db.models import Q
from aimr_backend.settings import err_logger
from django.http import JsonResponse
from rest_framework.views import APIView
from aimr_platform.common.Error import Error
from aimr_platform.models import WaterModel_Work, WaterModel_WorkList
from aimr_platform.status import App_status


# 获取是否有新任务
class TaskConfirmAPI(APIView):

    def post(self, request):
        """
            获取是否有新任务
            :param request:
            :return:
        """
        try:
            # 取得员工id
            emp_id = request.data['emp_id']
            # 取得该员工的任务
            works = WaterModel_Work.objects.filter(Q(emp_id=emp_id) & Q(work_accept_flag='01'))
            if works.__len__() > 0:
                ret = App_status.have_task
                # 任务详细表查询有多少个任务
                work_count = 0
                for work in works:
                    work_count += WaterModel_WorkList.objects.filter(Q(work_id=work.work_id) &
                                                                     Q(download_flg='0')).__len__()
                # 有新任务时，返回任务个数
                ret['result_data'] = {
                    'result': True,
                    'work_count': work_count
                }
            else:
                # 有新任务时，返回任务个数0
                ret = App_status.have_no_task
                ret['result_data'] = {
                    'result': False,
                    'work_count': 0
                }

        except Exception as e:
            # 输出log日志并且返回状态
            err_logger.error(str(e))
            ret = Error.catchError('500', str(e))
        return JsonResponse(ret)
