# -*- coding:utf-8 -*-
# @Author:Ruuku
# @Time: 2021/1/5 21:36

from django.urls import path

from . import views

urlpatterns = [
    path('', views.run_service, name='service'),
]