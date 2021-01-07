from django.contrib.auth import logout
from django.shortcuts import render
from django.template import RequestContext


def run_service(request):
    context = {'hello': 'Hello World!'}
    print(context)
    return render(request, 'service.html', context)


# Create your views here.


def check_user(request):
    print(request.method)
    logout(request)
    if request.method == "GET" and "username" not in request.session:
        return render(request, "login.html", context={
            'code': 2,
            'msg': 'have to login',
            'dis': 'none',
            'wait': 3
        })
    if request.method == "POST":
        if "username" in request.session:
            return render(request, "service.html", context={
                'code': 1,
                'msg': 'loaned',
                'wait': 3
            })
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            # todo:调用检查username是否正确的函数
            if username == "18302010013" and password == "1234":
                # 若正确
                request.session['username'] = username
                # 获取权限
                request.session['auth'] = 0
                context = {
                    'code': 1,
                    'msg': 'login success',
                    'wait': 3,
                    'name': username,
                    'auth': '主治医生'
                }
                return render(request, "service.html", context=context)
            else:
                return render(request, "login.html", context={
                    'code': 2,
                    'msg': 'login fail',
                    'dis': 'block',
                    'wait': 3
                })
    elif "username" in request.session:
        return render(request, "service.html", context={
            'code': 1,
            'msg': 'loaned',
            'wait': 3
        })
