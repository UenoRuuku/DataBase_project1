import inspect
import json
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.append('../')
sys.path.append('../..')
sys.path.append('../../..')

from django.contrib.auth import logout
from django.shortcuts import render
from django.template import RequestContext
from Service.BaseService import *


def run_service(request):
    context = {'hello': 'Hello World!'}
    print(context)
    return render(request, 'service.html', context)


# Create your views here.


def check_user(request):
    logout(request)

    if request.method == "GET":
        return render(request, "login.html", context={
            'code': 2,
            'msg': 'have to login',
            'dis': 'none',
            'wait': 3
        })
    if request.GET.get("logout"):
        logout(request)
        return render(request, "login.html", context={
            'code': 2,
            'msg': 'logout',
            'wait': 3
        })
    if request.method == "POST":
        if "username" in request.session:
            return render(request, "wardNurse.html", context={
                'code': 1,
                'msg': 'loaned',
                'name': request.session["username"],
                'wait': 3
            })
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            # todo:调用检查username是否正确的函数
            (k, v, d) = login(username, password)
            if k:
                # 若正确
                request.session['username'] = username
                # 获取权限
                request.session['auth'] = v
                request.session['id'] = d
                context = {
                    'code': 1,
                    'msg': 'login success',
                    'wait': 3,
                    'name': request.session['username'],
                    'auth': v
                }
                if v == "doctor":
                    return render(request, "service.html", context=context)
                elif v == "nurse_master":
                    return render(request, "nurse.html", context=context)
                elif v == "ward_nurse":
                    return render(request, "wardNurse.html", context=context)
                elif v == "em_nurse":
                    return render(request, "emNurse.html", context=context)
            else:
                return render(request, "login.html", context={
                    'code': 2,
                    'msg': 'login fail',
                    'dis': 'block',
                    'wait': 3
                })
    elif "username" in request.session:
        context = {
            'code': 1,
            'msg': 'loaned',
            'name': request.session["username"],
            'wait': 3
        }
        if request.session['auth'] == "doctor":
            return render(request, "service.html", context=context)
        elif request.session['auth'] == "nurse_master":
            return render(request, "nurse.html", context=context)
        elif request.session['auth'] == "ward_nurse":
            return render(request, "wardNurse.html", context=context)
        elif request.session['auth'] == "em_nurse":
            return render(request, "emNurse.html", context=context)
