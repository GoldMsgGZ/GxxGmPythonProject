#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 作者：wangy
# 功能：此范例是业务数据生成模块
import traceback

import MySQLdb


MYSQL_HOST = "192.168.55.156"
MYSQL_PORT = 3306
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "mysql"
MYSQL_DBNAME = "auth-cas"


class GxxGmLEVAMdb:

    def __init__(self):
        self.detail = ""
        self.org_infos = list()


    def initialize_levam_orgs_info(self):
        # 从系统中初始化一些数据
        # 主要是组织架构部门信息，还有用户信息
        db = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USERNAME, passwd=MYSQL_PASSWORD, db=MYSQL_DBNAME,
                             charset="utf8")
        cursor = db.cursor()  # 创建一个游标对象
        # 搜索所有部门
        sql = "SELECT * FROM `uap_tb_gmvcs_organize`;"


        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                org_info = dict()
                org_info["org_id"] = row[0]
                org_info["duty_range"] = row[1]
                org_info["extend"] = row[2]
                org_info["order_no"] = int(row[3])
                org_info["org_code"] = row[4]
                org_info["org_name"] = row[5]
                org_info["path"] = row[6]
                org_info["update_time"] = str(row[7])
                org_info["parent"] = row[8]
                org_info["source"] = row[9]

                # 搜索部门所有用户
                sql2 = "SELECT * FROM `uap_tb_gmvcs_user` WHERE org_id=\"%s\";" % (org_info["org_id"].encode("utf8"))
                user_infos = list()

                # 执行SQL语句
                cursor.execute(sql2)
                # 获取所有记录列表
                results = cursor.fetchall()
                for row in results:
                    user_info = dict()
                    user_info["uid"] = row[0]
                    user_info["account"] = row[1]
                    user_info["admin"] = row[2]
                    user_info["create_time"] = row[3]
                    user_info["create_user"] = row[4]
                    user_info["email"] = row[5]
                    user_info["enable"] = row[6]
                    user_info["extend"] = row[7]
                    user_info["gender"] = row[8]
                    user_info["id_card"] = row[9]
                    user_info["is_deleted"] = row[10]
                    user_info["last_login_time"] = row[11]
                    user_info["login_status"] = row[12]
                    user_info["mobel_phone"] = row[13]
                    user_info["password"] = row[14]
                    user_info["repeat_login"] = row[15]
                    user_info["spell_abbr"] = row[16]
                    user_info["spell_full"] = row[17]
                    user_info["update_time"] = row[18]
                    user_info["user_code"] = row[19]
                    user_info["user_name"] = row[20]
                    user_info["user_type"] = row[21]
                    user_info["job_type"] = row[22]
                    user_info["org_id"] = row[23]
                    user_info["police_type"] = row[24]
                    user_info["last_login_ip"] = row[25]
                    user_info["source"] = row[26]
                    user_info["login_fail_num"] = row[27]
                    user_info["is_black_role"] = row[28]
                    user_info["pwd_valid_date"] = row[29]
                    user_info["pwd_expire_date"] = row[30]
                    user_info["login_limit"] = row[31]
                    user_info["ip_limit"] = row[32]
                    user_info["account_valid_days"] = row[33]
                    user_info["account_expire_date"] = row[34]
                    user_info["is_valid"] = row[35]

                    user_infos.append(user_info)
                    # print (user_info)

                org_info["users"] = user_infos
                self.org_infos.append(org_info)
                # print (org_info)

        except Exception:
            traceback.print_exc()

        # 关闭数据库，避免内存泄漏
        db.close()