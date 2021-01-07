# -*- coding:utf-8 -*-
# @Author:Ruuku
# @Time: 2020/11/18 16:30

# 所有数据均应该存放在config目录下
# 包括数据库的相关信息和静态文件的路径
import logging
import os

PROJECT_NAME = "DataBase_project1"
curPath = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = curPath[:curPath.find(PROJECT_NAME + "\\") + len(PROJECT_NAME + "\\")]
print("PROJECT_ROOT", ROOT_PATH)
IP = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "991221wzl"
DB_NAME = "hospital"

LOG_ROOT = ROOT_PATH + "/static/logs/database.log"
LOG_LEVEL = logging.DEBUG
LOG_NAME = "database"
