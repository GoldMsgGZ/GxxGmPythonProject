#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

q1 = u'''
简答题第七题：涉密人员脱密期管理主要有哪些要求？
（一）明确脱密期限；
（二）与原机关、单位签订保密承诺书，做出继续履行保密义务、不泄露所知悉国家秘密的承诺；
（三）及时清退所持有和使用的全部涉密载体和涉密信息设备，并办理移交手续；
（四）未经审查批准，不得擅自出境；
（五）不得到境外驻华机构、组织或者外资企业工作；
（六）不得为境外组织人员或者外资企业提供劳务、咨询或者其他服务。
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