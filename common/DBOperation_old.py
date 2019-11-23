# # -*- coding:utf-8 -*-
import pymysql
from config import readConfig
#
# MYSQL_INFO ={"ip": readConfig.DB_IP,
#             "user": readConfig.DB_USER,
#             "password": readConfig.DB_PASSWORD,
#             "databases": readConfig.DB_DATABASES,
#             "port": readConfig.DB_PORT,
#             "charset": readConfig.DB_CHARSET
#              }
#
#
# class DB:
#     """数据库相关操作"""
#
#     def __init__(self):
#         self.db_info = MYSQL_INFO
#         self.conn = DB.__Connection_db(self.db_info)  # 建立数据库连接
#
#     @staticmethod
#     def __Connection_db(db_info):
#         """
#         静态方法，从连接池中取出连接，连接数据库，并返回游标
#         :param MYSQL_INFO: 数据库配置
#         :return: 输出游标
#         """
#         try:
#             lists = []
#             db1 = pymysql.connect(
#                                     host = readConfig.DB_IP,
#                                     user = readConfig.DB_USER,
#                                     passwd = readConfig.DB_PASSWORD
#                                     )
#             cursor = db1.cursor()
#             cursor.execute("show databases;")
#             select_list =list(cursor.fetchall())
#             for tuples in select_list:
#                 lists.append(tuples[0])
#             if readConfig.DB_DATABASES in lists:
#                 conn = pymysql.connect(
#                                     host = readConfig.DB_IP,
#                                     user = readConfig.DB_USER,
#                                     passwd = readConfig.DB_PASSWORD,
#                                     db = readConfig.DB_DATABASES
#                                     )
#                 return conn
#             else:
#                 cursor.execute("create database "+ readConfig.DB_PASSWORD)
#                 db1.commit()
#                 db1.close()
#                 conn = pymysql.connect(
#                                     host = readConfig.DB_IP,
#                                     user = readConfig.DB_USER,
#                                     passwd = readConfig.DB_PASSWORD,
#                                     db = readConfig.DB_DATABASES
#                                     )
#                 return conn
#         except Exception as a:
#             print("数据库连接异常：%s"%a)
#
#
#     def Select_db(self,sql):
#         """查询，并获取所有行数数据"""
#         try:
#             cursor = self.conn.cursor()             # 创建游标
#             cursor.execute(sql)
#         except Exception as a:
#             self.conn.rollback()                    # sql执行异常后回滚
#             print("执行 SQL 语句出现异常：%s" % a)
#         else:
#             show_database = cursor.fetchall()
#             cursor.close()                          # 关闭游标
#             return list(show_database)
#
#     def Insert_db(self,sql):
#         """创建、插入、更新、删除数据"""
#         try:
#             cursor = self.conn.cursor()             # 创建游标
#             cursor.execute(sql)
#         except Exception as a:
#             self.conn.rollback()                    # sql 执行异常后回滚
#             print("执行 SQL 语句出现异常：%s" % a)
#         else:
#             self.conn.commit()                      # 提交事物，在向数据库插入(或update)一条数据时必须要有这个方法，否则数据不会被真正的插入
#             cursor.close()
#             return True
#
#     def Closs_db(self):
#         """关闭mysql"""
#         try:
#             self.conn.close()                       # 关闭数据库连接
#         except Exception as a:
#             print("数据库关闭时异常：%s" % a)
#
#

"""
说明:
1.maketable()  格式 : tablename(表名),**field(key='字段名',value='字段说明')  默认的字段类型为varchar(255)
2.insertsqlone()  格式 : tablename,**field(key='字段名',value='字段值')  **field长度不限
3.querysql()  格式 : *Choicefield(表名=列表第一个值+查询的字段。),**kwargs(条件例如 id='1314' 长度限为“1”)
4.updateone() 格式 : *kw(表名=列表第一个值+字段+字段需要更新的值),**field(查询条件 比如id='1')
5.deleteone() 格式 : tablename,**field(查询条件 比如 id=1)
"""





class DB(object):

    def __init__(self):
        self.host = readConfig.DB_IP
        self.user = readConfig.DB_USER
        self.passwd = readConfig.DB_PASSWORD
        self.db = readConfig.DB_DATABASES
        self.port = readConfig.DB_PORT
        self.charset = readConfig.DB_CHARSET
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                         passwd=self.passwd, db=self.db)
        except Exception as abnormal:
            print("数据库连接错误，错误内容%s " % abnormal)
        # 创建一个游标对象
        self.cursor = self.conn.cursor()

    def __del__(self):
        """关闭"""
        self.cursor.close()
        self.conn.close()

    def Select_db(self,sql):
        """查询，并获取所有行数数据"""
        try:
            self.cursor.execute(sql)
        except Exception as a:
            self.conn.rollback()                    # sql执行异常后回滚
            print("执行 SQL 语句出现异常：%s" % a)
        else:
            show_database = self.cursor.fetchall()
            self.cursor.close()                          # 关闭游标
            return list(show_database)

    def Insert_db(self,sql):
        """创建、插入、更新、删除数据"""
        try:
            self.cursor.execute(sql)
        except Exception as a:
            self.conn.rollback()                    # sql 执行异常后回滚
            print("执行 SQL 语句出现异常：%s" % a)
        else:
            self.conn.commit()                      # 提交事物，在向数据库插入(或update)一条数据时必须要有这个方法，否则数据不会被真正的插入
            self.cursor.close()
            return True
