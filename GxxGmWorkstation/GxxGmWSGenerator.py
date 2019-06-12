#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
import datetime
import random

import MySQLdb

# 注册采集站设备

INSTANCE_COUNT = 2000
WORKSTATION_GBCODE_PRE = "4401040190128"
WORKSTATION_GBCODE_START = 1600000

db_config = \
    {
        'host': '192.168.55.10',
        'port': 3306,
        'user': 'root',
        'passwd': 'Gosuncn_2019',
        'db': 'uom-device-manager',
        'charset': 'utf8'
    }

# 连接到数据库
database = MySQLdb.connect(**db_config)
cursor = database.cursor()


for index in range(INSTANCE_COUNT):

    # 生成设备编码
    gbcode_id_number = "%07d" % (WORKSTATION_GBCODE_START + index)
    gbcode_str = WORKSTATION_GBCODE_PRE + gbcode_id_number
    print ("生成设备编码：" + gbcode_str)

    # 组装SQL语句
    # 生成时间
    take_time = datetime.datetime.now()
    take_time_str = take_time.strftime('%Y%m%d%H%M%S')
    take_time_str2 = take_time.strftime('%Y-%m-%d %H:%M:%S')

    rid = "RID-FAKE" + gbcode_str + take_time_str + gbcode_str
    address = "guangzhou"
    admin = "admin"
    auth_key = "1"
    default_expiredays = 365
    domain = "domain"
    downlod_url_prefix = "http://www.baidu.com"
    extend = ""
    gbcode = gbcode_str
    hid = "00-00-00-00-00"
    ip = "192.168.55.10"
    is_deleted = 0
    manufacturer = "GXX"
    name = gbcode_str
    online_status = 0
    org_code = "44010401"
    org_name = "one"
    org_path = "/org_path/"
    org_rid = "1"
    parent_storage_rid = ""
    phone = "13000000000"
    play_info = ""
    regist_time = take_time_str2
    root_path = ""
    security_rules = ""
    status_code = 1
    total_capacity = 1000
    used_capacity = 400
    ws_code = ""
    ws_conf = ""
    ws_modelnum = 0
    update_time = take_time_str2
    version = "3.4.5"
    source = ""

    sql_string = \
        "insert into uom_tb_gmvcs_device_workstation" \
        "(rid, address, admin, auth_key, default_expiredays, domain, downlod_url_prefix, extend, gbcode, hid, ip, is_deleted, manufacturer, name, " \
        "online_status, org_code, org_name, org_path, org_rid, parent_storage_rid, phone, play_info, regist_time, root_path, security_rules, status_code, " \
        "total_capacity, used_capacity, ws_code, ws_conf, ws_modelnum, update_time, version, source) " \
        "values " \
        "(\"%s\", \"guangzhou\", \"admin\", \"1\", 365, \"domain\", \"http://www.baidu.com\", \"\", \"%s\", \"00-00-00-00-00\", " \
        "\"192.168.55.10\", 0, \"GXX\", \"%s\", 0, \"44010401\", \"one\", \"/org_path/\", \"1\", \"\", \"13000000000\", " \
        "\"\", \"%s\", \"\", \"%s\", 1, 1000, 400, " \
        "\"\", \"\", 0, \"%s\", \"3.4.5\", \"\")" % (rid, gbcode, name, regist_time, security_rules, update_time)

    try:
        # 执行sql语句
        cursor.execute(sql_string)
        # 提交到数据库执行
        database.commit()
    except:
        # 发生错误时回滚
        database.rollback()

database.close()
