from connector.connectMysql import db

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

    cursor.execute("select ta_id from treatment_area where area_nurse_master=%d" % u_id)
    result = cursor.fetchall()
    ta_id = result[0][0]

    cursor.execute("insert into ward_nurse_treatment_area values (%d, %d)" % (add_u_id, ta_id))
    db.commit()
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
    for area in area_id:
        cursor.execute("select count(u_id) from ward_nurse_treatment_area "
                       "where ta_id=%d and u_id=%d" % (area, delete_u_id))
        result = cursor.fetchall()
        if result[0][0] > 0:
            delete_permission = True
            break

    if not delete_permission:
        return 0
    else:
        cursor.execute("delete from user where u_id=%d" % delete_u_id)
        cursor.execute("delete from ward_nurse_treatment_area where u_id=%d" % delete_u_id)
        cursor.execute("delete from sickbed_ward_nurse where u_id=%d" % delete_u_id)
        db.commit()
        return 1
