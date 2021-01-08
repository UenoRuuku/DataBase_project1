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
from util import logger
from util import config

# Create your views here.

log = logger.create_logger(config.LOG_LEVEL, config.LOG_ROOT, config.LOG_NAME)


def unpack(request):
    code = int(request.POST.get("code"))
    print(code)
    log.info(str(request.session["username"]) + str(request.session["auth"]) + "访问了数据库")
    back_dic = ""
    if code == 1:
        back_dic = getPatientOut()
    elif code == 2:
        back_dic = getAllPatient()
    elif code == 3:
        back_dic = getAllNurse()
    elif code == 4:
        back_dic = getExPatient()
    elif code == 5:
        back_dic = patientOut()
    elif code == 6:
        back_dic = moreOperation()
    return HttpResponse(json.dumps(back_dic))


def getPatientOut():
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


def getAllPatient():
    log.info("获取当前治疗区域的病人信息")
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


def getAllNurse():
    log.info("获取当前治疗区域的病房护士信息")
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


def getExPatient():
    log.info("获取病房护士负责的病人信息")
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
