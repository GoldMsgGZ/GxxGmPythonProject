#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 本例会使用redis组件，需要执行 pip install redis 进行安装

############################################################################
#
# Redis中的List在内存中类似于一个name对应一个list来存储
#
#
############################################################################

import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 3

# 连接到Redis
# redis_instance = redis.Redis(host="127.0.0.1", port=6379, db=1)
redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# lpush & lpushx
# 在name对应的list中添加元素，累加的，每个新的元素都添加到列表最左边
# lpushx只有在name存在的时候才添加
print ("\n=======================开始lpush & lpushx测试===========================\n")
redis_instance.lpushx("list_name_l", 1)
redis_instance.lpush("list_name_l", 2)
redis_instance.lpushx("list_name_l", 1)
redis_instance.lpush("list_name_l", 3, 4, 5)

# rpush & rpushx
# 在name对应的list中添加元素，累加的，每个新的元素都添加到列表最右边
# rpushx只有在name存在的时候才添加
print ("\n=======================开始rpush & rpushx测试===========================\n")
redis_instance.rpushx("list_name_r", 1)
redis_instance.rpush("list_name_r", 2)
redis_instance.rpush("list_name_r", 3, 4, 5)
redis_instance.rpushx("list_name_r", 1)

# llen
# name对应的list元素个数
print ("\n=======================开始llen测试===========================\n")
redis_instance.llen("list_name_l")

# linsert(name, where, refvalue, value)
# 在对应列表的某一值前或后插入一个新值
#
print ("\n=======================开始linsert测试===========================\n")
redis_instance.linsert("list_name_l", "BEFORE", "2", "SSSSS")

# lset
# 对list中某一索引位置重新赋值
print ("\n=======================开始lset测试===========================\n")
print (redis_instance.lset("list_name_l", 3, "lset新的赋值"))

