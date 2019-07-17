#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 作者：wangy
# 功能：此范例是模拟生成
import random
import time

from GxxGmCascade import GxxGmBaseData


class GxxGmGA:

    def __init__(self):
        self.detail = u"主要生成警情、案件信息"


    def generate_jq_aj(self, item_count):
        # 生成已关联的警情案件信息
        receive_alarm_json = dict()
        receive_alarm_json["jj"] = list()

        handle_alarm_situation_json = dict()
        handle_alarm_situation_json["cj"] = list()

        case_info_json = dict()
        case_info_json["aj"] = list()

        for index in range(item_count):
            # 这里处理一下，接警人，处警人均为同一人，部门也是所属部门的
            org_code, org_name, police_code, police_name = GxxGmBaseData.get_org_and_police(self.orgs)
            # 生成警情类型
            alarm_situation_id, alarm_situation_type = GxxGmBaseData.get_alarm_situation_type()
            # 生成案发地点和警情信息
            province_name, province_code, city_name, city_code, county_name, county_code = GxxGmBaseData.get_random_division()
            alarm_situation_info, address = GxxGmBaseData.get_alarm_content(province_name, city_name, county_name,
                                                                            GxxGmBaseData.road, alarm_situation_type)

            # 构建接警信息
            receive_alarm = dict()
            receive_alarm["bjfs"] = GxxGmBaseData.get_alarm_type()  # 报警方式
            receive_alarm["bjnr"] = alarm_situation_info  # 报警内容
            receive_alarm["bjrdh"] = GxxGmBaseData.get_phone_nunber()  # 报警人电话
            receive_alarm["bjrxb"] = random.choice(["男", "女"])  # 报警人性别
            receive_alarm["bjrxm"] = GxxGmBaseData.get_person_name()  # 报警人姓名
            receive_alarm["bjsj"] = GxxGmBaseData.get_current_datetime()  # 报警事件
            receive_alarm["djsj"] = GxxGmBaseData.get_current_datetime()
            receive_alarm["gxsj"] = GxxGmBaseData.get_current_datetime()
            receive_alarm["jjdw"] = org_code  # 接警单位
            receive_alarm["jjdwmc"] = org_name
            receive_alarm["jjr"] = police_code  # 接警人
            receive_alarm["jjrmc"] = police_name  # 接警人名称
            receive_alarm["jqbh"] = "JQ" + org_code + str(GxxGmBaseData.get_current_datetime())  #
            receive_alarm["jqlb"] = alarm_situation_id  #
            receive_alarm["jqlbmc"] = alarm_situation_type  #
            receive_alarm["jqmc"] = alarm_situation_info  #
            receive_alarm["sfdd"] = address  #
            receive_alarm["sfsj"] = GxxGmBaseData.get_current_datetime()  #
            receive_alarm["wj"] = list()  #
            receive_alarm_json["jj"].append(receive_alarm)

            # 生成警情信息
            handle_alarm_situation = dict()
            handle_alarm_situation["cjdh"] = "CJ" + org_code + str(GxxGmBaseData.get_current_datetime())
            handle_alarm_situation["cjdw"] = org_code
            handle_alarm_situation["cjdwmc"] = org_name
            handle_alarm_situation["cjr"] = police_code
            handle_alarm_situation["cjrmc"] = police_name
            handle_alarm_situation["cjsj"] = GxxGmBaseData.get_current_datetime()
            handle_alarm_situation["ddxcsj"] = GxxGmBaseData.get_current_datetime()
            handle_alarm_situation["djsj"] = GxxGmBaseData.get_current_datetime()
            handle_alarm_situation["gxsj"] = GxxGmBaseData.get_current_datetime()
            handle_alarm_situation["jqbh"] = receive_alarm["jqbh"]
            handle_alarm_situation["mjyj"] = ""
            handle_alarm_situation_json["cj"].append(handle_alarm_situation)

            case_info = dict()
            case_info["afdd"] = address
            case_info["afsj"] = GxxGmBaseData.get_current_datetime()
            case_info["ajbh"] = "AJ" + org_code + str(GxxGmBaseData.get_current_datetime())
            case_info["ajlb"] = alarm_situation_id
            case_info["ajlbmc"] = alarm_situation_type
            case_info["ajly"] = ""
            case_info["ajmc"] = alarm_situation_info
            case_info["anzt"] = "0300"
            case_info["jasj"] = GxxGmBaseData.get_current_datetime()
            case_info["jjbh"] = list()
            case_info["jjbh"].append(receive_alarm["jqbh"])
            case_info["jyaq"] = alarm_situation_info
            case_info["lasj"] = GxxGmBaseData.get_current_datetime()
            case_info["rksj"] = GxxGmBaseData.get_current_datetime()
            case_info["sldw"] = org_code
            case_info["sldwmc"] = org_name
            case_info["wjxx"] = list()
            case_info["ysqssj"] = GxxGmBaseData.get_current_datetime()
            case_info["zbdw"] = org_code
            case_info["zbdwmc"] = org_name
            case_info["zbmjxm"] = police_name
            case_info["zbr"] = police_code
            case_info_json["aj"].append(case_info)

            time.sleep(0.001)

        return receive_alarm_json, handle_alarm_situation_json, case_info_json


    def generate_jq(self, item_count):
        # 生成已关联的警情案件信息
        receive_alarm_json = dict()
        receive_alarm_json["jj"] = list()

        handle_alarm_situation_json = dict()
        handle_alarm_situation_json["cj"] = list()

        for index in range(item_count):
            # 这里处理一下，接警人，处警人均为同一人，部门也是所属部门的
            org_code, org_name, police_code, police_name = GxxGmBaseData.get_org_and_police(self.orgs)
            # 生成警情类型
            alarm_situation_id, alarm_situation_type = GxxGmBaseData.get_alarm_situation_type()
            # 生成案发地点和警情信息
            province_name, province_code, city_name, city_code, county_name, county_code = GxxGmBaseData.get_random_division()
            alarm_situation_info, address = GxxGmBaseData.get_alarm_content(province_name, city_name, county_name,
                                                                            GxxGmBaseData.road, alarm_situation_type)

            # 构建接警信息
            receive_alarm = dict()
            receive_alarm["bjfs"] = GxxGmBaseData.get_alarm_type()  # 报警方式
            receive_alarm["bjnr"] = alarm_situation_info  # 报警内容
            receive_alarm["bjrdh"] = GxxGmBaseData.get_phone_nunber()  # 报警人电话
            receive_alarm["bjrxb"] = random.choice(["男", "女"])  # 报警人性别
            receive_alarm["bjrxm"] = GxxGmBaseData.get_person_name()  # 报警人姓名
            receive_alarm["bjsj"] = GxxGmBaseData.get_current_datetime()  # 报警事件
            receive_alarm["djsj"] = GxxGmBaseData.get_current_datetime()
            receive_alarm["gxsj"] = GxxGmBaseData.get_current_datetime()
            receive_alarm["jjdw"] = org_code  # 接警单位
            receive_alarm["jjdwmc"] = org_name
            receive_alarm["jjr"] = police_code  # 接警人
            receive_alarm["jjrmc"] = police_name  # 接警人名称
            receive_alarm["jqbh"] = "JQ" + org_code + str(GxxGmBaseData.get_current_datetime())  #
            receive_alarm["jqlb"] = alarm_situation_id  #
            receive_alarm["jqlbmc"] = alarm_situation_type  #
            receive_alarm["jqmc"] = alarm_situation_info  #
            receive_alarm["sfdd"] = address  #
            receive_alarm["sfsj"] = GxxGmBaseData.get_current_datetime()  #
            receive_alarm["wj"] = list()  #
            receive_alarm_json["jj"].append(receive_alarm)

            # 生成警情信息
            handle_alarm_situation = dict()
            handle_alarm_situation["cjdh"] = "CJ" + org_code + str(GxxGmBaseData.get_current_datetime())
            handle_alarm_situation["cjdw"] = org_code
            handle_alarm_situation["cjdwmc"] = org_name
            handle_alarm_situation["cjr"] = police_code
            handle_alarm_situation["cjrmc"] = police_name
            handle_alarm_situation["cjsj"] = GxxGmBaseData.get_current_datetime()
            handle_alarm_situation["ddxcsj"] = GxxGmBaseData.get_current_datetime()
            handle_alarm_situation["djsj"] = GxxGmBaseData.get_current_datetime()
            handle_alarm_situation["gxsj"] = GxxGmBaseData.get_current_datetime()
            handle_alarm_situation["jqbh"] = receive_alarm["jqbh"]
            handle_alarm_situation["mjyj"] = ""
            handle_alarm_situation_json["cj"].append(handle_alarm_situation)

            time.sleep(0.001)

        return receive_alarm_json, handle_alarm_situation_json
