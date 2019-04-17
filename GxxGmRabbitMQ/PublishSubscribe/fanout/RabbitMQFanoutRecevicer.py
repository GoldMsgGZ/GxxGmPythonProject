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

# 必须通过queue来收消息
# 不指定queue的名字，RabbitMQ会随机分配一个名字，exclusive=True会在使用此queue的消费者断开后，自动将queue删除
result = channel.queue_declare(queue='', exclusive=True)

# 取得queue的名字
queue_name = result.method.queue

# 将随机生成的queue名字绑定到exchange上面
channel.queue_bind(exchange='logs', queue=queue_name)

print (" [*] Waiting for logs. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print (" [x] %r" % body)


channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)
channel.start_consuming()

