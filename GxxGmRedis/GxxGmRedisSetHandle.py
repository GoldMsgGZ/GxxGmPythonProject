#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 本例会使用redis组件，需要执行 pip install redis 进行安装

############################################################################
#
# Redis中的Set是不允许重复的列表
#
############################################################################

import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 4

# 连接到Redis
# redis_instance = redis.Redis(host="127.0.0.1", port=6379, db=1)
redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# sedd
# 给对应的集合中添加元素
print ("\n=======================开始 sedd 测试===========================\n")
redis_instance.sadd("set_name", "aa")
redis_instance.sadd("set_name", "aa", "bb")

# smembers
#




