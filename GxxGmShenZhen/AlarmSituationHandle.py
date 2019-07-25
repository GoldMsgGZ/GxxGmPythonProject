#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#

alarm_situation_json_string = []

for jj_info in alarm_situation_json_string:
    print ("接警单编号：" + jj_info["jjdbh"])
    print ("呼入时间：" + jj_info["hrsj"])
    print ("报警时间：" + jj_info["bjsj"])
    print ("话终时间：" + jj_info["hzsj"])
    print ("案发时间：" + jj_info["afsj"])
    print ("通知时间：" + jj_info["tztime"])
    print ("出动时间：" + jj_info["cdtime"])
    print ("到达时间：" + jj_info["ddtime"])
    print ("数据更新时间：" + jj_info["sjgxsj"])
    print ("首次上传时间：" + jj_info["scscsj"])
    print ("送入警综时间：" + jj_info["srjzsj"])
    print ("================================================================")
