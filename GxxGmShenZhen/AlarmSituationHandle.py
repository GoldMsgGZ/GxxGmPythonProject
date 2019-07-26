#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#

# 读取指定文件
import json

FILE_PATH = ""
file_object = open(unicode(FILE_PATH, "utf8"))
file_content = file_object.read()

# 字符串查找
start_pos = file_content.find("<ns:return>") + len("<ns:return>")
end_pos = file_content.find("</ns:return>")
json_string = file_content[start_pos:end_pos]
json_string_utf8 = json_string.decode("gbk").encode("utf8")
json_object = json.loads(json_string_utf8)

for jj_info in json_object:
    print (u"接警单编号：" + jj_info["jjdbh"])
    print (u"呼入时间：" + jj_info["hrsj"])
    print (u"报警时间：" + jj_info["bjsj"])
    print (u"话终时间：" + jj_info["hzsj"])
    print (u"案发时间：" + jj_info["afsj"])
    print (u"通知时间：" + jj_info["tztime"])
    print (u"出动时间：" + jj_info["cdtime"])
    print (u"到达时间：" + jj_info["ddtime"])
    print (u"数据更新时间：" + jj_info["sjgxsj"])
    print (u"首次上传时间：" + jj_info["scscsj"])
    print (u"送入警综时间：" + jj_info["srjzsj"])
    print (u"案发地点：" + jj_info["afdd"])
    print (u"处警情况：\n-----------------------------\n" + jj_info["cjqk"] + "\n-----------------------------\n")
    print (u"报警内容：\n-----------------------------\n" + jj_info["bjnr"] + "\n-----------------------------\n")
    print ("================================================================")
