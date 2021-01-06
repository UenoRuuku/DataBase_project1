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
    #       并将新增病房护士的 u_id 和找到的 ta_id 插入 ward_nurse_treatment_area 表中


def delete_ward_nurse(u_id, delete_u_id):
    """
    :param u_id: 护士长的主键
    :type u_id: 整数
    :param delete_u_id: 删除的病房护士的主键
    :type delete_u_id: 整数
    """
    # 查找 treatment_area 表，找到 u_id 对应的 ta_id 并判断 delete_u_id, ta_id 是否在 ward_nurse_treatment_area 表中
    # 如果在，则从 user, ward_nurse_treatment_area 和 sickbed_ward_nurse 表中将 delete_u_id 的记录删除
