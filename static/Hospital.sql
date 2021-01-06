create table user
(
    u_id int auto_increment,
    username varchar (20) not null,
    password varchar (20) not null,
    name varchar (20),
    info varchar (100),
    user_type varchar (15) check (user_type in
    ('doctor', 'nurse_master', 'ward_nurse', 'em_nurse')),
    primary key (u_id)
);

create table treatment_area
(
    ta_id int auto_increment,
    area_type varchar (10) check (area_type in
    ('轻症治疗区域', '重症治疗区域', '危重症治疗区域')),
    area_doctor int,
    area_nurse_master int,
    primary key (ta_id),
    foreign key (area_doctor) references user (u_id)
        on delete set null,
    foreign key (area_nurse_master) references user (u_id)
        on delete set null
);

create table ward
(
    w_id int auto_increment,
    total_bed int,
    available_bed int,
    ward_area int not null,
    primary key (w_id),
    foreign key (ward_area) references treatment_area (ta_id)
        on delete cascade
);

create table sickbed
(
    b_id int auto_increment,
    bed_status int default 0 check (bed_status in
    (0, 1)),
    primary key (b_id)
);

create table ward_nurse_sickbed
(
    b_id int,
    u_id int,
    primary key (b_id)
);

create table ward_sickbed
(
    w_id int,
    b_id int,
    primary key (w_id, b_id)
);

create table patient
(
    p_id int auto_increment,
    name varchar (20),
    info varchar (100),
    -- -1：可以出院  0：处于病房  1：处于隔离区或者病情评级与治疗区域不符
    transfer int check (transfer in
    (-1, 0, 1)),
    primary key (p_id)
);

create table sickbed_patient
(
    b_id int,
    p_id int,
    primary key (b_id)
);

create table NAT_report
(
    r_id int auto_increment,
    result varchar (2) check (result in
    ('阴性', '阳性')),
    time timestamp not null,
    illness_level varchar (3) check (illness_level in
    ('轻症', '重症', '危重症')),
    p_id int not null,
    primary key (r_id),
    foreign key (p_id) references patient (p_id)
        on delete cascade
);

create table patient_status
(
    ps_id int auto_increment,
    time timestamp not null,
    temperature numeric (3, 1),
    symptom varchar (100),
    life_status varchar (4) check (life_status in
    ('康复出院', '在院治疗', '病亡')),
    curr_report int,
    p_id int not null,
    primary key (ps_id),
    foreign key (curr_report) references NAT_report (r_id)
        on delete set null,
    foreign key (p_id) references patient (p_id)
        on delete cascade
);