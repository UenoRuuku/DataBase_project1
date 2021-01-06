from connector.connectMysql import db

cursor = db.cursor()


def add_nat_report(result, time, illness_level, p_id):
    """
    :param result: 病人的核酸检测结果
    :type result: 字符串，'阴性' 或 '阳性'
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


def update_patient_life_status(life_status, p_id):
    """
    :param life_status: 病人更改后的生命状态
    :type life_status: 字符串，'康复出院'，'在院治疗' 或 '病亡'
    :param p_id: 病人的主键
    :type p_id: 整数
    """
    # 更新 patient_status 表中对应 p_id 的且 time 是最新的那一条记录的 life_status
    # 如果病人病亡，更新对应的 sickbed_ward_nurse, sickbed 和 sickbed_patient 表中的内容
