from Service.BaseService import *

cursor = db.cursor()


def add_nat_report(check_result, time, illness_level, p_id):
    """
    :param check_result: 病人的核酸检测结果
    :type check_result: 字符串，'阴性' 或 '阳性'
    :param time: 核酸检测的时间
    :type time: 字符串，格式为 yyyy-mm-dd hh:mm:ss，例如，2021-01-06 20:34:11
    :param illness_level: 病人的病情等级
    :type illness_level: 字符串，'轻症'，'重症' 或 '危重症'
    :param p_id: 核算检测单所属的病人的主键
    :type p_id: 整数
    """
    # 如果满足了出院条件，将病人的 transfer 属性设置为 -1
    # 如果病情等级发生了变化，且没有新的病情等级的空闲护士或病房，将病人的 transfer 属性设置为 1 表示病人待转移
    # 如果病情等级发生了变化，且存在新的病情等级的空闲护士和病房，
    #       更新对应的 sickbed_ward_nurse, sickbed 和 sickbed_patient 表中的内容
    cursor.execute("insert into nat_report (result, time, illness_level, p_id) values "
                   "('%s', '%s', '%s', %d)" % (check_result, time, illness_level, p_id))

    if check_patient_discharge(p_id):
        cursor.execute("update patient set transfer=-1 where p_id=%d" % p_id)
    else:
        cursor.execute("select illness_level from nat_report where p_id=%d order by time desc" % p_id)
        result = cursor.fetchall()
        if result[0][0] != result[1][0]:
            cursor.execute("update patient set transfer=1 where p_id=%d" % p_id)
            transfer_patient(illness_level)
    db.commit()
    return 1


def update_nat_illness_level(illness_level, p_id):
    """
    :param illness_level: 病人更改后的病情等级
    :type illness_level: 字符串，'轻症'，'重症' 或 '危重症'
    :param p_id: 病人的主键
    :type p_id: 整数
    """
    # 更新 nat_report 表中对应 p_id 的且 time 是最新的那一条记录的 illness_level
    # 如果满足了出院条件，将病人的 transfer 属性设置为 -1
    # 如果没有新的病情等级的空闲护士或病房，将病人的 transfer 属性设置为 1 表示病人待转移
    # 如果存在新的病情等级的空闲护士和病房，更新对应的 sickbed_ward_nurse, sickbed 和 sickbed_patient 表中的内容
    cursor.execute("select r_id, illness_level from nat_report where p_id=%d order by time desc" % p_id)
    result = cursor.fetchall()
    if len(result) == 0:
        return 0
    latest_report_id = result[0][0]
    latest_illness_level = result[0][1]
    if illness_level != latest_illness_level:
        cursor.execute("update nat_report set illness_level='%s' where r_id=%d" % (illness_level, latest_report_id))

        if check_patient_discharge(p_id):
            cursor.execute("update patient set transfer=-1 where p_id=%d" % p_id)
        else:
            cursor.execute("update patient set transfer=1 where p_id=%d" % p_id)
            transfer_patient(illness_level)
    db.commit()
    return 1


def update_patient_life_status(life_status, p_id):
    """
    :param life_status: 病人更改后的生命状态
    :type life_status: 字符串，'康复出院'，'在院治疗' 或 '病亡'
    :param p_id: 病人的主键
    :type p_id: 整数
    """
    # 更新 patient_status 表中对应 p_id 的且 time 是最新的那一条记录的 life_status
    # 如果病人病亡或康复出院，更新对应的 sickbed_ward_nurse, sickbed 和 sickbed_patient 表中的内容
    # 之后触发 patient_transfer
    cursor.execute("select ps_id, life_status from patient_status where p_id=%d order by time desc" % p_id)
    result = cursor.fetchall()
    if len(result) == 0:
        return 0
    latest_status_id = result[0][0]
    latest_life_status = result[0][1]
    if latest_life_status == '病亡' or latest_life_status == '康复出院' or life_status == latest_life_status:
        return 0
    else:
        cursor.execute("update patient_status set life_status='%s' where ps_id=%d" % (life_status, latest_status_id))
        if life_status == '病亡' or life_status == '康复出院':
            cursor.execute("select b_id from sickbed_patient where p_id=%d" % p_id)
            result = cursor.fetchall()
            sickbed_id = result[0][0]
            cursor.execute("delete from sickbed_ward_nurse where b_id=%d" % sickbed_id)
            cursor.execute("update sickbed set bed_status=0 where b_id=%d" % sickbed_id)
            cursor.execute("delete from sickbed_patient where b_id=%d" % sickbed_id)

            cursor.execute("select illness_level from nat_report where p_id=%d order by time desc" % p_id)
            result = cursor.fetchall()
            transfer_patient(result[0][0])
        db.commit()
        return 1
