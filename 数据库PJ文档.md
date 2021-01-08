## 数据库PJ文档

> 18302010013  王中亮
>
> 18302010035  梁超毅

### ER图

![ER图（实际建立）](ER图（实际建立）.png)



### 数据库表结构说明

- **user表**

  - u_id：用户实体的主键，系统自增
  - username：登录用户名
  - password：登录密码
  - name：用户的姓名
  - info：用户的详细信息
  - user_type：用户类型，包括医生、护士长、病房护士、急诊护士

- **treatment_area表**

  - ta_id：治疗区域的主键，系统自增
  - area_type：治疗区域类型，包括轻症治疗区域、重症治疗区域、危重症治疗区域
  - area_doctor：治疗区域主治医生的主键，外键引用user表
  - area_nurse_master：治疗区域护士长的主键，外键引用user表

- **ward表**

  - w_id：病房的主键，系统自增
  - total_bed：病房最多容纳的病床数量
  - ward_area：病房所在的治疗区域的主键，外键引用treatmen_area表

- **sickbed表**

  - b_id：病床的主键，系统自增
  - bed_status：病床当前的状态，0表示空闲，1表示已占用
  - w_id：病床所在的病房的主键，外键引用ward表

- **patient表**

  - p_id：病人的主键，系统自增
  - name：病人的姓名
  - info：病人的详细信息
  - transfer：病人当前状态的一个属性，-1表示待出院，1表示待转移到其他区域

- **nat_report表**

  - r_id：核酸检测单的主键，系统自增
  - result：核酸检测的结果，取值为阴性或阳性
  - time：核酸检测的时间
  - illness_level：本次核酸检测的病人的病情等级
  - p_id：核酸检测的病人的主键，外键引用patient表

- **patient_status表**

  - ps_id：病人每日状态的主键，系统自增
  - time：记录这一条状态的时间
  - temperature：病人的体温
  - symptom：病人存在的症状
  - life_status：病人的生命状态，取值为康复出院、在院治疗或病亡
  - curr_report：病人最新的核酸检测单的主键，外键引用nat_report表
  - p_id：这一条状态所属的病人的主键，外键引用patient表

- **ward_nurse_treatment_area表**

  记录了ward_nurse和treatment_area之间的联系，一位ward_nurse最多和一个treatment_area相关联，因此将ward_nurse的主键作为联系集的主键

- **sickbed_ward_nurse表**

  记录了sickbed和ward_nurse之间的联系，一个sickbed最多和一个ward_nurse相关联，因此将sickbed的主键作为联系集的主键

- **sickbed_patient表**

  记录了sickbed和patient之间的联系，一个sickbed和一个patient之间一一对应，因此任意一方的主键都可作为该联系集的主键。此处选择了sickbed的主键作为联系集的主键

### 索引定义说明

数据库中的所有主键、外键都会自动创建索引，此处只说明自动建立的索引之外的索引

```sql
create index username_index on user (username);
create index ward_area_index on ward (ward_area);
create index patient_transfer_index on patient (transfer);
create index report_patient_index on NAT_report (p_id);
create index status_life_index on patient_status (life_status);
create index status_patient_index on patient_status (p_id);
```

- **username_index**

  系统使用过程中，对user的查询主要是登录时根据username查询到对应的password，因此为user表的username属性创建索引，加快根据username查询用户的效率

- **ward_area_index**

  为ward表的ward_area属性建立索引。ward_area指示了该ward所在的治疗区域，查询某个治疗区域中的ward时使用该索引可以加快查询效率

- **patient_transfer_index**

  为patient表中的transfer属性建立索引。在根据是否需要转移区域筛选病人时，使用该索引可以加快筛选查询的效率

- **report_patient_index**

  为nat_repoort表中的p_id属性建立索引。p_id指示了该nat_report所属的病人，查询某个病人的核酸检测单时使用该索引可以加快查询效率

- **status_life_index**

  为patient_status表中的life_status属性建立索引。life_status标识了病人的生命状态，在根据生命状态筛选病人时，使用该索引可以加快筛选查询的效率

- **status_patient_index**

  为patient_status表中的p_id属性建立索引。p_id指示了该patient_status所属的病人，查询某个病人日常状态时使用该索引可以加快查询效率



### 核心功能与储存过程

- **病人转移区域**

  隔离区中有病人时或者病人的病情等级发生变化而对应治疗区域中没有空闲资源时，病人会处于“待转移”的状态。当区域中因为病人转移或者病亡、出院等原因出现空闲资源时，待转移的病人需要转移到空闲的区域，而转移的病人又会产生新的空闲资源，形成一个递归。下面介绍病人转移区域功能的逻辑及相关SQL语句。

  1. **触发病人转移事件**

     当病人病情等级变化、病人病亡、病人出院时，会触发病人转移事件，调用`transfer_patient(illness_level)`函数，其中 illness_level 是出现了空闲资源的治疗区域对应的病情等级

  2. **查找所有需要转入对应区域的病人**

     查找需要转入对应区域的病人的SQL语句如下：

     ```sql
     select p_id from nat_report where p_id=%d and illness_level='%s' order by time desc
     select life_status from patient_status where p_id=%d order by time desc
     ```

     前一句找到最新的 illness_level 为对应 illness_level 的所有病人，后一句查找这些病人的 life_status 并将所有在院治疗的病人筛选出来（生命状态不为在院治疗的病人无需转移）

  3. **优先将隔离区的病人转移到空闲区域**

     隔离区的病人优先转移，因此系统先查找隔离区中的所有需要转入 illness_level 对应的区域的病人，将它们转入空闲区域。隔离区中的病人为所有待转移病人中没有病床的病人。查询病人病床的SQL语句如下：

     ```sql
     select b_id from sickbed_patient where p_id=%d
     ```

     将其中结果为空的病人筛选出来即为隔离区的病人。将病人转移的SQL语句如下：

     ```sql
     -- 将病床护士与病床解除关系
     delete from sickbed_ward_nurse where b_id=%d
     -- 将病床的状态设置为 0 （空闲）
     update sickbed set bed_status=0 where b_id=%d
     -- 将病人与病床解除关系
     delete from sickbed_patient where b_id=%d
     -- 将病人的待转移属性 transfer 设置为 0
     update patient set transfer=0 where p_id=%d
     -- 建立新的病床护士与病床的关系
     insert into sickbed_ward_nurse values (%d, %d)
     -- 将新的病床的状态设置为 1 （已占用）
     update sickbed set bed_status=1 where b_id=%d
     -- 建立新的病人与病床的关系
     insert into sickbed_patient values (%d, %d)
     ```

     执行上述SQL语句即完成了病人的转移

  4. **将其他治疗区域的病人转移到空闲区域**

     若步骤 3 完成后，illness_level 对应的区域中仍有空闲资源，则将其它治疗区域中待转移到该治疗区域的病人转移，转移逻辑与步骤 3 中类似。每次转移成功，就意味着病人的转出区域出现了空闲资源，因此需要递归调用 `transfer_patient(illness_level)`方法，这里的 illness_level 为转出区域对应的的病情等级。

     一旦转移过程中发现当前区域已经没有空闲资源了（床位或者病房护士不足），函数立即返回，保证了递归会收敛

  5. **递归调用返回，病人转移任务结束**

  上述步骤完成后，一次病人转移事件即处理结束。所有转移过程中所有的空闲资源都会得到利用。

- **病人查询筛选**

  系统为用户提供了多种查询和筛选病人的功能。下面介绍几种筛选以及相关SQL语句。

  1. 主治医生筛选当前区域所有的病人的 id, name, life_status, transfer 属性

     ```sql
     -- 获取当前区域中的所有病人的 id
     select p_id from sickbed_patient natural join sickbed natural join ward,treatment_area where ward_area=ta_id and area_doctor=%d
     -- 获取病人的 id, name, life_status, transfer 属性
     select patient.p_id,name,life_status,transfer 
     from patient left join patient_status on patient.p_id=patient_status.p_id 
     where patient.p_id=%d order by time desc
     ```

     首先对 sickbed_patient, sickbed, treatment_area 三个表做自然连接，取出主治医生管理的区域的所有病床上的病人 id

     之后，将 patient 与 patient_status 做左外连接并按照时间排序，得到所有病人最新的 life_status，并与 id, name, transfer 属性作为查询结果返回

  2. 主治医生筛选当前区域所有待出院的病人

     ```python
     for item in all_patient:
         if item[3] == -1:
             info_to_query.append(item)
     ```

     1 中已经将区域内的所有病人筛选出来了，因此筛选区域内所有待出院的病人只需要将所有病人中 transfer 属性为 -1 的病人筛选出来。使用一个简单的循环即可实现

- **护士长增删病房护士**

  1. 增加病房护士时，需要找到护士长对应的治疗区域，将新病房护士插入 user 表中，之后将新病房护士加入对应的治疗区域中。对应的SQL语句如下：

     ```sql
     -- 将新病房护士插入 user 表中
     insert into user (username, password, name, user_type) values ('%s', '%s', '%s', '%s')
     -- 查找护士长对应的治疗区域
     select ta_id, area_type from treatment_area where area_nurse_master=%d
     -- 将新病房护士加入对应治疗区域
     insert into ward_nurse_treatment_area values (%d, %d)
     ```

     之后，由于对应的治疗区域出现的新的空闲资源（新的病房护士），系统需要调用`transfer_patient()`函数对病人进行转移，函数的参数为新病房护士加入的治疗区域对应的病情等级

  2. 删除病房护士时，需要查询护士长对应的治疗区域中是否存在该护士，若存在才可以删除。对应的SQL语句如下：

     ```sql
     -- 寻找删除的护士是否存在于护士长管理的治疗区域中
     select count(u_id) from ward_nurse_treatment_area where ta_id=%d and u_id=%d
     -- 将病房护士从 user 表中移除
     delete from user where u_id=%d
     -- 将病房护士从对应治疗区域中移除
     delete from ward_nurse_treatment_area where u_id=%d
     ```

     之后，如果被删除的病房护士有正在照顾的病人，则将这些病人的 transfer 属性设置为 1 表明这些病人需要进行转移，之后调用 `transfer_patient()`函数对病人进行转移，函数的参数为被删除的病房护士对应的治疗区域。对应的SQL语句如下：

     ```sql
     -- 查找被删除的病房护士正在照顾的病人
     select p_id from sickbed_ward_nurse natural join sickbed_patient where u_id=%d
     -- 将病人的 transfer 属性设置为 1
     update patient set transfer=1 where p_id=%d
     -- 将被删除的病房护士与病床的关系解除
     delete from sickbed_ward_nurse where u_id=%d
     ```

  系统中涉及到资源变化的操作进行后，一定要触发病人转移的事件保证资源能够立即得到分配利用。

- 其它

  由于系统中的信息筛选和储存涉及到很多SQL语句与逻辑，在此无法一一列出，具体实现请参考源代码。
