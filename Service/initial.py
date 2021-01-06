from connector.connectMysql import db
from util import config
import pymysql

database = pymysql.connect(config.IP, config.DB_USER, config.DB_PASSWORD)
cursor = database.cursor()
cursor.execute("drop database %s" % config.DB_NAME)
cursor.execute("create database %s" % config.DB_NAME)
database.commit()
database.close()

cursor = db.cursor()
sql_file = open("../static/Hospital.sql", "r+", encoding="utf-8")
all_sql = sql_file.read().split(";")
for sql in all_sql:
    if sql.strip() != '':
        cursor.execute(sql)
db.commit()


