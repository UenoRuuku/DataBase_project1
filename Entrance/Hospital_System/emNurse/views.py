import inspect
import json
import os
import sys
import time

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.append('../')
sys.path.append('../..')
sys.path.append('../../..')

from django.http import HttpResponse, JsonResponse
from util import logger
from util import config
from Service.EmNurseService import *

# Create your views here.

from util.logger import logggg as log


def unpack(request):
    code = int(request.POST.get("code"))
    id = request.session["id"]
    log.info(str(request.session["username"]) + str(request.session["auth"]) + "访问了数据库")
    back_dic = ""
    if code == 1:
        print("go fuck your self")
    elif code == 2:
        back_dic = getAllPatient(id)
    elif code == 3:
        name = request.POST.get("name")
        result = request.POST.get("result")
        level = request.POST.get("level")
        information = request.POST.get("information")
        back_dic = addPatient(name, result, level, information)
    elif code == 4:
        choose1 = request.POST.get("choose1")
        choose2 = int(request.POST.get("choose2"))
        back_dic = getExPatient(choose1, choose2)
    return HttpResponse(json.dumps(back_dic))


def getAllPatient(id):
    log.info("获取所有的病人")
    back_list = em_nurse_query_patient(int(id), -1)
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    status = [
        "可出院",
        "治疗中",
        "待转移"
    ]
    for (a, b, c) in back_list:
        if c is None:
            c = "暂无"
        item = {"id": a, "name": b, "status": c}
        back_dic["data"].append(item)
    return json.dumps(back_dic)


def getExPatient(choose1, choose2):
    log.info("按照筛选条件搜索病人的病人")
    back_list = em_nurse_query_patient(choose1, int(choose2))
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    status = [
        "可出院",
        "治疗中",
        "待转移"
    ]
    for (a, b, c) in back_list:
        if c is None:
            c = "暂无"
        item = {"id": a, "name": b, "status": c}
        back_dic["data"].append(item)
    return json.dumps(back_dic)


def addPatient(name, result, level, information):
    re = [
        "阴性",
        "阳性"
    ]
    le = [
        "轻症",
        "重症",
        "危重症"
    ]
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    second = time.localtime().tm_sec
    time_str = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second)

    add_patient(name, re[int(result)], time_str, le[int(level)], information)
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    return json.dumps(back_dic)
