# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: urls.py
@time: 2020/9/08 09:30
"""
from django.urls import path

from aimr_platform.views.android.TaskConfirm import TaskConfirmAPI
from aimr_platform.views.pc.Login import LoginAPI
from aimr_platform.views.pc.MapInfo import MapInfoAPI
from aimr_platform.views.pc.Meter import MeterAPI
from aimr_platform.views.pc.Task import TaskAPI
from aimr_platform.views.pc.Price import PriceAPI
from aimr_platform.views.pc.Portal import PortalAPI
from aimr_platform.views.pc.Map import MapAPI
from aimr_platform.views.pc.DataCreate import DataCreateAPI
from aimr_platform.views.android.AndroidTask import AndroidTaskAPI


urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('meter/', MeterAPI.as_view()),
    path('portal/', PortalAPI.as_view()),
    path('task/', TaskAPI.as_view()),
    path('price/', PriceAPI.as_view()),
    path('map/', MapAPI.as_view()),
    path('map_info/', MapInfoAPI.as_view()),
    path('android_task/', AndroidTaskAPI.as_view()),
    path('task_confirm/', TaskConfirmAPI.as_view()),
    path('data_create/', DataCreateAPI.as_view()),
]

