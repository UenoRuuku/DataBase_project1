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
    :type info: 字符串，不长于 100 字符
    """
    # 如果没有空闲护士或者对应病情等级的空闲病房，将病人的 transfer 属性设置为 1 表示病人处于隔离区
    # 如果存在空闲护士或者对应病情等级的空闲病房，将病人的 transfer 属性设置为 0
    #       并且更新对应的 sickbed_ward_nurse, sickbed 和 sickbed_patient 表中的内容
