#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

q1 = u'''
简答题第四题：在岗人员保密承诺书主要包括哪些内容。
（一）认真遵守国家保密法律、法规和规章制度，履行保密义务。
（二）不提供虚假个人信息，自愿接受保密审查。
（三）不违规记录、存储、复制国家秘密信息，不违规留存涉密载体。
（四）不以任何方式泄露所接触和知悉的国家秘密。
（五）未经单位审查批准，不擅自发表涉及未公开工作内容的文章、著述。
（六）离岗时，自愿接受脱密期管理，签订保密承诺书。
（七）违反上述承诺，自愿承担党纪、政纪责任和法律后果。
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