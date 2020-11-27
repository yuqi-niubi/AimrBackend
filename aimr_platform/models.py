# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: models.py
@time: 2020/9/24 15:30
"""

from django.db import models


# 一般用水水价码表
class WaterMaster_Price_General(models.Model):
    # id
    id = models.AutoField(primary_key=True, blank=False, null=False)
    # 水表口径
    meter_base_size = models.CharField(default=None, max_length=5, blank=False, null=True)
    # 基本水价
    meter_base_price = models.CharField(default=None, max_length=10, blank=False, null=True)
    # 1m³~5m³
    onetothree = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 6m³~10m³
    sixtoten = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 11m³~20m³
    eletotwenty = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 21m³~30m³
    twonetothirty = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 31m³~50m³
    thonetofifty = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 51m³~100m³
    fifonetohun = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 101m³~200m³
    hunonetotwohun = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 201m³~1000m³
    twohunonetohus = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 1001m³以上
    husoneabove = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 用水类型
    meter_usetype = models.CharField(default='一般用', max_length=10, blank=False, null=False)


# 污水水价码表
class WaterMaster_Price_Sewage(models.Model):
    # id
    id = models.AutoField(primary_key=True, blank=False, null=False)
    # 0m³~8m³
    otoeight = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 9m³~20m³
    ninetotwenty = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 21m³~50m³
    twonetofifty = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 51m³~100m³
    fifonetohun = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 101m³~200m³
    hunonetotwohun = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 201m³~500m³
    twohunonetofihun = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 501m³~1000m³
    fihunonetohus = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 1001m³以上
    husoneabove = models.CharField(default=0, max_length=10, blank=False, null=False)
    # 用水类型
    meter_usetype = models.CharField(default='一般污水', max_length=10, blank=False, null=False)


# 员工角色表
class WaterMaster_Role(models.Model):
    # 自增长ID
    id = models.AutoField(primary_key=True, blank=False, null=False)
    # 角色ID
    role_id = models.CharField(default='02', max_length=2, blank=False, null=False)
    # 角色名
    role_name = models.CharField(default='抄表员', max_length=5, blank=True, null=False)


# 员工表
class WaterModel_Emp(models.Model):
    # 员工ID
    emp_id = models.AutoField(primary_key=True, blank=False, null=False)
    # 员工名
    emp_name = models.CharField(default='默认名称', max_length=10, blank=False, null=False)
    # 员工账号
    emp_code = models.CharField(default='0', max_length=10, blank=False, null=False, unique=True)
    # 员工密码
    emp_password = models.CharField(default='0', max_length=10, blank=False, null=False)
    # 员工头像
    emp_img_name = models.TextField(default=None, blank=True, null=True)
    # 员工邮箱
    emp_email = models.CharField(default='', max_length=50, blank=True, null=False)
    # 员工电话
    emp_tel = models.CharField(default='', max_length=20, blank=True, null=False)
    # 员工角色 参照WaterMaster_Role中角色字段
    emp_role = models.CharField(default='02', max_length=5, blank=False, null=False)
    # 登录时间
    login_time = models.DateTimeField(blank=True, null=False)
    # 上次登录时间
    last_login_time = models.DateTimeField(blank=True, null=False)
    # token
    emp_token = models.TextField(default='', blank=True, null=False)
    # token生成时间
    token_create_time = models.DateTimeField(blank=True, null=True)
    # token失效时间
    token_expired_time = models.DateTimeField(blank=True, null=True)


# 路线表
class WaterModel_Route(models.Model):
    # 路线id
    route_id = models.AutoField(primary_key=True, blank=False, null=False)
    # 路线名
    route_name = models.CharField(default='', max_length=10, blank=True, null=False)
    # 基准日
    datum_date = models.CharField(default='', max_length=2, blank=True, null=False)
    # 奇偶区分 1:奇数 2：偶数
    parity_distinction = models.CharField(default='', max_length=1, blank=True, null=True)
    # 员工ID
    emp_id = models.CharField(default='', max_length=50, blank=True, null=True)


# 任务送信码表
class WaterMaster_SendWork(models.Model):
    # id
    id = models.AutoField(primary_key=True, blank=False, null=False)
    # 任务接受ID
    send_work_id = models.CharField(default='01', max_length=2, blank=False, null=False)
    # 任务接受名
    send_work_name = models.CharField(default='なし', max_length=5, blank=False, null=False)


# 任务抄表码表
class WaterMaster_MeterWork(models.Model):
    # id
    id = models.AutoField(primary_key=True, blank=False, null=False)
    # 抄表状态ID
    meter_work_id = models.CharField(default='00', max_length=2, blank=False, null=False)
    # 抄表状态名
    meter_work_name = models.CharField(default='未検針', max_length=10, blank=False, null=False)


# 任务识别码表
class WaterMaster_WorkRecognition(models.Model):
    # id
    id = models.AutoField(primary_key=True, blank=False, null=False)
    # 识别ID
    recognition_work_id = models.CharField(default='00', max_length=2, blank=False, null=False)
    # 识别名
    recognition_work_name = models.CharField(default='自動識別', max_length=5, blank=False, null=False)


# 异常状态码表
class WaterMaster_UnusualStatus(models.Model):
    # id
    id = models.AutoField(primary_key=True, blank=False, null=False)
    # 异常状态ID
    unusual_status_id = models.CharField(default='00', max_length=2, blank=False, null=False)
    # 异常状态名
    unusual_status_name = models.CharField(default='未対応', max_length=5, blank=False, null=False)


# 水表型号码表
class WaterModel_MeterType(models.Model):
    # id
    id = models.AutoField(primary_key=True, blank=False, null=False)
    # 水表型号ID
    meter_type_id = models.CharField(default='00', max_length=5, blank=False, null=False)
    # 水表口径
    meter_caliber = models.CharField(default='13', max_length=5, blank=False, null=False)


# 通知表
class WaterModel_Message(models.Model):
    # id
    id = models.AutoField(primary_key=True, blank=False, null=False)
    # 通知状态
    msg_status = models.CharField(default='01', max_length=2, blank=False, null=False)
    # 通知状态名
    msg_status_name = models.CharField(default='未读', max_length=5, blank=False, null=False)


# 路线详细表
class WaterModel_RouteList(models.Model):
    # 路线详细ID
    routelist_id = models.AutoField(primary_key=True, blank=False, null=False)
    # 物件名
    res_name = models.CharField(default='默认物件名', max_length=20, blank=False, null=False)
    # 位置
    position = models.CharField(default='默认位置', max_length=50, blank=False, null=False)
    # 当前路线水表数
    meter_count = models.IntegerField(default=0, blank=False, null=False)
    # x坐标
    x_position = models.TextField(default='', blank=True, null=False)
    # y坐标
    y_position = models.TextField(default='', blank=True, null=False)
    # 任务顺
    task_smooth = models.IntegerField(default=1, blank=True, null=False)
    # 路线id
    route_id = models.CharField(default='', max_length=50, blank=True, null=True)


# 表卡表
class WaterModel_Meter(models.Model):
    # 表卡id
    meter_id = models.AutoField(primary_key=True, blank=False, null=False)
    # お客様番号
    meter_customer_no = models.CharField(default='0', max_length=20, blank=False, null=False, unique=True)
    # 水表号
    meter_no = models.CharField(default='0', max_length=20, blank=False, null=False, unique=True)
    # 二维码
    meter_qr_code = models.CharField(default='0', max_length=100, blank=False, null=False, unique=True)
    # 异常状态 参照WaterMaster_UnusualStatus异常状态ID
    unusual_status = models.CharField(default='', max_length=2, blank=True, null=True)
    # 水表所在位置图片
    img_position = models.TextField(default=None, blank=True, null=True)
    # 持有人
    meter_customer_name = models.CharField(default='', max_length=10, blank=False, null=False)
    # 持有人住址
    meter_customer_address = models.CharField(default='', max_length=100, blank=True, null=False)
    # 持有人电话
    meter_customer_tel = models.CharField(default='', max_length=20, blank=False, null=False)
    # 水表型号 参照WaterModel_MeterType水表型号ID
    meter_type = models.CharField(default='00', max_length=5, blank=False, null=False)
    # 水表使用期间from
    meter_use_during_from = models.DateField(blank=True, null=True)
    # 水表使用期间to
    meter_use_during_to = models.DateField(blank=True, null=True)
    # 路线详细id
    routelist_id = models.CharField(default='', max_length=50, blank=True, null=True)


# 任务表
class WaterModel_Work(models.Model):
    # 任务ID
    work_id = models.AutoField(primary_key=True, blank=False, null=False)
    # 任务年月
    work_batch_ym = models.CharField(default='', max_length=6, blank=True, null=False)
    # 发送任务标题
    work_send_message_title = models.CharField(default='默认标题', max_length=20, blank=False, null=False)
    # 发送任务日时
    work_send_message_date = models.DateTimeField(blank=True, null=True)
    # 接收标识 WaterMaster_SendWork任务接受ID
    work_accept_flag = models.CharField(default='01', max_length=2, blank=False, null=False)
    # 接收日时
    work_accept_date = models.DateTimeField(blank=False, null=True)
    # 员工ID
    emp_id = models.CharField(default='', max_length=50, blank=True, null=True)
    # 路线id
    route_id = models.CharField(default='', max_length=50, blank=True, null=True)


# 任务详细表
class WaterModel_WorkList(models.Model):
    # 任务详细id
    work_details_id = models.AutoField(primary_key=True, blank=False, null=False)
    # 抄表日期
    meter_reading_date = models.DateField(blank=False, null=True)
    # 抄表数
    meter_count = models.CharField(default='--', max_length=10, blank=True, null=True)
    # 前回抄表数
    meter_count_last = models.CharField(default='--', max_length=10, blank=True, null=True)
    # 抄表状态 参照WaterMaster_MeterWork抄表状态ID
    meter_reading_status = models.CharField(default='00', max_length=2, blank=True, null=False)
    # お客様番号
    meter_cust_no = models.CharField(default='0', max_length=20, blank=False, null=False)
    # 持有人
    meter_cust_name = models.CharField(default='', max_length=10, blank=False, null=False)
    # 持有人住址
    meter_cust_add = models.CharField(default='', max_length=100, blank=True, null=True)
    # 持有人电话
    meter_cust_tel = models.CharField(default='', max_length=20, blank=False, null=False)
    # 识别方式 参照WaterMaster_WorkRecognition识别ID
    recognition_type = models.CharField(default=None, max_length=2, blank=True, null=True)
    # 抄表图片
    img_name = models.TextField(default=None, blank=True, null=True)
    # 异常报告日
    unusual_report_date = models.DateField(blank=True, null=True)
    # 异常状态 参照WaterMaster_UnusualStatus异常状态ID
    unusual_status = models.CharField(default='', max_length=2, blank=True, null=True)
    # 异常信息是否已读  1:已读，0:未读
    unusual_report_read_status = models.CharField(default='', max_length=5, blank=True, null=True)
    # お客様状態  0：正常   1：欠费   2：故障
    meter_customer_status = models.CharField(default='0', max_length=5, blank=True, null=False)
    # 是否下载(0:未下载；1:已下载)
    download_flg = models.CharField(default='0', max_length=5, blank=False, null=False)
    # 员工ID
    emp_id = models.CharField(default='', max_length=50, blank=True, null=True)
    # 发送ID
    message_id = models.CharField(default='', max_length=50, blank=True, null=True)
    # 任务ID
    work_id = models.CharField(default='', max_length=50, blank=True, null=True)
    # 水表ID
    meter_id = models.CharField(default='', max_length=50, blank=True, null=True)
