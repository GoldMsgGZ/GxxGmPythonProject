#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 作者：wangy
# 功能：此范例是模拟下级平台向目标上级推送业务级联信息

import json
import time
import requests

import GxxGmGA

###########################################################################
# 首先是配置信息

# DOMAIN 和 AUTHKEY 需要在平台级联功能处增加级联平台
DOMAIN = "53000000"
AUTHKEY = "00000000902001100763"

ITEM_COUNT = 100

class GxxGmPlatform:


    def __init__(self):
        self.platform_id="0001" # 平台ID
        self.ga = GxxGmGA.GxxGmGA()


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
        OPENAPI_RECEIVEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/ps/basic/" \
                                            "info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
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
        OPENAPI_HANDLEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/hs/basic/" \
                                           "info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
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

        OPENAPI_HANDLEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/cm/basic/" \
                                           "info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
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

        OPENAPI_HANDLEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/cm/basic/" \
                                           "info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
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