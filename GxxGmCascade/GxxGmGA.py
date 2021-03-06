#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 作者：wangy
# 功能：此范例是模拟生成
import random
import time

import GxxGmBaseData


class GxxGmGA:

    def __init__(self):
        self.detail = u"主要生成警情、案件信息"
        self.base_data = GxxGmBaseData.GxxGmBaseData()


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
            org_code, org_name, police_code, police_name = self.base_data.get_org_and_police(self.base_data.levam_db.org_infos)
            # 生成警情类型
            alarm_situation_id, alarm_situation_type = self.base_data.get_alarm_situation_type()
            # 生成案发地点和警情信息
            province_name, province_code, city_name, city_code, county_name, county_code = self.base_data.get_random_division()
            alarm_situation_info, address = self.base_data.get_alarm_content(province_name, city_name, county_name,
                                                                             GxxGmBaseData.road, alarm_situation_type)

            # 构建接警信息
            receive_alarm = dict()
            receive_alarm["bjfs"] = self.base_data.get_alarm_type()  # 报警方式
            receive_alarm["bjnr"] = alarm_situation_info  # 报警内容
            receive_alarm["bjrdh"] = self.base_data.get_phone_nunber()  # 报警人电话
            receive_alarm["bjrxb"] = random.choice(["男", "女"])  # 报警人性别
            receive_alarm["bjrxm"] = self.base_data.get_person_name()  # 报警人姓名
            receive_alarm["bjsj"] = self.base_data.get_current_datetime()  # 报警事件
            receive_alarm["djsj"] = self.base_data.get_current_datetime()
            receive_alarm["gxsj"] = self.base_data.get_current_datetime()
            receive_alarm["jjdw"] = org_code  # 接警单位
            receive_alarm["jjdwmc"] = org_name
            receive_alarm["jjr"] = police_code  # 接警人
            receive_alarm["jjrmc"] = police_name  # 接警人名称
            receive_alarm["jqbh"] = "JQ" + org_code + str(self.base_data.get_current_datetime())  #
            receive_alarm["jqlb"] = alarm_situation_id  #
            receive_alarm["jqlbmc"] = alarm_situation_type  #
            receive_alarm["jqmc"] = alarm_situation_info  #
            receive_alarm["sfdd"] = address  #
            receive_alarm["sfsj"] = self.base_data.get_current_datetime()  #
            receive_alarm["wj"] = list()  #
            receive_alarm_json["jj"].append(receive_alarm)

            # 生成警情信息
            handle_alarm_situation = dict()
            handle_alarm_situation["cjdh"] = "CJ" + org_code + str(self.base_data.get_current_datetime())
            handle_alarm_situation["cjdw"] = org_code
            handle_alarm_situation["cjdwmc"] = org_name
            handle_alarm_situation["cjr"] = police_code
            handle_alarm_situation["cjrmc"] = police_name
            handle_alarm_situation["cjsj"] = self.base_data.get_current_datetime()
            handle_alarm_situation["ddxcsj"] = self.base_data.get_current_datetime()
            handle_alarm_situation["djsj"] = self.base_data.get_current_datetime()
            handle_alarm_situation["gxsj"] = self.base_data.get_current_datetime()
            handle_alarm_situation["jqbh"] = receive_alarm["jqbh"]
            handle_alarm_situation["mjyj"] = ""
            handle_alarm_situation_json["cj"].append(handle_alarm_situation)

            case_info = dict()
            case_info["afdd"] = address
            case_info["afsj"] = self.base_data.get_current_datetime()
            case_info["ajbh"] = "AJ" + org_code + str(self.base_data.get_current_datetime())
            case_info["ajlb"] = alarm_situation_id
            case_info["ajlbmc"] = alarm_situation_type
            case_info["ajly"] = ""
            case_info["ajmc"] = alarm_situation_info
            case_info["anzt"] = "0300"
            case_info["jasj"] = self.base_data.get_current_datetime()
            case_info["jjbh"] = list()
            case_info["jjbh"].append(receive_alarm["jqbh"])
            case_info["jyaq"] = alarm_situation_info
            case_info["lasj"] = self.base_data.get_current_datetime()
            case_info["rksj"] = self.base_data.get_current_datetime()
            case_info["sldw"] = org_code
            case_info["sldwmc"] = org_name
            case_info["wjxx"] = list()
            case_info["ysqssj"] = self.base_data.get_current_datetime()
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
            org_code, org_name, police_code, police_name = self.base_data.get_org_and_police(
                self.base_data.levam_db.org_infos)
            # 生成警情类型
            alarm_situation_id, alarm_situation_type = self.base_data.get_alarm_situation_type()
            # 生成案发地点和警情信息
            province_name, province_code, city_name, city_code, county_name, county_code = \
                self.base_data.get_random_division()
            alarm_situation_info, address = self.base_data.get_alarm_content(province_name, city_name, county_name,
                                                                             GxxGmBaseData.road, alarm_situation_type)

            # 构建接警信息
            receive_alarm = dict()
            receive_alarm["bjfs"] = self.base_data.get_alarm_type()  # 报警方式
            receive_alarm["bjnr"] = alarm_situation_info  # 报警内容
            receive_alarm["bjrdh"] = self.base_data.get_phone_nunber()  # 报警人电话
            receive_alarm["bjrxb"] = random.choice(["男", "女"])  # 报警人性别
            receive_alarm["bjrxm"] = self.base_data.get_person_name()  # 报警人姓名
            receive_alarm["bjsj"] = self.base_data.get_current_datetime()  # 报警事件
            receive_alarm["djsj"] = self.base_data.get_current_datetime()
            receive_alarm["gxsj"] = self.base_data.get_current_datetime()
            receive_alarm["jjdw"] = org_code  # 接警单位
            receive_alarm["jjdwmc"] = org_name
            receive_alarm["jjr"] = police_code  # 接警人
            receive_alarm["jjrmc"] = police_name  # 接警人名称
            receive_alarm["jqbh"] = "JQ" + org_code + str(self.base_data.get_current_datetime())  #
            receive_alarm["jqlb"] = alarm_situation_id  #
            receive_alarm["jqlbmc"] = alarm_situation_type  #
            receive_alarm["jqmc"] = alarm_situation_info  #
            receive_alarm["sfdd"] = address  #
            receive_alarm["sfsj"] = self.base_data.get_current_datetime()  #
            receive_alarm["wj"] = list()  #
            receive_alarm_json["jj"].append(receive_alarm)

            # 生成警情信息
            handle_alarm_situation = dict()
            handle_alarm_situation["cjdh"] = "CJ" + org_code + str(self.base_data.get_current_datetime())
            handle_alarm_situation["cjdw"] = org_code
            handle_alarm_situation["cjdwmc"] = org_name
            handle_alarm_situation["cjr"] = police_code
            handle_alarm_situation["cjrmc"] = police_name
            handle_alarm_situation["cjsj"] = self.base_data.get_current_datetime()
            handle_alarm_situation["ddxcsj"] = self.base_data.get_current_datetime()
            handle_alarm_situation["djsj"] = self.base_data.get_current_datetime()
            handle_alarm_situation["gxsj"] = self.base_data.get_current_datetime()
            handle_alarm_situation["jqbh"] = receive_alarm["jqbh"]
            handle_alarm_situation["mjyj"] = ""
            handle_alarm_situation_json["cj"].append(handle_alarm_situation)

            time.sleep(0.001)

        return receive_alarm_json, handle_alarm_situation_json


    def generate_dzjk(self, item_count):
        # 生成电子监控信息(非现场处罚)

        dzjk = dict()
        dzjk["wtpz"] = list()

        for index in range(item_count):
            # 这里处理一下，接警人，处警人均为同一人，部门也是所属部门的
            org_code, org_name, police_code, police_name = self.base_data.get_org_and_police(
                self.base_data.levam_db.org_infos)

            alarm_situation_id, alarm_situation_type = self.base_data.get_alarm_situation_type()
            province_name, province_code, city_name, city_code, county_name, county_code = \
                self.base_data.get_random_division()
            alarm_situation_info, address = self.base_data.get_alarm_content(province_name, city_name, county_name,
                                                                             GxxGmBaseData.road, alarm_situation_type)
            wtpz = dict()
            wtpz["cjjg"] = org_code                         # 违法采集机关，需在系统存在
            wtpz["hphm"] = self.base_data.get_car_card()    # 号牌号码
            wtpz["hpzl"] = "普通车辆"   # 号牌种类
            wtpz["jdsbh"] = "JDS" + org_code + str(self.base_data.get_current_datetime())  # 决定书编号
            wtpz["wfbh"] = "WFBH" + org_code + str(self.base_data.get_current_datetime())   # 违法编号
            wtpz["wfdz"] = address   # 违法地址
            wtpz["wfsj"] = self.base_data.get_current_datetime()   # 违法时间
            wtpz["wftzsh"] = "WFTZSH" + org_code + str(self.base_data.get_current_datetime()) # 违法通知书编号
            wtpz["wfxw"] = "WFXW" + org_code + str(self.base_data.get_current_datetime())   # 违法行为代码
            wtpz["wj"] = list()
            wtpz["xh"] = "XH" + org_code + str(self.base_data.get_current_datetime())    # 序号
            wtpz["zqmj"] = police_code   # 执勤民警警号，需在系统存在
            dzjk["wtpz"].append(wtpz)

            time.sleep(0.001)

        return dzjk


    def generate_qzhcsh(self, item_count):
        # 生成强制措施(现场违法)

        qzhcsh = dict()
        qzhcsh["qzcs"] = list()

        for index in range(item_count):
            # 这里处理一下，接警人，处警人均为同一人，部门也是所属部门的
            org_code, org_name, police_code, police_name = self.base_data.get_org_and_police(
                self.base_data.levam_db.org_infos)

            alarm_situation_id, alarm_situation_type = self.base_data.get_alarm_situation_type()
            province_name, province_code, city_name, city_code, county_name, county_code = \
                self.base_data.get_random_division()
            alarm_situation_info, address = self.base_data.get_alarm_content(province_name, city_name, county_name,
                                                                             GxxGmBaseData.road, alarm_situation_type)

            qzcs = dict()
            qzcs["dsr"] = self.base_data.get_person_name() # 当事人
            qzcs["hphm"] = self.base_data.get_car_card() # 号牌号码
            qzcs["hpzl"] = "普通车辆" # 号牌种类
            qzcs["jszh"] = self.base_data.get_person_id() # 驾驶证号
            qzcs["pzbh"] = "" #
            qzcs["wfdz"] = "" #
            qzcs["wfsj"] = "" #
            qzcs["wfxw1"] = "" # 违法行为1
            qzcs["wfxw2"] = ""
            qzcs["wfxw3"] = ""
            qzcs["wfxw4"] = ""
            qzcs["wfxw5"] = ""
            qzcs["wj"] = list()
            qzcs["wslb"] = "" # 文书类别
            qzcs["xh"] = "" # 序号
            qzcs["zqbm"] = "" # 执勤部门编号
            qzcs["zqmj"] = "" # 执勤民警警号

            qzhcsh["wtpz"].append(qzcs)

            time.sleep(0.001)

        return qzhcsh


if __name__ == "__main__":
    ga = GxxGmGA()
    jqaj = ga.generate_jq_aj(100)
    # print (jqaj)

    fxch = ga.generate_dzjk(1)
    print (fxch)
