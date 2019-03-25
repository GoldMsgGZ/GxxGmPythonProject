#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 本例会读取CPU、内存利用率，需要安装psutil，安装命令为：pip install psutil
# 本例会发送HTTP请求，需要安装request，安装命令为：pip install requests

import psutil
import requests


###################################################################
# 这里是模拟器配置信息
INSTANCE_COUNT = 1

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

        self.gateway_ip = "127.0.0.1"
        self.getway_port = "6802"

    def startup(self, device_code, auth_key, domain, ip, version, gateway_ip, gateway_port):
        # 采集站开机
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

        heart_beat = {}
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

        response = requests.post(url=url, data=heart_beat)

        # {
        #     "code": 0,
        #     "message": "SUCCESS",
        #     "body": {
        #         "gzz_xh": "44010401901281918586",
        #         "name": "测试工作站001",
        #         "bmbh": "44010401",
        #         "bmmc": "一级部门",
        #         "admin": "",
        #         "phone": "",
        #         "address": "办公区",
        #         "wsconf": "{\"device_rule\":{\"bLUETOOTH\":\"0\",\"cDROM\":\"0\",\"mODEM\":\"0\",\"uDISK\":\"0\",\"uSB_KEYBOARD\":\"0\"},\"dsj_register_rule\":1,\"export_rule\":{\"export_to_common\":\"0\",\"export_to_ga\":\"0\"},\"net_rule\":{\"netsmon\":\"0\"},\"sys_rule\":{\"process\":[]}}",
        #         "regtime": "2019-02-28 18:22:18",
        #         "svrtime": "2019-03-02 19:03:19"
        #     }
        # }

        return 0

    def put_file_info(self):
        # 上报文件信息

        file_info = {}

        # 文件编号，遵循编号规则
        file_info["wjbh"]
        # 文件别名
        file_info["wjbm"]
        # 文件拍摄时间:YYYY-MM-DD hh:mm:ss
        file_info["pssj"]
        # 文件大小,单位字节
        file_info["wjdx"]
        # 文件类型:0视频、1音频、2图片、3文本、4其他、5-99预留
        file_info["wjlx"] = 0
        # 秒，非视频语音为0
        file_info["wjsc"] = 900
        # 文件备注：0普通文件，1执法仪重点标记文件
        file_info["bzlx"] = 0
        # 单位编号或部门编号
        file_info["jgdm"]
        # 单位名称或部门名称
        file_info["dwmc"]
        # 警员编号
        file_info["jybh"]
        # 警员姓名
        file_info["jy_xm"]
        # 执法仪产品型号，通用版需遵循编号规则
        file_info["cpxh"]
        # 采集站产品编码编号，遵循编号规则
        file_info["gzz_xh"] = self.device_code
        # 上传时间，格式为：yyyy-MM-dd HH:mm:ss
        file_info["scsj"]
        # 采集工作站上原文件相对路径
        file_info["ccwz"]
        # 采集工作站上原文件本机存储路径
        file_info["wlwz"]
        # HTTP访问路径
        file_info["bfwz"] = ""
        # 存储服务器
        file_info["ccfwq"] = ""
        # 采集工作站上缩略图存放的相对路径
        file_info["sltxdwz"] = ""

        file_infos = []
        file_infos.append(file_info)

        url_base = "http://" + self.gateway_ip + ":" + self.gateway_port + \
                   "/openapi/workstation/v3/wsinfo/heartbeat?gzz_xh=%s&authkey=%s&domain=%s"
        url = url_base % (self.device_code, self.auth_key, self.domain)

        response = requests.post(url=url, data=file_infos)

        return 0

    def get_suborgs(self):
        # 获取子部门列表

        return 0

    def get_users_in_org(self):
        # 获取指定部门下的直属用户列表

        return 0


if __name__ == "__main__":
    print "本地测试"

