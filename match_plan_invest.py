# -*- coding:utf-8 -*-
import requests
import traceback
import json
import pymysql
import MysqlDirver

#1.连接数据库，找到对应的出借订单


#2.查看未出借的剩余订单需要匹配什么类型资产


#3.调整数据库，调整为对应匹配模式


#4.跑投资匹配请求--普通资产满标申请银行放款--普通资产满标起息确认


#5.检查用户锁定状态，是否处于锁定状态，未锁定


#6.打印日志到后台，进行实时跟踪