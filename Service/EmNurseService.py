from Service.BaseService import *

cursor = db.cursor()


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

    found, (sickbed_id, nurse_id) = find_available_sickbed_and_nurse(illness_level)
    if found == 0:
        cursor.execute("insert into patient (name, info, transfer) values "
                       "('%s', '%s', %d)" % (name, info, 1))
        p_id = db.insert_id()
        cursor.execute("insert into nat_report (result, time, illness_level, p_id) values "
                       "('%s', '%s', '%s', %d)" % (check_result, time, illness_level, p_id))
        db.commit()
        return 0
    else:
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
