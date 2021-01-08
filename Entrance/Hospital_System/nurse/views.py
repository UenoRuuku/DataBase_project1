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
from Service.NurseMasterService import *
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
        back_dic = getAllNurse(id)
    elif code == 4:
        choose = request.POST.get("choose")
        back_dic = getExPatient(id, choose)
    elif code == 5:
        back_dic = patientOut()
    elif code == 6:
        back_dic = moreOperation()
    elif code == 7:
        nurse = request.POST.get("nurse")
        back_dic = getPatientByNurse(nurse)
    elif code == 8:
        nurse = request.POST.get("nurse")
        back_dic = nurseDelete(id, nurse)
    elif code == 9:
        back_dic = getAllWard(id)
    elif code == 10:
        name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        back_dic = addNurse(id, name, username, password)
    return HttpResponse(json.dumps(back_dic))


def addNurse(id, name, username, password):
    log.info("添加护士"+name)
    add_ward_nurse(id, username, password, name)
    return {
        "code": "1",
        "msg": "success",
        "data": []
    }


def getAllWard(id):
    log.info("获取所有病床")
    back_list = nurse_master_query_sickbed_and_patient(id)
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    for (a, b, c, d, e) in back_list:
        item = {"sid": a, "sstatus": b, "pid": c, "pname": d, "pinfo": e}
        back_dic["data"].append(item)
    return json.dumps(back_dic)


def getAllPatient(id):
    log.info("获取当前治疗区域的病人信息")
    back_list = nurse_master_query_patient(id, -1)
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
    print(back_list)
    for (a, b, c, d) in back_list:
        item = {"id": a, "name": b, "status": c + status[d + 1]}
        back_dic["data"].append(item)
    return json.dumps(back_dic)


def getAllNurse(id):
    result = nurse_master_query_nurses(int(id))
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": [
        ]
    }
    for (a, b, c, d, e) in result:
        auth = 0
        if e == "nurse_master":
            auth = 1
        item = {
            "id": a,
            "name": c,
            "auth": auth
        }
        back_dic["data"].append(item)
    return json.dumps(back_dic)


def getPatientByNurse(nurse):
    log.info("获取" + str(nurse) + "负责的病人")
    back_list = nurse_master_query_nurse_patient(int(nurse))
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    for (a, b, c) in back_list:
        item = {"id": a, "name": b, "status": c}
        back_dic["data"].append(item)
    return json.dumps(back_dic)


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


def patientOut():
    log.info("获取所有可以出院的病人")
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": [
            {
                "id": "1",
                "name": "sb",
                "status": "可出院"
            }
        ]
    }
    print(json.dumps(back_dic))
    return json.dumps(back_dic)


def moreOperation():
    log.info("修改该区域病房护士信息")
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": [
            {
                "id": "1",
                "name": "sb",
                "status": "可出院"
            }
        ]
    }
    print(json.dumps(back_dic))
    return json.dumps(back_dic)


def getPatientByNurse(nurse):
    log.info("获取" + str(nurse) + "负责的病人")
    back_list = nurse_master_query_nurse_patient(int(nurse))
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    print(back_list)
    for (a, b, c) in back_list:
        item = {"id": a, "name": b, "status": c}
        back_dic["data"].append(item)
    return json.dumps(back_dic)


def nurseDelete(id, nurse):
    log.info("删除护士" + str(nurse))
    delete_ward_nurse(id, int(nurse))
    return {
        "code": "1",
        "msg": "success",
        "data": []
    }
