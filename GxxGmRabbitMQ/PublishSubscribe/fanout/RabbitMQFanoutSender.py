#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import pika
import time
import sys


# 生成凭证，创建连接
credentials = pika.PlainCredentials('login', 'login')
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials))

# 创建通道
channel = connection.channel()

# 发送消息类型为fanout，就是给所有人发消息
channel.exchange_declare(exchange='logs', exchange_type='fanout')

while True:
    message = ' '.join(sys.argv[1:]) or "Hello World ! %s" % time.time()
    channel.basic_publish(exchange="logs", routing_key="", body=message)
    #time.sleep(1)
    print ("Send msg to MQ : %s" % message)

connection.close()
