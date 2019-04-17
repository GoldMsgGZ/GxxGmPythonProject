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

# 声明队列'task_queue'，RabbitMQ的消息队列机制如果不存在那么数据将会被丢弃
# 这里声明队列，应该就会创建这个队列
channel.queue_declare(queue='task_queue')

# make message persistent（就是消息持久化）
# properties = pika.BasicProperties(delivery_mode=2)

# for index in range(0, 1000000):
while True:
    message = ' '.join(sys.argv[1:]) or "Hello World ! %s" % time.time()
    channel.basic_publish(exchange="", routing_key="task_queue", body=message)
    time.sleep(0.1)
    print ("Send msg to MQ : %s" % message)

connection.close()
