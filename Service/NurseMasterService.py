from Service.BaseService import *

cursor = db.cursor()


def add_ward_nurse(u_id, username, password, name):
    """
    :param u_id: 护士长的主键
    :type u_id: 整数
    :param username: 新增的病房护士的用户名
    :type username: 字符串，不长于 20 字符
    :param password: 新增的病房护士的密码
    :type password: 字符串，不长于 20 字符
    :param name: 新增的病房护士的名字
    :type name: 字符串，不长于 20 字符
    """
    # 将新增的病房护士插入 user 表中
    # 查找 treatment_area 表，找到 u_id 对应的 ta_id
    #       并将新增病房护士的 add_u_id 和找到的 ta_id 插入 ward_nurse_treatment_area 表中

    cursor.execute("insert into user (username, password, name, user_type) values "
                   "('%s', '%s', '%s', '%s')" % (username, password, name, 'ward_nurse'))
    add_u_id = db.insert_id()

    cursor.execute("select ta_id, area_type from treatment_area where area_nurse_master=%d" % u_id)
    result = cursor.fetchall()
    ta_id = result[0][0]
    area_type = result[0][1]

    cursor.execute("insert into ward_nurse_treatment_area values (%d, %d)" % (add_u_id, ta_id))
    db.commit()

    transfer_patient(area_type[:-4])

    return 1


def delete_ward_nurse(u_id, delete_u_id):
    """
    :param u_id: 护士长的主键
    :type u_id: 整数
    :param delete_u_id: 删除的病房护士的主键
    :type delete_u_id: 整数
    """
    # 查找 treatment_area 表，找到 u_id 对应的 ta_id 并判断 delete_u_id, ta_id 是否在 ward_nurse_treatment_area 表中
    # 如果在，则从 user, ward_nurse_treatment_area 和 sickbed_ward_nurse 表中将 delete_u_id 的记录删除

    area_id = []
    cursor.execute("select ta_id from treatment_area where area_nurse_master=%d" % u_id)
    result = cursor.fetchall()
    for item in result:
        area_id.append(item[0])
    if len(area_id) == 0:
        return 0

    delete_permission = False
    area_type = None
    for area in area_id:
        cursor.execute("select count(u_id) from ward_nurse_treatment_area "
                       "where ta_id=%d and u_id=%d" % (area, delete_u_id))
        result = cursor.fetchall()
        if result[0][0] > 0:
            delete_permission = True
            cursor.execute("select area_type from treatment_area where ta_id=%d" % area)
            result = cursor.fetchall()
            area_type = result[0][0]
            break

    if not delete_permission:
        return 0
    else:
        cursor.execute("delete from user where u_id=%d" % delete_u_id)
        cursor.execute("delete from ward_nurse_treatment_area where u_id=%d" % delete_u_id)

        # 查找被删除的病房护士正在照顾的所有病人并将其 transfer 属性设置为 1
        cursor.execute("select p_id from sickbed_ward_nurse natural join sickbed_patient "
                       "where u_id=%d" % delete_u_id)
        result = cursor.fetchall()
        for item in result:
            cursor.execute("update patient set transfer=1 where p_id=%d" % item[0])

        cursor.execute("delete from sickbed_ward_nurse where u_id=%d" % delete_u_id)
        db.commit()

        transfer_patient(area_type[:-4])

        return 1


def nurse_master_query_patient(nurse_master_id, query_type):
    """
    :param nurse_master_id: 护士长的主键
    :param query_type: -1：查询所有病人 0：’康复出院‘的病人 1：’在院治疗‘的病人 2：’病亡‘的病人
    3：可出院的病人 4：不可出院的病人 5：待转入其他区域的病人 6：不需转入其他区域的病人
    :return: 满足筛选条件的所有病人的元组
    """
    all_patient = []
    cursor.execute("select p_id from sickbed_patient natural join sickbed natural join ward,"
                   "treatment_area where ward_area=ta_id and area_nurse_master=%d" % nurse_master_id)
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
    elif query_type == 5:
        for item in all_patient:
            if item[3] == 1:
                info_to_query.append(item)
    elif query_type == 6:
        for item in all_patient:
            if item[3] != 1:
                info_to_query.append(item)
    return info_to_query


def nurse_master_query_nurses(nurse_master_id):
    """
    :param nurse_master_id: 护士长的主键
    :return: 护士长管理的区域的护士长和病房护士的信息
    """
    info_to_query = []
    cursor.execute("select u_id,username,name,info,user_type "
                   "from user natural join ward_nurse_treatment_area natural join treatment_area "
                   "where area_nurse_master=%d" % nurse_master_id)
    result = cursor.fetchall()
    for item in result:
        info_to_query.append(item)
    return info_to_query


def nurse_master_query_nurse_patient(ward_nurse_id):
    """
    :param ward_nurse_id: 需要查询的病房护士的主键
    :return: 该病房护士照顾的所有病人的信息
    """
    info_to_query = []
    cursor.execute("select p_id,name,info "
                   "from patient natural join sickbed_patient natural join sickbed_ward_nurse "
                   "where u_id=%d" % ward_nurse_id)
    result = cursor.fetchall()
    for item in result:
        info_to_query.append(item)
    return info_to_query


def nurse_master_query_sickbed_and_patient(nurse_master_id):
    """
    :param nurse_master_id: 护士长的主键
    :return: 护士长管理的区域的病床和病床上的病人的信息
    """
    info_to_query = []
    sickbeds = []
    cursor.execute("select b_id from sickbed natural join ward, treatment_area "
                   "where ward_area=ta_id and area_nurse_master=%d" % nurse_master_id)
    result = cursor.fetchall()
    for item in result:
        sickbeds.append(item[0])
    for b_id in sickbeds:
        cursor.execute("select b_id,bed_status from sickbed where b_id=%d" % b_id)
        result = cursor.fetchall()
        sickbed = result[0]
        if sickbed[1] == 1:
            cursor.execute("select p_id,name,info from sickbed_patient natural join patient "
                           "where b_id=%d" % sickbed[0])
            result = cursor.fetchall()
            info_to_query.append((sickbed[0], sickbed[1], result[0][0], result[0][1], result[0][2]))
        else:
            info_to_query.append((sickbed[0], sickbed[1], None, None, None))
    return info_to_query
