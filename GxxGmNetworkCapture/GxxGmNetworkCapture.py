#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 此范例用于进行网络抓包
# 由于需要使用winpcapy，需要执行 pip install winpcapy
# 由于需要使用pcap，需要执行 pip install pypcap
#

from __future__ import print_function
import traceback
import dpkt
from winpcapy import WinPcapDevices, WinPcapUtils


def capture_callback(win_pcap, param, header, pkt_dat):
    # 抓包回调函数，其中pkt_dat是包数据
    # 前面框架已经搭好了。接下来可以开始分析数据包了

    # 首先拆以太包
    eth_pkt = dpkt.ethernet.Ethernet(pkt_dat)
    if eth_pkt.data.__class__.__name__ == "IP":
        # 载荷是IP包
        ip_pkt = eth_pkt.data
        print ("IP包载荷类型:%d" % ip_pkt.p)

        # 这里可以取出源IP和目标IP
        src_ip = '%d.%d.%d.%d' % tuple(map(ord, list(ip_pkt.src)))
        dst_ip = '%d.%d.%d.%d' % tuple(map(ord, list(ip_pkt.dst)))

        # 拆IP包
        if ip_pkt.data.__class__.__name__ == "TCP":
            # 载荷是TCP包
            tcp_pkt = ip_pkt.data

            # 这里可以拿到源端口和目标端口
            src_port = tcp_pkt.sport
            dst_port = tcp_pkt.dport

            print ("抓到TCP包 || 源 >>> %s:%d || 目标 >>> %s:%d" % (src_ip, src_port, dst_ip, dst_port))

            if dst_port == 80:
                # 载荷是HTTP包
                http_pkt = tcp_pkt.data

                if http_pkt:
                    # 解码HTTP包
                    try:
                        http_data = dpkt.http.Request(http_pkt)
                        print (http_data)
                    except Exception:
                        print(traceback.print_exc())


if __name__ == "__main__":
    # 首先遍历当前系统所有的网卡实例
    print (u"正在遍历当前系统存在的网卡实例...")
    network_device_list = WinPcapDevices.list_devices().items()

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
        WinPcapUtils.capture_on_device_name(target_device_id, capture_callback)

        print (u"开始抓包，按Enter键退出...")
        input()
    else:
        print (u"不存在的网卡，退出...")



