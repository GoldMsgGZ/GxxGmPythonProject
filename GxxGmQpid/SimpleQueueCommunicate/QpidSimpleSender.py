#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

from kombu import Connection, Exchange, Queue

media_exchange = Exchange('media', 'direct', durable=True)
video_queue = Queue('video', exchange=media_exchange, routing_key='video')

with Connection('amqp://admin:admin@localhost//', login_method='AMQPLAIN') as conn:

    #conn.connect()

    # 生产
    producer = conn.Producer(serializer='json')
    producer.publish({'name': '/tmp/local1.avi', 'size': 1301013}, exchange=media_exchange, routing_key='video', declare=[video_queue])
