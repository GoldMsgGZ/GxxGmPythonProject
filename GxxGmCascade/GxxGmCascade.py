#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
#
# 作者：王煜
# 功能：此范例是模拟下级平台向目标上级推送业务级联信息


###########################################################################
# 首先是配置信息
import traceback

import MySQLdb
import datetime
import json
import random
import time

import requests

MYSQL_HOST = "192.168.55.156"
MYSQL_PORT = 3306
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "mysql"
MYSQL_DBNAME = "auth-cas"

# DOMAIN 和 AUTHKEY 需要在平台级联功能处增加级联平台
DOMAIN = "53000000"
AUTHKEY = "00000000902001100763"


# 警情信息上报格式
# {
#     "cj":[
#         {
#             "cjdh":"", # 处警单号
#             "cjdw":"", # 处警单位
#             "cjdwmc":"", # 处警单位名称
#             "cjr":"", # 处警人
#             "cjrmc":"", # 处警人名称
#             "cjsj":"2019-07-13T15:52:04.265Z", # 处警时间
#             "ddxcsj":"2019-07-13T15:52:04.265Z", # 到达现场时间
#             "djsj":"2019-07-13T15:52:04.265Z", #
#             "gxsj":"2019-07-13T15:52:04.265Z", # 更新时间
#             "jqbh":"", # 警情编号
#             "mjyj":"" # 民警***
#         }
#     ]
# }

# 接警信息上报格式
# {
#     "jj": [
#         {
#             "bjfs":"", # 报警方式
#             "bjnr":"", # 报警内容
#             "bjrdh":"", # 报警人电话
#             "bjrxb":"", # 报警人性别
#             "bjrxm":"", # 报警人姓名
#             "bjsj":"2019-07-13T15:52:04.265Z",
#             "djsj":"2019-07-13T15:52:04.265Z",
#             "gxsj":"2019-07-13T15:52:04.265Z",
#             "jjdw":"", # 接警单位
#             "jjr":"", # 接警人
#             "jjrmc":"", # 接警人名称
#             "jqbh":"", # 警情编号
#             "jqlb":"", # 警情类别
#             "jqlbmc":"", # 警情类别名称
#             "jqmc":"", # 警情名称
#             "sfdd":"", # 事发地点
#             "sfsj":"2019-07-13T15:52:04.265Z", # 事发时间
#             "wj":[
#                 ""
#             ] # 文件
#         }
#     ]
# }

# 案件信息上报格式
# {
#     "aj": [
#         {
#             "afdd":"", # 案发地址
#             "afsj":"2019-07-13T15:52:04.265Z", # 案发时间
#             "ajbh":"", # 案件编号
#             "ajlb":"", # 案件类别
#             "ajlbmc":"", # 案件类别名称
#             "ajly":"", # 案件来源
#             "ajmc":"", # 案件名称
#             "anzt":"", # 案件状态
#             "jasj":"2019-07-13T15:52:04.265Z", # 结案时间？
#             "jjbh":[
#                 ""
#             ], # 接警编号
#             "jyaq":"", # 警员案情？
#             "lasj":"2019-07-13T15:52:04.265Z", # 立案时间
#             "rksj":"2019-07-13T15:52:04.265Z", # 入库时间
#             "sldw":"", # **单位
#             "sldwmc":"", # **单位名称
#             "wjxx":[
#                 {
#                     "clfl":"", # ****
#                     "gllx":"ZDGL", # 关联类型
#                     "wjbh":"", # 文件编号
#                 }
#             ], # 文件信息
#             "ysqssj":"2019-07-13T15:52:04.265Z", # 移送起诉时间
#             "zbdw":"", # 追捕单位
#             "zbdwmc":"",
#             "zbmjxm":"", # 追捕民警姓名
#             "zbr":"" # 追捕人
#         }
#     ]
# }

# 姓氏
first_name = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨",
              "朱", "秦", "尤", "许", "何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏", "陶", "姜",
              "戚", "谢", "邹", "喻", "柏", "水", "窦", "章", "云", "苏", "潘", "葛", "奚", "范", "彭", "郎",
              "鲁", "韦", "昌", "马", "苗", "凤", "花", "方", "俞", "任", "袁", "柳", "酆", "鲍", "史", "唐",
              "费", "廉", "岑", "薛", "雷", "贺", "倪", "汤", "滕", "殷", "罗", "毕", "郝", "邬", "安", "常",
              "乐", "于", "时", "傅", "皮", "卞", "齐", "康", "伍", "余", "元", "卜", "顾", "孟", "平", "黄",
              "和", "穆", "萧", "尹", "姚", "邵", "湛", "汪", "祁", "毛", "禹", "狄", "米", "贝", "明", "臧",
              "计", "伏", "成", "戴", "谈", "宋", "茅", "庞", "熊", "纪", "舒", "屈", "项", "祝", "董", "梁",
              "杜", "阮", "蓝", "闵", "席", "季", "麻", "强", "贾", "路", "娄", "危", "江", "童", "颜", "郭",
              "梅", "盛", "林", "刁", "钟", "徐", "邱", "骆", "高", "夏", "蔡", "田", "樊", "胡", "凌", "霍",
              "虞", "万", "支", "柯", "昝", "管", "卢", "莫", "经", "房", "裘", "缪", "干", "解", "应", "宗",
              "丁", "宣", "贲", "邓", "郁", "单", "杭", "洪", "包", "诸", "左", "石", "崔", "吉", "钮", "龚",
              "程", "嵇", "邢", "滑", "裴", "陆", "荣", "翁", "荀", "羊", "於", "惠", "甄", "曲", "家", "封",
              "芮", "羿", "储", "靳", "汲", "邴", "糜", "松", "井", "段", "富", "巫", "乌", "焦", "巴", "弓",
              "牧", "隗", "山", "谷", "车", "侯", "宓", "蓬", "全", "郗", "班", "仰", "秋", "仲", "伊", "宫",
              "宁", "仇", "栾", "暴", "甘", "钭", "厉", "戎", "祖", "武", "符", "刘", "景", "詹", "束", "龙",
              "叶", "幸", "司", "韶", "郜", "黎", "蓟", "薄", "印", "宿", "白", "怀", "蒲", "邰", "从", "鄂",
              "索", "咸", "籍", "赖", "卓", "蔺", "屠", "蒙", "池", "乔", "阴", "鬱", "胥", "能", "苍", "双",
              "闻", "莘", "党", "翟", "谭", "贡", "劳", "逄", "姬", "申", "扶", "堵", "冉", "宰", "郦", "雍",
              "卻", "璩", "桑", "桂", "濮", "牛", "寿", "通", "边", "扈", "燕", "冀", "郏", "浦", "尚", "农",
              "温", "别", "庄", "晏", "柴", "瞿", "阎", "充", "慕", "连", "茹", "习", "宦", "艾", "鱼", "容",
              "向", "古", "易", "慎", "戈", "廖", "庾", "终", "暨", "居", "衡", "步", "都", "耿", "满", "弘",
              "匡", "国", "文", "寇", "广", "禄", "阙", "东", "欧", "殳", "沃", "利", "蔚", "越", "夔", "隆",
              "师", "巩", "厍", "聂", "晁", "勾", "敖", "融", "冷", "訾", "辛", "阚", "那", "简", "饶", "空",
              "曾", "毋", "沙", "乜", "养", "鞠", "须", "丰", "巢", "关", "蒯", "相", "查", "后", "荆", "红",
              "游", "竺", "权", "逯", "盖", "益", "桓", "公", "万", "俟", "司马", "上官", "欧阳",
              "夏侯", "诸葛", "闻人", "东方", "赫连", "皇甫", "尉迟", "公羊",
              "澹台", "公冶", "宗政", "濮阳", "淳于", "单于", "太叔", "申屠",
              "公孙", "仲孙", "轩辕", "令狐", "钟离", "宇文", "长孙", "慕容",
              "鲜于", "闾丘", "司徒", "司空", "丌官", "司寇", "仉督", "子车",
              "颛孙", "端木", "巫马", "公西", "漆雕", "乐正", "壤驷", "公良",
              "拓跋", "夹谷", "宰父", "谷梁", "晋楚", "闫法", "汝鄢", "涂钦",
              "段干", "百里", "东郭", "南门", "呼延", "归海", "羊舌", "微生",
              "岳帅", "缑亢", "况郈", "有琴", "梁丘", "左丘", "东门", "西门",
              "商牟", "佘佴", "伯赏", "南宫"]

# 名字
name = ["蔼", "仁", "容", "德", "轩", "贤", "良", "伦", "正", "清", "义", "诚", "直", "道", "颖", "灵", "睿",
        "锐", "哲", "慧", "敦", "迪", "明", "晓", "显", "悉", "晰", "维", "学", "思", "悟", "析", "文", "书",
        "勤", "俊", "威", "英", "健", "壮", "焕", "挺", "帅", "秀", "伟", "武", "雄", "巍", "松", "柏", "山",
        "石", "婵", "娟", "姣", "妯", "婷", "姿", "媚", "婉", "丽", "妩", "美", "倩", "兰", "达", "耀", "兴",
        "荣", "华", "旺", "盈", "丰", "余", "昌", "盛", "乎", "安", "静", "顺", "通", "坦", "泰", "然", "宁",
        "定", "和", "康", "毅", "独", "刚", "强", "衡", "韧", "恒", "坚", "力", "决", "定", "立", "主", "志",
        "意", "自", "梁", "栋", "维", "启", "克", "伦", "翔", "旭", "鹏", "泽", "晨", "辰", "士", "以", "建",
        "家", "致", "树", "炎", "盛", "雄", "琛", "钧", "冠", "策", "腾", "楠", "榕", "风", "航", "弘", "义",
        "兴", "良", "飞", "彬", "富", "和", "鸣", "朋", "斌", "行", "时", "泰", "博", "磊", "民", "友", "志",
        "清", "坚", "庆", "若", "德", "彪", "伟", "刚", "勇", "毅", "俊", "峰", "强", "军", "平", "保", "东",
        "文", "辉", "力", "明", "永", "健", "世", "广", "海", "山", "仁", "波", "宁", "福", "生", "龙", "元",
        "全", "国", "胜", "学", "祥", "才", "发", "武", "新", "利", "顺", "信", "子", "杰", "涛", "昌", "成",
        "康", "星", "光", "天", "达", "安", "岩", "中", "茂", "进", "林", "有", "诚", "先", "敬", "震", "振",
        "壮", "会", "思", "群", "豪", "心", "邦", "承", "乐", "绍", "功", "松", "善", "厚", "裕"]


alarm_type = ["电话报警", "派出所报警"]
alarm_content = [
    {"id": "0001", "type": "抢劫"},
    {"id": "0002", "type": "盗窃"},
    {"id": "0003", "type": "吸毒"},
    {"id": "0004", "type": "打架"},
    {"id": "0005", "type": "赌博"},
    {"id": "0006", "type": "卖淫"},
    {"id": "0007", "type": "嫖娼"},
    {"id": "0008", "type": "诈骗"},
    {"id": "0009", "type": "杀人"},
    {"id": "0010", "type": "拐卖妇女儿童"},
    {"id": "0011", "type": "猥亵"}
]

# http://www.mca.gov.cn/article/sj/xzqh/2019/201901-06/201906211421.html
# 2019年5月中华人民共和国县以上行政区划代码
# 这里仅采用广东地区，后续可以考虑扩展
org = [
    {
        "id": "440000",
        "name": "广东省",
        "cities": [
            {"id": "440100", "name": "广州市", "counties": [
                {"id": "440103", "name": "荔湾区"},
                {"id": "440104", "name": "越秀区"},
                {"id": "440105", "name": "海珠区"},
                {"id": "440106", "name": "天河区"},
                {"id": "440111", "name": "白云区"},
                {"id": "440112", "name": "黄埔区"},
                {"id": "440113", "name": "番禺区"},
                {"id": "440114", "name": "花都区"},
                {"id": "440115", "name": "南沙区"},
                {"id": "440117", "name": "从化区"},
                {"id": "440118", "name": "增城区"}
            ]},
            {"id": "440200", "name": "韶关市", "counties": [
                {"id": "440203", "name": "武江区"},
                {"id": "440204", "name": "浈江区"},
                {"id": "440205", "name": "曲江区"},
                {"id": "440222", "name": "始兴县"},
                {"id": "440224", "name": "仁化县"},
                {"id": "440229", "name": "翁源县"},
                {"id": "440232", "name": "乳源瑶族自治县"},
                {"id": "440233", "name": "新丰县"},
                {"id": "440281", "name": "乐昌市"},
                {"id": "440282", "name": "南雄市"}
            ]},
            {"id": "440300", "name": "深圳市", "counties": [
                {"id": "440303", "name": "罗湖区"},
                {"id": "440304", "name": "福田区"},
                {"id": "440305", "name": "南山区"},
                {"id": "440306", "name": "宝安区"},
                {"id": "440307", "name": "龙岗区"},
                {"id": "440308", "name": "盐田区"},
                {"id": "440309", "name": "龙华区"},
                {"id": "440310", "name": "坪山区"},
                {"id": "440311", "name": "光明区"}
            ]},
            {"id": "440400", "name": "珠海市", "counties": [
                {"id": "440402", "name": "香洲区"},
                {"id": "440403", "name": "斗门区"},
                {"id": "440404", "name": "金湾区"}
            ]},
            {"id": "440500", "name": "汕头市", "counties": [
                {"id": "440507", "name": "龙湖区"},
                {"id": "440511", "name": "金平区"},
                {"id": "440512", "name": "濠江区"},
                {"id": "440513", "name": "潮阳区"},
                {"id": "440514", "name": "潮南区"},
                {"id": "440515", "name": "澄海区"},
                {"id": "440523", "name": "南澳县"}
            ]},
            {"id": "440600", "name": "佛山市", "counties": [
                {"id": "440515", "name": "禅城区"},
                {"id": "440515", "name": "南海区"},
                {"id": "440515", "name": "顺德区"},
                {"id": "440515", "name": "三水区"},
                {"id": "440515", "name": "高明区"}
            ]},
            {"id": "440700", "name": "江门市", "counties": [
                {"id": "440703", "name": "蓬江区"},
                {"id": "440704", "name": "江海区"},
                {"id": "440705", "name": "新会区"},
                {"id": "440781", "name": "台山市"},
                {"id": "440783", "name": "开平市"},
                {"id": "440784", "name": "鹤山市"},
                {"id": "440785", "name": "恩平市"}
            ]},
            {"id": "440800", "name": "湛江市", "counties": [
                {"id": "440802", "name": "赤坎区"},
                {"id": "440803", "name": "霞山区"},
                {"id": "440804", "name": "坡头区"},
                {"id": "440811", "name": "麻章区"},
                {"id": "440823", "name": "遂溪县"},
                {"id": "440825", "name": "徐闻县"},
                {"id": "440881", "name": "廉江市"},
                {"id": "440882", "name": "雷州市"},
                {"id": "440883", "name": "吴川市"}
            ]},
            {"id": "440900", "name": "茂名市", "counties": [
                {"id": "440902", "name": "茂南区"},
                {"id": "440904", "name": "电白区"},
                {"id": "440981", "name": "高州市"},
                {"id": "440982", "name": "化州市"},
                {"id": "440983", "name": "信宜市"}
            ]},
            {"id": "441200", "name": "肇庆市", "counties": [
                {"id": "441202", "name": "端州区"},
                {"id": "441203", "name": "鼎湖区"},
                {"id": "441204", "name": "高要区"},
                {"id": "441223", "name": "广宁县"},
                {"id": "441224", "name": "怀集县"},
                {"id": "441225", "name": "封开县"},
                {"id": "441226", "name": "德庆县"},
                {"id": "441284", "name": "四会市"}
            ]},
            {"id": "441300", "name": "惠州市", "counties": [
                {"id": "441302", "name": "惠城区"},
                {"id": "441303", "name": "惠阳区"},
                {"id": "441322", "name": "博罗县"},
                {"id": "441323", "name": "惠东县"},
                {"id": "441324", "name": "龙门县"}
            ]},
            {"id": "441400", "name": "梅州市", "counties": [
                {"id": "441402", "name": "梅江区"},
                {"id": "441403", "name": "梅县区"},
                {"id": "441422", "name": "大埔县"},
                {"id": "441423", "name": "丰顺县"},
                {"id": "441424", "name": "五华县"},
                {"id": "441426", "name": "平远县"},
                {"id": "441427", "name": "蕉岭县"},
                {"id": "441481", "name": "兴宁市"}
            ]},
            {"id": "441500", "name": "汕尾市", "counties": [
                {"id": "441502", "name": "城区"},
                {"id": "441521", "name": "海丰县"},
                {"id": "441523", "name": "陆河县"},
                {"id": "441581", "name": "陆丰市"}
            ]},
            {"id": "441600", "name": "河源市", "counties": [
                {"id": "441602", "name": "源城区"},
                {"id": "441621", "name": "紫金县"},
                {"id": "441622", "name": "龙川县"},
                {"id": "441623", "name": "连平县"},
                {"id": "441624", "name": "和平县"},
                {"id": "441625", "name": "东源县"}
            ]},
            {"id": "441700", "name": "阳江市", "counties": [
                {"id": "441702", "name": "江城区"},
                {"id": "441704", "name": "阳东区"},
                {"id": "441721", "name": "阳西县"},
                {"id": "441781", "name": "阳春市"}
            ]},
            {"id": "441800", "name": "清远市", "counties": [
                {"id": "441802", "name": "清城区"},
                {"id": "441803", "name": "清新区"},
                {"id": "441821", "name": "佛冈县"},
                {"id": "441823", "name": "阳山县"},
                {"id": "441825", "name": "连山壮族瑶族自治县"},
                {"id": "441826", "name": "连南瑶族自治县"},
                {"id": "441881", "name": "英德市"},
                {"id": "441882", "name": "连州市"}
            ]},
            {"id": "441900", "name": "东莞市", "counties": []},
            {"id": "442000", "name": "中山市", "counties": []},
            {"id": "445100", "name": "潮州市", "counties": [
                {"id": "445102", "name": "湘桥区"},
                {"id": "445103", "name": "潮安区"},
                {"id": "445122", "name": "饶平县"}
            ]},
            {"id": "445200", "name": "揭阳市", "counties": [
                {"id": "445202", "name": "榕城区"},
                {"id": "445203", "name": "揭东区"},
                {"id": "445222", "name": "揭西县"},
                {"id": "445224", "name": "惠来县"},
                {"id": "445281", "name": "普宁市"}
            ]},
            {"id": "445300", "name": "云浮市", "counties": [
                {"id": "445302", "name": "云城区"},
                {"id": "445303", "name": "云安区"},
                {"id": "445321", "name": "新兴县"},
                {"id": "445322", "name": "郁南县"},
                {"id": "445381", "name": "罗定市"}
            ]}
            ]
    }
]

road = ["鳌鱼岗四巷", "北环路", "北街路", "上十二巷", "柴栏田南便新村六巷", "车陂农场路", "车陂美东街", "车站路", "程界成龙街",
        "晨邮路", "车陂街", "东风东路", "东风东路", "大观北路", "大观路", "东圃大观南路", "东马路", "东乔大道", "东横二路",
        "东横三路", "东横一路", "东横三路三巷", "大塘边街", "东横三路六巷", "东横四路", "东社四巷", "东社直街", "东圃菁映路",
        "大坝东环街", "东圃湖边街", "东康街南巷", "东圃二横路", "东岸路", "东圃陂东路", "大片北路", "大观中路", "福庭街", "富华街",
        "龙洞步行街", "广河高速公路", "环城高速公路", "广利路", "烟草宿舍", "光谱中路", "高地龙口巷", "广棠西路", "广园快速路",
        "广氮金安路", "广州大道中", "广和路", "广河高速公路", "广园快速路", "环城高速公路", "广园快速路", "花城大道",
        "黄村新村大街", "汇景中路", "花枝路", "黄村环场路", "护林路", "华南东侧路", "黄埔大道东", "合晖街", "胡岗新村八巷",
        "华景西街", "华晖街", "虹口街", "黄猄坳路", "河水西街", "河水大街一横巷", "宏御东路", "含珠街", "火炉山南路", "横圳路",
        "华讯街", "华明路", "荷包岭新街", "葫芦岭街六巷", "葫芦岭街二巷", "葫芦岭街三巷", "华美路", "葫芦岭街五巷", "吉山大园街",
        "吉兴街", "金颖东二街", "金颖东二南街", "金颖西横街", "金融南路", "京珠高速", "景邮路", "金鸡西街二巷路", "金安路",
        "江月路", "剑咀大街", "金曦路", "剑咀路", "金融东路", "科韵路", "柯木塱金铺东一街", "柯木塱新村西街", "柯木塱新村南街",
        "柯木塱上涂屋西二街", "柯木塱西路", "柯木塱坳头北新街", "柯木塱背坪榄排街", "科学大道", "科翔路", "科珠路", "柯木塱背坪拾排街",
        "科韵路", "柯木塱欧岗南一街", "林和东路", "灵山东路", "莲塘路", "龙洞山庄大街", "龙口东路", "龙洞商业步行街", "罗浮山路",
        "莲溪路", "揽月路", "粮仓街", "凌塘村新村大街南巷", "龙盛街", "龙岗东路", "猎德大道荔园一巷", "龙光里大街", "龙步新村北巷",
        "濂泉路", "龙湖路", "蓝屋一街", "蓝屋北街", "明豪二街", "明豪三街", "明豪一街", "梅东北延长线", "沐陂东路", "牛利岗大街社区",
        "南翔一路", "南便街", "饭堂巷", "南富大街", "欧岗西街二巷", "欧岗南二街", "前段路", "融星路", "融和路", "融德路", "水荫路",
        "神舟路", "水荫横路", "思成路", "深涌路", "水荫路石东街", "石材大街", "石牌绿荷西大街", "石牌岗顶南大路", "上元岗元岗街",
        "上元岗还原街一巷", "棠下涌东路", "塘石新街一巷", "塘石大街三巷", "塘石二街二巷", "塘石一街", "棠下西沙二巷", "棠下荷光二横路",
        "泰盛路", "田心路", "棠下大片路", "棠东东南路", "棠下南闸大街", "天河区东圃大马路西二巷"]

phone_title = ["130", "131", "132", "133", "134", "135", "136",
               "137", "138", "139", "159", "169", "179", "189", "177"]


def get_alarm_type():
    # 获取报警类型
    # 获取一个随机数
    return random.choice(alarm_type)


def get_alarm_situation_type():
    real_alarm_content = random.choice(alarm_content)
    alarm_situation_id = real_alarm_content["id"]
    alarm_situation_type = real_alarm_content["type"]
    return alarm_situation_id, alarm_situation_type


def get_random_division():
    province_info = random.choice(org)
    province_name = province_info["name"]
    province_code = province_info["id"]
    province_cities = province_info["cities"]
    city_info =  random.choice(province_cities)
    city_name = city_info["name"]
    city_code = city_info["id"]
    city_counties = city_info["counties"]
    if len(city_counties) > 0:
        county_info = random.choice(city_counties)
        county_name = county_info["name"]
        county_code = county_info["id"]
    else:
        county_name = city_name
        county_code = city_code

    return province_name, province_code, city_name, city_code, county_name, county_code


def get_alarm_content(province_, city_, county_, road_, alarm_situation_type_):
    # 生成报警内容
    address = province_
    address = address + city_
    address = address + county_
    address = address + random.choice(road_)
    real_alarm_content = address
    real_alarm_content = real_alarm_content + "发生"
    real_alarm_content = real_alarm_content + alarm_situation_type_
    real_alarm_content = real_alarm_content + "事件"
    return real_alarm_content, address


def get_person_name():
    # 生成名字
    name_1 = random.choice(first_name)
    name_2 = random.choice(name)
    name_3 = random.choice(name)

    # 是否使用三个字的名字
    if random.choice([True, False]):
        person_name = name_1 + name_2 + name_3
    else:
        person_name = name_1 + name_2

    return person_name


def get_phone_nunber():
    phone_number = random.choice(phone_title)
    for index in range(8):
        phone_number = phone_number + random.choice(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

    return phone_number


def get_current_datetime():
    t = time.time()
    now_time = int(round(t * 1000))
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime('%Y%m%d%H%M%S')
    current_time_str2 = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return now_time


def init_data_from_system():
    # 从系统中初始化一些数据
    # 主要是组织架构部门信息，还有用户信息
    db = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USERNAME, passwd=MYSQL_PASSWORD, db=MYSQL_DBNAME, charset="utf8")
    cursor = db.cursor()  # 创建一个游标对象
    # 搜索所有部门
    sql = "SELECT * FROM `uap_tb_gmvcs_organize`;"

    org_infos = list()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            org_info = dict()
            org_info["org_id"] = row[0]
            org_info["duty_range"] = row[1]
            org_info["extend"] = row[2]
            org_info["order_no"] = int(row[3])
            org_info["org_code"] = row[4]
            org_info["org_name"] = row[5]
            org_info["path"] = row[6]
            org_info["update_time"] = str(row[7])
            org_info["parent"] = row[8]
            org_info["source"] = row[9]

            # 搜索部门所有用户
            sql2 = "SELECT * FROM `uap_tb_gmvcs_user` WHERE org_id=\"%s\";" % (org_info["org_id"].encode("utf8"))
            user_infos = list()

            # 执行SQL语句
            cursor.execute(sql2)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                user_info = dict()
                user_info["uid"] = row[0]
                user_info["account"] = row[1]
                user_info["admin"] = row[2]
                user_info["create_time"] = row[3]
                user_info["create_user"] = row[4]
                user_info["email"] = row[5]
                user_info["enable"] = row[6]
                user_info["extend"] = row[7]
                user_info["gender"] = row[8]
                user_info["id_card"] = row[9]
                user_info["is_deleted"] = row[10]
                user_info["last_login_time"] = row[11]
                user_info["login_status"] = row[12]
                user_info["mobel_phone"] = row[13]
                user_info["password"] = row[14]
                user_info["repeat_login"] = row[15]
                user_info["spell_abbr"] = row[16]
                user_info["spell_full"] = row[17]
                user_info["update_time"] = row[18]
                user_info["user_code"] = row[19]
                user_info["user_name"] = row[20]
                user_info["user_type"] = row[21]
                user_info["job_type"] = row[22]
                user_info["org_id"] = row[23]
                user_info["police_type"] = row[24]
                user_info["last_login_ip"] = row[25]
                user_info["source"] = row[26]
                user_info["login_fail_num"] = row[27]
                user_info["is_black_role"] = row[28]
                user_info["pwd_valid_date"] = row[29]
                user_info["pwd_expire_date"] = row[30]
                user_info["login_limit"] = row[31]
                user_info["ip_limit"] = row[32]
                user_info["account_valid_days"] = row[33]
                user_info["account_expire_date"] = row[34]
                user_info["is_valid"] = row[35]

                user_infos.append(user_info)
                # print (user_info)

            org_info["users"] = user_infos
            org_infos.append(org_info)
            # print (org_info)

    except Exception:
        traceback.print_exc()

    # 关闭数据库，避免内存泄漏
    db.close()

    return org_infos


def get_org_and_police(org_infos):
    # 随机获取接处警部门以及民警
    while True:
        org_info = random.choice(org_infos)
        if len(org_info["users"]) == 0:
            continue

        user_info = random.choice(org_info["users"])
        break

    return org_info["org_code"].encode("utf8"), org_info["org_name"].encode("utf8"), user_info["user_code"].encode("utf8"), user_info["user_name"].encode("utf8")


class GxxGmPlatform:

    def __init__(self):
        self.platform_id="0001" # 平台ID
        self.orgs = init_data_from_system()

    def send_alarm_situations(self):
        # 发送警情信息
        # 首先生成接警信息

        receive_alarm_json = dict()
        receive_alarm_json["jj"] = list()

        handle_alarm_situation_json = dict()
        handle_alarm_situation_json["cj"] = list()

        for index in range(1000):

            # 这里处理一下，接警人，处警人均为同一人，部门也是所属部门的
            org_code, org_name, police_code, police_name = get_org_and_police(self.orgs)
            # 生成警情类型
            alarm_situation_id, alarm_situation_type = get_alarm_situation_type()
            # 生成案发地点和警情信息
            province_name, province_code, city_name, city_code, county_name, county_code = get_random_division()
            alarm_situation_info, address = get_alarm_content(province_name, city_name, county_name, road, alarm_situation_type)

            # 构建接警信息
            receive_alarm = dict()
            receive_alarm["bjfs"] = get_alarm_type()                        # 报警方式
            receive_alarm["bjnr"] = alarm_situation_info                    # 报警内容
            receive_alarm["bjrdh"] = get_phone_nunber()                     # 报警人电话
            receive_alarm["bjrxb"] = random.choice(["男", "女"])             # 报警人性别
            receive_alarm["bjrxm"] = get_person_name()                              # 报警人姓名
            receive_alarm["bjsj"] = get_current_datetime()                          # 报警事件
            receive_alarm["djsj"] = get_current_datetime()
            receive_alarm["gxsj"] = get_current_datetime()
            receive_alarm["jjdw"] = org_code                                        # 接警单位
            receive_alarm["jjdwmc"] = org_name
            receive_alarm["jjr"] = police_code                                      # 接警人
            receive_alarm["jjrmc"] = police_name                                    # 接警人名称
            receive_alarm["jqbh"] = "JQ" + org_code + str(get_current_datetime())                  #
            receive_alarm["jqlb"] = alarm_situation_id                      #
            receive_alarm["jqlbmc"] = alarm_situation_type                  #
            receive_alarm["jqmc"] = alarm_situation_info                    #
            receive_alarm["sfdd"] = address                                 #
            receive_alarm["sfsj"] = get_current_datetime()                  #
            receive_alarm["wj"] = list()                                    #
            receive_alarm_json["jj"].append(receive_alarm)

            # 生成警情信息
            handle_alarm_situation = dict()
            handle_alarm_situation["cjdh"] = "CJ" + org_code + str(get_current_datetime())
            handle_alarm_situation["cjdw"] = org_code
            handle_alarm_situation["cjdwmc"] = org_name
            handle_alarm_situation["cjr"] = police_code
            handle_alarm_situation["cjrmc"] = police_name
            handle_alarm_situation["cjsj"] = get_current_datetime()
            handle_alarm_situation["ddxcsj"] = get_current_datetime()
            handle_alarm_situation["djsj"] = get_current_datetime()
            handle_alarm_situation["gxsj"] = get_current_datetime()
            handle_alarm_situation["jqbh"] = receive_alarm["jqbh"]
            handle_alarm_situation["mjyj"] = ""
            handle_alarm_situation_json["cj"].append(handle_alarm_situation)



        # 发送接警信息
        post_header = dict()
        post_header["Content-Type"] = "application/json"
        post_header["Accept"] = "application/json"

        # 这里目前会返回500
        # print (json.dumps(receive_alarm_json))
        OPENAPI_RECEIVEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/ps/basic/info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
        response = requests.post(url=OPENAPI_RECEIVEALARMSITUATION_URL, data=json.dumps(receive_alarm_json),
                                 headers=post_header)
        err_code = 0
        if response.status_code != 200:
            err_code = response.status_code
            return err_code
        else:
            err_code = 0

        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
                print(u"发送接警信息失败！" + str(err_code))
                return err_code
        except ValueError:
            print(u"发送接警信息失败！")
            return -1

        # print (json.dumps(handle_alarm_situation_json))
        OPENAPI_HANDLEALARMSITUATION_URL = "http://192.168.55.156:6803/openapi/levam/platform/upload/hs/basic/info?domain=" + DOMAIN + "&authkey=" + AUTHKEY
        response = requests.post(url=OPENAPI_HANDLEALARMSITUATION_URL, data=json.dumps(handle_alarm_situation_json),
                                 headers=post_header)
        err_code = 0
        if response.status_code != 200:
            err_code = response.status_code
            return err_code
        else:
            err_code = 0

        try:
            content_json = json.loads(response.content)
            if content_json['code'] != 0:
                err_code = content_json['code']
                print(u"发送处警信息失败！")
                return err_code
        except ValueError:
            print(u"发送处警信息失败！")
            return -1

        return err_code



if __name__ == "__main__":
    init_data_from_system()
    platform = GxxGmPlatform()

    while True:
        platform.send_alarm_situations()