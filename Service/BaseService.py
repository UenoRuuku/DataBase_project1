from connector.connectMysql import db

cursor = db.cursor()


def insert_user(username, password, name, user_type):
    cursor.execute("insert into user (username, password, name, user_type)"
                   " values ('%s', '%s', '%s', '%s')" % (username, password, name, user_type))


def check_patient_discharge():
    # 对于轻症患者，若连续 3 天体温正常（低于 37.3 摄氏度）且
    # 连续两次核酸检测结果均为阴性（两次检测间隔时间至少为 24 小时），则该患者可以康复出院
    return False
