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


def em_nurse_query_patient(area_type, query_type):
    """
    :param area_type: 指定的治疗区域，取值为 ‘轻症治疗区域’ ‘重症治疗区域’ 或 ‘危重症治疗区域’
    :param query_type: -1：查询所有病人 0：隔离区的病人
    1：’康复出院‘的病人 2：’在院治疗‘的病人 3：’病亡‘的病人
    4：‘轻症’的病人 5：‘重症’的病人 6：‘危重症’的病人
    :return: 满足筛选条件的所有病人的元组
    """
    info_to_query = []
    if query_type < 1:
        cursor.execute("select patient.p_id,patient.name "
                       "from patient left join sickbed_patient on patient.p_id=sickbed_patient.p_id "
                       "where transfer<>-1")
        all_patient = cursor.fetchall()
        if query_type == -1:
            for item in all_patient:
                cursor.execute("select area_type "
                               "from treatment_area, ward natural join sickbed natural join sickbed_patient "
                               "where ta_id=ward_area and p_id=%d" % item[0])
                result = cursor.fetchall()
                if len(result) != 0:
                    info_to_query.append((item[0], item[1], result[0][0]))
                else:
                    cursor.execute("select life_status from patient_status "
                                   "where p_id=%d order by time desc" % item[0])
                    result = cursor.fetchall()
                    if len(result) == 0 or result[0][0] == '在院治疗':
                        info_to_query.append((item[0], item[1], '隔离区'))
        elif query_type == 0:
            for item in all_patient:
                cursor.execute("select area_type "
                               "from treatment_area, ward natural join sickbed natural join sickbed_patient "
                               "where ta_id=ward_area and p_id=%d" % item[0])
                result = cursor.fetchall()
                if len(result) == 0:
                    cursor.execute("select life_status from patient_status "
                                   "where p_id=%d order by time desc" % item[0])
                    result = cursor.fetchall()
                    if len(result) == 0 or result[0][0] == '在院治疗':
                        info_to_query.append((item[0], item[1], '隔离区'))
    else:
        cursor.execute("select p_id from sickbed_patient natural join sickbed natural join ward,"
                       "treatment_area where ward_area=ta_id and area_type='%s'" % area_type)
        all_patient = cursor.fetchall()
        if query_type == 1:
            cursor.execute("select p_id,name,life_status,transfer "
                           "from patient natural join patient_status "
                           "where life_status='%s'" % '康复出院')
            result = cursor.fetchall()
            for item in result:
                info_to_query.append(item)
        elif query_type == 2:
            for p_id in all_patient:
                cursor.execute("select patient.p_id,name,life_status "
                               "from patient left join patient_status on patient.p_id=patient_status.p_id "
                               "where patient.p_id=%d order by time desc" % p_id)
                result = cursor.fetchall()
                if len(result) != 0 and result[0][2] == '在院治疗':
                    info_to_query.append(result[0])
        elif query_type == 3:
            cursor.execute("select p_id,name,life_status,transfer "
                           "from patient natural join patient_status "
                           "where life_status='%s'" % '病亡')
            result = cursor.fetchall()
            for item in result:
                info_to_query.append(item)
        elif query_type == 4:
            for p_id in all_patient:
                cursor.execute("select p_id,name,illness_level from patient natural join nat_report "
                               "where p_id=%d order by time desc" % p_id)
                result = cursor.fetchall()
                if len(result) != 0 and result[0][2] == '轻症':
                    info_to_query.append(result[0])
        elif query_type == 5:
            for p_id in all_patient:
                cursor.execute("select p_id,name,illness_level from patient natural join nat_report "
                               "where p_id=%d order by time desc" % p_id)
                result = cursor.fetchall()
                if len(result) != 0 and result[0][2] == '重症':
                    info_to_query.append(result[0])
        elif query_type == 6:
            for p_id in all_patient:
                cursor.execute("select p_id,name,illness_level from patient natural join nat_report "
                               "where p_id=%d order by time desc" % p_id)
                result = cursor.fetchall()
                if len(result) != 0 and result[0][2] == '危重症':
                    info_to_query.append(result[0])
    return info_to_query
