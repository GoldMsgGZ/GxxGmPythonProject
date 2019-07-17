#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 作者：wangy
# 功能：此范例是模拟下级平台向目标上级推送业务级联信息


###########################################################################
# 首先是配置信息
import traceback

import MySQLdb
import json
import random
import time
import requests
import GxxGmBaseData



# DOMAIN 和 AUTHKEY 需要在平台级联功能处增加级联平台
import GxxGmGA

DOMAIN = "53000000"
AUTHKEY = "00000000902001100763"

ITEM_COUNT = 100

# 报警类型
alarm_type = ["110电话报警", "派出所报警", "社会面报警"]


def get_alarm_type():
    # 获取报警类型
    # 获取一个随机数
    return random.choice(alarm_type)

#
alarm_content = [
    {"id": "0001", "type": "抢劫"},
    {"id": "0002", "type": "盗窃"},
    {"id": "0003", "type": "吸毒"},
    {"id": "0004", "type": "打架"},
    {"id": "0005", "type": "赌博"},
    {"id": "0006", "type": "卖淫"},
    {"id": "0007", "type": "嫖娼"},
    {"id": "0008", "type": "诈骗"},
    {"id": "0009", "type": "杀人"},
    {"id": "0010", "type": "拐卖妇女儿童"},
    {"id": "0011", "type": "猥亵"}
]


def get_alarm_situation_type():
    real_alarm_content = random.choice(alarm_content)
    alarm_situation_id = real_alarm_content["id"]
    alarm_situation_type = real_alarm_content["type"]
    return alarm_situation_id, alarm_situation_type





def get_org_and_police(org_infos):
    # 随机获取接处警部门以及民警
    while True:
        org_info = random.choice(org_infos)
        if len(org_info["users"]) == 0:
            continue

        user_info = random.choice(org_info["users"])
        break

    return org_info["org_code"].encode("utf8"), org_info["org_name"].encode("utf8"),\
           user_info["user_code"].encode("utf8"), user_info["user_name"].encode("utf8")


class GxxGmPlatform:

    def __init__(self):
        self.platform_id="0001" # 平台ID
        self.ga = GxxGmGA()

    def send_alarm_situations(self):
        # 发送警情信息
        # 首先生成接警信息
        receive_alarm_json, handle_alarm_situation_json, case_info_json = self.ga.generate_jq_aj(ITEM_COUNT)

        # 发送接警信息
        post_header = dict()
        post_header["Content-Type"] = "application/json"
        post_header["Accept"] = "application/json"

        # 这里目前会返回500
        # print (json.dumps(receive_alarm_json))
        OPENAPI_RECEIVEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/ps/basic/info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
        response = requests.post(url=OPENAPI_RECEIVEALARMSITUATION_URL, data=json.dumps(receive_alarm_json),
                                 headers=post_header)
        err_code = 0
        if response.status_code != 200:
            err_code = response.status_code
            return err_code
        else:
            err_code = 0

        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
                print(u"发送接警信息失败！" + str(err_code))
                return err_code
        except ValueError:
            print(u"发送接警信息失败！")
            return -1

        # 等待1秒，确保接警信息已经在数据库存在
        time.sleep(1)

        # print (json.dumps(handle_alarm_situation_json))
        OPENAPI_HANDLEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/hs/basic/info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
        response = requests.post(url=OPENAPI_HANDLEALARMSITUATION_URL, data=json.dumps(handle_alarm_situation_json),
                                 headers=post_header)
        err_code = 0
        if response.status_code != 200:
            err_code = response.status_code
            return err_code
        else:
            err_code = 0

        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
                print(u"发送处警信息失败！")
                return err_code
        except ValueError:
            print(u"发送处警信息失败！")
            return -1

        # 等待1秒，确保接警信息已经在数据库存在
        time.sleep(1)

        OPENAPI_HANDLEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/cm/basic/info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
        response = requests.post(url=OPENAPI_HANDLEALARMSITUATION_URL, data=json.dumps(case_info_json),
                                 headers=post_header)
        err_code = 0
        if response.status_code != 200:
            err_code = response.status_code
            return err_code
        else:
            err_code = 0

        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
                print(u"发送案件信息失败！")
                return err_code
        except ValueError:
            print(u"发送案件信息失败！")
            return -1

        return err_code


    def send_case(self):
        # 发送案件信息
        case_info_json = self.ga.generate_jq_aj(ITEM_COUNT)

        post_header = dict()
        post_header["Content-Type"] = "application/json"
        post_header["Accept"] = "application/json"

        OPENAPI_HANDLEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/cm/basic/info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
        response = requests.post(url=OPENAPI_HANDLEALARMSITUATION_URL, data=json.dumps(case_info_json),
                                 headers=post_header)
        err_code = 0
        if response.status_code != 200:
            err_code = response.status_code
            return err_code
        else:
            err_code = 0

        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
                print(u"发送案件信息失败！")
                return err_code
        except ValueError:
            print(u"发送案件信息失败！")
            return -1

        return 0


if __name__ == "__main__":
    platform = GxxGmPlatform()

    while True:
        # 生成警情、发送警情信息
        platform.send_alarm_situations()

        # 生成并发送案件信息，这里上报的是未关联警情的
        # platform.send_case()