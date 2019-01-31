# -*- coding:utf-8 -*-
import pymysql
from pymysql import cursors
import os
import configparser as cparser
#读取db_config.ini配置


class MysqlDiver():
    def __init__(self,db,host,port,user,password):
        self.base_dir = str(os.path.abspath(__file__))
        #self.base_dir = self.base_dir.replace('\\','/')
        self.dirver_dir = self.base_dir+'/my.cnf'
        #self.dirver_dir = self.dirver_dir.replace('\\','/')
        self.cf = cparser.ConfigParser()
        self.cf.read(self.dirver_dir)
        self.db = db
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):

        conn = pymysql.connect(
            host=str(self.host),
            port=3306,
            user=str(self.user),
            password=str(self.password),
            db=self.db,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        return conn,cur

# if __name__ == '__main__':
#     md = MysqlDiver()
#     print(md.dirver_dir)
#     conn,cur = md.connect()
#     sql = """SELECT tuprofile.id_no FROM \
#     pj_test1_user.`t_user` tuser LEFT JOIN \
#     pj_test1_user.`t_user_profile` tuprofile \
#     ON tuser.id=tuprofile.user_id \
#     WHERE tuser.cellphone='%s';""" % ('13715000023')
#     cur.execute(sql)
#     result = cur.fetchall()
#     print(dict(result[0]).get('id_no'))