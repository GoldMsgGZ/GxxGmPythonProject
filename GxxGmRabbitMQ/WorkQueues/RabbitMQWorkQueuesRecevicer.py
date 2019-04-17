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


def callback(ch, method, properties, body):
    print (" [x] Received %r" % body)
    #time.sleep(1)
    print (" [x] Done")

    print ("method.delivery_tag", method.delivery_tag)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue='task_queue', auto_ack=False)
print (" [*] Waiting for message. To exit press CTRL+C")
channel.start_consuming()
