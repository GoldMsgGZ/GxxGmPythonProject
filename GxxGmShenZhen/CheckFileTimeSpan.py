#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 需要用到的一些方法：
#   os.getcwd()            返回当前工作目录
#   os.path.getatime(file) 输出文件访问时间
#   os.path.getctime(file) 输出文件的创建时间
#   os.path.getmtime(file) 输出文件最近修改时间
import ConfigParser
import datetime
import logging
import os
import time



# 读取配置文件
cf = ConfigParser.ConfigParser()
cf.read("CheckFileTimeSpan.ini")

# 扫描根路径
BASR_DIR = cf.get("RUNNING_CFG", "ROOT_DIR")
# 扫描时间间隔
ENUM_TIME_SPAN = cf.getint("RUNNING_CFG", "ENUM_TIME_SPAN")

# 初始化日志配置
current_time = datetime.datetime.now()
current_time_str = current_time.strftime('%Y%m%d%H%M%S')
logging_filename = current_time_str + ".log"
logging.basicConfig(level=logging.INFO, filename=logging_filename, filemode="a",
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger()

# 首先遍历目录
file_list = os.listdir(BASR_DIR)

while True:
    for file_info in file_list:
        path = os.path.join(BASR_DIR, file_info)
        if os.path.isfile(path):
            current_time = datetime.datetime.now()
            current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            create_time = os.path.getctime(path)
            create_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(create_time))
            modify_time = os.path.getmtime(path)
            modify_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modify_time))
            access_time = os.path.getatime(path)
            access_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(access_time))

            logger.info("[FILE] >>> " + path.decode("gbk").encode("utf8"))
            logger.info("当前时间：" + current_time_str)
            logger.info("创建时间：" + create_time_str)
            logger.info("修改时间：" + modify_time_str)
            logger.info("访问时间：" + access_time_str)
            logger.info("============================================================")
            print ("[FILE] >>> " + path.decode("gbk").encode("utf8"))
            print ("当前时间：" + current_time_str)
            print ("创建时间：" + create_time_str)
            print ("修改时间：" + modify_time_str)
            print ("访问时间：" + access_time_str)
        # elif os.path.isdir(path):
        #     print ("[DIRECTORY] >>> " + path)

            print ("============================================================")

    time.sleep(ENUM_TIME_SPAN)



