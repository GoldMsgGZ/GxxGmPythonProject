#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

q1 = u'''
简答题第六题：涉密人员的保密工作责任主要有哪些？
（一）严格遵守保密法律法规、规章制度；自觉接受保密教育培训；
（二）依法保管和使用涉密载体及设施；制止和纠正违反保密规定的行为；
（三）接受保密监督检查；
（四）发现泄密隐患或行为及时报告，并积极采取补救措施
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