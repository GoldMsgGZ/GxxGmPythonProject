#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
import json

FILE_PATH = ""
file_object = open(unicode(FILE_PATH, "utf8"))
file_content = file_object.read()

# 字符串查找
start_pos = file_content.find("<ns:return>") + len("<ns:return>")
end_pos = file_content.find("</ns:return>")
json_string = file_content[start_pos:end_pos]
json_string_utf8 = json_string.decode("gbk").encode("utf8")
handle_alarm_situation_handles = json.loads(json_string_utf8)

for cj_info in handle_alarm_situation_handles:
    print (u"处警单编号：" + cj_info["cjdbh"])
    print (u"接警单编号：" + cj_info["jjdbh"])
    print (u"处警时间：" + cj_info["cjsj"])
    print (u"处警结束时间（网络派单时间）：" + cj_info["cjjssj"])
    print (u"派单到达时间：" + cj_info["pdddsj"])
    print (u"派单接收时间：" + cj_info["pdjssj"])
    print (u"打印时间：" + cj_info["dysj"])
    print (u"处警时间：" + cj_info["cjsj"])
    print (u"数据更新时间：" + cj_info["sjgxsj"])
    print (u"首次上传时间：" + cj_info["scscsj"])
    print (u"备注时间：" + cj_info["bzsj"])
    print (u"到达现场时间：" + cj_info["ddxcsj"])
    print (u"处警移交时间：" + cj_info["cjyjsj"])
    print (u"出警时间：" + cj_info["pcjsj"])
    print ("=====================================================================")
