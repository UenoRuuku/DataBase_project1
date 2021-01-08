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

# Create your views here.

log = logger.create_logger(config.LOG_LEVEL, config.LOG_ROOT, config.LOG_NAME)


def unpack(request):
    code = int(request.POST.get("code"))
    id = request.session["id"]
    print(code)
    log.info(str(request.session["username"]) + str(request.session["auth"]) + "访问了数据库")
    back_dic = ""
    if code == 1:
        back_dic = getPatientOut(id)
    elif code == 2:
        back_dic = getAllPatient(id)
    elif code == 3:
        back_dic = getAllNurse(id)
    elif code == 4:
        choose = int(request.POST.get("param")["choose"])
        back_dic = getExPatient(choose, id)
    elif code == 5:
        back_dic = patientOut(id)
    elif code == 6:
        back_dic = moreOperation(id)
    elif code == 7:
        nurse = int(request.POST.get("param[nurse]"))
        back_dic = getPatientByNurse(nurse)
    elif code == 8:
        die = int(request.POST.get("param")["id"])
        back_dic = patientDie(die, id)

    return HttpResponse(json.dumps(back_dic))


def getPatientOut(id):
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


def getAllPatient(id):
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


def getAllNurse(id):
    log.info("获取所有护士和护士长")
    back_dic = {
        "code": "1",
        "msg": "success",
        "data": [
            {
                "id": "1",
                "name": "sb",
                "auth": 0
            }
        ]
    }
    print(json.dumps(back_dic))
    return json.dumps(back_dic)


def getExPatient(choose, id):
    log.info("按照筛选条件搜索病人的病人")
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


def patientOut(pid, id):
    log.info("使" + str(pid) + "病人出院")
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


def patientDie(die, id):
    log.info("使" + str(die) + "病人死亡")
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


def getPatientByNurse(nurse):
    log.info("获取" + str(nurse) + "负责的病人")
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
    return json.dumps(back_dic)
