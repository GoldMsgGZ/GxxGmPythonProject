#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# Author : WangYu
# Date   : 2019-06-14 21:21
# Detail : 此脚本用于将Excel数据读取出来，并存入数据库
#          本例使用xlrd读取Excel文件，pip install xlrd
#          本例使用MySQLdb进行数据库导入，pip install mysqldb
#
import datetime

import xlrd
import MySQLdb


# Excel路径，尽量使用英文路径
EXCEL_PATH = "E:\\脱敏版.xls"

# MySQL参数
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASS = "video"
MYSQL_DB = "levam"

# 重点人员库ID
PERSON_DB_ID = 2

# 存放重点人员人脸图片的FTP目录
FTP_DIR="/disk0/upload/20190614/"

# 连接到MySQL数据库
db = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB, charset='utf8')
#获取操作游标
cursor = db.cursor()

# 打开Excel
excel_handle = xlrd.open_workbook(EXCEL_PATH)

# 根据索引获取第一个sheet
sheet = excel_handle.sheet_by_index(0)

# 获得行数、列数
row_num = sheet.nrows
col_num = sheet.ncols

# 获取当前时间戳
take_time = datetime.datetime.now()
take_time_str2 = take_time.strftime('%Y-%m-%d')



try:
    # # 创建重点人员库
    # sql = "INSERT INTO uap_tb_gmvcs_key_person_type_db(db_name, db_desc, create_time, update_time) VALUES('重点人员库', '在逃人员', '2019-06-14', '2019-06-14');"
    # cursor.execute(sql)
    # db.commit()

    # 读取Excel中的数据，导入重点人员
    for index in range(1, row_num):
        person_name = sheet.row_values(index)[0]
        id_card = sheet.row_values(index)[1]
        birth_date = int(sheet.row_values(index)[2])
        key_person_detail = sheet.row_values(index)[3]
        person_district = sheet.row_values(index)[4]
        person_address = sheet.row_values(index)[5]
        person_reg_img = FTP_DIR + str(id_card) + ".jpg"

        sql = "insert " \
              "into uap_tb_gmvcs_key_person_recognition(person_id, key_person_type_db_id, id_card, person_name, birth_date, key_person_detail, person_district, person_address, person_reg_img, remarks, create_time, update_time, is_deleted)" \
              "values (\"%s\", %d, \"%s\", \"%s\", %d, \"%s\", \"%s\", \"%s\", \"%s\", \"\", \"%s\", \"%s\", 0)" % (id_card, PERSON_DB_ID, id_card, person_name, birth_date, key_person_detail, person_district, person_address, person_reg_img, take_time_str2, take_time_str2)

        cursor.execute(sql)

    db.commit()

except Exception as e:
    db.rollback()

db.close()