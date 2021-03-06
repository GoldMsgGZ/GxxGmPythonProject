#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 本例会读取CPU、内存利用率，需要安装psutil，安装命令为：pip install psutil
# 本例会发送HTTP请求，需要安装request，安装命令为：pip install requests


from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
import psutil
import requests
import time
import json
import datetime
from threadpool import ThreadPool, makeRequests


###################################################################
# 这里是模拟器配置信息

INSTANCE_COUNT = 500

# 工作站信息
WORKSTATION_GBCODE_PRE = "4401040190128"
WORKSTATION_GBCODE_START = 1600500
WORKSTATION_IP = "10.10.16.59"
WORKSTATION_VERSION = "3.4.5"
WORKSTATION_AUTHKEY = "GM3019013044030358901281317526"
WORKSTATION_DOMAIN = "44030300"

# 网关信息
GATEWAY_IP = "192.168.55.10"
GATEWAY_PORT = "6801"

# 接入的执法仪信息
DSJ_GBCODE = "44030358901511317526"

# 工作频率，单位：秒
# 心跳频率
HEARTBEAT_RATE = 1
# 子部门查询频率
QUERY_SUBORG_RATE = 1
# 用户信息查询频率
QUERY_USER_RATE = 1
# 文件信息上报频率
PUT_FILES_RATE = 10


class GxxGmWSSimulator:
    # 本类型定义了高新兴国迈采集工作站模拟器
    # 模拟器应该实现以下功能：
    # 1.发送心跳
    # 2.查询组织架构与用户信息
    # 3.上报文件信息


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
        self.dsj_code = ""
        self.workstation_org_domain = ""

        self.gateway_ip = "127.0.0.1"
        self.gateway_port = "6802"


    def startup(self, device_code, auth_key, domain, ip, version, dsj_code, gateway_ip, gateway_port):
        # 采集站开机
        # auth_key一般为机器码
        # domain一般为系统ID
        self.device_code = device_code
        self.auth_key = auth_key
        self.domain = domain
        self.ip = ip
        self.version = version
        self.dsj_code = dsj_code

        self.gateway_ip = gateway_ip
        self.gateway_port = gateway_port

        # 首先发送一波请求，验证连通性
        url = "https://" + self.gateway_ip + ":" + self.gateway_port + "/openapi/workstation/v3/ping"
        response = requests.get(url, verify=False)

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
        heart_beat["cp"] = int(cpu)
        heart_beat["ram"] = int(ram)
        heart_beat["raid_zt"] = 101
        heart_beat["bjlx"] = 0
        heart_beat["version"] = self.version

        # 发送心跳，这里会获得当前执法仪所属部门
        url_base = "https://" + self.gateway_ip + ":" + self.gateway_port + \
                 "/openapi/workstation/v3/wsinfo/heartbeat?gzz_xh=%s&authkey=%s&domain=%s"
        url = url_base % (self.device_code, self.auth_key, self.domain)

        post_header = dict()
        post_header["Content-Type"] = "application/json"
        post_header["Accept"] = "application/json"

        response = requests.post(url=url, data=json.dumps(heart_beat), headers=post_header, verify=False, timeout=0.01)

        print(response.content)

        err_code = 0
        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
                return err_code
        except ValueError:
            print("Get heartbeat info failed！")
            return -1

        # 解析数据
        self.workstation_org_id = content_json["body"]["bmbh"]
        self.workstation_org_domain = content_json["body"]["bmbh"][0:8]

        return err_code


    def get_suborgs(self):
        # 获取子部门列表

        url_base = "https://" + self.gateway_ip + ":" + self.gateway_port +\
                   "/openapi/workstation/v3/suborg?gzz_xh=%s&authkey=%s&domain=%s&sjbmbh=%s"
        url = url_base % (self.device_code, self.auth_key, self.domain, self.workstation_org_id)
        response = requests.get(url, verify=False)

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
                return err_code
        except ValueError:
            print("Get sub orgs info failed！")
            return -1

            # 解析数据
        self.suborgs_list = content_json["body"]

        return err_code


    def get_users_info_org(self):
        # 获取指定部门下的直属用户列表

        url_base = "https://" + self.gateway_ip + ":" + self.gateway_port + \
                   "/openapi/workstation/v3/userinfo?gzz_xh=%s&authkey=%s&domain=%s&bmbh=%s"
        url = url_base % (self.device_code, self.auth_key, self.domain, self.workstation_org_id)
        response = requests.get(url, verify=False)

        err_code = 0
        if response.status_code != 200:
            err_code = response.status_code
            return err_code
        else:
            err_code = 0

        print(response.content)

        # 保存当前采集站所在部门所有民警列表
        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
                return err_code
        except ValueError:
            print("Get user info failed！")
            return -1

        # 解析数据
        self.police_list = content_json["body"]

        return err_code


    def put_file_info(self):
        # 上报文件信息

        # 根据当前派出所民警情况，上报文件信息，每人每次至少上报10条
        file_infos = list()
        file_index = 0
        for police_info in self.police_list:
            for index in range(10):
                file_index += 1
                # 这里要构建几个内容：
                # 获得当前时间
                take_time = datetime.datetime.now()
                take_time_str = take_time.strftime('%Y%m%d%H%M%S')
                take_time_str2 = take_time.strftime('%Y-%m-%d %H:%M:%S')

                import_time = datetime.datetime.now()
                import_time_str = import_time.strftime('%Y%m%d%H%M%S')
                import_time_str2 = import_time.strftime('%Y-%m-%d %H:%M:%S')

                # 文件编号
                wjbh = "%s_%s%s0000%s%04d" % (self.workstation_org_domain, self.dsj_code, take_time_str, import_time_str, file_index)

                # 文件别名
                wjbm = "%s%s%04d.mp4" % (self.dsj_code, take_time, index)

                # 开始组装文件信息
                file_info = dict()
                # 1.文件编号，遵循编号规则
                file_info["wjbh"] = wjbh
                # 2.文件别名
                file_info["wjbm"] = wjbm
                # 3.文件拍摄时间:YYYY-MM-DD hh:mm:ss
                file_info["pssj"] = take_time_str2
                # 4.文件大小,单位字节
                file_info["wjdx"] = 1.5 * 1024 * 1024 * 1024
                # 5.文件类型:0视频、1音频、2图片、3文本、4其他、5-99预留
                file_info["wjlx"] = "0"
                # 6.秒，非视频语音为0
                file_info["wjsc"] = 900
                # 7.文件备注：0普通文件，1执法仪重点标记文件
                file_info["bzlx"] = "0"
                # 8.单位编号或部门编号，使用民警部门编号的话，有可能是12位的
                file_info["jgdm"] = police_info["bmbh"]
                # 9.警员单位名称或部门名称
                file_info["dwmc"] = police_info["bmmc"]
                # 10.警员编号
                file_info["jybh"] = police_info["jybh"]
                # 11.警员姓名
                file_info["jy_xm"] = police_info["jyxm"]
                # 12.执法仪产品型号，通用版需遵循编号规则
                file_info["cpxh"] = self.dsj_code
                # 13.采集站产品编码编号，遵循编号规则
                file_info["gzz_xh"] = self.device_code
                # 14.上传时间，格式为：yyyy-MM-dd HH:mm:ss
                file_info["scsj"] = import_time_str2
                # 15.采集工作站上原文件相对路径
                file_info["ccwz"] = "\\Workstation\\1.mp4"
                # 16.采集工作站上原文件本机存储路径
                file_info["wlwz"] = "D:\\Workstation\\1.mp4"
                # 17.HTTP访问路径
                file_info["bfwz"] = ""
                # 18.存储服务器
                file_info["ccfwq"] = ""
                # 19.采集工作站上缩略图存放的相对路径
                file_info["sltxdwz"] = ""

                print(json.dumps(file_info))
                file_infos.append(file_info)
                #time.sleep(1)

        # 发送请求信息
        url_base = "https://" + self.gateway_ip + ":" + self.gateway_port + \
                   "/openapi/workstation/v3/wsinfo/heartbeat?gzz_xh=%s&authkey=%s&domain=%s"
        url = url_base % (self.device_code, self.auth_key, self.domain)

        post_header = dict()
        post_header["Content-Type"] = "application/json"
        post_header["Accept"] = "application/json"

        # 这里目前会返回500
        print(json.dumps(file_infos))
        response = requests.post(url=url, data=json.dumps(file_infos), headers=post_header, verify=False)

        return 0


    def run(self):
        # 采集站开始运行
        heartbeat_count = HEARTBEAT_RATE
        query_suborg_count = QUERY_SUBORG_RATE
        query_user_count = QUERY_USER_RATE
        put_files_count = PUT_FILES_RATE

        while True:

            # 发送心跳
            if heartbeat_count == HEARTBEAT_RATE:
                self.send_heartbeat()
                heartbeat_count = 0

            # 查询子部门
            if query_suborg_count == QUERY_SUBORG_RATE:
                self.get_suborgs()
                query_suborg_count = 0

            # 查询子部门用户
            if query_user_count == QUERY_USER_RATE:
                self.get_users_info_org()
                query_user_count = 0

            # # 创建一个线程，等待上传重要文件
            # # 上传文件信息
            # if put_files_count == PUT_FILES_RATE:
            #     self.workstation.put_file_info()
            #     put_files_count = 0

            # 睡眠1毫秒
            time.sleep(0.001)

            heartbeat_count += 1
            query_suborg_count += 1
            query_user_count += 1
            put_files_count += 1


def workstation_func(gbcode):
    workstation = GxxGmWSSimulator()
    err_code = workstation.startup(device_code=gbcode, auth_key=WORKSTATION_AUTHKEY,
                                   domain=WORKSTATION_DOMAIN, ip=WORKSTATION_IP, version=WORKSTATION_VERSION,
                                   dsj_code=DSJ_GBCODE, gateway_ip=GATEWAY_IP, gateway_port=GATEWAY_PORT)

    if err_code != 0:
        print("未连通采集站接入网关...")
        exit()

    workstation.run()


if __name__ == "__main__":
    print("本地测试采集工作站")

    # 创建线程池
    device_list = list()
    for index in range(INSTANCE_COUNT):
        # 根据模拟器实例个数进来生成对应的采集站国标编码
        gbcode_id_number = "%07d" % (WORKSTATION_GBCODE_START + index)
        gbcode = WORKSTATION_GBCODE_PRE + gbcode_id_number
        device_list.append(gbcode)
        print ("生成设备编码：" + gbcode)

    pool = ThreadPool(INSTANCE_COUNT)
    threadpool_requests = makeRequests(workstation_func, device_list)
    [pool.putRequest(req) for req in threadpool_requests]
    pool.wait()





