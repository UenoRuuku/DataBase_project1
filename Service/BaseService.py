from connector.connectMysql import db

cursor = db.cursor()
max_patient_per_nurse = {'轻症': 3, '重症': 2, '危重症': 1}


def insert_user(username, password, name, user_type):
    cursor.execute("insert into user (username, password, name, user_type)"
                   " values ('%s', '%s', '%s', '%s')" % (username, password, name, user_type))


def login(username, password):
    """
    :param username: 登录的用户名
    :param password: 登录的密码
    :return: 登录密码是否与数据库相符
    """
    cursor.execute("select password from user where username='%s'" % username)
    result = cursor.fetchall()
    if len(result) != 0 and result[0][0] == password:
        return True
    else:
        return False


def find_available_sickbed_and_nurse(illness_level):
    # 寻找对应治疗区域
    area_id = []
    cursor.execute("select ta_id from treatment_area where area_type='%s'" % (illness_level + '治疗区域'))
    result = cursor.fetchall()
    for item in result:
        area_id.append(item[0])
    if len(area_id) == 0:
        return 0, (0, 0)

    # 寻找一个空闲病床
    sickbed_id = None
    for area in area_id:
        cursor.execute("select b_id, bed_status from ward natural join sickbed where ward_area=%d" % area)
        result = cursor.fetchall()
        for item in result:
            if item[1] == 0:
                sickbed_id = item[0]
                break
        if sickbed_id is not None:
            break
    if sickbed_id is None:
        return 0, (0, 0)

    # 寻找一位空闲病房护士
    nurses = []
    for area in area_id:
        cursor.execute("select u_id from ward_nurse_treatment_area where ta_id=%d" % area)
        result = cursor.fetchall()
        for u_id in result:
            nurses.append(u_id[0])
    nurse_id = None
    for nurse in nurses:
        cursor.execute("select count(*) from sickbed_ward_nurse where u_id=%d" % nurse)
        result = cursor.fetchall()
        if result[0][0] < max_patient_per_nurse[illness_level]:
            nurse_id = nurse
            break
    if nurse_id is None:
        return 0, (0, 0)
    else:
        return 1, (sickbed_id, nurse_id)


def check_patient_discharge(p_id):
    # 如果病人的 transfer 已经是 -1 ，直接返回 True
    cursor.execute("select transfer from patient where p_id=%d" % p_id)
    result = cursor.fetchall()
    if result[0][0] == -1:
        return True
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
        if item[0] != '阴性' or item[2] != '轻症':
            break
        else:
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


def transfer_patient(illness_level):
    """
    声明有病人需要转入 illness_level 下的治疗区域，或该区域出现了空闲资源，将所有待转入对应区域的病人转入
    :param illness_level: 有病人要转入的或出现了空闲资源的治疗区域对应的病情等级
    :type illness_level: 字符串，'轻症'，'重症' 或 '危重症'
    """
    # 找到所有病情等级为 illness_level 的待转移的在院治疗病人
    p_to_transfer = []
    temp = []
    cursor.execute("select p_id from patient where transfer=1")
    patients_id = cursor.fetchall()
    for item in patients_id:
        cursor.execute("select p_id from nat_report "
                       "where p_id=%d and illness_level='%s' order by time desc" % (item[0], illness_level))
        result = cursor.fetchall()
        if len(result) != 0:
            temp.append(result[0][0])
    for p_id in temp:
        cursor.execute("select life_status from patient_status "
                       "where p_id=%d order by time desc" % p_id)
        result = cursor.fetchall()
        if len(result) == 0 or result[0][0] == '在院治疗':
            p_to_transfer.append(p_id)

    # 优先选择隔离区（没有病床）的病人
    no_bed = []
    have_bed = []
    for p_id in p_to_transfer:
        cursor.execute("select b_id from sickbed_patient where p_id=%d" % p_id)
        result = cursor.fetchall()
        if len(result) == 0:
            no_bed.append(p_id)
        else:
            have_bed.append((p_id, result[0][0]))
    for p_id in no_bed:
        found, (bed_id, nurse_id) = find_available_sickbed_and_nurse(illness_level)
        if found == 0:
            db.commit()
            return
        else:
            cursor.execute("update patient set transfer=0 where p_id=%d" % p_id)
            cursor.execute("insert into sickbed_ward_nurse values (%d, %d)" % (bed_id, nurse_id))
            cursor.execute("update sickbed set bed_status=1 where b_id=%d" % bed_id)
            cursor.execute("insert into sickbed_patient values (%d, %d)" % (bed_id, p_id))

    new_available_bed = []
    new_area = []
    for (p_id, old_bed_id) in have_bed:
        found, (bed_id, nurse_id) = find_available_sickbed_and_nurse(illness_level)
        if found == 1:
            cursor.execute("delete from sickbed_ward_nurse where b_id=%d" % old_bed_id)
            cursor.execute("update sickbed set bed_status=0 where b_id=%d" % old_bed_id)
            cursor.execute("delete from sickbed_patient where b_id=%d" % old_bed_id)

            cursor.execute("update patient set transfer=0 where p_id=%d" % p_id)
            cursor.execute("insert into sickbed_ward_nurse values (%d, %d)" % (bed_id, nurse_id))
            cursor.execute("update sickbed set bed_status=1 where b_id=%d" % bed_id)
            cursor.execute("insert into sickbed_patient values (%d, %d)" % (bed_id, p_id))
            new_available_bed.append(old_bed_id)
        else:
            break

    if len(new_available_bed) == 0:
        db.commit()
        return
    for new_bed in new_available_bed:
        cursor.execute("select ward_area from ward natural join sickbed where b_id=%d" % new_bed)
        result = cursor.fetchall()
        cursor.execute("select area_type from treatment_area where ta_id=%d" % result[0][0])
        result = cursor.fetchall()
        if len(result) != 0 and (result[0][0] not in new_area):
            new_area.append(result[0][0])
    for area in new_area:
        transfer_patient(area[:-4])
