import time

from django.shortcuts import render

# Create your views here.
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

from django.http import HttpResponse, JsonResponse
from Service.WardNurseService import *
from util import logger
from util.logger import logggg as log
from util import config


# Create your views here.


def unpack(request):
    code = int(request.POST.get("code"))
    log.info(str(request.session["username"]) + str(request.session["auth"]) + "访问了数据库")
    back_dic = ""
    id = int(request.session["id"])
    if code == 1:
        print("go fuck yourself")
    elif code == 2:
        back_dic = getAllPatient(id)
    elif code == 3:
        pid = request.POST.get("pid")
        back_dic = getNat(pid)
    elif code == 4:
        choose = request.POST.get("choose")
        back_dic = getExPatient(id, choose)
    elif code == 5:
        pid = request.POST.get("pid")
        temp = request.POST.get("temp")
        sympton = request.POST.get("sympton")
        liveStatus = request.POST.get("liveStatus")
        cur_id = request.POST.get("currentID")
        back_dic = updateNat(pid, temp, sympton, liveStatus, cur_id)
    return HttpResponse(json.dumps(back_dic))


def updateNat(pid, temp, sympton, liveStatus, cur_id):
    log.info("更新" + pid + "核酸检测单")
    status = [
        "在院治疗",
        "病亡"
    ]
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    second = time.localtime().tm_sec
    time_str = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second)
    record_patient_status(time_str, float(temp), sympton, status[int(liveStatus)], int(cur_id), int(pid))
    return json.dumps(back_dic)


def getAllPatient(id):
    log.info("获取当前治疗区域的病人信息")
    back_list = ward_nurse_query_patient(id, -1)
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

    for (a, b, c, d) in back_list:
        life = 0
        if c == "病亡":
            life = 1
        if c is None:
            c = "暂无"
        item = {"id": a, "name": b, "status": c + "," + status[d + 1], "life": life}
        back_dic["data"].append(item)
    return json.dumps(back_dic)


def getNat(pid):
    log.info("获取病人" + pid + "核酸检测结果")
    (a, b, c, d) = ward_nurse_query_nat_report(int(pid))
    item = {
        "id": a,
        "time": str(c),
        "live": d,
        "result": b
    }
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": item
    }
    return back_dic

