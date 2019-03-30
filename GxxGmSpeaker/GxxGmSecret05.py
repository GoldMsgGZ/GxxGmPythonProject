#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

q1 = u'''
简答题第五题：请列举资质单位与涉密人员签订的劳动合同或者补充协议应当包含的内容
（一）涉密人员的权利与义务；
（二）涉密人员应当遵守的保密纪律和有关限制性规定；
（三）因履行保密职责导致涉密人员利益受到损害，资质单位给予补偿的规定；
（四）涉密人员因违反保密规定而被无条件调离涉密岗位或给予辞退等处罚的规定；
（五）因认真履行保密职责，资质单位给予涉密人员奖励的规定；
（六）涉密人员应当遵守的其他有关事项。
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