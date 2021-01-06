from connector.connectMysql import db

cursor = db.cursor()


def add_patient(name, result, time, illness_level, info='无'):
    """
    :param name: 病人姓名
    :type name: 字符串，不长于 20 字符
    :param result: 病人的核酸检测结果
    :type result: 字符串，'阴性' 或 '阳性'
    :param time: 核酸检测的时间
    :type time: 字符串，格式为 yyyy-mm-dd hh:mm:ss，例如，2021-01-06 20:34:11
    :param illness_level: 病人的病情等级
    :type illness_level: 字符串，'轻症'，'重症' 或 '危重症'
    :param info: 病人的其他基本信息，默认为 '无'
    :type info: 字符串，不长于100字符
    """
    # 如果没有空闲护士或者对应病情等级的空闲病房，将病人的 transfer 属性设置为 1 表示病人处于隔离区
    # 如果存在空闲护士或者对应病情等级的空闲病房，将病人的 transfer 属性设置为 0
    #       并且更新对应的 sickbed_ward_nurse, sickbed 和 sickbed_patient 表中的内容


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


def record_patient_status(time, temperature, symptom, life_status, curr_report, p_id):
    """
    :param time: 登记病人状态的时间
    :type time: 字符串，格式为 yyyy-mm-dd hh:mm:ss，例如，2021-01-06 20:34:11
    :param temperature: 病人的体温
    :type temperature: 浮点数，格式为 xx.x，例如，37.3
    :param symptom: 病人存在的症状
    :type symptom: 字符串，不长于100字符
    :param life_status: 病人的生命状态
    :type life_status: 字符串，'康复出院'，'在院治疗' 或 '病亡'
    :param curr_report: 病人最新的核酸检测单的主键
    :type curr_report: 整数
    :param p_id: 病人的主键
    :type p_id: 整数
    """
    # 如果满足了出院条件，将病人的 transfer 属性设置为 -1
