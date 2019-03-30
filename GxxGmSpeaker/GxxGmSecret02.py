#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

q1 = u'''
简答题第二题：请叙述涉密信息系统集成资质申请单位保密管理制度应涉及的主要方面。
（一） 保密组织架构与职责。
（二） 保密教育培训 。
（三） 涉密人员管理 。
（四） 涉密载体管理 。
（五） 保密设施及设备管理 。
（六） 保密室管理 。
（七） 涉密项目实施现场管理 。
（八） 保密监督检查 。
（九） 保密工作考核与奖惩 。
（十） 泄密事件报告与查处 。
（十一） 涉密宣传报道管理 。
（十二） 保密工作经费 。
（十三） 保密风险评估与管理 。
（十四） 资质证书使用与管理。
（十五） 保密管理持续改进机制。 
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