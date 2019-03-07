"""投资匹配"""
# -*- coding:utf-8 -*-
import requests
import traceback
import json
import pymysql
import time
import datetime
from MysqlDirver import MysqlDiver
from invest_run_test import AutoInvest

# 待出借的订单需匹配的资产类型（1：授权3.0--匹配普通资产，2：授权3.0--匹配债转资产，3：智能2.0--匹配债转资产，4：智能2.0--匹配普通资产，5：票票贷--匹配普通资产）

def match_general_3_assert_invest(conn,cur):
    #找出全部需准备下单并匹配3.0普通资产的订单
    autoInvester = AutoInvest()
    users_list = autoInvester.run_invest(1)
    #判断是否出借成功
    invest_status_sql = """SELECT a.`invest_status` FROM `invest_app_invest` a,`invest_app_match` b,`invest_app_product` c \
    WHERE a.`id`=b.`User_id` AND b.`Type_id`=c.`id` AND c.`id`=%d ORDER BY a.`id` LIMIT 1;""" % (1)
    cur.execute(invest_status_sql)
    invest_status_result = cur.fetchall()
    if(isinstance(invest_status_result,list)):
        invest_status = invest_status_result[0]["invest_status"]
        if(invest_status==1 and len(invest_status_result)==1): #判断type=1的所有出借订单，已出借完成
            #步骤1：配置pj_test3_other.`t_debt_limit`表中的当日的债转金额为0，使全部出借订单匹配普通标的
            now_date_str = datetime.datetime.now()
            now_date = str(now_date_str).split(" ")[0]
            update_debit_sql = """UPDATE pj_test3_other.`t_debt_limit` a SET a.`debt_limit`=0.000000 WHERE a.`effect_date`=%s;""" % now_date
            try:
                test_env_cur,test_env_conn = MysqlDiver(db='test3',host='192.168.1.179',port=3306,user='sp2p_web',password='123456')
                test_env_cur.execute(update_debit_sql)
                test_env_conn.connect()
            except:
                traceback.print_exc()
            #步骤2：执行1,3任务，查看对应出借订单状态，及普通标的满标情况
            rsp1 = requests.post("http://192.168.1.188:8084/pj-p2p-job/p2gRun/01matchPlanInvest")
            if(rsp1.status_code == 200):
                print(">>>1号：投资匹配 --> 成功")
            rsp2 = requests.post("http://192.168.1.188:8084/pj-p2p-job/p2gRun/03allInvestMakeLoan")
            if(rsp2.status_code == 200):
                print(">>>3号：普通资产满标申请银行放款 --> 成功")
            #步骤3：执行4任务，满标起息确认
            time.sleep(10)
            rsp3 = requests.post("http://192.168.1.188:8084/pj-p2p-job/p2gRun/04allProductMakeLoan")
            if(rsp3.status_code == 200):
                print(">>>4号：普通资产满标起息确认 --> 成功")
            #步骤4：检查对应出借订单状态是否处于锁定中，若锁定中更新表状态为1


        else:
            autoInvester.run_invest(1)

    else:
        traceback.print_exc()

def match_debt_3_assert_invest(conn,cur):
    #找出全部需准备下单并匹配3.0债转资产的订单
    autoInvester = AutoInvest()
    autoInvester.run_invest(2)
    ##判断是否出借成功
    invest_status_sql = """SELECT a.`invest_status` FROM `invest_app_invest` a,`invest_app_match` b,`invest_app_product` c \
    WHERE a.`id`=b.`User_id` AND b.`Type_id`=c.`id` AND c.`id`=%d ORDER BY a.`id` LIMIT 1;""" % (2)
    cur.execute(invest_status_sql)
    invest_status_result = cur.fetchall()
    print(invest_status_result)


def match_general_2_assert_invest(conn,cur):
    #找出全部需准备下单并匹配2.0普通资产的订单
    autoInvester = AutoInvest()
    autoInvester.run_invest(3)

def match_debt_2_assert_invest(conn,cur):
    #找出全部需准备下单并匹配2.0债转资产的订单
    autoInvester = AutoInvest()
    autoInvester.run_invest(4)

def match_general_PPD_assert_invest(conn,cur):
    #先购买2.0的产品，最好是同一个用户一笔或者两笔订单匹配到同一个标的
    buy_2_sql = """UPDATE pj_test3_core.t_plan a SET a.`prod_version`=3 WHERE a.id IN (7,9) AND a.`prod_version`=2 AND a.`status`=1; """
    cur.execute(buy_2_sql)
    conn.commit()
    #找出全部需准备下单并匹配票票贷的订单
    autoInvester = AutoInvest()
    autoInvester.run_invest(5)

    #判断t_product表，是否存在230的普通标的，并且标的未过期，金额为6000元，不足的if_del设置为1的状态

    # 判断是否出借成功
    invest_status_sql = """SELECT a.`invest_status` FROM `invest_app_invest` a,`invest_app_match` b,`invest_app_product` c \
        WHERE a.`id`=b.`User_id` AND b.`Type_id`=c.`id` AND c.`id`=%d ORDER BY a.`id` LIMIT 1;""" % (5)
    cur.execute(invest_status_sql)
    invest_status_result = cur.fetchall()
    if (isinstance(invest_status_result, list)):
        invest_status = invest_status_result[0]["invest_status"]
        while(True):
            if (invest_status == 1 and len(invest_status_result) == 1):  # 判断type=1的所有出借订单，已出借完成
                #出借完成，重新设置为2
                restore_sql = """UPDATE pj_test3_core.t_plan a SET a.`prod_version`=2 WHERE a.id IN (7,9) AND a.`prod_version`=3 AND a.`status`=1; """
                cur.execute(restore_sql)
                conn.commit()
                #重新将if_del设置为0 不删除

                #跑投资匹配任务 1,3,4 成功

                #2、修改t_plan_invest智能出借投资记录为票票贷记录  注意对应t_plan_invest需要置为if_del = 1；

                #3、再次按照以下sql来执行即可；

                #4、done
                break
            else:
                autoInvester.run_invest(5)
                continue

#0.连接本地数据库
def main():
    dbDriver = MysqlDiver(db='test1',host='127.0.0.1',port=3306,user='root',password='pj123456')
    conn,cur = dbDriver.connect()
    # 待出借的订单需匹配的资产类型（1：授权3.0--匹配普通资产，2：授权3.0--匹配债转资产，3：智能2.0--匹配债转资产，4：智能2.0--匹配普通资产，5：票票贷--匹配普通资产）
    uninvest_order_type_sql = """SELECT c.id FROM `invest_app_invest` a,`invest_app_match` b,`invest_app_product` c \
                                WHERE a.`id`=b.`User_id` AND b.`Type_id`=c.`id` AND a.`invest_status`=0 GROUP BY c.id;"""
    try:
        cur.execute(uninvest_order_type_sql)
        type_result = cur.fetchall()
        print("ahaahahah:",type_result)
        type_list = []
        if(isinstance(type_result,list)):
            for type in type_result:
                # 针对type类型进行循环去执行投资逻辑任务
                if type["id"] == 1:  # 1：授权3.0--匹配普通资产
                    match_general_3_assert_invest(conn, cur)
                elif type["id"] == 2:  # 2：授权3.0--匹配债转资产
                    match_debt_3_assert_invest(conn, cur)
                elif type["id"] == 3:  # 3：智能2.0--匹配债转资产
                    match_general_2_assert_invest(conn, cur)
                elif type["id"] == 4:  # 4：智能2.0--匹配普通资产
                    match_debt_2_assert_invest(conn, cur)
                elif type["id"] == 5:  # 5：票票贷--匹配普通资产
                    match_general_PPD_assert_invest(conn, cur)
        else:
            traceback.print_exc() #打印错误日志


    except:
        traceback.print_exc()
    finally:
        conn.close()
if __name__ == '__main__':
    main()

#1.连接数据库，找到对应的出借订单


#2.查看未出借的剩余订单需要匹配什么类型资产


#3.调整数据库，调整为对应匹配模式


#4.跑投资匹配请求--普通资产满标申请银行放款--普通资产满标起息确认


#5.检查用户锁定状态，是否处于锁定状态，未锁定

#6.已锁定，更新Invests的锁定状态

#6.打印日志到后台，进行实时跟踪


