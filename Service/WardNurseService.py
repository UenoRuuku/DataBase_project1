from connector.connectMysql import db
from Service.BaseService import check_patient_discharge

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
    if check_patient_discharge(p_id):
        cursor.execute("update patient set transfer=-1 where p_id=%d" % p_id)
    db.commit()
