#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

# 本例会使用redis组件，需要执行 pip install redis 进行安装

import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1

# 连接到Redis
# redis_instance = redis.Redis(host="127.0.0.1", port=6379, db=1)
redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# 使用连接池连接到Redis
# redis_connection_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)#redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
# redis_instance = redis.Redis(redis_connection_pool)

# set & get
# 单条插入，可设置超时时长
print ("\n=======================开始set & get测试===========================\n")
redis_instance.set(name="name", value="测试超时", ex=10)
print (redis_instance.get("name"))

# mset & mget
# 批量插入/查询
print ("\n=======================开始mset & mget测试===========================\n")
redis_instance.mset({"name1": "111", "name2": "1234567890", "name3": "333", "go": "go"})
print (redis_instance.mget({"name1", "name2", "go"}))

# getset
# 刷新数据
print ("\n=======================开始getset测试===========================\n")
redis_instance.getset("name1", "现在是一个新值")
print (redis_instance.get("name1"))

# getrange(key, start, end)
# 获取值域指定区间的结果
print ("\n=======================开始getrange测试===========================\n")
print (redis_instance.getrange("name2", 1, 4))

# setbit & getbit
# 二进制位插入/查询
print ("\n=======================开始setbit & getbit测试===========================\n")
string = "123456"
redis_instance.set("bit_name1", string)
for index in string:
    print (index, ord(index), bin(ord(index)))

redis_instance.setbit("bit_name1", 6, 0)
print (redis_instance.get("bit_name1"))
print (redis_instance.getbit("bit_name1", 1))
print (redis_instance.getbit("bit_name1", 2))
print (redis_instance.getbit("bit_name1", 3))
print (redis_instance.getbit("bit_name1", 4))
print (redis_instance.getbit("bit_name1", 5))
print (redis_instance.getbit("bit_name1", 6))
print (redis_instance.getbit("bit_name1", 7))
print (redis_instance.getbit("bit_name1", 8))
print (redis_instance.getbit("bit_name1", 9))
print (redis_instance.getbit("bit_name1", 10))

# bitcount
# 获取对应二进制中1的个数
print ("\n=======================开始bitcount测试===========================\n")
print (redis_instance.bitcount("bit_name1", 0, 7))

# strlen
# 计算key所指的字符串值长度
print ("\n=======================开始strlen测试===========================\n")
print (redis_instance.strlen("bit_name1"))
print (redis_instance.strlen("name1"))
print (redis_instance.strlen("name2"))

# incr(name=val, amount=value)
# 当val不存在时，创建val，初始值为value，否则自增value
print ("\n=======================开始incr测试===========================\n")
#print (redis_instance.incr("incr1", amount=99))
for index in range(100):
    print (redis_instance.incr("incr1", amount=1))

# decr
# 自减，与incr逻辑类似
print ("\n=======================开始decr测试===========================\n")
for index in range(100):
    print (redis_instance.decr("incr1", amount=1))

# append
# 在字符串后追加数据
print ("\n=======================开始append测试===========================\n")
redis_instance.set("append", "str1")
print (redis_instance.get("append"))
redis_instance.append("append", "str234567890")
print (redis_instance.get("append"))
