from connector.connectMysql import db
from Service.UserService import *
from util import config
import pymysql

treatment_area = ['轻症治疗区域', '重症治疗区域', '危重症治疗区域']
init_ward_number = [2, 2, 2]
init_ward_nurse_per_area = [3, 2, 2]
sickbed_per_ward = [4, 2, 1]

database = pymysql.connect(config.IP, config.DB_USER, config.DB_PASSWORD)
cursor = database.cursor()
cursor.execute("drop database if exists %s" % config.DB_NAME)
cursor.execute("create database %s" % config.DB_NAME)
database.commit()
database.close()

cursor = db.cursor()
sql_file = open("../static/Hospital.sql", "r+", encoding="utf-8")
all_sql = sql_file.read().split(";")
sql_file.close()
for sql in all_sql:
    if sql.strip() != '':
        cursor.execute(sql)
db.commit()

sql_file = open("../static/HospitalIndex.sql", "r+", encoding="utf-8")
all_sql = sql_file.read().split(";")
sql_file.close()
for sql in all_sql:
    if sql.strip() != '':
        cursor.execute(sql)
db.commit()

# 初始医院人员
insert_user('doctor1', '111', '万医生', 'doctor')
insert_user('doctor2', '222', '兔医生', 'doctor')
insert_user('doctor3', '333', '岁医生', 'doctor')
insert_user('nurse_master1', '111', '万护士长', 'nurse_master')
insert_user('nurse_master2', '222', '兔护士长', 'nurse_master')
insert_user('nurse_master3', '333', '岁护士长', 'nurse_master')
insert_user('ward_nurse11', '111', '万万病房护士', 'ward_nurse')
insert_user('ward_nurse12', '111', '万兔病房护士', 'ward_nurse')
insert_user('ward_nurse13', '111', '万岁病房护士', 'ward_nurse')
insert_user('ward_nurse21', '222', '兔万病房护士', 'ward_nurse')
insert_user('ward_nurse22', '222', '兔兔病房护士', 'ward_nurse')
insert_user('ward_nurse31', '333', '岁万病房护士', 'ward_nurse')
insert_user('ward_nurse32', '333', '岁兔病房护士', 'ward_nurse')
insert_user('em_nurse1', '111', '万护士', 'em_nurse')
insert_user('em_nurse2', '222', '兔护士', 'em_nurse')
insert_user('em_nurse3', '333', '岁护士', 'em_nurse')
db.commit()

# 治疗区域简单的初始化
ward_nurse_index = 6
for i in range(len(treatment_area)):
    cursor.execute("insert into treatment_area "
                   "(area_type, area_doctor, area_nurse_master) values ('%s', %d, %d)" %
                   (treatment_area[i], i + 1, i + 4))
    for j in range(init_ward_nurse_per_area[i]):
        ward_nurse_index += 1
        cursor.execute("insert into ward_nurse_treatment_area "
                       "(u_id, ta_id) values (%d, %d)" % (ward_nurse_index, i + 1))
db.commit()

# 病房、病床简单的初始化
ward_index = 0
sickbed_index = 0
for i in range(len(treatment_area)):
    for j in range(init_ward_number[i]):
        cursor.execute("insert into ward "
                       "(total_bed, available_bed, ward_area) values (%d, %d, %d)" %
                       (sickbed_per_ward[i], sickbed_per_ward[i], i + 1))
        ward_index += 1
        for k in range(sickbed_per_ward[i]):
            cursor.execute("insert into sickbed (bed_status, w_id) values "
                           "(0, %d)" % ward_index)
            sickbed_index += 1
db.commit()
