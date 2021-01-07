from connector.connectMysql import db

cursor = db.cursor()


def insert_user(username, password, name, user_type):
    cursor.execute("insert into user (username, password, name, user_type)"
                   " values ('%s', '%s', '%s', '%s')" % (username, password, name, user_type))


def check_patient_discharge(p_id):
    # 对于轻症患者，若连续 3 天体温正常（低于 37.3 摄氏度）且
    # 连续两次核酸检测结果均为阴性（两次检测间隔时间至少为 24 小时），则该患者可以康复出院
    total_nat = cursor.execute("select result, time, illness_level from nat_report "
                               "where p_id=%d order by time desc" % p_id)
    if total_nat < 2:
        return False
    result = cursor.fetchall()

    latest_time = None
    nat_pass = False
    for item in result:
        if item[0] == '阴性' and item[2] == '轻症':
            if latest_time is None:
                latest_time = item[1]
            elif (latest_time - item[1]).total_seconds() >= 86400:
                nat_pass = True
                break
    if not nat_pass:
        return False

    total_status = cursor.execute("select temperature from patient_status "
                                  "where p_id=%d and life_status='在院治疗' order by time desc" % p_id)
    if total_status < 3:
        return False
    result = cursor.fetchall()

    status_pass = True
    for i in range(3):
        if result[i][0] >= 37.3:
            status_pass = False
            break
    if not status_pass:
        return False
    else:
        return True
