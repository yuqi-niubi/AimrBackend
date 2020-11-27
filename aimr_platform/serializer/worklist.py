# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: worklist.py
@time: 2020/9/28 11:00
"""

from typing import Dict, Any
from aimr_platform.models import WaterModel_WorkList


def WaterModel_WorkListSerializer(worklist: WaterModel_WorkList) -> Dict[str, Any]:
    return{
        'work_details_id': worklist.work_details_id,
        'meter_reading_date': worklist.meter_reading_date,
        'meter_count': worklist.meter_count,
        'meter_count_last': worklist.meter_count_last,
        'meter_reading_status': worklist.meter_reading_status,
        'meter_cust_no': worklist.meter_cust_no,
        'meter_cust_name': worklist.meter_cust_name,
        'meter_cust_add': worklist.meter_cust_add,
        'meter_cust_tel': worklist.meter_cust_tel,
        'recognition_type': worklist.recognition_type,
        'img_name': worklist.img_name,
        'unusual_report_date': worklist.unusual_report_date,
        'unusual_status': worklist.unusual_status,
        'unusual_report_read_status': worklist.unusual_report_read_status,
        'meter_customer_status': worklist.meter_customer_status,
        'download_flg': worklist.download_flg,
        'emp_id': worklist.emp_id,
        'work_id': worklist.work_id,
        'meter_id': worklist.meter_id,
    }














#
# from rest_framework import worklist
# from aimr_platform.models import WaterModel_WorkList
#
#
# # 用户数据format方法
# class WaterModel_WorkListSerializer(worklist.Serializer):
#     work_details_id: worklist.IntegerField
#     meter_reading_date: worklist.DateField
#     meter_count: worklist.CharField
#     meter_count_last: worklist.CharField
#     meter_reading_status: worklist.CharField
#     meter_cust_no: worklist.CharField
#     meter_cust_name: worklist.CharField
#     meter_cust_add: worklist.CharField
#     meter_cust_tel: worklist.CharField
#     recognition_type: worklist.CharField
#     img_name: worklist.CharField
#     unusual_report_date: worklist.DateField
#     unusual_status: worklist.CharField
#     unusual_report_read_status: worklist.CharField
#     meter_customer_status: worklist.CharField
#     download_flg: worklist.CharField
#     emp_id: worklist.PrimaryKeyRelatedField(read_only:'True')
#     message_id: worklist.PrimaryKeyRelatedField(read_only:'True')
#     work_id: worklist.PrimaryKeyRelatedField(read_only:'True')
#     meter_id: worklist.PrimaryKeyRelatedField(read_only:'True')
#
