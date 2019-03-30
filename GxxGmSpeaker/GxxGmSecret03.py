#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

q1 = u'''
简答题第三题：保密行政管理部门依法对机关、单位执行保密法律法规的哪些情况进行检查？
（一）保密工作责任制落实情况。
（二）保密制度建设情况。
（三）保密宣传教育培训情况。
（四）涉密人员管理情况。
（五）国家秘密确定、变更和解除情况。
（六）国家秘密载体管理情况。
（七）信息系统和信息设备保密管理情况。
（八）互联网使用保密管理情况。
（九）保密技术防护设施设备配备使用情况。
（十）涉密场所及保密要害部门、部位管理情况。
（十一）涉密会议、活动管理情况。
（十二）信息公开保密审查情况。
'''


import pyttsx

print q1
engine = pyttsx.init()

#语速控制
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)

while True:
    engine.say(q1)
    engine.runAndWait()
# 朗读一次
#engine.endLoop()