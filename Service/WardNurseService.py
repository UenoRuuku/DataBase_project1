from Service.BaseService import *

cursor = db.cursor()


def record_patient_status(time, temperature, symptom, life_status, curr_report, p_id):
    """
    :param time: 登记病人状态的时间
    :type time: 字符串，格式为 yyyy-mm-dd hh:mm:ss，例如，2021-01-06 20:34:11
    :param temperature: 病人的体温
    :type temperature: 浮点数，格式为 xx.x，例如，37.3
    :param symptom: 病人存在的症状
    :type symptom: 字符串，不长于 100 字符
    :param life_status: 病人的生命状态
    :type life_status: 字符串，'康复出院'，'在院治疗' 或 '病亡'
    :param curr_report: 病人最新的核酸检测单的主键
    :type curr_report: 整数
    :param p_id: 病人的主键
    :type p_id: 整数
    """
    # 如果满足了出院条件，将病人的 transfer 属性设置为 -1

    cursor.execute("insert into patient_status (time, temperature, symptom, life_status, curr_report, p_id) "
                   "values ('%s', %.1f, '%s', '%s', %d, %d)"
                   % (time, temperature, symptom, life_status, curr_report, p_id))
    if life_status == '病亡':
        cursor.execute("select b_id from sickbed_patient where p_id=%d" % p_id)
        result = cursor.fetchall()
        sickbed_id = result[0][0]
        cursor.execute("delete from sickbed_ward_nurse where b_id=%d" % sickbed_id)
        cursor.execute("update sickbed set bed_status=0 where b_id=%d" % sickbed_id)
        cursor.execute("delete from sickbed_patient where b_id=%d" % sickbed_id)

        cursor.execute("select area_type from ward natural join sickbed, treatment_area "
                       "where ward_area=ta_id and b_id=%d" % sickbed_id)
        result = cursor.fetchall()
        if len(result) != 0:
            transfer_patient(result[0][0][:-4])
    elif check_patient_discharge(p_id):
        cursor.execute("update patient set transfer=-1 where p_id=%d" % p_id)
    db.commit()
    return 1


def ward_nurse_query_nat_report(p_id):
    """
    :param p_id: 病人的主键
    :return: 病人的最新核算检测单
    """
    cursor.execute("select r_id,result,time,illness_level from nat_report "
                   "where p_id=%d order by time desc" % p_id)
    result = cursor.fetchall()
    if len(result) != 0:
        return result[0]


def ward_nurse_query_patient(ward_nurse_id, query_type):
    """
    :param ward_nurse_id: 病房护士的主键
    :param query_type: -1：查询所有病人 0：’康复出院‘的病人 1：’在院治疗‘的病人 2：’病亡‘的病人
    3：可出院的病人 4：不可出院的病人
    :return: 满足筛选条件的所有病人的元组
    """
    all_patient = []
    cursor.execute("select p_id from sickbed_patient natural join sickbed natural join sickbed_ward_nurse "
                   "where u_id=%d" % ward_nurse_id)
    temp = cursor.fetchall()
    for p_id in temp:
        cursor.execute("select patient.p_id,name,life_status,transfer "
                       "from patient left join patient_status on patient.p_id=patient_status.p_id "
                       "where patient.p_id=%d order by time desc" % p_id)
        result = cursor.fetchall()
        if len(result) != 0:
            all_patient.append(result[0])
    info_to_query = []
    if query_type == -1:
        info_to_query = all_patient
    elif query_type == 0:
        for item in all_patient:
            if item[2] == '康复出院':
                info_to_query.append(item)
    elif query_type == 1:
        for item in all_patient:
            if item[2] == '在院治疗':
                info_to_query.append(item)
    elif query_type == 2:
        for item in all_patient:
            if item[2] == '病亡':
                info_to_query.append(item)
    elif query_type == 3:
        for item in all_patient:
            if item[3] == -1:
                info_to_query.append(item)
    elif query_type == 4:
        for item in all_patient:
            if item[3] != -1:
                info_to_query.append(item)
    return info_to_query
