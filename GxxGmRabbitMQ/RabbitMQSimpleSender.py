#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8


import pika
import time

# 生成凭证，创建连接
credentials = pika.PlainCredentials('login', 'login')
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials))

# 创建通道
channel = connection.channel()

# 声明队列'hello'，RabbitMQ的消息队列机制如果不存在那么数据将会被丢弃
# 这里声明队列，应该就会创建这个队列
channel.queue_declare(queue='hello')

# 给队列中添加消息
for index in range(1, 9999999):
    # 得到当前时间戳
    data = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    channel.basic_publish(exchange="", routing_key="hello", body=data)

print("发送完成")

channel.close()
