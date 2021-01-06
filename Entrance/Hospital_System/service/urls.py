# -*- coding:utf-8 -*-
# @Author:Ruuku
# @Time: 2021/1/5 20:35

from django.urls import path

from . import views

urlpatterns = [
    # path('', views.run_service, name='service'),
    path('', views.check_user, name='service'),
]