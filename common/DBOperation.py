#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import time, re
from config import readConfig






class DB:
    """
    轻量级python类连接到MySQL
    """

    _dbconfig = None
    _cursor = None
    _connect = None
    _error_code = "" # error_code from MySQLdb

    TIMEOUT_DEADLINE = 30 # 如果超过30秒，则退出连接
    TIMEOUT_THREAD = 10 # 连接的阈值
    TIMEOUT_TOTAL = 0 # 连接浪费的总时间

    def __init__(self, dbconfig):
        """
        读取数据库配置信息，并生成数据库连接及游标
        :param dbconfig:配置信息dict变量
        """
        try:
            self._dbconfig = dbconfig
            self._connect = pymysql.connect(
                                            host = self._dbconfig['host'],
                                            port = self._dbconfig['port'],
                                            user = self._dbconfig['user'],
                                            passwd = self._dbconfig['passwd'],
                                            db = self._dbconfig['db'],
                                            charset = self._dbconfig['charset'],
                                            connect_timeout = self.TIMEOUT_THREAD
                                            )
        except pymysql.Error as e:
            self._error_code = e.args[0]
            error_msg = "%s --- %s" % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), type(e).__name__), e.args[0], e.args[1]
            print (error_msg)

            if self.TIMEOUT_TOTAL < self.TIMEOUT_DEADLINE:
                interval = 0
                self.TIMEOUT_TOTAL += (interval + self.TIMEOUT_THREAD)
                time.sleep(interval)
                return self.__init__(dbconfig)
            raise Exception(error_msg)

        self._cursor = self._connect.cursor(pymysql.cursors.DictCursor)

    def select(self, sql, ret_type="all"):
        """
        查询数据库数据
        :param sql:sql语句
        :param ret_type:选择查询所有结果，查询一条数据，还是查询结果行数
        :return:输出查询结果
        """
        try:
            self._cursor.execute("SET NAMES UTF8MB4")           # 强制将它们发起的数据库链接设置成UTF8编码
            self._cursor.execute(sql)
            if ret_type == "all":
                return self.rowsarray(self._cursor.fetchall())
            elif ret_type == "one":
                return self._cursor.fetchone()
            elif ret_type == "count":
                return self._cursor.rowcount
        except pymysql.Error as e:
            self._error_code = e.args[0]
            print ("Mysql execute error:",e.args[0],e.args[1])
            return False

    def dml(self, sql):
        """
        更新、删除、插入,当执行插入语句后，返回最新插入行的主键ID；当执行更新，删除时，返回True
        :param sql:
        :return:
        """
        try:
            self._cursor.execute("SET NAMES UTF8MB4")              # 强制将它们发起的数据库链接设置成UTF8编码
            self._cursor.execute(sql)
            type = self.dml_type(sql)
            if type == "insert":
                id = self._connect.insert_id()
                self._connect.commit()
                return id
            else:
                self._connect.commit()
                return True

        except pymysql.Error as e:
            self._error_code = e.args[0]
            # print ("Mysql execute error:",e.args[0],e.args[1])
            print("Mysql execute error:", e.args[0])
            return False

    def dml_type(self, sql):
        """
        根据SQL语句，返回是delete or update or insert语句
        :param sql:
        :return:
        """
        re_dml = re.compile("^(?P<dml>\w+)\s+", re.I)
        m = re_dml.match(sql)
        if m:
            if m.group("dml").lower() == "delete":
                return "delete"
            elif m.group("dml").lower() == "update":
                return "update"
            elif m.group("dml").lower() == "insert":
                return "insert"
        print ("%s --- Warning: '%s' is not dml." % (time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), sql))
        return False

    def rowsarray(self, data):
        """
        将元组转移到数组
        :param data:
        :return:
        """
        result = []
        for da in data:
            if type(da) is not dict:
                raise Exception("Format Error: data is not a dict.")
            result.append(da)
        return result

    def __del__(self):
        '''关闭游标、关闭数据库'''
        try:
            self._cursor.close()
            self._connect.close()
        except:
            pass

    def close(self):
        self.__del__()


# if __name__ == "__main__":
#
#     # 配置信息，其中host, port, user, passwd, db为必需
#
#     dbconfig = {"host":readConfig.DB_IP,
#                 "port":readConfig.DB_PORT,
#                 "user":readConfig.DB_USER,
#                 "passwd":readConfig.DB_PASSWORD,
#                 "db":readConfig.DB_DATABASES,
#                 "charset":readConfig.DB_CHARSET}
#     db = DB(dbconfig) # 创建DB对象，若连接超时，会自动重连
#
#     # 查找(select, show)都使用select()函数
#     sql_select = """select * from  proxy_ip limit 1;"""
#     result_all = db.select(sql_select) # 返回全部数据
#     print(result_all)
#     result_count = db.select(sql_select, 'count') # 返回有多少行
#     print(result_count)
#     result_one = db.select(sql_select, 'one') # 返回一行
#     print(result_one)
#
#     # 增删改都使用dml()函数
#     sql_update = """update  zlzp_html_url set url = "http114984250" where id =1;"""
#     print( db.dml(sql_update))
#
#     sql_delete = """delete from html_content where numbering = 114984250;"""
#     print(db.dml(sql_delete))
#
#     sql_insert = """insert into html_url(numbering,url) values(123456,"http:www.bai.com");"""
#     print(db.dml(sql_insert))
#
#     db.close() # 操作结束，关闭对象

