#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
import json

import requests

THREAD_COUNT = 1

SERVER_IP = "192.168.56.98"
SERVER_PORT = "99"


class GVObject:

    def __init__(self):
        self.token = ""
        self.ip = "127.0.0.1"
        self.port = "123"


    def login(self, ip, port):
        # 登录
        url_format = "http://%s:%s/GoVideo/Server/LoginRequest?SequenceID=%s&LoginID=%s&LoginType=107&UserName=%s&Password=%s&LoginIP=%s"
        url = url_format % (ip, port, "107", "107", "107", "admin", "admin", "192.168.56.99")

        response = requests.get(url)

        try:
            content_json = json.loads(response.content)
            errcode = content_json['Message']['OperResult']

            if errcode != 0:
                print ("Login to GV failed... errcode : %d" % (content_json['Message']['OperResult']))
                return errcode
            else:
                # 保存Token
                self.token = content_json['Message']['OperResult']
                self.ip = ip
                self.port = port

        except ValueError:
            print ("Parse response failed...")
            return -1

        return 0


    def add_devices(self, device_list):
        # 添加设备
        url_format = "http://%s:%s/GoVideo/Serviceconfig/SetDeviceRequest"
        url = url_format % (self.ip, self.port)

        post_header = dict()
        post_header["Content-Type"] = "application/json;charset=gb2312"
        post_header["Accept"] = "application/json"
        post_header["SequenceID"] = "5"
        post_header["Token"] = self.token

        # 组装业务数据
        message = dict()
        message["DeviceCount"] = len(device_list)
        message["DeviceInfoList"] = device_list

        business_data = dict()
        business_data["Massage"] = message
        business_data_json = json.dumps(business_data)

        response = requests.post(url=url, data=business_data_json, headers=post_header)

        try:
            content_json = json.loads(response.content)
            errcode = content_json['Message']['OperResult']

            if errcode != 0:
                print ("Register devices to GV failed... errcode : %d" % (content_json['Message']['OperResult']))
                return errcode

        except ValueError:
            print ("Parse response failed...")
            return -1

        return 0
