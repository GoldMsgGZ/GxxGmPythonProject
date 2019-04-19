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

# 发送消息类型为direct
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# 根据参数设置路由key
routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'

while True:
    message = ' '.join(sys.argv[1:]) or "Hello World ! %s" % time.time()
    channel.basic_publish(exchange="topic_logs", routing_key=routing_key, body=message)
    time.sleep(1)
    print ("Send %r:%r" % (routing_key, message))

connection.close()

