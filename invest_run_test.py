"""出借订单"""
# -*- coding:utf-8 -*-
import pymysql
import traceback
import json
import requests
import MysqlDirver
import ast

def fff(dict,num,key):
    return dict[num][key]

def ddd(dict,key):
    return dict[key]

def deal_headers(hearder):
    if hearder:
        return "Bearer "+hearder
    else:
        traceback.print_exc()

class AutoInvest():

    def __init__(self):
        pass

#登陆操作
    def login(self,url,user_name,pass_word):
        print("test_log:login_url>>>>>>",url)
        login_url = url+"/pj-common/login"
        print("test_log:login_url>>>>>>",login_url)
        login_headers = {
            "Content-Type":"application/json"
        }

        login_load = {"username": user_name, "password": pass_word, "imageCode": "111111", "clientType": "WEB"}
        response = requests.post(login_url, headers=login_headers, data=json.dumps(login_load))
        try:
            if response.content:
                print("login_log>>>",response.json())
        except Exception:
            traceback.print_exc()
        finally:
            if response.status_code == 200:
                rsp = response.json()["data"]["token"]
                return rsp

#登陆成功后，出借产品
    def submitInvestOrder(self,investCount,investTotal,conn,cursor,productId,url,hearders,investAmt,planId,investStatus):
        invest_url = url+"/pj-p2p-core/pcFront/planInvest/v3.0/submitInvestOrder"
        invest_load = {"investAmt":investAmt,"couponId":"","planId":planId}
        header = deal_headers(hearders)
        invest_hearder = {
            "Content-Type":"application/json",
            "Authorization":header
        }
        print("test_log:investStatus>>>>>>",investStatus)

        if investStatus == 0:
            response = requests.post(invest_url,headers=invest_hearder,data=json.dumps(invest_load))
            if response.content:
                print("invest_log>>>",response.json())
                if response.json()["retMsg"] == "OK" and investCount == investTotal :
                    update_state = """UPDATE `invest_app_invest` SET invest_status=%d WHERE id=%d;""" % (1,productId)
                    cursor.execute(update_state)
                    conn.commit()
                    return True

                if response.json()["retMsg"] != "OK":
                    print_err_msg =  """UPDATE `invest_app_invest` SET err_msg=concat("%s",err_msg) WHERE id=%d;""" % (response.json(),productId)
                    cursor.execute(print_err_msg)
                    conn.commit()
                    return True

                if response.json()["retMsg"] == "用户名或密码错误":
                    print_err_msg = """UPDATE `invest_app_invest` SET err_msg=concat("%s",err_msg) WHERE id=%d;""" % (
                    response.json(), productId)
                    cursor.execute(print_err_msg)
                    conn.commit()
                    return True

        else:
            return 0

    def run_invest(self,type):
        request_status = False #请求脚本执行状态

        r = MysqlDirver.MysqlDiver(db='test1',host='127.0.0.1',port=3306,user='root',password='pj123456')
        conn,cursor = r.connect()
        sql1 = """SELECT a.* FROM `invest_app_invest` a,`invest_app_match` b,`invest_app_product` c  \
        WHERE a.`id`=b.`User_id` AND b.`Type_id`=c.`id` AND c.`id`=%d;""" % (type)
        cursor.execute(sql1)
        result = cursor.fetchall()
        run_invest_user_dict = {}
        for index in range(len(result)):
            hearder = self.login(url=fff(result, index, "pjb_url"), user_name=fff(result, index, "user_name"),
                                   pass_word=fff(result, index, "pass_word"))
            run_invest_user_dict["id"]=fff(result, index, "id")
            run_invest_user_dict["user_name"]=fff(result, index, "user_name")
            sql2 = """
               select * from invest_app_invest where id=%s and invest_status=%d
               """ % (fff(result,index, "id"),0)
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            print("result2",result2)
            for product in result2:
                invest_total = int(ddd(product,"invest_total"))
                for invest_num in range(invest_total):
                    print(invest_num)
                    self.submitInvestOrder(url=fff(result,index,"pjb_url"), investCount=invest_num+1,investTotal=invest_total,conn=conn, cursor=cursor, productId=int(ddd(product, "id")),
                                             hearders=hearder,
                                             investAmt=ddd(product, "invest_amount"), planId=ddd(product, "plan_id"),
                                             investStatus=ddd(product, "invest_status"))
        return run_invest_user_dict




# if __name__ == '__main__':
#
#     invester = AutoInvest()
#     invester.run_invest(1) # 出借订单





