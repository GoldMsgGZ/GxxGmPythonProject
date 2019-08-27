#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 本例用于接收识别结果
# 本例使用了WebSocket客户端，需要执行以下命令：pip install websocket-client
import json

import websocket
from websocket import create_connection


websocket_server_address = "ws://192.168.2.100/sub"
ws = websocket.create_connection(websocket_server_address)

while True:
    result = ws.recv()
    result_json = json.loads(result)
    # 判断结果内是否含有机动车
    if len(result_json["detail"]["Vehicles"]) > 0:
        # 有机动车
        for vehicle_info in result_json["detail"]["Vehicles"]:
            print(u"车牌号码：" + vehicle_info["Recognize"]["Plate"]["Licence"])
            print(u"车牌颜色：" + vehicle_info["Recognize"]["Plate"]["Color"]["Name"])
            print("车牌所在帧时间：" + str(vehicle_info["Timestamp"]))
            print("====================================================")
    # print(result_json)
    else:
        print(result_json)

ws.close()
