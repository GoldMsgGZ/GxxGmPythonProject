#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 此范例为视频分析盒子通道状态监控以及任务添加管理模块
# 此模块本质就是模仿前端用户登录到系统内
# 不停的获取通道状态来判断通道分析是否结束
# 一旦通道分析结束，则立即添加下一个文件进入通道
#
# 经过测试验证，可以直接推送HTTP地址

# 获取四个通道的状态：
# GET /app/aiboxManagerAPI/config_handler/get_channelparam
# 返回的json数据中，通道数据包含detail的时候表示正在执行分析，没有则表示分析结束
#
# 为某通道设置分析任务
# POST /app/aiboxManagerAPI/config_handler/set_channelparam
# POST参数：{"SrcType":4,"ChannelId":4,"ChannelName":"4","PlaySpeed":16,"FilePath":"http://192.168.2.1/live/20190805165706409.mp4","GBDeviceId":"","StartTime":1566885138000,"EndTime":1567180800000}
#

import hashlib
import json
import thread
import time

import requests
import websocket

ShenJingServerIp = "192.168.2.100"


class GxxGmShenJingClient:

    def __init__(self):
        self.url = ""
        self.cookies = ""

    def login(self, username, password):
        # 登录URL
        object_url_format = "http://%s/app/aiboxManagerAPI/login_handler/login?username=%s&pwd=%s"

        # 计算MD5后的
        m = hashlib.md5()
        m.update(password)
        hashed_password = m.hexdigest()

        # 真实的登录URL
        real_http = object_url_format % (ShenJingServerIp, username, hashed_password)

        # requests发送POST请求
        response = requests.get(real_http)

        if response.status_code != 200:
            # 登录出错了
            return response.status_code
        else:
            # 保存Cookie
            self.cookies = response.headers._store["set-cookie"][1]
            return response.status_code


    def get_channel_state(self):
        # 获取通道状态
        object_url_format = "http://%s/app/aiboxManagerAPI/config_handler/get_channelparam"

        real_http = object_url_format % ShenJingServerIp

        header = dict()
        header["Cookie"] = self.cookies

        # request发送GET请求
        response = requests.get(url=real_http, headers=header)

        if response.status_code != 200:
            # 获取通道信息失败
            return response.status_code, list()
        else:
            content_data = response.content
            content_data_json = json.loads(content_data)

            channel_states = list()
            channel_list = content_data_json["data"]["channelinfolist"]
            for channel_info in channel_list:
                # 检查
                channel_state = dict()
                channel_state["ChannelId"] = channel_info["ChannelId"]
                channel_state["ChannelName"] = channel_info["ChannelName"]

                if channel_info.has_key("detail"):
                    channel_state["IsFree"] = False
                else:
                    channel_state["IsFree"] = True

                channel_states.append(channel_state)

        return response.status_code, channel_states


    def set_channel_task(self, channel_id, file_http_path, play_speed):
        # 设置通道任务
        object_url_format = "http://%s/app/aiboxManagerAPI/config_handler/set_channelparam"

        real_http = object_url_format % ShenJingServerIp

        # 获取当前时间戳毫秒数
        t = time.time()
        now_time = int(round(t * 1000))

        post_data = dict()
        post_data["ChannelId"] = channel_id
        post_data["ChannelName"] = str(channel_id)
        post_data["FilePath"] = file_http_path
        post_data["GBDeviceId"] = ""
        post_data["PlaySpeed"] = play_speed
        post_data["SrcType"] = 4
        post_data["StartTime"] = now_time
        post_data["EndTime"] = now_time + 3600000

        # requests发送POST请求
        header = dict()
        header["Cookie"] = self.cookies
        header["Content-Type"] = "application/json"
        header["Accept"] = "application/json"

        response = requests.post(url=real_http, data=json.dumps(post_data), headers=header)

        if response.status_code != 200:
            # 获取通道信息失败
            return response.status_code
        else:
            return response.status_code


def recv_thread(thread_name, delay):
    # 这里定义线程函数，创建一个WebSocket客户端，接收盒子返回的结果
    # 这里没有处理WebSocket客户端等待超时后的异常处理情况

    websocket_server_address = "ws://%s/sub" % ShenJingServerIp
    ws = websocket.create_connection(websocket_server_address)

    while True:
        result = ws.recv()
        result_json = json.loads(result)
        # 判断结果内是否含有机动车
        if len(result_json["detail"]["Vehicles"]) > 0:
            # 有机动车
            for vehicle_info in result_json["detail"]["Vehicles"]:
                if vehicle_info["Recognize"].has_key("Plate"):
                    # 实际上在这里就可以处理相关请求，例如发送给省厅平台，或者缓存到列表中，启动一个线程池进行推送
                    print(u"车牌号码：" + vehicle_info["Recognize"]["Plate"]["Licence"])
                    print(u"车牌颜色：" + vehicle_info["Recognize"]["Plate"]["Color"]["Name"])
                    print("车牌所在帧时间：" + str(vehicle_info["Timestamp"]))
                    print("====================================================")


if __name__ == "__main__":
    # 首先构建一个视频列表，实际应用中是从我们的数据库文件表中拿视频文件下载地址
    video_list = list()
    video_list.append("http://192.168.2.1/live/1.mp4")
    video_list.append("http://192.168.2.1/live/2.mp4")
    video_list.append("http://192.168.2.1/live/3.mp4")
    video_list.append("http://192.168.2.1/live/4.mp4")
    video_list.append("http://192.168.2.1/live/5.mp4")
    video_list.append("http://192.168.2.1/live/6.mp4")

    # 创建一个线程，连接目标WebSocket
    thread.start_new_thread(recv_thread, ("Thread-1", 2,))

    # 创建一个实例对象，登录到盒子
    client = GxxGmShenJingClient()
    client.login("admin", "123456")

    # 主线程逻辑业务
    # 每个5秒钟检查一次各通道的运行状态，如果为空闲状态，则向其添加分析任务，否则等待下一次检查
    while True:
        # 获取通道状态
        errcode, channel_states = client.get_channel_state()

        for channel_state in channel_states:
            if channel_state["IsFree"] == True:
                # 有空闲的通道，从列表中取出一个文件，加入通道中进行分析
                print(u"通道" + channel_state["ChannelName"] + u"空闲，准备加入任务")

                # 文件列表为空了，可以跳出循环结束任务了
                if len(video_list) == 0:
                    break

                # 取出最近一条文件记录，添加到对应通道中
                http_url = video_list.pop()
                client.set_channel_task(channel_id=channel_state["ChannelId"], file_http_path=http_url, play_speed=1)

        # 等待5秒
        time.sleep(5)
