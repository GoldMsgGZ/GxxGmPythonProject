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
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]   #接收那些消息（指info，还是空），没写就报错
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0]) #定义了三种接收消息方式info,warning,error
    sys.exit(1)

for severity in severities: #[error  info  warning]，循环severities
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)  #循环绑定关键字
print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(on_message_callback=callback, queue=queue_name,)
channel.start_consuming()

