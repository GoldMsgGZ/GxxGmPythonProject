#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 此模块用于分析数据包
import dpkt



def parse_ip_pkt(eth_pkt):
    # 解析IP包
    ip_pkt = eth_pkt.data

    # 判断载荷是哪一种
    payload_type = ip_pkt.p

    if payload_type == 0:
        # 单纯的IP包
        return 0
    elif payload_type == 1:
        # ICMP包
        return 0



def parse_ethernet_pkt(pkt_dat):
    # 解析以太包
    eth_pkt = dpkt.ethernet.Ethernet(pkt_dat)

    # 判断载荷是哪一种
    if eth_pkt.data.__class__.__name__ == "IP":
        # 载荷为IP包
        print ("载荷为IP包")

        # 调用IP包解析处理函数
        parse_ip_pkt(eth_pkt.data)
    elif eth_pkt.data.__class__.__name__ == "IPX":
        # 载荷为IPX包
        print ("载荷为IPX包")
    elif eth_pkt.data.__class__.__name__ == "IP6":
        # 载荷为IPv6包
        print ("载荷为IPv6包")
    elif eth_pkt.data.__class__.__name__ == "ARP":
        # 载荷为ARP包
        print ("载荷为ARP包")
    elif eth_pkt.data.__class__.__name__ == "PPP":
        # 载荷为PPP包
        print ("载荷为PPP包")