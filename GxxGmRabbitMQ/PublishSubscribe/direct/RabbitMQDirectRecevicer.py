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

channel.exchange_declare(exchange='direct_logs', type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue


