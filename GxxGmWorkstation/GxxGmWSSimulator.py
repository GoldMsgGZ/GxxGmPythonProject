#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 本例会读取CPU、内存利用率，需要安装psutil，安装命令为：pip install psutil
# 本例会发送HTTP请求，需要安装request，安装命令为：pip install requests

import psutil
import requests
import time
import json


###################################################################
# 这里是模拟器配置信息
INSTANCE_COUNT = 1

HEARTBEAT_RATE = 5
QUERY_SUBORG_RATE = 5
QUERY_USER_RATE = 5

# 测试当前计算机的CPU占用率和内存占用率
#ram = psutil.virtual_memory().percent
#cpu = psutil.cpu_percent(None)
#print ram
#print cpu

# 测试格式化字符串
# print "%07d" % 1
#
# url_base = "http://" + "127.0.0.1" + ":" + "6802" + \
#                  "/openapi/workstation/v3/wsinfo/heartbeat?gzz_xh=%s&authkey=%s&domain=%s"
# url = url_base % ("111222333", "auth_key", "domain")
# print url



class GxxGmWSSimulator:
    # 本类型定义了高新兴国迈采集工作站模拟器
    # 模拟器应该实现以下功能：
    # 1.发送心跳
    # 2.查询组织架构与用户信息
    # 3.

    def __init__(self):
        # 初始化几个成员变量
        self.device_code = ""
        self.auth_key = "GxxGm"
        self.domain = "GxxGm"
        self.ip = "127.0.0.1"
        self.version = "3.4.5"
        self.workstation_org_id = ""
        self.police_list = list()
        self.suborgs_list = list()

        self.gateway_ip = "127.0.0.1"
        self.gateway_port = "6802"

    def startup(self, device_code, auth_key, domain, ip, version, gateway_ip, gateway_port):
        # 采集站开机
        # auth_key一般为机器码
        # domain一般为系统ID
        self.device_code = device_code
        self.auth_key = auth_key
        self.domain = domain
        self.ip = ip
        self.version = version

        self.gateway_ip = gateway_ip
        self.gateway_port = gateway_port

        # 首先发送一波请求，验证连通性
        url = "http://" + self.gateway_ip + ":" + self.gateway_port + "/openapi/workstation/v3/ping"
        response = requests.get(url)

        if response.status_code != 200:
            err_code = response.status_code
        else:
            err_code = 0

        return err_code

    def send_heartbeat(self):
        # 构建当前心跳信息

        # 获取当前CPU、内存使用率
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(None)

        heart_beat = dict()
        heart_beat["gzz_xh"] = self.device_code
        heart_beat["gzz_ipdz"] = self.ip
        heart_beat["zxzt"] = "1"
        heart_beat["qizt"] = "1"
        heart_beat["cczrl"] = 4 * 1024 * 1024
        heart_beat["syzrl"] = 500 * 1024
        heart_beat["cpu"] = int(cpu)
        heart_beat["ram"] = int(ram)
        heart_beat["raid_zt"] = 101
        heart_beat["bjlx"] = 0
        heart_beat["version"] = self.version

        # 发送心跳，这里会获得当前执法仪所属部门
        url_base = "http://" + self.gateway_ip + ":" + self.gateway_port + \
                 "/openapi/workstation/v3/wsinfo/heartbeat?gzz_xh=%s&authkey=%s&domain=%s"
        url = url_base % (self.device_code, self.auth_key, self.domain)

        post_header = dict()
        post_header["Content-Type"] = "application/json"
        post_header["Accept"] = "application/json"

        response = requests.post(url=url, data=json.dumps(heart_beat), headers=post_header)

        print response.content

        err_code = 0
        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
        except ValueError:
            print "Get heartbeat info failed！"
            return -1

        # 解析数据
        self.workstation_org_id = content_json["body"]["bmbh"]

        return err_code

    def put_file_info(self):
        # 上报文件信息

        # 根据当前派出所民警情况，上报文件信息，每人每次至少上报10条
        file_infos = list()
        for police_info in self.police_list:
            for index in range(10):

                # 这里要构建几个内容：
                # 获得当前时间
                # 文件编号
                wjbh = "%s_%s%s0000%s%04d" % (self.domain, )

        file_info = dict()

        # 文件编号，遵循编号规则
        file_info["wjbh"] = ""
        # 文件别名
        file_info["wjbm"] = ""
        # 文件拍摄时间:YYYY-MM-DD hh:mm:ss
        file_info["pssj"] = ""
        # 文件大小,单位字节
        file_info["wjdx"] = ""
        # 文件类型:0视频、1音频、2图片、3文本、4其他、5-99预留
        file_info["wjlx"] = 0
        # 秒，非视频语音为0
        file_info["wjsc"] = 900
        # 文件备注：0普通文件，1执法仪重点标记文件
        file_info["bzlx"] = 0
        # 单位编号或部门编号
        file_info["jgdm"] = ""
        # 警员单位名称或部门名称
        file_info["dwmc"] = ""
        # 警员编号
        file_info["jybh"] = ""
        # 警员姓名
        file_info["jy_xm"] = ""
        # 执法仪产品型号，通用版需遵循编号规则
        file_info["cpxh"] = ""
        # 采集站产品编码编号，遵循编号规则
        file_info["gzz_xh"] = self.device_code
        # 上传时间，格式为：yyyy-MM-dd HH:mm:ss
        file_info["scsj"] = ""
        # 采集工作站上原文件相对路径
        file_info["ccwz"] = ""
        # 采集工作站上原文件本机存储路径
        file_info["wlwz"] = ""
        # HTTP访问路径
        file_info["bfwz"] = ""
        # 存储服务器
        file_info["ccfwq"] = ""
        # 采集工作站上缩略图存放的相对路径
        file_info["sltxdwz"] = ""


        file_infos.append(file_info)

        url_base = "http://" + self.gateway_ip + ":" + self.gateway_port + \
                   "/openapi/workstation/v3/wsinfo/heartbeat?gzz_xh=%s&authkey=%s&domain=%s"
        url = url_base % (self.device_code, self.auth_key, self.domain)

        response = requests.post(url=url, data=file_infos)

        return 0

    def get_suborgs(self):
        # 获取子部门列表

        url_base = "http://" + self.gateway_ip + ":" + self.gateway_port +\
                   "/openapi/workstation/v3/suborg?gzz_xh=%s&authkey=%s&domain=%s&sjbmbh=%s"
        url = url_base % (self.device_code, self.auth_key, self.domain, self.workstation_org_id)
        response = requests.get(url)

        err_code = 0
        if response.status_code != 200:
            return response.status_code
        else:
            err_code = 0

        # 这里可以列出子部门列表
        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
        except ValueError:
            print "Get sub orgs info failed！"
            return -1

            # 解析数据
        self.suborgs_list = content_json["body"]

        return err_code

    def get_users_info_org(self):
        # 获取指定部门下的直属用户列表

        url_base = "http://" + self.gateway_ip + ":" + self.gateway_port + \
                   "/openapi/workstation/v3/userinfo?gzz_xh=%s&authkey=%s&domain=%s&bmbh=%s"
        url = url_base % (self.device_code, self.auth_key, self.domain, self.workstation_org_id)
        response = requests.get(url)

        err_code = 0
        if response.status_code != 200:
            err_code = response.status_code
            return err_code
        else:
            err_code = 0

        print response.content

        # 保存当前采集站所在部门所有民警列表
        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
        except ValueError:
            print "Get user info failed！"
            return -1

        # 解析数据
        self.police_list = content_json["body"]

        return err_code


if __name__ == "__main__":
    print "本地测试采集工作站"

    workstation = GxxGmWSSimulator()
    err_code = workstation.startup(device_code="44030358901281317526", auth_key="GM3019013044030358901281317526",
                                   domain="44030300", ip="10.10.16.59", version="3.5.4", gateway_ip="192.168.56.97",
                                   gateway_port="6801")

    if err_code != 0:
        print "未连通采集站接入网关..."
        exit()

    heartbeat_count = HEARTBEAT_RATE
    query_suborg_count = QUERY_SUBORG_RATE
    query_user_count = QUERY_USER_RATE

    while True:

        # 发送心跳
        if heartbeat_count == HEARTBEAT_RATE:
            workstation.send_heartbeat()
            heartbeat_count = 0

        # 查询子部门
        if query_suborg_count == QUERY_SUBORG_RATE:
            workstation.get_suborgs()
            query_suborg_count = 0

        # # 查询子部门用户
        if query_user_count == QUERY_USER_RATE:
            workstation.get_users_info_org()
            query_user_count = 0

        # 创建一个线程，等待上传重要文件
        # 上传文件信息

        time.sleep(1)

        heartbeat_count += 1
        query_suborg_count += 1
        query_user_count += 1

