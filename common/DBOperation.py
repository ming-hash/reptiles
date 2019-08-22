# -*- coding:utf-8 -*-
import pymysql
from config import readConfig

MYSQL_INFO ={"host": readConfig.DB_IP,
            "user": readConfig.DB_USER,
            "passwd": readConfig.DB_PASSWORD,
            "db": readConfig.DB_DATABASES
             }


class DB:
    """数据库相关操作"""

    def __init__(self):
        self.conn = DB.__Connection_db(MYSQL_INFO)  # 建立数据库连接

    @staticmethod
    def __Connection_db(MYSQL_INFO):
        """
        静态方法，从连接池中取出连接，连接数据库，并返回游标
        :param MYSQL_INFO: 数据库配置
        :return: 输出游标
        """
        # try:
        #     lists = []
        #     print("?")
        #     db1 = pymysql.connect(
        #                             host = MYSQL_INFO['host'],
        #                             user = MYSQL_INFO['user'],
        #                             passwd = MYSQL_INFO['passwd']
        #                             )
        #     print("=")
        #     cursor = db1.cursor()
        #     print("==")
        #     cursor.execute("show databases;")
        #     print("===")
        #     select_list =list(cursor.fetchall())
        #     print("====")
        #     for tuples in select_list:
        #         lists.append(tuples[0])
        #     if MYSQL_INFO["db"] in lists:
        #         db = pymysql.connect(
        #                             host = MYSQL_INFO['host'],
        #                             user = MYSQL_INFO['user'],
        #                             passwd = MYSQL_INFO['passwd'],
        #                             db= MYSQL_INFO['db']
        #                             )
        #         return db
        #     else:
        #         cursor.execute("create database "+ MYSQL_INFO["db"])
        #         db1.commit()
        #         db1.close()
        #         db = pymysql.connect(
        #                             host = MYSQL_INFO['host'],
        #                             user = MYSQL_INFO['user'],
        #                             passwd = MYSQL_INFO['passwd'],
        #                             db= MYSQL_INFO['db'],
        #                             )
        #         return db
        # except Exception as a:
        #     print("数据库连接异常：%s"%a)
        lists = []
        print(MYSQL_INFO['passwd'])
        db1 = pymysql.connect(
                                host = MYSQL_INFO['host'],
                                user = MYSQL_INFO['user'],
                                passwd = MYSQL_INFO['passwd']
                                )
        print("=")
        cursor = db1.cursor()
        print("==")
        cursor.execute("show databases;")
        print("===")
        select_list =list(cursor.fetchall())
        print("====")
        for tuples in select_list:
            lists.append(tuples[0])
        if MYSQL_INFO["db"] in lists:
            db = pymysql.connect(
                                host = MYSQL_INFO['host'],
                                user = MYSQL_INFO['user'],
                                passwd = MYSQL_INFO['passwd'],
                                db= MYSQL_INFO['db']
                                )
            return db
        else:
            cursor.execute("create database "+ MYSQL_INFO["db"])
            db1.commit()
            db1.close()
            db = pymysql.connect(
                                host = MYSQL_INFO['host'],
                                user = MYSQL_INFO['user'],
                                passwd = MYSQL_INFO['passwd'],
                                db= MYSQL_INFO['db'],
                                )
            return db

    def Select_db(self,sql):
        """查询，并获取所有行数数据"""
        try:
            cursor = self.conn.cursor()             # 创建游标
            cursor.execute(sql)
        except Exception as a:
            self.conn.rollback()                    # sql执行异常后回滚
            print("执行 SQL 语句出现异常：%s" % a)
        else:
            show_database = cursor.fetchall()
            cursor.close()                          # 关闭游标
            return list(show_database)

    def Insert_db(self,sql):
        """创建、插入、更新、删除数据"""
        try:
            cursor = self.conn.cursor()             # 创建游标
            cursor.execute(sql)
        except Exception as a:
            self.conn.rollback()                    # sql 执行异常后回滚
            print("执行 SQL 语句出现异常：%s" % a)
        else:
            self.conn.commit()                      # 提交事物，在向数据库插入(或update)一条数据时必须要有这个方法，否则数据不会被真正的插入
            cursor.close()
            return True

    def Closs_db(self):
        """关闭mysql"""
        try:
            self.conn.close()                       # 关闭数据库连接
        except Exception as a:
            print("数据库关闭时异常：%s" % a)



