from connector.connectMysql import db

cursor = db.cursor()

max_patient_per_nurse = {'轻症': 3, '重症': 2, '危重症': 1}


def add_patient(name, check_result, time, illness_level, info='无'):
    """
    :param name: 病人姓名
    :type name: 字符串，不长于 20 字符
    :param check_result: 病人的核酸检测结果
    :type check_result: 字符串，'阴性' 或 '阳性'
    :param time: 核酸检测的时间
    :type time: 字符串，格式为 yyyy-mm-dd hh:mm:ss，例如，2021-01-06 20:34:11
    :param illness_level: 病人的病情等级
    :type illness_level: 字符串，'轻症'，'重症' 或 '危重症'
    :param info: 病人的其他基本信息，默认为 '无'
    :type info: 字符串，不长于 100 字符
    """
    # 如果没有空闲护士或者对应病情等级的空闲病房，将病人的 transfer 属性设置为 1 表示病人处于隔离区
    # 如果存在空闲护士或者对应病情等级的空闲病房，将病人的 transfer 属性设置为 0
    #       并且更新对应的 sickbed_ward_nurse, sickbed 和 sickbed_patient 表中的内容

    # 寻找对应治疗区域
    area_id = []
    cursor.execute("select ta_id from treatment_area where area_type='%s'" % (illness_level + '治疗区域'))
    result = cursor.fetchall()
    for item in result:
        area_id.append(item[0])
    if len(area_id) == 0:
        cursor.execute("insert into patient (name, info, transfer) values "
                       "('%s', '%s', %d)" % (name, info, 1))
        p_id = db.insert_id()
        cursor.execute("insert into nat_report (result, time, illness_level, p_id) values "
                       "('%s', '%s', '%s', %d)" % (check_result, time, illness_level, p_id))
        db.commit()
        return 0

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
        cursor.execute("insert into patient (name, info, transfer) values "
                       "('%s', '%s', %d)" % (name, info, 1))
        p_id = db.insert_id()
        cursor.execute("insert into nat_report (result, time, illness_level, p_id) values "
                       "('%s', '%s', '%s', %d)" % (check_result, time, illness_level, p_id))
        db.commit()
        return 0

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
        cursor.execute("insert into patient (name, info, transfer) values "
                       "('%s', '%s', %d)" % (name, info, 1))
        p_id = db.insert_id()
        cursor.execute("insert into nat_report (result, time, illness_level, p_id) values "
                       "('%s', '%s', '%s', %d)" % (check_result, time, illness_level, p_id))
        db.commit()
        return 0

    # 将病人加入治疗区域
    cursor.execute("insert into patient (name, info, transfer) values "
                   "('%s', '%s', %d)" % (name, info, 0))
    p_id = db.insert_id()
    cursor.execute("insert into nat_report (result, time, illness_level, p_id) values "
                   "('%s', '%s', '%s', %d)" % (check_result, time, illness_level, p_id))
    cursor.execute("insert into sickbed_ward_nurse values (%d, %d)" % (sickbed_id, nurse_id))
    cursor.execute("update sickbed set bed_status=1 where b_id=%d" % sickbed_id)
    cursor.execute("insert into sickbed_patient values (%d, %d)" % (sickbed_id, p_id))
    db.commit()
    return 1
