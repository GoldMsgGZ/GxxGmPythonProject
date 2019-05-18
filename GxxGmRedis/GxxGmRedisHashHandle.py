#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 本例会使用redis组件，需要执行 pip install redis 进行安装

############################################################################
#
# Redis中的Hash在内存中类似于一个name对应一个dic来存储
#
#
############################################################################

import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 2

# 连接到Redis
# redis_instance = redis.Redis(host="127.0.0.1", port=6379, db=1)
redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# hset & hget
# 不存在则创建
print ("\n=======================开始hset & hget测试===========================\n")
print ("即将执行：redis_instance.hset(name=\"dic_name\", key=\"a1\", value=\"aa\")")
for index in range(10):
    redis_instance.hset(name="dic_name", key="a%d" % index, value="%d%d%d" % (index, index, index))

print ("获取第一个值：")
print (redis_instance.hget("dic_name", "a1"))

# print ("获取所有值：")
# print (redis_instance.hgetall("dic_name"))


