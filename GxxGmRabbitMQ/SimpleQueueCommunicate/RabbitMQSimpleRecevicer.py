#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 此项目使用了第三方库pika，这里需要在终端输入：pip install pika 进行安装


import pika


# 生成凭证，创建连接
credentials = pika.PlainCredentials('login', 'login')
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672, '/', credentials))

# 创建通道
channel = connection.channel()

# 声明队列'hello'，RabbitMQ的消息队列机制如果不存在那么数据将会被丢弃
# 这里声明队列，应该就会创建这个队列
channel.queue_declare(queue='hello')


def callback(ch, method, propertise, body):
    print("  [x] Receviced %r" % body)


channel.basic_consume(on_message_callback=callback, queue='hello', auto_ack=True)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
