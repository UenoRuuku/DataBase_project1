from Service.EmNurseService import *
from Service.WardNurseService import *
from Service.NurseMasterService import *
from Service.DoctorService import *

for i in range(11):
    add_patient("轻症患者", "阴性", "2021-01-01 01:01:01", "轻症", "我为什么在这里啊")
add_ward_nurse(4, "temp_nurse", "000", "临时病房护士")
delete_ward_nurse(4, 17)
add_ward_nurse(4, "temp_nurse", "000", "临时病房护士")
delete_ward_nurse(4, 18)
for i in range(1, 12):
    record_patient_status('2021-01-01 02:02:02', 37.2, 'no', '在院治疗', i, i)
add_nat_report('阴性', '2021-01-02 01:01:01', '重症', 10)
update_nat_illness_level('危重症', 1)
record_patient_status('2021-01-02 02:02:02', 37.2, 'no', '在院治疗', 12, 10)
record_patient_status('2021-01-03 02:02:02', 37.2, 'no', '在院治疗', 12, 10)
add_nat_report('阴性', '2021-01-04 01:01:01', '轻症', 10)
add_nat_report('阴性', '2021-01-05 01:01:01', '轻症', 10)
for i in range(3):
    add_patient("重症患者", "阴性", "2021-01-05 01:01:01", "重症", "我为什么在这里啊")
add_patient("危重症患者", "阳性", "2021-01-06 01:01:01", "危重症", "我为什么在这里啊")
add_patient("轻症患者", "阴性", "2021-01-07 01:01:01", "轻症", "我为什么在这里啊")
update_nat_illness_level('重症', 3)
add_patient("重症患者", "阴性", "2021-01-07 01:01:01", "重症", "我为什么在这里啊")
add_ward_nurse(5, "temp_nurse", "000", "临时重症病房护士")
# 添加重症病房护士后，系统中所有待转入的病人都已自动转入相应病房
update_nat_illness_level('危重症', 12)
update_nat_illness_level('重症', 4)
update_nat_illness_level('轻症', 1)
update_patient_life_status('康复出院', 10)
update_patient_life_status('康复出院', 1)
update_patient_life_status('病亡', 5)
for i in range(12, 18):
    record_patient_status('2021-01-7 03:03:03', 37.2, 'no', '在院治疗', i + 4, i)
record_patient_status('2021-01-7 04:04:04', 37.2, 'no', '病亡', 19, 15)
