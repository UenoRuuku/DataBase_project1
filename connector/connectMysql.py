# -*- coding:utf-8 -*-
# @Author:Ruuku
# @Time: 2020/11/18 16:22

import pymysql
from util import config

db = pymysql.connect(config.IP, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
