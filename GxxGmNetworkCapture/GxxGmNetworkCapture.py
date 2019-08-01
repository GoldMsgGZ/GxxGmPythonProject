#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 此范例用于进行网络抓包
# 由于需要使用winpcapy，需要执行 pip install winpcapy
#
import datetime

from winpcapy import WinPcapDevices, WinPcapUtils


class GxxGmWinPcap:

    def __init__(self):
        self.version = "1.0"


    def enum_network_devices(self):
        # 枚举当前系统所有已安装的网卡实例
        return WinPcapDevices.list_devices()


    def capture_ny_device_name(self, device_name, packet_callback):
        # 开始抓取
        WinPcapUtils.capture_on_device_name(device_name, packet_callback)


def capture_callback(win_pcap, param, header, pkt_dat):
    # 抓包回调函数，其中pkt_dat是包数据
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    print ("[" + current_time_str + "]" + "收到数据，长度为：" + str(header.contents.len))

    # 前面框架已经搭好了。接下来可以开始分析数据包了


if __name__ == "__main__":
    # 首先遍历当前系统所有的网卡实例
    print (u"正在遍历当前系统存在的网卡实例...")
    winpcap = GxxGmWinPcap()
    network_device_list = winpcap.enum_network_devices().items()

    for device_info in network_device_list:
        print (u"网卡名称：" + device_info[1])
        print (u"网卡ID：" + device_info[0])
        print ("-------------------------------------")

    # 输入一个需要抓取的网卡ID
    print (u"请输入需要跟踪的目标网卡名称")
    target_device_id = ""
    target_device_name = raw_input("")
    for device_info in network_device_list:
        if target_device_name == device_info[1]:
            target_device_id = device_info[0]

    if target_device_id != "":
        winpcap.capture_ny_device_name(target_device_id, capture_callback)

        print (u"开始抓包，按Enter键退出...")
        input()
    else:
        print (u"不存在的网卡，退出...")



