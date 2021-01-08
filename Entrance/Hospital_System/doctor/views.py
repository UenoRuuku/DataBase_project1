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
from util import logger
from util import config
from Service.DoctorService import *

# Create your views here.

from util.logger import logggg as log


def unpack(request):
    code = int(request.POST.get("code"))
    id = request.session["id"]
    log.info(str(request.session["username"]) + str(request.session["auth"]) + "访问了数据库")
    back_dic = ""
    if code == 1:
        back_dic = getPatientOut(id)
    elif code == 2:
        back_dic = getAllPatient(id)
    elif code == 3:
        back_dic = getAllNurse(id)
    elif code == 4:
        choose = int(request.POST.get("choose"))
        back_dic = getExPatient(choose, id)
    elif code == 5:
        pid = int(request.POST.get("pid"))
        back_dic = patientOut(pid)
    elif code == 6:
        pid = int(request.POST.get("pid"))
        life = int(request.POST.get("life"))
        back_dic = moreOperation(pid, life)
    elif code == 7:
        nurse = int(request.POST.get("param[nurse]"))
        back_dic = getPatientByNurse(nurse)
    elif code == 8:
        die = int(request.POST.get("pid"))
        back_dic = patientDie(die, id)
    elif code == 10:
        result = request.POST.get("result")
        date = request.POST.get("date")
        life = request.POST.get("life")
        pid = request.POST.get("pid")
        back_dic = addNat(pid, result, life, date)
    return HttpResponse(json.dumps(back_dic))


def getPatientOut(id):
    log.info("获取所有可以出院的病人")
    back_list = doctor_query_patient(int(id), 3)
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
        item = {"id": a, "name": b, "status": c + "," + status[d + 1], "life": life}
        back_dic["data"].append(item)
    return json.dumps(back_dic)


def getAllPatient(id):
    log.info("获取所有可以出院的病人")
    back_list = doctor_query_patient(int(id), -1)
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


def getAllNurse(id):
    log.info("获取所有护士和护士长")
    result = doctor_query_nurses(int(id))
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


def getExPatient(choose, id):
    log.info("按照筛选条件搜索病人的病人")
    back_list = doctor_query_patient(id, int(choose))
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


def patientOut(pid):
    log.info("使" + str(pid) + "病人出院")
    update_patient_life_status("康复出院", pid)
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": [
        ]
    }
    return json.dumps(back_dic)


def patientDie(die, id):
    log.info("使" + str(die) + "病人死亡")
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    update_patient_life_status("病亡", die)
    return json.dumps(back_dic)


def moreOperation(id, life):
    life_str = ""
    if life == 1:
        life_str = "轻症"
    if life == 2:
        life_str = "重症"
    if life == 3:
        life_str = "危重症"
    log.info("修改" + str(id) + "评级为" + str(life_str))
    update_nat_illness_level(life_str, id)
    back_dic = {
        "code": "1",
        "msg": "success",
    }
    return json.dumps(back_dic)


def getPatientByNurse(nurse):
    log.info("获取" + str(nurse) + "负责的病人")
    back_list = doctor_query_nurse_patient(int(nurse))
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    for (a, b, c) in back_list:
        if c is None:
            c = "暂无"
        item = {"id": a, "name": b, "status": c}
        back_dic["data"].append(item)
    return json.dumps(back_dic)


def addNat(id, result, life, date):
    log.info("添加核酸检测单给" + str(id))
    il_level = [
        "轻症",
        "重症",
        "危重症"
    ]
    result_level = [
        "阴性",
        "阳性"
    ]
    add_nat_report(result_level[int(result)], date, il_level[int(life) - 1], int(id))
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": []
    }
    return json.dumps(back_dic)
