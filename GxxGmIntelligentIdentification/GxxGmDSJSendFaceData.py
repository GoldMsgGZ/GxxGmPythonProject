#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 本例将一张人脸图片Base64后发送给识别后台
# 本例会使用 requests 组件，如未安装，需要执行 pip install requests

import base64
import json
import requests
import threadpool

THREAD_COUNT = 60
LOOP_COUNT = 200

FACE_IMAGE = "E:\\xampp\\htdocs\\image\\demo.jpg"
SERVER_IP = "127.0.0.1"
SERVER_PORT = "6008"
HTTP_URI = "/gmvcs/instruct/recognition/face/getResult"


def thread_func(param):
    # 打开文件
    face_image_fileobj = open(FACE_IMAGE, "rb")
    face_image_data = face_image_fileobj.read()
    face_image_base64 = base64.b64encode(face_image_data)
    face_image_fileobj.close()

    #print (face_image_base64)

    # 构建JSON，然后HTTP发送POST请求
    post_body = dict()
    post_body["deviceId"] = "44010401901511243840"
    post_body["base64Picture"] = face_image_base64

    url = "http://" + SERVER_IP + ":" + SERVER_PORT + HTTP_URI

    post_header = dict()
    post_header["Content-Type"] = "application/json"
    post_header["Accept"] = "application/json"

    # 这里目前会返回500
    #print json.dumps(post_body)
    for count in range(LOOP_COUNT):
        response = requests.post(url=url, data=json.dumps(post_body), headers=post_header)
        #response.close()



name_list = list()
for index in range(THREAD_COUNT):
    name_list.append("param")

pool = threadpool.ThreadPool(THREAD_COUNT)
reqs = threadpool.makeRequests(thread_func, name_list)
[pool.putRequest(req) for req in reqs]
pool.wait()