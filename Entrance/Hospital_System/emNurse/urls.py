# -*- coding:utf-8 -*-
# @Author:Ruuku
# @Time: 2021/1/8 23:19
from django.urls import path

from . import views

urlpatterns = [
    # path('', views.run_service, name='service'),
    path('', views.unpack, name='emNurse'),
]