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
    print(code)
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
        
        back_dic = updateNat()
    elif code == 6:
        back_dic = moreOperation()
    elif code == 7:
        nurse = request.POST.get("nurse")
        back_dic = getPatientByNurse(nurse)
    elif code == 8:
        nurse = request.POST.get("nurse")
        back_dic = nurseDelete(id, nurse)
    return HttpResponse(json.dumps(back_dic))


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
        item = {"id": a, "name": b, "status": c + status[d + 1], "life": life}
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


def getExPatient(id, choose):
    log.info("按照筛选条件搜索病人的病人")
    back_list = nurse_master_query_patient(id, int(choose))
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
        print(a, b, c, d)
        life = 0
        if c == "病亡":
            life = 1
        item = {"id": a, "name": b, "status": c + "," + status[d + 1], "life": life}
        back_dic["data"].append(item)
    return json.dumps(back_dic)
