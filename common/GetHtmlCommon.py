# -*- coding:utf-8 -*-
import os
import sys
import time
import json
import os
from urllib import parse  # 用来转换中文和url
import records
import pymysql

import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from myconfig import readConfig


class ReadJson:
    """读取json配置文件，获取各条件字典，输出参数列表"""

    def __init__(self):
        self.projects_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.json_path = os.path.join(self.projects_path, "myconfig", "select_condition.json")
        self.read_all = {}
        self.wuhan_area_key = []
        self.provide_salary_key = []
        self.work_year_key = []
        self.education_key = []

    def readall(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.read_all = json.load(f)
        for key in self.read_all["WuHanArea"]:
            self.wuhan_area_key.append(key)
        for key in self.read_all["ProvideSalary"]:
            self.provide_salary_key.append(key)
        for key in self.read_all["WorkYear"]:
            self.work_year_key.append(key)
        for key in self.read_all["Education"]:
            self.education_key.append(key)

    def read_wuhan_area(self, a, b=None):
        WuHanArea_all = self.read_all["WuHanArea"]
        if b == 0:
            return WuHanArea_all[a][0]
        elif b == 1:
            return WuHanArea_all[a][1]
        elif b == 2:
            return WuHanArea_all[a][2]
        else:
            return WuHanArea_all[a]

    def read_provide_salary(self, a, b=None):
        ProvideSalary_all = self.read_all["ProvideSalary"]
        if b == 0:
            return ProvideSalary_all[a][0]
        elif b == 1:
            return ProvideSalary_all[a][1]
        elif b == 2:
            return ProvideSalary_all[a][2]
        else:
            return ProvideSalary_all[a]

    def read_work_year(self, a, b=None):
        WorkYear_all = self.read_all["WorkYear"]
        if b == 0:
            return WorkYear_all[a][0]
        elif b == 1:
            return WorkYear_all[a][1]
        elif b == 2:
            return WorkYear_all[a][2]
        else:
            return WorkYear_all[a]

    def read_education(self, a, b=None):
        Education_all = self.read_all["Education"]
        if b == 0:
            return Education_all[a][0]
        elif b == 1:
            return Education_all[a][1]
        elif b == 2:
            return Education_all[a][2]
        else:
            return Education_all[a]

    def edit_keyword(self, a, b=None):
        if len(a) == 0:
            a = " "
            zlzpkeyword_url = "&kt=3"
            lgwkeyword_url = ""
        else:
            zlzpkeyword_url = "".join(["&kw=", parse.quote(a), "&kt=3"])
            lgwkeyword_url = parse.quote(a)

        # 前程无忧的中文转到url中需要经过两次编码，将%编码为%25
        qcwykeyword_url1 = parse.quote(a)
        qcwykeyword_url = parse.quote(qcwykeyword_url1)

        if b == 0:
            return qcwykeyword_url
        elif b == 1:
            return zlzpkeyword_url
        elif b == 2:
            return lgwkeyword_url
        else:
            return [qcwykeyword_url, zlzpkeyword_url, lgwkeyword_url]

    def Connect_url(self):
        """选择条件，并拼接成完整url"""

        keyword_input = input("请输入工作关键字：")

        print("请从中选择工作区域：{}".format(self.wuhan_area_key))
        WuHanArea_input = input("请输入工作区域：").strip()

        print("请从中选择薪酬范围：{}".format(self.provide_salary_key))
        ProvideSalary_input = input("请输入薪酬范围：").strip()

        print("请从中选择工作年限：{}".format(self.work_year_key))
        WorkYear_input = input("请输入工作年限：").strip()

        print("请从中选择学历要求：{}".format(self.education_key))
        Education_input = input("请输入学历要求：").strip()

        return (keyword_input, WuHanArea_input, ProvideSalary_input, WorkYear_input, Education_input)


class GatHtml:
    """
    获取三个网站的html源码
    """

    def __init__(self):
        self.qcwy_url = "https://search.51job.com"
        self.zlzp_url = "https://fe-api.zhaopin.com/c/i/sou?pageSize=1000"
        self.lgw_url = "https://www.lagou.com/"

    def Get_qcwy_html(self):
        """获取前程无忧查找工作网页的源码"""
        sessions = requests.session()
        response = sessions.get(self.qcwy_url)
        response.encoding = "gbk"
        soup_html = BeautifulSoup(response.text, "lxml")
        return soup_html

    def Get_html(self, url):
        """获取拼接后的HTML源码"""
        response = requests.get(url)
        response.encoding = "gbk"
        soup_html = BeautifulSoup(response.text, "lxml")
        return soup_html


# 未完成部分

# class Get_Cookie:
#     """获取cookie"""
#
#     def get_cookie(url):
#         browser = webdriver.Chrome()
#         browser.get(url)
#         cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]
#         cookiestr = ';'.join(item for item in cookie)
#         return cookiestr
#
#         # new_cookie_list = get_cookie(url)
#         # for cookie1 in new_cookie_list:
#         #     if "expiry" in cookie1.keys():
#         #         new_cookie_timestamp = int(cookie1["expiry"])
#         #         print(new_cookie_timestamp)
#         #         print(cookie1)


class WriteDB:
    """
    将解析的内容写入数据库
    """

    def __init__(self):
        self.times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        self.DB = records.Database(
            'mysql+pymysql://{}:{}@{}:{}/{}'.format(readConfig.DB_USER, readConfig.DB_PASSWORD, readConfig.DB_IP,
                                                    readConfig.DB_PORT, readConfig.DB_DATABASES))
        self.qcwy_table1 = readConfig.qcwy_table1
        self.qcwy_table2 = readConfig.qcwy_table2
        self.zlzp_table1 = readConfig.zlzp_table1
        self.zlzp_table2 = readConfig.zlzp_table2
        self.lgw_table1 = readConfig.lgw_table1
        self.lgw_table2 = readConfig.lgw_table2
        self.qcwy_create_table_sql1 = """
        create table `{}` (
                        `id` int unsigned auto_increment,
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `uuid` int not null,
                        `url` varchar(150) not null,
                        primary key(`id`)
                        ) DEFAULT CHARSET=UTF8MB4;""".format(self.qcwy_table1)
        self.qcwy_create_table_sql2 = """
        create table `{}` (
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `uuid` int not null,
                        `money` VARCHAR(30),
                        `welfare` VARCHAR(100),
                        `region` VARCHAR(30),
                        `workyear` VARCHAR(30),
                        `education` VARCHAR(30),
                        `hiringnumber` VARCHAR(30),
                        `releasetime` VARCHAR(30),
                        `position` VARCHAR(40),
                        `company_name` VARCHAR(40),
                        `positioninformation` VARCHAR(6000),
                        `workaddress` VARCHAR(100),
                        `companyinformation` VARCHAR(8000)
                        ) DEFAULT CHARSET=UTF8MB4;""".format(self.qcwy_table2)
        self.zlzp_create_table_sql1 = """
        create table `{}` (
                        `id` int unsigned auto_increment,
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `uuid` VARCHAR(40) not null,
                        `url` varchar(150) not null,
                        `position` VARCHAR(40),
                        `company_name` VARCHAR(40),
                        `region` VARCHAR(30),
                        `releasetime` VARCHAR(30),
                        `money` VARCHAR(30),
                        `education` VARCHAR(30),
                        `workyear` VARCHAR(30),
                        primary key(`id`)
                        ) DEFAULT CHARSET=UTF8MB4;""".format(self.zlzp_table1)
        self.zlzp_create_table_sql2 = """
        create table `{}` (
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `uuid` VARCHAR(40) not null,
                        `welfare` VARCHAR(100),
                        `hiringnumber` VARCHAR(30),
                        `positioninformation` VARCHAR(6000),
                        `workaddress` VARCHAR(100)
                        ) DEFAULT CHARSET=UTF8MB4;""".format(self.zlzp_table2)
        self.lgw_create_table_sql1 = """
        create table `{}` (
                        `id` int unsigned auto_increment,
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `uuid` VARCHAR(40) not null,
                        `url` varchar(150) not null,
                        `position` VARCHAR(40),
                        `company_name` VARCHAR(40),
                        `region` VARCHAR(30),
                        `releasetime` VARCHAR(30),
                        `money` VARCHAR(30),
                        `education` VARCHAR(30),
                        `workyear` VARCHAR(30),
                        primary key(`id`)
                        ) DEFAULT CHARSET=UTF8MB4;""".format(self.lgw_table1)
        self.lgw_create_table_sql2 = """
        create table `{}` (
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `uuid` VARCHAR(40) not null,
                        `welfare` VARCHAR(100),
                        `hiringnumber` VARCHAR(30),
                        `positioninformation` VARCHAR(6000),
                        `workaddress` VARCHAR(100)
                        ) DEFAULT CHARSET=UTF8MB4;""".format(self.lgw_table2)

    def check_tables(self):
        """
        检查前程无忧、智联招聘、拉勾网的存储表是否存在，不存在则创建相应表
        :return: 运行完成后，返回true
        """
        tables = self.DB.query("show tables;")
        show_tables_list = [table["Tables_in_testdb"] for table in tables.all(as_dict=True)]
        if self.qcwy_table1 not in show_tables_list:
            self.DB.query(self.qcwy_create_table_sql1)
        if self.qcwy_table2 not in show_tables_list:
            self.DB.query(self.qcwy_create_table_sql2)

        if self.zlzp_table1 not in show_tables_list:
            self.DB.query(self.zlzp_create_table_sql1)
        if self.zlzp_table2 not in show_tables_list:
            self.DB.query(self.zlzp_create_table_sql2)

        if self.lgw_table1 not in show_tables_list:
            self.DB.query(self.lgw_create_table_sql1)
        if self.lgw_table2 not in show_tables_list:
            self.DB.query(self.lgw_create_table_sql2)
        return True

    def delete_tables(self):
        """删除所有表"""
        for table in [self.qcwy_table1, self.qcwy_table2, self.zlzp_table1, self.zlzp_table2, self.lgw_table1,
                      self.lgw_table2]:
            self.DB.query("""drop table {};""".format(table))

    def qcwy_insert_html_url_table(self, id_url_dict):
        """写入前程无忧爬取的数据到数据库,将每条招聘的id、url存入htmlurl表中"""
        # 插入time,id,url数据，数据库中有则更新
        select_html_url_sql = """select uuid from {};""".format(self.qcwy_table1)
        uuid_list = [i["uuid"] for i in self.DB.query(select_html_url_sql).all(as_dict=True)]
        for key, value in id_url_dict.items():
            if int(key) in uuid_list:
                update_html_url_sql = """update {} set times = "{}",url = "{}" where uuid = "{}";""".format(
                    self.qcwy_table1, self.times, value, key)
                self.DB.query(update_html_url_sql)
            else:
                insert_html_url_sql = """insert into {}(times,uuid,url) values("{}","{}","{}");""".format(
                    self.qcwy_table1, self.times, key, value)
                self.DB.query(insert_html_url_sql)

    def qcwy_insert_html_content_table(self, rown_dicts):
        """将每条招聘的具体解析内容存入表中"""
        # 插入time,id等数据，数据库中有则更新
        select_html_content_sql = """select uuid from {};""".format(self.qcwy_table2)
        uuid_list = [i["uuid"] for i in self.DB.query(select_html_content_sql).all(as_dict=True)]
        for key, value in rown_dicts.items():
            if int(key) in uuid_list:
                print("正在更新代号为 {} 的数据".format(key))
                update_html_content_sql = """
                            update {} set times = "{}",money = "{}",welfare = "{}",region = "{}",workyear = "{}",education = "{}",hiringnumber = "{}",releasetime = "{}",position = "{}",company_name = "{}",positioninformation = "{}",workaddress = "{}",companyinformation = "{}" where uuid = "{}";""".format(
                    self.qcwy_table2, self.times, value[0], value[1], value[2], value[3], value[4], value[5], value[6],
                    value[7], value[8], value[9], value[10], pymysql.escape_string(value[11]), key)
                self.DB.query(update_html_content_sql)
            else:
                print("正在写入代号为 {} 的数据".format(key))
                insert_html_content_sql = """
                            insert into {}(times,uuid,money,welfare,region,workyear,education,hiringnumber,releasetime,position,company_name,positioninformation,workaddress,companyinformation) values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");""".format(
                    self.qcwy_table2, self.times, key, value[0], value[1], value[2], value[3], value[4], value[5],
                    value[6], value[7], value[8], value[9], value[10], pymysql.escape_string(value[11]))
                self.DB.query(insert_html_content_sql)

    def zlzp_insert_html_url_table(self, id_url_dict):
        """将每条招聘的id、url存入htmlurl表中"""
        """写入智联招聘爬取的数据到数据库"""
        # 插入time,id,url数据，数据库中有则更新
        for id_url in id_url_list:
            if id_url["id"] in db.Select_db("""select numbering from zlzp_html_url;"""):
                db.Insert_table(
                    """update zlzp_html_url set times = "%s",url = "%s",position = "%s",company_name = "%s",region = "%s",releasetime = "%s",money = "%s",education = "%s",workyear = "%s" where numbering = "%s";""" % (
                        times, id_url["id_url"], id_url["position"], id_url["company_name"], id_url["region"],
                        id_url["releasetime"], id_url["money"], id_url["education"], id_url["workyear"], id_url["id"]))
            else:
                db.Insert_table("""insert into zlzp_html_url(times,numbering,url,position,company_name,region,releasetime,money,education,workyear) 
                values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");""" % (times,
                                                                                 id_url["id"],
                                                                                 id_url["id_url"],
                                                                                 id_url["position"],
                                                                                 id_url["company_name"],
                                                                                 id_url["region"],
                                                                                 id_url["releasetime"],
                                                                                 id_url["money"],
                                                                                 id_url["education"],
                                                                                 id_url["workyear"]))

    def zlzp_insert_html_content_table(self, rown_dicts):
        """将每条招聘的具体解析内容存入表中"""
        """写入智联招聘爬取的数据到数据库"""

        # 插入time,id等数据，数据库中有则更新
        for key, value in rown_dicts.items():
            if key in db.Select_db("""select numbering from zlzp_html_content;"""):
                print("正在更新代号为 {} 的数据".format(key))
                db.Insert_table(
                    """update zlzp_html_content set times = "%s",welfare = "%s",hiringnumber = "%s",positioninformation = "%s",workaddress = "%s" where numbering = "%s";""" % (
                        times, value[0], value[1], value[2], value[3], key))
            else:
                print("正在写入代号为 {} 的数据".format(key))
                db.Insert_table("""insert into zlzp_html_content(times,numbering,welfare,hiringnumber,positioninformation,workaddress)
                      values("{0}","{1}","{2}","{3}","{4}","{5}");""".format(
                    times, key, value[0], value[1], value[2], value[3]))

    def lgw_insert_html_url_table(self, id_url_dict):
        """将每条招聘的id、url存入htmlurl表中"""
        """写入拉勾网爬取的数据到数据库"""
        # 插入time,id,url数据，数据库中有则更新
        for id_url in id_url_list:
            if id_url["id"] in db.Select_db("""select numbering from zlzp_html_url;"""):
                db.Insert_table(
                    """update zlzp_html_url set times = "%s",url = "%s",position = "%s",company_name = "%s",region = "%s",releasetime = "%s",money = "%s",education = "%s",workyear = "%s" where numbering = "%s";""" % (
                        times, id_url["id_url"], id_url["position"], id_url["company_name"], id_url["region"],
                        id_url["releasetime"], id_url["money"], id_url["education"], id_url["workyear"], id_url["id"]))
            else:
                db.Insert_table("""insert into zlzp_html_url(times,numbering,url,position,company_name,region,releasetime,money,education,workyear)
                values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");""" % (times,
                                                                                 id_url["id"],
                                                                                 id_url["id_url"],
                                                                                 id_url["position"],
                                                                                 id_url["company_name"],
                                                                                 id_url["region"],
                                                                                 id_url["releasetime"],
                                                                                 id_url["money"],
                                                                                 id_url["education"],
                                                                                 id_url["workyear"]))

    def lgw_insert_html_content_table(self, rown_dicts):
        """将每条招聘的具体解析内容存入表中"""
        """写入拉勾网爬取的数据到数据库"""
        # 插入time,id等数据，数据库中有则更新
        for key, value in rown_dicts.items():
            if key in db.Select_db("""select numbering from zlzp_html_content;"""):
                print("正在更新代号为 {} 的数据".format(key))
                db.Insert_table(
                    """update zlzp_html_content set times = "%s",welfare = "%s",hiringnumber = "%s",positioninformation = "%s",workaddress = "%s" where numbering = "%s";""" % (
                        times, value[0], value[1], value[2], value[3], key))
            else:
                print("正在写入代号为 {} 的数据".format(key))
                db.Insert_table("""insert into zlzp_html_content(times,numbering,welfare,hiringnumber,positioninformation,workaddress)
                      values("{0}","{1}","{2}","{3}","{4}","{5}");""".format(
                    times, key, value[0], value[1], value[2], value[3]))

    def Close_db(self):
        self.DB.close()


if __name__ == "__main__":
    db = WriteDB()
    db.check_tables()
    qcwy_id_url_dict = {
        '100911781': 'https://jobs.51job.com/wuhan-jxq/100911781.html?s=01&t=0',
        '116935497': 'https://jobs.51job.com/wuhan/116935497.html?s=01&t=0',
        '118866038': 'https://jobs.51job.com/wuhan-hsq/118866038.html?s=01&t=0',
        '106162515': 'https://jobs.51job.com/wuhan/106162515.html?s=01&t=0',
        '114613922': 'https://jobs.51job.com/wuhan-hsq/114613922.html?s=01&t=0',
        '115029874': 'https://jobs.51job.com/wuhan-hyq/115029874.html?s=01&t=0',
        '116773773': 'https://jobs.51job.com/wuhan-dhxjs/116773773.html?s=01&t=0',
        '86002907': 'https://jobs.51job.com/wuhan/86002907.html?s=01&t=0',
        '119046863': 'https://jobs.51job.com/wuhan-hsq/119046863.html?s=01&t=0',
        '116990989': 'https://jobs.51job.com/wuhan-jhq/116990989.html?s=01&t=0',
        '112814900': 'https://jobs.51job.com/wuhan/112814900.html?s=01&t=0',
        '112739050': 'https://jobs.51job.com/wuhan-dhxjs/112739050.html?s=01&t=0',
        '113768149': 'https://jobs.51job.com/wuhan/113768149.html?s=01&t=0',
        '114247753': 'https://jobs.51job.com/wuhan-hsq/114247753.html?s=01&t=0',
        '109948900': 'https://jobs.51job.com/wuhan-hsq/109948900.html?s=01&t=0',
        '118288804': 'https://jobs.51job.com/wuhan/118288804.html?s=01&t=0',
        '107600815': 'https://jobs.51job.com/wuhan-hsq/107600815.html?s=01&t=0',
        '119044700': 'https://jobs.51job.com/wuhan-wcq/119044700.html?s=01&t=0',
        '111398581': 'https://jobs.51job.com/wuhan-hsq/111398581.html?s=01&t=0',
        '117060548': 'https://jobs.51job.com/wuhan-dhxjs/117060548.html?s=01&t=0',
        '115605279': 'https://jobs.51job.com/wuhan-dhxjs/115605279.html?s=01&t=0',
        '113668853': 'https://jobs.51job.com/wuhan/113668853.html?s=01&t=0',
        '118746917': 'https://jobs.51job.com/wuhan-hsq/118746917.html?s=01&t=0',
        '117247880': 'https://jobs.51job.com/wuhan/117247880.html?s=01&t=0',
        '114608231': 'https://jobs.51job.com/wuhan-jxq/114608231.html?s=01&t=0',
        '118885784': 'https://jobs.51job.com/shenzhen-nsq/118885784.html?s=01&t=0',
        '106619673': 'https://jobs.51job.com/wuhan/106619673.html?s=01&t=0',
        '92210147': 'https://jobs.51job.com/wuhan-hsq/92210147.html?s=01&t=0',
        '116973099': 'https://jobs.51job.com/wuhan/116973099.html?s=01&t=0',
        '117100199': 'https://jobs.51job.com/wuhan-hsq/117100199.html?s=01&t=0',
        '109429357': 'https://jobs.51job.com/wuhan/109429357.html?s=01&t=0',
        '114863528': 'https://jobs.51job.com/wuhan/114863528.html?s=01&t=0',
        '116927216': 'https://jobs.51job.com/wuhan/116927216.html?s=01&t=0',
        '114542733': 'https://jobs.51job.com/wuhan/114542733.html?s=01&t=0',
        '115784264': 'https://jobs.51job.com/wuhan/115784264.html?s=01&t=0',
        '110061445': 'https://jobs.51job.com/wuhan-qkq/110061445.html?s=01&t=0',
        '118919135': 'https://jobs.51job.com/wuhan/118919135.html?s=01&t=0',
        '117292478': 'https://jobs.51job.com/wuhan/117292478.html?s=01&t=0',
        '116650171': 'https://jobs.51job.com/wuhan/116650171.html?s=01&t=0',
        '116644534': 'https://jobs.51job.com/wuhan/116644534.html?s=01&t=0',
        '116467100': 'https://jobs.51job.com/wuhan/116467100.html?s=01&t=0',
        '115821791': 'https://jobs.51job.com/wuhan-jaq/115821791.html?s=01&t=0',
        '117849157': 'https://jobs.51job.com/wuhan-hsq/117849157.html?s=01&t=0',
        '111462661': 'https://jobs.51job.com/wuhan/111462661.html?s=01&t=0',
        '110629762': 'https://jobs.51job.com/wuhan-jxq/110629762.html?s=01&t=0',
        '116529612': 'https://jobs.51job.com/wuhan-hsq/116529612.html?s=01&t=0',
        '111883832': 'https://jobs.51job.com/wuhan-hsq/111883832.html?s=01&t=0',
        '119035668': 'https://jobs.51job.com/wuhan/119035668.html?s=01&t=0',
        '116418678': 'https://jobs.51job.com/wuhan-jhq/116418678.html?s=01&t=0',
        '118250096': 'https://jobs.51job.com/wuhan-jxq/118250096.html?s=01&t=0',
        '118904543': 'https://jobs.51job.com/wuhan-dhxjs/118904543.html?s=01&t=0',
        '103118891': 'https://jobs.51job.com/suzhou-gxq/103118891.html?s=01&t=0',
        '115549137': 'https://jobs.51job.com/wuhan/115549137.html?s=01&t=0',
        '116535741': 'https://jobs.51job.com/wuhan-hsq/116535741.html?s=01&t=0',
        '117782126': 'https://jobs.51job.com/wuhan/117782126.html?s=01&t=0',
        '118458453': 'https://jobs.51job.com/guilin/118458453.html?s=01&t=0',
        '116865207': 'https://jobs.51job.com/wuhan-jxq/116865207.html?s=01&t=0',
        '112492792': 'https://jobs.51job.com/wuhan-jxq/112492792.html?s=01&t=0',
        '116336958': 'https://jobs.51job.com/wuhan/116336958.html?s=01&t=0',
        '78817674': 'https://jobs.51job.com/wuhan-hsq/78817674.html?s=01&t=0',
        '116064076': 'https://jobs.51job.com/wuhan-hsq/116064076.html?s=01&t=0',
        '109397800': 'https://jobs.51job.com/wuhan-jxq/109397800.html?s=01&t=0',
        '118969247': 'https://jobs.51job.com/wuhan-hsq/118969247.html?s=01&t=0',
        '62584854': 'https://jobs.51job.com/wuhan-dhxjs/62584854.html?s=01&t=0',
        '103064461': 'https://jobs.51job.com/wuhan/103064461.html?s=01&t=0',
        '117357789': 'https://jobs.51job.com/wuhan/117357789.html?s=01&t=0',
        '117255710': 'https://jobs.51job.com/wuhan-hsq/117255710.html?s=01&t=0',
        '118565607': 'https://jobs.51job.com/wuhan-dhxjs/118565607.html?s=01&t=0',
        '114915028': 'https://jobs.51job.com/wuhan-dhxjs/114915028.html?s=01&t=0',
        '116565043': 'https://jobs.51job.com/wuhan/116565043.html?s=01&t=0',
        '100706538': 'https://jobs.51job.com/wuhan/100706538.html?s=01&t=0',
        '79714827': 'https://jobs.51job.com/wuhan/79714827.html?s=01&t=0',
        '107160175': 'https://jobs.51job.com/wuhan-hsq/107160175.html?s=01&t=0',
        '88188442': 'https://jobs.51job.com/wuhan/88188442.html?s=01&t=0',
        '85855805': 'https://jobs.51job.com/wuhan-hsq/85855805.html?s=01&t=0',
        '84204448': 'https://jobs.51job.com/wuhan-hsq/84204448.html?s=01&t=0',
        '98466633': 'https://jobs.51job.com/wuhan-jxq/98466633.html?s=01&t=0',
        '118192576': 'https://jobs.51job.com/wuhan-hsq/118192576.html?s=01&t=0',
        '112873490': 'https://jobs.51job.com/wuhan/112873490.html?s=01&t=0',
        '116050651': 'https://jobs.51job.com/wuhan/116050651.html?s=01&t=0',
        '111009216': 'https://jobs.51job.com/wuhan/111009216.html?s=01&t=0',
        '110284101': 'https://jobs.51job.com/wuhan/110284101.html?s=01&t=0',
        '118358324': 'https://jobs.51job.com/wuhan-whjj/118358324.html?s=01&t=0',
        '115439380': 'https://jobs.51job.com/wuhan-hpq/115439380.html?s=01&t=0',
        '118129292': 'https://jobs.51job.com/wuhan-wcq/118129292.html?s=01&t=0',
        '114574719': 'https://jobs.51job.com/wuhan-hsq/114574719.html?s=01&t=0',
        '45021829': 'https://jobs.51job.com/wuhan-jhq/45021829.html?s=01&t=0',
        '116235388': 'https://jobs.51job.com/guangzhou/116235388.html?s=01&t=0',
        '118481203': 'https://jobs.51job.com/wuhan-wcq/118481203.html?s=01&t=0',
        '84733450': 'https://jobs.51job.com/wuhan-jxq/84733450.html?s=01&t=0',
        '116639044': 'https://jobs.51job.com/wuhan-wcq/116639044.html?s=01&t=0',
        '118480910': 'https://jobs.51job.com/wuhan-wcq/118480910.html?s=01&t=0',
        '112008229': 'https://jobs.51job.com/wuhan-dhxjs/112008229.html?s=01&t=0',
        '117426579': 'https://jobs.51job.com/wuhan/117426579.html?s=01&t=0',
        '116159883': 'https://jobs.51job.com/wuhan-hsq/116159883.html?s=01&t=0',
        '110663775': 'https://jobs.51job.com/wuhan/110663775.html?s=01&t=0',
        '82424003': 'https://jobs.51job.com/wuhan-jxq/82424003.html?s=01&t=0',
        '118367289': 'https://jobs.51job.com/wuhan-dhxjs/118367289.html?s=01&t=0',
        '118140323': 'https://jobs.51job.com/wuhan-dxhq/118140323.html?s=01&t=0',
        '111084404': 'https://jobs.51job.com/wuhan/111084404.html?s=01&t=0',
        '83106848': 'https://jobs.51job.com/wuhan-hsq/83106848.html?s=01&t=0',
        '95924091': 'https://jobs.51job.com/wuhan/95924091.html?s=01&t=0',
        '115633857': 'https://jobs.51job.com/wuhan/115633857.html?s=01&t=0',
        '116271296': 'https://jobs.51job.com/wuhan/116271296.html?s=01&t=0',
        '109556147': 'https://jobs.51job.com/wuhan-qkq/109556147.html?s=01&t=0',
        '116884763': 'https://jobs.51job.com/wuhan/116884763.html?s=01&t=0',
        '110010833': 'https://jobs.51job.com/wuhan-dhxjs/110010833.html?s=01&t=0',
        '104659950': 'https://jobs.51job.com/wuhan/104659950.html?s=01&t=0',
        '85435329': 'https://jobs.51job.com/wuhan/85435329.html?s=01&t=0',
        '85549528': 'https://jobs.51job.com/wuhan/85549528.html?s=01&t=0',
        '118904295': 'https://jobs.51job.com/wuhan-dhxjs/118904295.html?s=01&t=0',
        '118904135': 'https://jobs.51job.com/wuhan-dhxjs/118904135.html?s=01&t=0',
        '118877518': 'https://jobs.51job.com/wuhan-dhxjs/118877518.html?s=01&t=0',
        '118877249': 'https://jobs.51job.com/wuhan-dhxjs/118877249.html?s=01&t=0',
        '118294805': 'https://jobs.51job.com/wuhan/118294805.html?s=01&t=0',
        '107816950': 'https://jobs.51job.com/wuhan/107816950.html?s=01&t=0',
        '116519192': 'https://jobs.51job.com/wuhan-dhxjs/116519192.html?s=01&t=0',
        '115698060': 'https://jobs.51job.com/wuhan-hsq/115698060.html?s=01&t=0',
        '100640736': 'https://jobs.51job.com/wuhan-jxq/100640736.html?s=01&t=0',
        '111219215': 'https://jobs.51job.com/wuhan-jxq/111219215.html?s=01&t=0',
        '110603544': 'https://jobs.51job.com/wuhan-jxq/110603544.html?s=01&t=0',
        '102356421': 'https://jobs.51job.com/wuhan/102356421.html?s=01&t=0',
        '114465453': 'https://jobs.51job.com/wuhan-dhxjs/114465453.html?s=01&t=0',
        '113512376': 'https://jobs.51job.com/wuhan-hsq/113512376.html?s=01&t=0',
        '115604874': 'https://jobs.51job.com/wuhan-dhxjs/115604874.html?s=01&t=0',
        '118192225': 'https://jobs.51job.com/wuhan-hsq/118192225.html?s=01&t=0',
        '118887378': 'https://jobs.51job.com/shenzhen-nsq/118887378.html?s=01&t=0',
        '118356639': 'https://jobs.51job.com/wuhan/118356639.html?s=01&t=0',
        '118356607': 'https://jobs.51job.com/wuhan/118356607.html?s=01&t=0',
        '118356510': 'https://jobs.51job.com/wuhan/118356510.html?s=01&t=0',
        '106619895': 'https://jobs.51job.com/wuhan-jxq/106619895.html?s=01&t=0',
        '116139231': 'https://jobs.51job.com/wuhan-dhxjs/116139231.html?s=01&t=0',
        '117259291': 'https://jobs.51job.com/wuhan-hsq/117259291.html?s=01&t=0',
        '116780939': 'https://jobs.51job.com/wuhan/116780939.html?s=01&t=0',
        '118207652': 'https://jobs.51job.com/wuhan-dhxjs/118207652.html?s=01&t=0',
        '115784314': 'https://jobs.51job.com/wuhan/115784314.html?s=01&t=0'}
    qcwy_rown_dicts = {
        '100911781': ['', '五险一金|补充医疗保险|免费班车|员工旅游|专业培训|绩效奖金|年终奖金|定期体检|', '武汉-江夏区', '1年经验', '大专', '招若干人', '12-09发布',
                      '测试工程师', '“前程无忧”51job.com（光谷）',
                      '\n\n岗位职责：\n1、参与产品开发和需求讨论，制订测试计划，并与团队成员沟通确保测试能顺利执行并完成；\n2、根据产品设计、需求文档等，自行设计和编写测试用例；\n3、自行搭建产品测试环境，并完成相关的测试，对测试实施过程中发现的问题进行跟踪分析和反馈，完整地记录测试结果，编写完整的测试报告等相关的技术文档；\n4、组织产品的测试实施工作，保障测试的进展和完成，及时沟通解决重大测试问题，确保测试目标的达成；\n5、总结测试过程中发现的问题，做好记录、及时反馈，并提出书面分析和改善对策报告。\n\n任职要求：\n1、1年以上产品测试经验；\n2、了解并使用相关测试工具，熟悉测试计划、测试用例、测试方案、bug跟踪及测试报告的实施；\n3、具备良好的逻辑分析能力，能根据业务需求及项目文档快速理解业务及需求；\n4、具备良好沟通、学习能力，有团队合作精神，工作责任心强。\n\n职能类别：软件测试系统测试\n关键字：测试软件测试\n',
                      '上班地址：光谷金融港B12栋前程无忧大楼',
                      '“前程无忧”(NASDAQ: JOBS) 是中国具有广泛影响力的人力资源服务供应商，在美国上市的中国人力资源服务企业。它运用了网络媒体及先进的移动端信息技术，加上经验丰富的专业顾问队伍，提供包括招聘猎头、培训测评和人事外包在内的全方位专业人力资源服务，现在全国25个城市设有服务机构，是国内领先的专业人力资源服务机构。51job (Nasdaq: JOBS) is a leading provider of integrated human resource services in China. Founded in 1998, 51job meets the needs of enterprises and job seekers through the entire talent management cycle, from initial recruitment to employee retention and career development. 51job’s online recruitment platforms, as well as mobile applications, connect millions of people with employment opportunities every day. 51job also provides a number of other value-added HR services, including business process outsourcing, training, professional assessment, executive search and compensation analysis. Leveraging technology and expertise with a large staff of experienced professionals, 51job serves hundreds of thousands of domestic and multinational corporate clients through 25 offices in Mainland China. In September 2004, 51job successfully completed its IPO on Nasdaq, and is the first publicly listed firm in the field of HR services in China.'],
        '116935497': ['', '', '武汉-江夏区', '无工作经验', '本科', '招若干人', '12-09发布', 'RD43 软件测试工程师（武汉） (职位编号：RD43)',
                      '深圳迈瑞生物医疗电子股份有限公司',
                      '此岗位仅面向武汉地区高校\n岗位职责：1、负责对产品进行软件测试，把关质量；2、理解软件需求、设计实现、临床使用并指导进行测试方案、用例的设计，测试执行，测试报告；3、负责缺陷的报告、过程跟踪、回归，对各类测试数据进行分析、统计和总结；4、参与产品的专项测试（包括但不限于灰盒测试、性能测试、自动化测试等）、测试工具的制定等相关工作。\n\n岗位要求：1、本科及以上学历，计算机，通信，信息技术，生物医学工程等相关专业；2、了解以下领域中的一种或几种知识：网络、数据库、操作系统、医用协议、IT、信息安全等；3、熟悉常用的软件测试理论和方法，掌握并能够指导实际应用；4、能看懂代码，并具备基本编程能力以完成相关测试实施、工具开发、脚本实现等。\n职能类别：医疗器械研发\n',
                      '职能类别：医疗器械研发',
                      '迈瑞总部位于深圳，为全球市场提供医疗器械产品。在中国超过 30 个省市自治区设有分公司，境外拥有 40 家子公司。全球员工近万人，其中研发人员占比超过 20%，外籍员工超过 12%，来自全球 30 多个国家及地区，形成了庞大的全球研发、营销和服务网络。迈瑞的主营业务覆盖生命信息与支持、体外诊断、医学影像三大领域，通过前沿技术创新，提供更完善的产品解决方案，帮助世界改善医疗条件、提高诊疗效率。'],
        '118866038': ['1.1-1.5万/月', '五险一金|餐饮补贴|专业培训|年终奖金|弹性工作|带薪年休假|调薪灵活|发展空间大|试用期全薪|', '武汉-洪山区', '3-4年经验', '本科',
                      '招若干人', '12-09发布', '嵌入式软件测试工程师', '东莞正扬电子机械有限公司武汉研发中心',
                      '负责武汉研发中心嵌入式软件的单元测试、集成测试以及系统测试，与硬件工程师、嵌入式软件工程师、视觉和机器学习算法工程师协同完成系统测试与调试工作。主要包括：\n1、编写测试方案、测试计划、测试用例，并搭建和维护测试软硬件环境；\n2、完成嵌入式软件的单元测试、集成测试以及系统测试；\n3、有效地执行测试用例，编写测试报告；\n4、准确地定位并跟踪问题，推动问题及时合理地解决。\n任职要求：\n1、本科及以上学历，计算机，软件工程，电子，通信等专业；\n2、三年以上嵌入式软件系统测试经验、工具使用经验或自动化测试经验；\n3、了解软件工程理论以及基本测试理论和测试方法；\n4、熟悉嵌入式软件开发流程，熟悉测试计划制定和测试用例设计方法和策略；\n5、掌握Linux系统基本操作和常用脚本编程；\n6、熟悉一种脚本编程语言（Python/Shell/Perl）者优先；\n7、熟悉C/C++编程规范，有两年以上实际编程经验者优先；\n8、具有良好的沟通和自主学习能力，较强的问题分析和处理能力，富有高度的责任心及团队合作精神。\n\n职能类别：软件工程师软件测试\n关键字：单元测试集成测试系统测试C编码经验嵌入式软件\n',
                      '上班地址：光谷金融港B6栋402室',
                      '东莞正扬电子机械有限公司（品牌KUS）成立于1984年，是一家集研发、生产、销售、服务为一体全球***的汽车、游艇液位传感器、尿素传感器及仪表供应商。产品广泛应用于卡车、巴士、工程机械、农业机械、游艇和发电机组等领域，市场占有率达90%。KUS发明生产了全球***款干簧管液位传感器，荣获国家高新技术企业、东莞市“倍增”计划企业、东莞市专利优势企业等殊荣。\xa0\xa0\xa0\xa0\xa0\xa0东莞正扬武汉研发中心依托于总公司在汽车行业数十年的深厚积累及对ADAS（高级驾驶辅助系统）领域的大力投入支持，于2018年正式成立，专注于汽车ADAS领域相关技术产品的研发。现已建成涵盖硬件，软件，算法（AI），测试，品质等各个方面的完善开发团队。在这汽车行业面临新四化（电动化，网联化，智能化，共享化）的百年未有之变革之际，欢迎大家加入我们，一起顺势前行！'],
        '106162515': ['', '', '武汉-洪山区', '无工作经验', '本科', '招8人', '12-09发布', '软件测试工程师(000406)（武汉） (职位编号：000406)', '软件与服务中心',
                      '1、计算机和软件相关专业，本科及以上学历；2、熟悉软件研发及测试流程，良好的计算机理论基础；3、有强烈的工作激情，愿意从事安全测试、性能测试、自动化测试开发等白盒测试工作；；4、有良好的团队精神和强烈的工作责任心；5、致力于投身软件行业\n职能类别：软件工程师软件工程师\n',
                      '职能类别：软件工程师软件工程师', '软件与服务中心诚聘'],
        '114613922': ['1-1.5万/月', '弹性工作|五险一金|高温补贴|带薪年假|餐饮补贴|加班补贴|绩效奖金|定期体检|5A级办公区|公司氛围好|', '武汉-洪山区', '3-4年经验', '大专',
                      '招1人', '12-09发布', '软件测试工程师', '东方网力科技股份有限公司',
                      '岗位职责：\n参与项目的需求分析，从测试角提供交互优化建议；\n制定测试计划，编写测试用例和测试报告，跟踪需求和bug；\n负责测试技术预研，搭建和维护自动化测试框架；\n进行功能和性能测试；\n岗位要求：\n1、计算机相关专业；\n2、3年及以上工作经验，有大型互联网产品测试经验，有微服务架构系统测试经验优先，有AI相关测试经验优先；\n3、熟练使用JAVA/PYTHON或其他脚本语言；\n4、熟悉linux常用命令，熟悉Postgresql数据库，有性能测试经验优先；\n5、工作细心，耐心，有责任心，有较强的沟通能力和团队协作精神，抗压能力强，富有激情，能快速融入到快节奏的工作环境。\n职能类别：软件工程师\n',
                      '上班地址：关山大道保利国际中心15楼',
                      '东方网力（NetPosa，SZSE: 300367）是全球视频监控管理平台的领导厂商，致力于在安防人工智能时代，成为安防AI平台和AI智能前端的引领者，为世界构建Video+IoT+AI的公共安全视界。东方网力成立于2000年9月，于2014年1月29日在深圳证券交易所创业板上市。得益于客户的支持，已成为中国***、全球第三的视频监控管理平台领导品牌。在人工智能时代，基于对行业技术发展趋势"云化大数据、软硬一体化、深度人工智能"的理解，在全球范围内加大了深度学习、视频结构化、AI智能摄像机方面的研发和产业化投入，重点强化公司AI硬件能力建设，联合跨行业领导厂商和投资基金成立万象人工智能研究院，期待在下一个十年，成为全球人工智能领域的领导厂商。企业使命：构建公共安全视界企业愿景：全球最具竞争力的视频监控平台供应商；安防人工智能平台的引领者公司地址：北京市朝阳区望京阜通东大街1号望京soho二号塔c座26层简历邮箱：zhaopin@netposa.com'],
        '115029874': ['1-2万/月', '五险一金|员工旅游|餐饮补贴|绩效奖金|年终奖金|定期体检|', '武汉-汉阳区', '8-9年经验', '本科', '招若干人', '12-09发布', '软件测试经理',
                      '上海派拉软件股份有限公司',
                      '\n岗位职责：\n1、根据软件需求设计测试用例、测试方案；\n2、有效地执行测试用例，编写测试报告及测试相关文档；\n3、能够根据项目要求，独立搭建测试环境；\n4、准确地定位并跟踪问题，推动问题及时合理地解决；\n5、完成对项目的软件功能、性能及安全方面的测试。\n\n岗位要求：\n1、计算机相关专业，本科以上学历，8年及以上软件测试经验，有5年以上测试团队管理经验；\n2、具有建立软件测试和质量管理体系的成功经验；具有监控开发团队和产品团队上线产品质量的成功经验优先；\n3、具备性能测试需求分析、设计规划能力和分析性能测试数据的能力；\n4、具有搭建测试环境，自动化测试框架及编写相关测试脚本的能力；\n5、熟悉功能测试、性能测试、黑盒以及白盒测试方法；\n6、熟练使用linux/Aix操作系统、熟悉常用的网络协议和网络的基本知识、能使用抓包工具分析抓包数据；熟悉常用编程语言如JAVA、JS、html5、python、Shell等\n7、学习能力强、善于思考总结、工作认真、责任心强、能承担压力。\n\n【关于我们】\n1、丰厚奖金+各种补贴+弹性工作+五险一金+法定假期+商业保险+员工体检\n2、员工集体旅游/团建+优秀员工个人/家庭出国游+优秀达人出游+各种有的没的你想到的想不到的福利\n3、每年1-2次调薪+代码大神专业技能手把手培训+优秀人才股权激励+宽广的晋升空间\n4、读书会+马拉松+达人旅行团是我们的日常传统，CEO带着你一起冲刺马拉松。。。\n5、生日会+周年庆+丰富多彩的部门团建。\n\nPS：\n1、对，我们不打卡！不打卡！！不打卡！！！\n2、有且不仅有以上福利，而且是真的真的真的有~~~\n3、加入我们，每天与***大神面对面，我们的团队都是大神，真的真的真的，都是都是都是~~~\n\n【了解我们】\n1、官网：http://www.paraview.cn/\n2、公众号：派拉软件\n职能类别：软件测试\n关键字：测试经理软件测试\n',
                      '上班地址：沌口经济开发区经开万达广场C6-2202',
                      '派拉软件股份有限公司（简称：派拉软件，股票代码：831194）是中国领先的身份安全服务提供商，数据定义、AI驱动、智能算法、场景分析，为企业和机构提供跨业务、跨用户的全生命周期身份数据价值创新服务，涉及统一身份管理、互联网用户管理、用户行为分析、特权身份管控、移动安全管理、SaaS应用安全管理等相关的软件产品、解决方案和咨询与实施服务，已经为汽车、制造、金融、保险、证券、零售、教育等行业的500多家大中型企业成功提供了身份安全和价值创新服务。目前，派拉软件在上海、北京、广州、长春、武汉设有服务机构。是经政府认定的高新技术企业、软件企业、企业研发机构、专精特新中小企业和上海市科技小巨人培育企业，通过了ISO9001质量体系认证和CMMI L3认证，拥有多项公安部安全产品销售许可和近30项知识产权。主要业务身份安全认证\xa0\xa0\xa0\xa0\xa0\xa0提供企业身份管理、账号管理、安全认证、单点登录、授权、审计的解决方案云计算安全\xa0\xa0\xa0\xa0\xa0\xa0提供SaaS应用的安全管理解决方案，包括身份管理、单点登录、业务数据加密移动信息化\xa0\xa0\xa0\xa0\xa0\xa0提供移动信息化解决方案，包括移动应用封装、分发、加密、单点登录等大数据\xa0\xa0\xa0\xa0\xa0\xa0提供大数据平台、大数据安全、大数据整合及相关行业解决方案等公司需要打造一支精悍的企业团队，将提供员工学习和自身能力全面提高的机会，使您与公司共同发展壮大，实现个人价值与企业发展的双重目的，达到共赢。公司对优秀人才实施股权激励制度，公司快速发展，为个人创造发展空间。【公司文化】1、强烈的工程师文化，追求IT技术的创新与专业的坚守，期待各类IT极客及代码洁癖爱好者，形成项目制管理的灵活作战单元，在项目中突破与自我实现！2、重视健康锻炼，马拉松运动是我们公司的一项传统。3、读书会是我们学习型组织的重要推动，达人团旅行也是公司评选优秀员工的专项活动。4、丰富多彩的部门团建，工作之余感受下团队生活的精彩。5、公司对优秀人才实施股权激励制度，公司快速发展，为个人创造发展空间。【公司福利】双休+五险一金+补贴+年终奖+绩效奖+带薪年假+带薪病假+国内外旅游+节日福利+团建活动+法定假日如果你心怀壮志，希望通过自己的努力创造价值，走向成功，请加入我们吧！公司名称：上海派拉软件股份有限公司公司地址：上海浦东新区张东路1388号27幢102室（地铁2号线广兰路地铁站下，步行15分钟即到）联系电话：021-58301883。公司主页：www.paravivew.cn'],
        '116773773': ['1-1.5万/月', '五险一金|餐饮补贴|通讯补贴|专业培训|定期体检|员工旅游|绩效奖金|年终奖金|交通补贴|股票期权|', '武汉-东湖新技术产业开发区', '无工作经验', '本科',
                      '招若干人', '12-09发布', '软件测试工程师（校园招聘）', '北京数字政通科技股份有限公司',
                      '岗位职责：\n\n1、从事软件产品及项目平台软件的测试工作；包括功能测试、性能测试和压力测试等；\n\n2、根据功能需求编制测试计划；\n\n3、编写测试用例并执行；\n\n4、提交Bug并跟踪Bug的处理情况；\n\n5、提交软件测试报告。\n\n岗位要求：\n\n1、熟悉至少一种常用开发语言；\n\n2、熟悉数据库原理，熟悉MySQL或Oracle数据库和存储过程；\n\n3、熟悉软件测试流程，具备良好的质量意识、逻辑思考能力强，思维缜密；\n\n3、具有较强的责任心，工作热情，做事细致耐心、踏实，善于人际沟通，团队协作能力强。\n\n职能类别：软件工程师\n',
                      '上班地址：光谷大道金融港B4栋12F',
                      '北京数字政通科技股份有限公司成立于2001年，2010年在深圳证券交易所上市（股票代码：300075），是中国领先的智慧城市应用与信息服务提供商，在数字化城市综合管理领域市场占有率超过60%，居于绝对领先的地位。公司以“创新数字城市，成就政通人和”为己任，迄今为止已经为包括北京、上海、天津、重庆、广州在内的300多个国内城市客户提供并实施了全面的数字化城市管理解决方案，在网格化城市管理、网格化社会管理、综合执法管理、综合管网管理、国土资源管理、城市规划管理、市政管理和信访管理等城市管理领域拥有广泛的客户案例。同时，为满足中国城市客户不断增长的服务需求，公司还提供二维/三维基础地理数据、实景影像数据、部件数据和人口房屋数据等城市核心应用数据的采集、普查与管理服务，及满足数字城市管理系统运行规范的专业服务外包、坐席托管等各种增值服务。\xa0\xa0\xa0\xa0\xa0\xa0\xa0公司注册资金4.2亿元，总资产14.12亿元，员工总数逾1000人，其中专业技术人员占比超过80%。公司总部位于北京，在北京和武汉设有研发中心，并在上海、武汉、天津、成都、开封、温州、宁波和威海等多个城市设有子/分公司。企业文化我们的使命\xa0对股东：以前瞻的眼光，高效的管理，稳健的发展实现股东价值最大化；\xa0对员工：以人为本，倾心为员工营造和谐向上的工作氛围，帮助员工实现个人职业发展和价值提升；\xa0对业界：以行业领先为己任，协同业界整体发展与进步；\xa0对社会：努力工作，共建和谐，创造价值，回报社会。我们的愿景\xa0成为中国领先的数字城市软件开发、运营与增值服务综合提供商，拥有丰富的自主知识产权产品，建立可持续发展的商业模式，为客户创造价值、为员工创造机会、为投资者创造财富，成为受人尊敬的企业。核心价值观\xa0创新、责任、诚信、人和发展理念技术创新推动政府管理与体制创新人才理念\xa0唯才是用，唯德重用员工是数字政通价值的缔造者，具有强烈进取心、创新力、良好沟通能力、并具有优秀团队精神的人才是企业的核心竞争力；创造公平、公正、公开的竞争环境，不拘一格降人才；重用高度认同数字政通企业理念的人才。技术理念不断创新，并在实践中沉淀并推广成熟技术，是数字政通应用研发的核心理念；把创新和经验与标准结合，使系统建设化繁杂为规范，是数字政通发展的原动力。'],
        '86002907': ['1-1.5万/月', '五险一金|年终奖金|定期体检|', '武汉-东湖新技术产业开发区', '3-4年经验', '本科', '招1人', '12-09发布', '软件测试工程师',
                     '武汉高德红外股份有限公司',
                     '职责描述：\n1、制定软件测评计划，分析软件测评需求；\n2、编制软件测评大纲、测试用例、测评报告；\n3、负责软件文档审核，C/C++C、VHDL代码静态分析、代码走查；\n4、负责DSP、FPGA、ARM平台软件测试仿真。\n任职要求：\n1、本科及本科以上学历，电子、通信、自动化等相关专业；\n2、精通C/C++、VHDL一种或多种语言编程；\n3、具备2年以上软件文档审查、嵌入式软件测试相关工作经验；\n4、熟悉Keil、CCS、Quartus开发环境，会使用ModeSim进行测试仿真；\n5、有用过C++test、Testbed、Klocwork、HDLDesigner等代码静态分析工具，熟悉代码检查规则集者优先。\n职能类别：测试工程师软件测试\n关键字：软件测评白盒黑盒测试测试工具klockworkVHDL\n',
                     '上班地址：湖北省武汉市东湖开发区黄龙山南路6号',
                     '武汉高德红外股份有限公司创立于1999年，是规模化从事红外探测器、红外热像仪、大型光电系统、防务类系统研发、生产、销售的高新技术上市公司。公司总市值超过200亿元，员工总数2300余人，其中研发团队近1000多人，营销服务网络遍布全球70多个国家和地区，并在比利时成了欧洲分公司。公司产品广泛应用于电力、冶金、石化、建筑、消防、执法、检验检疫、安防监控、车载夜视等民用领域。公司正以红外焦平面探测器产业化为契机，积极推进红外热成像产品的“消费品化”。\xa0\xa0\xa0\xa0\xa0\xa02010年公司顺利登陆深圳A股主板市场，股票代码：002414。'],
        '119046863': ['1-1.2万/月', '五险一金|周末双休|餐饮补贴|绩效奖金|年终奖金|节日福利|员工旅游|带薪年假|', '武汉-洪山区', '5-7年经验', '本科', '招1人',
                      '12-09发布', '软件测试主管', '武汉市驿宝通网络科技有限公司',
                      '1、参与研发流程改善，梳理研发管理流程及持续优化；\n2、参与产品需求分析，建立测试流程和测试规范，把控整体的产品质量；\n3、制定质量相关报告的规范，指导编写测试计划、测试用例、测试方案、测试报告等。\n4、带领质量团队完成产品测试和保证产品质量，推动开发团队提高测试能力和认识；跟踪分析问题，总结测试报告，归档测试用例，推动测试中发现缺陷并及时合理解决；\n5、带领测试团队引入或者研发自动化测试工具与性能测试工具，不断提升团队的测试效率和测试能力。\n任职要求：\n1、计算机或相关专业本科及以上学历，热爱软件测试工作；五年以上测试工作经验，3年以上团队管理经验；\n2、熟悉主流的测试技术,如UI自动化、接口自动化、性能、安全测试等，熟悉主流的测试工具，LR、JMETER、APPSCAN、SELENIUM2等\n3、熟悉软件工程，精通软件测试流程；熟悉至少一种编程语言，能够编写自动化测试脚本；\n4、熟练掌握静态代码分析、代码检查、功能确认与接口测试、全链路压力测试、覆盖率分析、性能分析、安全分析、稳定性分析、内存分析；\n5、熟悉至少两种自动化测试框架，熟练使用测试缺陷管理工具与项目管理工具；\n6、有较强的责任心，思维逻辑清晰，擅于跨团队沟通和协作。\n\n薪资福利：\n1.基本薪资+各类补贴\n2.购买五险一金\n3.周末双休，带薪年假\n4.5-15天超长年假，享受法定假期\n5.节假日、员工生日福利\n6.定期团建和员工旅游\n7.定期培训学习提升\nPs:公司文化：\n我们允许偶尔的迟到，允许办公室零食，允许谈笑风生\n我们鼓励轻松活跃的工作氛围，鼓励员工学习提升，鼓励跨部门协作沟通\n我们能给你什么：\n1.具有行业竞争力的薪酬\n2.优质的办公环境\n3.轻松随性的工作氛围\n4.人性化企业管理文化\n5.学习提升的机会和晋升空间\n职能类别：软件测试\n关键字：测试\n',
                      '上班地址：文化大道555号融创智谷A2栋201',
                      '武汉市驿宝通网络科技有限公司是一家专注于为金融行业提供一站式综合服务解决方案的提供商，深度服务于银行机构和保险公司，以云计算、移动互联网、大数据等新兴技术为支持，将行业应用深度融合，打造“电子招投标系统（SRM）、阳光惠采SaaS云平台、场景化积分商城SaaS系统、营销活动SaaS系统、O2O生活服务SaaS系统”五大核心系统，基于移动端（APP、微信）、PC端系统的技术开发及运营，同时联合线上及线下多种供应商渠道，整合全球资源，为企业提供“供应商管理、采购管理、积分商城、营销策划、微信/APP平台运营、营销礼品定制、增值服务平台“等综合服务解决方案。帮助银行和保险公司提升客户忠诚度，降低营销成本，提高客户服务效率，提升产品及服务的竞争力。\xa0\xa0\xa0\xa0目前已经与京东、苏宁易购、网易严选、齐心、晨光等大型电商平台或品牌供应商进行API对接，平台拥有商品SKU100多万个，线下商户服务网点3000多家，用户数已达到50多万。已服务中国人保、中国人寿、招商银行、中国银行、光大银行、湖北银行等金融客户30多家，业务范围覆盖湖北、湖南、北京、上海、江西、山西等省市。\xa0\xa0\xa0\xa0公司立足于湖北，以武汉为运营中心向全国发展，公司属于武汉“互联网+”重点项目，2016年被评为“新三板投融汇年度优秀企业”，2017年入选高新“瞪羚企业”。目前公司取得16项软件著作权，增值电信业务经营许可证，通过ISO9001质量管理体系认证。驿车宝为您提供：1.有竞争力的薪酬，每年享有调薪机会；2.完善的员工福利体系，购买五险一金；3.周末双休，国家法定假期，5-15天带薪年假；4.节假日、员工生日福利；5.定期团建和员工旅游；6.定期培训学习提升；7.永无止境的发展空间......公司文化：人性化管理，我们允许偶尔的迟到，允许办公室零食，允许谈笑风生；我们鼓励轻松活跃的工作氛围，鼓励员工学习提升，鼓励跨部门协作沟通......'],
        '116990989': ['1-1.5万/月', '做五休二|周末双休|弹性工作|带薪年假|五险一金|包吃|绩效奖金|节日福利|高温补贴|', '武汉-江汉区', '3-4年经验', '本科', '招2人',
                      '12-09发布', '软件测试工程师', '爱派克斯国际物流（中国）有限公司',
                      '1.负责需求分析、测试计划制定、测试用例设计、测试执行，协助项目经理保证项目质量与进度；\n2.负责公司各产品线的质量保证工作；\n3.负责测试相关平台、工具的设计与开发，提升工作效率与效果；\n4.跟踪定位产品中的缺陷或问题，与项目相关人员就项目进度和问题进行沟通。\n5.参与项目的需求和迭代开发计划的讨论和评审；\n6.制定项目的测试计划并设计测试用例；\n7.搭建测试环境、测试设计、执行及bug的定位、跟踪和管理；\n8.设计UI、接口自动化脚本或性能测试脚本，并执行自动化脚本；\n9.项目上线后，对产生线上Incident事件或技术缺陷进行case_study分析；\n10.通过总结、对外交流、技术钻研和培训，进行测试过程和测试方法的持续改进。\n职位要求\n1、本科及以上学历，计算机相关专业；\n2、具有4年以上测试或开发经验（测试经验不低于2年）；\n3、熟悉测试理论、流程与方法，熟练使用主流的功能或性能测试工具；\n4、具备一定的业务分析，沟通表达能力和综合协调能力，工作积极主动；\n5、良好的沟通能力和团队协作能力，具备高度责任感；\n6、具备强大的逻辑思辨能力，谈判能力和冲突管理能力者优先。\n7、能够基本掌握一门开发语言，java/php/.net；\n8、熟悉Oracle/SqlServer/Mysql/MongoDB等至少一种数据库管理系统，能够熟练编写SQL语句；\n职能类别：软件测试\n关键字：软件测试\n',
                      '上班地址：中央商务区soho城6栋3403',
                      '爱派克斯集团拥有一支敬业的专业物流团队以及遍布全球的代理服务网络，凭借着超越同行的勤奋精神，致力于为客户提供高质量的物流服务。公司的宗旨是“用***的热情满足客户的需求”，对工作的高度热情使得公司从同行中脱颖而出，并在业界享有盛誉。\xa0\xa0\xa0爱派克斯集团由鼎尖国际物流有限公司、无锡中旅新桥国际货运（代理）有限责任公司、环宇天马国际货运代理有限公司合并成立，专业提供综合物流解决方案。三家企业在物流和运输行业均享有很高的声誉可谓是强强联手、优势互补、资源共享。2009年国际航空运输协会（IATA）210家代理人排名中，无锡中旅和北京环宇天马均名列前茅，分别为第8名、第12名。现今，通过分布在美国、中国的15个分支机构及遍布多个国家的代理网络，爱派克斯集团可以提供给客户一个全球化的货运网络、庞大的仓储配送体系、高效的库存管理解决方案、精致的客户服务和现代化的运作能力。\xa0\xa0\xa0爱派克斯集团在上海、广州、北京和青岛等中国沿海的诸多沿海港口城市建立了分公司。这些分公司的良好运作促进了爱派集团国内公司与美国公司的成功协作和高效沟通。通过合作，鼎尖国际物流有限公司，无锡中旅新桥国际货运（代理）有限责任公司，环宇天马国际货运代理有限公司均扩大了其占有的市场份额。声明我公司在所有招聘活动中一贯坚持“公平、公开、公正”的原则。为切实保障各位应聘者的利益，维护我公司的品牌和社会形象， 声明如下：我公司主要通过前程无忧网、智联招聘网、猎聘网发布招聘信息， 未授权上述招聘渠道以外的企业单位和个人发布此类招聘信息。任何单位和个人未经我公司授权，不得以我公司名义发布招聘信息；相关网站不得刊载相关信息， 一经发现我公司将考虑通过法律途径追究其责任的权利，以保障广大求职者的权利和我公司的名誉。我公司提醒广大求职者提高警惕，通过正规渠道了解招聘信息，警惕上当受骗。特此声明\xa0爱派克斯国际物流有限公司'],
        '112814900': ['1-1.5万/月', '五险一金|餐饮补贴|绩效奖金|', '武汉-江汉区', '5-7年经验', '大专', '招10人', '12-09发布', '高级软件测试工程师-武汉-01781',
                      '京北方信息技术股份有限公司',
                      '岗位职责\n1、参与编写测试方案，制定测试计划；\n2、参与编写测试文档和测试用例；\n3、搭建项目测试环境、更新测试软件，部署测试系统。\n\n任职要求\n1.大专毕业8年及以上，本科毕业6年及以上，理工科、管理学等相关专业毕业；\n2.熟悉功能测试，了解不同产品的测试侧重点，能快速分析需求并设计测试案例；\n3.熟悉一种测试案例管理工具和缺陷管理工具的使用，了解测试集成；\n4.了解测试管理生命周期，具备测试风险控制能力；\n5.有自动化测试经验者优先（代码层面）；\n6.掌握windows、linux等主流操作系统，具备系统部署和测试环境搭建、产品发布能力。\n职能类别：软件测试\n关键字：测试银行自动化测试\n',
                      '上班地址：东湖新技术开发区楚平路99号（靠近2号线杨家湾地铁站）',
                      '京北方信息技术股份有限公司（以下简称京北方）致力于为国内外金融机构客户提供信息技术服务（ITO）及业务流程外包服务（BPO），并立志成为国内***的金融IT综合服务提供商。\xa0\xa0\xa0\xa0京北方总部位于北京，在广东、山东、江苏、黑龙江设有多个全资子公司，在超过20个中心城市设有分支机构及办事处，业务及服务中心遍布全国所有地级市。公司顺应产业变革和客户需求，坚持创新驱动发展，先后被认定为国家高新技术企业、中关村高新技术企业、信息系统集成及服务二级资质企业，并获得跨地区增值电信业务许可证，同时设有北京市企业技术中心、企业博士后工作站。\xa0\xa0\xa0\xa0京北方遵循严格的质量和安全标准，实施严密的安全措施，拥有成熟可靠的管理和开发流程，顺利通过CMMI5评估、ISO9001质量管理体系认证、ISO27001信息安全管理体系认证、ISO20000信息技术服务管理认证、ISO14001环境管理体系认证、OHSAS18001职业健康安全管理体系认证。同时，掌握多项金融IT行业核心技术，拥有自主知识产权的国家专利近20项，软件著作权80余项，具备高质量的全时、全国服务交付能力，IT信息风险管控能力及信息技术连续性服务管理能力。\xa0\xa0\xa0\xa0如今，京北方充分利用互联网、云计算、大数据、人工智能、虚拟现实等新兴技术，凭借深厚的行业背景、国内领先的技术实力及创新的思维，对银行、保险、证券、信托、基金、租赁、资产管理等金融行业客户，打造出覆盖客户渠道、业务处理、管理决策等咨询及解决方案，囊括营运管理、风险管理、合规管理、精准营销、电商平台、互联网金融等核心业务领域。基于公司成熟的外包服务体系及专业的外包团队，满足客户对业务咨询、软件开发、软件测试、应用系统运维、基础架构运维、桌面（含柜面）外包在内的多层次外包需求。京北方实时洞察客户需求，创新发展路径，帮助客户提升行业竞争力，驱动其实现商业变革和卓越业绩。\xa0\xa0\xa0\xa0服务以信息化推动进步。凭借广泛的行业经验和强大的本地化服务能力，在业务流程外包领域，京北方拥有涵盖数据处理类、业务处理类、业务营销类等一系列外包服务产品，能为客户提供驻场式、基地式、租赁式等多种外包服务。京北方在潍坊、大庆、无锡拥有独立的大型外包基地。\xa0\xa0\xa0\xa0面向未来，京北方将持续秉承“客户满意、员工支持、股东默契、价值链协同、社会认可”的企业核心价值观，坚守“合法、合规、合理”的经营准则，通过专业化与多元化的产品和服务，释放信息技术的力量，把信息技术价值转化为客户价值，助力客户尽享科技变革所带来的卓越运营，为客户持续创造价值。'],
        '112739050': ['1-1.5万/月', '五险一金|年终奖金|股票期权|弹性工作|', '武汉-东湖新技术产业开发区', '无工作经验', '本科', '招2人', '12-09发布', '软件测试工程师',
                      '武汉市聚芯微电子有限责任公司',
                      '岗位职责：\n1、根据功能需求编写测试方案、设计测试用例；\n2、完成测试相关记录，并编写测试报告；\n3、向开发人员提交测试问题、测试过程，协助开发人员调试；\n4、协助芯片测试。\n\n任职要求：\n1、计算机相关专业本科以上学历，3年以上测试工作经验；\n2、有软件开发流程概念优先；\n3、具有linux平台应用软件或驱动软件功能测试经验；\n4、有一定的故障分析能力，能针对故障，从多方面设计实验说明故障现象，协助开发人员进行调试；\n5、能根据需求设计测试用例，编写测试脚本或简单的测试代码；\n6、有手机平台软件测试经验者优先；\n7、有较强软件开发能力者优先;\n8、具备良好的沟通能力，善于发现、分析和总结问题，有强烈的责任心，能承担较大的工作压力。\n职能类别：集成电路IC设计/应用工程师\n关键字：软件测试工程师软件测试测试\n',
                      '上班地址：湖北省武汉市江夏区高新大道未来科技城C4座4楼',
                      '武汉市聚芯微电子有限责任公司坐落于武汉光谷未来科技城，是一家专注于高性能模拟混合信号集成电路设计及其应用系统研发与销售的创新型高科技公司。\xa0\xa0\xa0\xa0公司由多位在欧美拥有丰富半导体行业经验的留学归国人员创办，核心团队聚集了在企业管理、产品开发、市场销售、财务管理和生产制造等各环节拥有卓越业绩的行业精英。其中研发团队全部拥有国内外顶尖大学硕士或博士学位，在传感器芯片设计、传感器融合算法等领域拥有国际一流的技术创新能力和丰富的产业化经验。而公司的市场及销售团队则长期扎根于国内智能手机及智能硬件产业链，拥有丰富的客户资源和市场开拓经验，并在此基础上善于针对中国本土市场需求做产品定义与规划，实现国际先进技术与本土实际需求有效对接。\xa0\xa0\xa0\xa0通过不断的技术积累和创新，聚芯微电子在传感器集成电路设计领域已拥有多项自主知识产权和专利，致力于向市场提供高精度、低功耗、超低噪声且具有创新应用的传感器芯片，在智能手机、人工智能、自动驾驶等热门行业和新兴市场具有广泛的应用前景。聚芯微电子致力于打造国际一流的高性能混合电路设计公司，为智慧中国打造传感中国芯。聚集最优秀的人，挑战从芯开始的事，我们的团队创芯，走心！新的开始你愿意和我们一起走吗？'],
        '113768149': ['1-2万/月', '五险一金|免费班车|交通补贴|餐饮补贴|弹性工作|住房补贴|加班补贴|带薪年假|股票期权|15薪|', '武汉-东湖新技术产业开发区', '无工作经验', '本科',
                      '招5人', '12-09发布', '软件测试工程师', '上海测开教育科技有限公司',
                      '1、负责公司产品研发过程中各阶段的软件测试；\n2、参与产品的需求分析，根据需求分析和设计文档，能够独立制定合理的测试方法，设计测试用例；\n3、按照测试用例内容搭建基本测试环境并确保环境有效性；\n4、根据测试结果，编写测试报告，并向相关人员及时反馈，跟踪并推动问题解决\n5、能够协助支持工程师完成对产品的改进和优化。\n\n任职要求：\n1、计算机相关专业专科及大专以上学历，2年以上软件测试相关工作经验；\n2、熟悉测试相关理论、方法和测试流程，熟悉常用的软件硬件测试工具及Bug管理工具；\n3、熟悉http、TCP/IP等网络协议；\n4、能够独立完成测试计划、测试报告和测试结果分析文档；\n5、熟悉常用的测试工具使用如Loadrunner、QTP等；\n职能类别：测试工程师\n',
                      '上班地址：洪山区',
                      '上海测开教育科技有限公司长期积极致力于从事、计算机、网络、数据、软件科技领域内的技术开发、技术咨询、技术服务、技术转让，网络工程，软件开发，计算机系统集成服务，商务咨询，企业管理咨询，市场信息咨询与调查，人才咨询，电子产品、计算机、软件及辅助设备的销售。上海测开教育科技有限公司，本着“客户第一，诚信至上，以人为本”的原则，欢迎国内外企业/公司/机构与本单位建立长期的合作关系。热诚欢迎各界朋友前来参观、考察、洽谈业务。公司自成立至今，不断吸取和借鉴国内外先进的经营和管理理念，努力实现公司业务、管理等方面自我超越！'],
        '114247753': ['1-1.5万/月', '五险一金|补充医疗保险|通讯补贴|餐饮补贴|定期体检|地铁周边|不打卡|扁平化管理|领导NICE|免费零食|', '武汉-洪山区', '3-4年经验', '本科',
                      '招2人', '12-09发布', '软件测试（街道口）', '北京腾赋网络科技有限公司',
                      '岗位职责：\n1、完成公司平台产品相关测试工作；\n2、根据产品需求和设计文档，制定测试计划，并分析测试需求、设计测试流程；\n3、编写并评审测试用例，在测试各环节与开发部门沟通保证测试输入和输出的正确性和完备性；\n4、执行具体测试任务并确认测试结果、缺陷跟踪，完成测试报告以及测试结果分析。\n\n任职要求：\n1、计算机或相关专业，本科学历3年以上软件测试经验（会性能测试或自动化测试）；\n2、熟悉软件测试流程，能够独立设计编写测试用例；\n3、熟悉Linux操作系统、熟练运用Linux命令；\n4、熟悉常见的脚本语言Python、Shell，可利用相关语言编写脚本工具；\n5、了解数据库及网络的相关知识；\n6、强烈的责任心，做事认真细致，具备良好的团队合作精神，沟通能力佳。\n7、具备有零售或者电商行业工作经验。\n职能类别：软件测试系统测试\n关键字：自动化测试性能测试\n',
                      '上班地址：武汉市洪山区街道口理工大孵化楼 - B座17楼1701',
                      '公司福利：1）五险一金，人身意外险、补充医疗保险；2）午餐餐补、晚餐补贴、打车费报销、通讯补贴；3）办公区免费零食、水果、下午茶；4）法定节假日礼品；5）不定期组织培训、交流分享会，助力员工成长与发展；6）年度员工体检；7）不定期的组织团建或聚会；8）更多惊喜等你来发现~~用人准则：人品、责任心、学习能力！公司简介：新零售领域第三方独立服务商资深零售行业专家和互联网技术精英组成的创业团队致力于新零售领域实体零售商的各种创新业务突破各种壁垒进而高度融合从门到门、端到端O+O，形成闭环并真正为各方带来切实的价值成立两年已上线数千家实体门店（包括京客隆，欧尚，新华都，美特好，正大优鲜等多个知名企业客户）与美团外卖、饿了么、京东到家、百度外卖等互联网平台深度合作'],
        '109948900': ['1-2万/月', '五险一金|补充医疗保险|员工旅游|餐饮补贴|年终奖金|定期体检|', '武汉-洪山区', '3-4年经验', '本科', '招1人', '12-09发布',
                      '软件测试工程师', '北京金山办公软件股份有限公司',
                      '1、负责WPSOffice的相关测试：制定测试计划、设计用例、执行用例、用例维护、评审；\n2、缺陷定位、跟进处理，项目测试过程及时做风险评估并可以深入总结；\n3、在项目中保持和开发&产品人员积极有效沟通，分析、推动问题合理解决，优化研发和测试过程；\n4、根据项目特点，尝试新方法、新工具提高测试效率，建设良好的全平台测试框架；\n\n任职要求：\n1、三年以上测试相关工作经验；\n2、能熟练使用Charles代理工具，用于日常抓包、分析定位问题、接口测试，会使用数据库常用工具及SQL语句者优先；\n3、具备较强的执行力、推动力，可独立负责大/中型项目测试，按时提供高质量可交付版本；\n4、具备较强的逻辑分析能力，思维敏捷，能了解开发代码逻辑者优先；\n5、具备较好的学习能力、协调能力及适应能力，有高度的责任心和主动性；\n6、会使用xmind整理测试思路、有较强文档编写能力者优先\n职能类别：软件测试软件工程师\n',
                      '上班地址：光谷APP广场2号楼17层',
                      '金山软件是中国最知名的软件企业之一，中国领先的应用软件和互联网服务提供商。目前，金山软件在珠海、北京、成都、大连、深圳五地分设研发中心，创造了WPS Office、金山词霸、金山毒霸、剑侠情缘、封神榜等众多知名产品。同时，金山旗下拥有国内知名的大型英语学习社区爱词霸网（www.iciba.com）以及在线游戏交流社区逍遥网（www.xoyo.com）。2007年10月9日，金山软件在香港主板成功上市（股份编号：03888.HK）。2008年，金山软件迎来了20周年的庆典，走过弱冠之年的金山软件将加速推进其技术立业及国际化战略。做世界一流的软件公司，是所有金山人永远不变的梦想。电话：(86-10)-82334488传真：(86-10)-82325655Kingsoft Corporation Limited is a leading software developer, distributor and service provider in China. Kingsoft now has R&D centers in Zhuhai, Beijing, Chengdu, Dalian, and Shenzhen. We have several well-known products such as Kingsoft Office, Kingsoft PowerWord, Kingsoft Internet Security and online games such as "JX Series" and "The First Myth". Kingsoft has set up some of China\'s largest online communities, including the most popular domestic online English learning website www.iciba.com and the online games website www.xoyo.com.On October 9th, 2007, Kingsoft was listed on the Hong Kong Stock Exchange (stock code: 03888.HK). 2008 was the 20th anniversary of Kingsoft. After twenty-year\'s struggles and development, Kingsoft will continue to accelerate the internationalization strategy based on techniques.Kingsoft people have never doubt their goal is to become a world-class software provider.'],
        '118288804': ['10-15万/年', '五险一金|餐饮补贴|年终奖金|定期体检|', '武汉-洪山区', '1年经验', '本科', '招若干人', '12-09发布', '软件测试-工程师(J11174)',
                      '长江存储科技有限责任公司',
                      '工作职责:\n1.制定测试计划、任务分配，追踪管理测试进度\n2.对系统变更进行测试，按时完成测试任务\n3.编写测试报告、设计测试用例\n4.搭建测试环境、执行测试用例\n5.根据Bug不同种类进行归类总结，提交Bug报告，并进行Bug修复验证\n6.参与需求评审以及测试Bug讨论，参与需求上线风险评审\n任职资格:\n1.有软件测试经验，了解测试要求及流程\n2.了解CMMI体系，能遵守CMMI体系要求测试\n3.了解Oracle、PL/SQL数据库，会写SQL查询、操作数据库\n4.了解自动化测试，能进行自动化测试脚本开发\n5.具备良好的沟通能力，较强的口头表达能力和文案编写能力\n6.有良好的执行能力，细心、仔细、有耐心、责任心强\n职能类别：其他\n',
                      '上班地址：未来三路国家存储器基地',
                      '长江存储科技有限责任公司（“长江存储”）于2016年7月在中国武汉成立，是一家专注于3D NAND闪存芯片设计、生产和销售的IDM存储器公司。长江存储为全球工商业客户提供存储器产品，广泛应用于移动设备、计算机、数据中心和消费电子产品等领域。2017年，长江存储在全资子公司武汉新芯12英寸集成电路制造工厂的基础上，通过自主研发和国际合作相结合的方式，成功设计并制造了中国首批3D NAND闪存芯片。长江存储在武汉、上海、北京等地设有研发中心，通过不懈努力和技术创新，致力于成为全球领先的NAND闪存解决方案提供商。'],
        '107600815': ['1-2万/月', '五险一金|年终奖金|', '武汉-洪山区', '5-7年经验', '本科', '招若干人', '12-09发布', '软件测试经理', '武汉盛华伟业科技股份有限公司',
                      '职位描述：\n1、参与研发流程改善，梳理研发管理流程及持续优化；\n2、参与产品需求分析，建立测试流程和测试规范，把控整体的产品质量；\n3、制定质量相关报告的规范，指导编写测试计划、测试用例、测试方案、测试报告等。\n4、带领质量团队完成产品测试和保证产品质量，推动开发团队提高测试能力和认识；跟踪分析问题，总结测试报告，归档测试用例，推动测试中发现缺陷并及时合理解决；\n5、带领测试团队引入或者研发自动化测试工具与性能测试工具，不断提升团队的测试效率和测试能力。\n\n任职要求：\n1、计算机或相关专业本科及以上学历，热爱软件测试工作；五年以上测试工作经验，3年以上团队管理经验；\n2、熟悉主流的测试技术,如UI自动化、接口自动化、性能、安全测试等，熟悉主流的测试工具，LR、JMETER、APPSCAN、SELENIUM2等\n3、熟悉软件工程，精通软件测试流程；熟悉至少一种编程语言，能够编写自动化测试脚本；\n4、熟练掌握静态代码分析、代码检查、功能确认与接口测试、全链路压力测试、覆盖率分析、性能分析、安全分析、稳定性分析、内存分析；\n5、熟悉至少两种自动化测试框架，熟练使用测试缺陷管理工具与项目管理工具；\n6、有较强的责任心，思维逻辑清晰，擅于跨团队沟通和协作。\n\n基本工资+五险+绩效奖金+年终奖+股票期权+其他\n职能类别：软件测试软件工程师\n关键字：经理软件测试\n',
                      '上班地址：东湖高新区武大科技园航域二期A1栋1302室',
                      '武汉盛华伟业科技有限公司是一家2009年10月注册的以软件、仪器仪表研发、物联网技术、大数据挖掘、人工智能技术和石油技术服务为核心业务的国家高新技术企业和软件服务企业业。\xa0\xa0\xa0\xa0公司始终坚持自主创新，致力于研发和服务，经过十多年耕耘和积累，打造了一支高端技术研发服务团队，现有员工85人，包括教授（博士）2名，，硕士16名，本科48名，并于2017年4月完成全员持股的股份制改造。\xa0\xa0\xa0\xa0公司经过十多年的致力拓展，在西北石油局、吐哈油田、新疆油田、长庆油田、玉门油田、大庆油田、江汉油田、江苏油田、胜利油田、中原油田、华北油田、吉林油田、华东石油局、中石化国际勘探公司等多家油田企业先后承担并完成了“远程数据传输”、“多井地层对比”、“随钻综合解释评价”、“水平井三维地质导向”等二十几项研究成果。特别是“数字化岩芯图文综合信息系统”、“随钻综合解释评价系统”、“钻井工程异常预警”等五十多项研究成果，公司于2012年以来迎合市场需求大力进行研发创新产品“井场数据一体化协同工作平台”，该平台将渗透到井场-基地生产作业的每个环节，实现了现场到基地的实时互动，全面实现井场生产数据的信息化管理和综合应用并被科技部鉴定为国际领先，同时公司分别与武汉理工大学、长江大学、上市公司北京中油瑞飞，新疆红友公司签订了长期资源整合合作框架协议。\xa0\xa0\xa0\xa0盛华人秉承“创新奋进、诚信为本、合作共赢”的企业精神，为中国梦而努力奋斗。未来，公司将继续致力于大数据分析、人工智能、VR技术在油气勘探开发领域的应用研究，实现生产过程的可视化、自动化、智能化应用，为数字工程技术、智慧油田建设做贡献。'],
        '119044700': ['1-1.5万/月', '五险一金|补充医疗保险|补充公积金|员工旅游|绩效奖金|年终奖金|出国机会|弹性工作|股票期权|定期体检|', '武汉-武昌区', '5-7年经验', '大专',
                      '招若干人', '12-09发布', '软件测试主管  年薪18万起', '狄艾恩（武汉）建筑规划设计有限公司',
                      '1、负责测试团队的技术规划、创新和应用,提高整体测试技术水平;\n2、负责测试项目工作的全局安排,并解决测试工作中出现的问题,保证测试工作的顺利开展;\n3、监控分析达成本部门质量目标的达成、提升本部门工作效率;\n4、评估测试方案、测试策略和相关测试报告;\n5、培养指导软件测试工程师,并组织相关培训工作,保证测试团队能力的持续提高;\n6、上级交办的其他事宜。\n职能类别：软件测试软件工程师\n关键字：软件测试\n',
                      '上班地址：武汉武昌汉街',
                      'GC是世界上知名的国际性多元化全球设计服务机构，最早成立于西班牙巴塞罗拉，后发展到墨西哥再到中国大陆地区的北京。作为“智慧化城市综合服务提供者”，GC是合力帮助城市打造可持续发展的，未来智慧城市的***合作伙伴。为此我们同各方一起打造中国城市化进程中的智慧城市。并持之以恒的改善及维护世界各地的自然和社会环境。在智慧化城市的产业链上GC 优化了各方资源，从科技、规划、运营、资本、管理等全方位整合，协助全球主要机构应对各种问题，.在各领域制定领先的切合实际的解决方案。GC旗下构建了GC设计、GC资本运作及GC建设，并拥有国际背景的核心团队，掌握着先进的国际理念，致力于用思想改变城市面貌，在城市的记忆中留下精神财富。为了更好的加快智慧化城市进程的速度，为人们提供更舒适，更具价值的场所。GC用智慧的经验点亮智慧的城市，为此由西班牙总部设计核心团队撰写的<>，已经由西班牙语翻译成中文，并将于近期在国内出版发行。'],
        '111398581': ['1-1.5万/月', '包住宿|免费班车|五险一金|绩效奖金|股票期权|餐饮补贴|', '武汉-洪山区', '3-4年经验', '本科', '招2人', '12-07发布',
                      '嵌入式软件测试工程师 (职位编号：0007)', '武汉蓝星科技股份有限公司',
                      '岗位职责：1、进行高可靠高安全嵌入式软件测试，包含代码测试、功能测试、性能测试、安全性测试等；2、编写测试计划、规划详细的测试方案、编写测试用例；3、根据测试计划搭建和维护测试环境；4、执行测试工作，提交测试报告。包括编写用于测试的自动测试脚本，完整地记录测试结果，编写完整的测试报告等相关的技术文档；5、对测试中发现的问题进行详细分析和准确定位，与开发人员讨论缺陷解决方案；6、对测试结果进行总结与统计分析，对测试进行跟踪，并提出反馈意见；任职资格：1、计算机相关专业本科以上学历，3年以上测试工作经验；2、具有计算机嵌入式编程、软件测试、系统集成等相关基础知识；3、熟练掌握C语言，理解能力强，善于阅读并理解代码，正确理解开发文档并编写用例；4、熟练掌握至少1门脚本语言（PYTHON、SHELL等）；5、有责任心、踏实、努力，具有良好的沟通能力、表达能力与逻辑思维能力；工作认真细致、善于思考、勤于学习；6、具有使用QAC，Tessy等软件测试工具经验的优先考虑；7、具有汽车电子行业工作经验者优先。\n职能类别：软件测试\n',
                      '上班地址：东二产业园黄龙山东路',
                      '武汉蓝星科技股份有限公司是2002年经湖北省人民政府批准成立的股份制企业，注册资本金13369万元。公司专注于LINUX嵌入式操作系统、图形软件系统等基础软件研发，在嵌入式操作系统、操作系统开发工具、系统平台等领域拥有完整自主知识产权，技术成果主要面向嵌入式市场，可广泛应用于医疗医美、航天军工、智能制造、AI智能、消费电子、电教设备、车辆信息化、智慧农业等行业领域，是领域内知名高新技术企业。\xa0\xa0\xa0全球LINUX基金会银牌会员\xa0\xa0\xa0开源车载系统平台联盟AGL银牌成员\xa0\xa0\xa0与华中科技大学建立联合实验室《嵌入式图形图像及计算机视觉联合实验室》\xa0\xa0\xa0《GB/T 26775-2011 车载音视频系统通用技术条件》国家标准起草单位\xa0\xa0\xa0《车载无线通信设备通用技术条件》行业/国标主任起草单位\xa0\xa0\xa0\xa0湖北省省级企业技术中心。。。。。。。。公司立足自主创新，研发人员占总人数70%。研发中心下辖可视图形计算事业群、OS 事业群、终端设计事业群和技术支持事业群等四个事业群。公司拥有深厚的技术积累，产业方向符合国家战略规划，正处于高速上升期，欢迎您的加入，共创美好明天'],
        '117060548': ['1.1-1.5万/月', '五险一金|交通补贴|餐饮补贴|专业培训|出国机会|年终奖金|', '武汉-东湖新技术产业开发区', '3-4年经验', '本科', '招若干人',
                      '12-07发布', '嵌入式软件测试工程师（武汉）', '东莞正扬电子机械有限公司',
                      '负责武汉研发中心嵌入式软件的单元测试、集成测试以及系统测试，与硬件工程师、嵌入式软件工程师、视觉和机器学习算法工程师协同完成系统测试与调试工作。主要包括：\n1、编写测试方案、测试计划、测试用例，并搭建和维护测试软硬件环境；\n2、完成嵌入式软件的单元测试、集成测试以及系统测试；\n3、有效地执行测试用例，编写测试报告；\n4、准确地定位并跟踪问题，推动问题及时合理地解决。\n任职要求：\n1、大专及以上学历，计算机，软件工程，电子，通信等专业；\n2、三年以上嵌入式软件系统测试经验、工具使用经验或自动化测试经验；\n3、了解软件工程理论以及基本测试理论和测试方法；\n4、熟悉嵌入式软件开发流程，熟悉测试计划制定和测试用例设计方法和策略；\n5、掌握Linux系统基本操作和常用脚本编程；\n6、熟悉一种脚本编程语言（Python/Shell/Perl）者优先；\n7、熟悉C/C++编程规范，有两年以上实际编程经验者优先；\n8、具有良好的沟通和自主学习能力，较强的问题分析和处理能力，富有高度的责任心及团队合作精神。\n\n东莞正扬武汉研发中心依托于总公司在汽车行业数十年的深厚积累及对ADAS（高级驾驶辅助系统）领域的大力投入支持，于2018年8月正式成立，专注于汽车ADAS领域相关技术产品的研发。现已建成涵盖硬件，软件，算法（AI），测试，品质等各个方面的完善开发团队。在这汽车行业面临新四化（电动化，网联化，智能化，共享化）的百年未有之变革之际，欢迎大家加入我们，一起顺势前行！\n职能类别：软件测试\n',
                      '上班地址：光谷金融港B6栋402室',
                      '一、公司介绍\xa0\xa0\xa0\xa0\xa0\xa0\xa0东莞正扬电子机械有限公司（品牌KUS）成立于1984年，是一家集研发、生产、销售、服务为一体全球***的汽车、游艇液位传感器、尿素传感器及仪表供应商。产品广泛应用于卡车、巴士、工程机械、农业机械、游艇和发电机组等领域，全球市场占有率超过85%，KUS发明生产了全球***款干簧管液位传感器。应国家及行业市场需求，借助正扬通路优势，KUS业务将走向多元化发展，于2018年成立新能源公司、智能制造公司，以不断提升公司综合能力及市场竟争力。公司荣获资质有国家高新技术企业、东莞市“倍增”计划企业、东莞市专利优势企业等称号。KUS全球化运营，总部位于广东省东莞市黄江镇，设有东莞正扬电子机械有限公司、广东正钢科技有限公司、智能制造公司、新能源公司，在台湾、深圳、美国、印度、荷兰、安徽等地都设有研发中心或分公司，现有规模4800人以上。产品销售范围覆盖欧洲、北美、亚洲、南美、澳州和非洲的主要国家和地区，主要终端客户有戴姆勒奔驰、沃尔沃（Volvo）、德国的大曼（MAN）、瑞典的斯堪尼亚（Scania）、帕卡、依维柯、雷诺、东风、一汽解放、重汽、福田、陕汽、日野、现代、卡特彼勒(CAT)、约翰迪尔(John Deere)、小松、日立、三一重工、徐工等国际知名公司。KUS拥有强大的研发团队与通过国家CNAS认可的实验室，拥有优秀的团队及完善的管理机制、软件投资SAP、OA、MES等。设备工艺涵盖机械、电子、ADAS、新能源、智能装备等领域，生产95%关键零部件实现自制，能为客户提供SCR系统后处理、液位测量、发动机监控和行驶信息的解决方案。产品市场份额遥遥领先于国内外同行，每年有数百万套的产品应用于各类车辆尾气减排系统中，为地球环境保护事业做出了不可磨灭的贡献。公司现已通过IATF16949:2016、ISO9001:2015、ISO14001:2015等体系认证，使之真正做到了绿色、环保、高效、安全生产。响应公司管理哲学思想，我们坚持做“好人”企业，让更多的人懂得感恩、知福、惜福，形成好人的行为，最终影响家人，影响社会。现应公司发展，诚邀各位有志之士加入，共创辉煌事业及美好生活！二、企业文化●正扬核心价值观：正直、当责、创新、团队●正扬企业使命：持续为客户创造***价值●正扬企业愿景：让呼吸更洁净；让驾驶更感知三、公司福利：●薪酬福利：提供具市场竞争力薪资，并设有年资奖、全勤奖、管理人员电话补贴等；年终奖金视公司当年盈利情况发放1-3个月；视工作业绩每年有1-3次调薪机会。●社保及公积金：购买五险、住房公积金。●自助餐厅：免费提供营养、丰富的自选早、中、晚、夜宵自助餐。●住宿条件：免费提供热水、空调、储物柜、书桌、独立卫生间及阳台等配置及WIFI（按宿舍区域）。●有薪假期：国家劳动法规定的法定节假日、工伤假，婚假，丧假，产假，陪产假、年休假。●康乐设施：福利社、图书室、乒乓球室、桌球室、羽毛球室、足球场、儿童游乐场、电视房、母婴室等。●员工福利及活动：每周加餐一次、生日购物卡、节假日礼品、年底举办尾牙抽奖晚会、定期或不定期的举办各类大型文体比赛活动、女子瑜伽班等。●员工子女关怀：长期为员工子女组织课后作业辅导班、兴趣爱好特长班，为在职员工解决后顾之忧。●培训机制：完善的培训体系，将分别为职员工提供入职、在职管理及技术、业余学习等类别的培训。四、交通指引：1、开车路线：导航地点可定位“东莞正扬电子机械有限公司”。2、您所在位置：先到黄江广场，再转镇内7路公交车（15分钟）或滴滴快车（5分钟）到我司。'],
        '115605279': ['1-1.2万/月', '五险一金|免费班车|员工旅游|餐饮补贴|通讯补贴|专业培训|绩效奖金|年终奖金|出国机会|', '武汉-东湖新技术产业开发区', '5-7年经验', '大专',
                      '招5人', '12-06发布', '软件测试工程师（WH）', '深圳市卓翼科技股份有限公司',
                      '1、计算机软件、电子信息及相关专业毕业，大学本科及以上学历\n2、5年以上无线路由器或网通类终端产品/CPE无线终端产品等相关产品软件测试工作经验\n3、熟悉软件测试流程、测试方法与理论，掌握主流的测试及管理工具，具备扎实的测试基本功，动手能力强\n4、能独立制定和编写测试方案、测试策略、测试计划、测试用例及输出测试报告\n5、熟悉无线路由器产品的应用、底层软件、WIFI/路由协议、网络安全、维管、功能等相关测试工作（FDE专项要求：在WiFi通信，网络安全，路由协议/应用/驱动/维管等测试技术方面有专项突出能力）\n6、具备高度的责任心、良好的沟通协调能力和团队合作意识，有较强的学习能力与工作抗压能力.\n\n岗位职责：\n1、根据产品需求规格与交互设计文档，编写软件测试方案与测试用例，制定测试策略与测试计划，对产品质量负责\n2、搭建测试环境，负责测试工作的执行，包括但不限于系统测试、功能测试、性能测试、压力测试、稳定性测试、兼容性测试、产品网络安全测试以及专项特性测试等，保证测试的正确性和完整性\n3、负责和产品开发等其他团队的沟通协作，按期完成测试交付\n4、跟踪定位缺陷或问题，推动问题回归闭环，完成测试报告并分析测试结果\n5、通过相关测试流程、策略、方法和工具创新，努力提升测试质量和效率\n职能类别：软件测试系统测试\n关键字：软件测试FDEWIFI/路由\n',
                      '上班地址：光谷未来科技城',
                      '深圳市卓翼科技股份有限公司（以下简称“卓翼科技”）创始于2004年，2010年3月在深交所挂牌上市（证券简称：卓翼科技，证券代码：002369）。卓翼科技专业从事通讯、计算机、消费类电子等3C产品的研发、制造与销售。在移动终端、网络通信、智能家居、可穿戴、自动化及消费产品领域，卓翼科技向全球客户提供设计、开发、生产、技术支持等优质服务。凭借强大的技术优势、开拓进取的专业态度和尽善尽美的服务精神，卓翼科技一直处于市场领先地位，与全球诸多顶尖客户精诚合作，共创未来。\xa0\xa0\xa0卓翼科技在全球拥有约10000名员工，在深圳、厦门、西安设有研发中心，在深圳、天津设有两个高度自动化的生产基地。依托自身研发、制造能力，卓翼科技可提供优秀的产品设计、完善的供应链管理以及专业的柔性智能制造，帮助客户把产品更快地投入市场，提高其成本效率。2015年起，卓翼科技在美国硅谷设立技术服务公司，重点扶持跟卓翼科技产业方向吻合的创新公司，助力全球智能硬件创新。作为全球领先的产品和服务解决方案提供商，卓翼科技坚持加大前沿技术驱动的创新投入，不断优化产品结构，逐步扩大生产自动化的应用，从规模驱动转变为效率驱动的行业领先企业。\xa0\xa0\xa0卓翼科技通过ISO9001标准化质量管理体系、ISO14001环境管理体系、OHSAS18001职业健康安全管理体系以及SA8000-2008社会责任管理体系的认证。卓翼科技相继获得深圳市工业500强、南山区民营领军企业、南山区纳税百强企业、中小企业诚信榜AAA上榜企业等各项荣誉。取得国家高新技术企业、深圳市市级研究开发中心等资质。\xa0\xa0\xa0面对滚滚而来的万物互联浪潮，卓翼科技将一如既往地肩负科技使命，心怀梦想，憧憬未来。努力抓住物联网时代提供的慷慨成长机遇，构筑产品、制造、创业加速为一体的综合服务平台；力争成为中国智能制造的标杆和创新创业合作的理想平台，成为一流的科技服务型企业。'],
        '113668853': ['1-1.8万/月', '', '武汉-东湖新技术产业开发区', '无工作经验', '大专', '招1人', '12-06发布', '软件测试工程师', '哈工智慧（武汉）科技有限公司',
                      '岗位职责：\n1、参与产品需求设计评审\n2、产品运行环境搭建\n3、产品功能测试、性能测试\n4、产品测试报告、用户手册及其他相关文档编写与管理\n5、产品研发及项目实施配置管理\n6、产品培训\n任职要求：\n1、硕士2年以上工作经验，本科3年以上工作经验，计算机、GIS或相关专业，211/985高校优先；\n2、熟悉Oracle、MySql等常用数据库的安装、调优，熟悉SQL语句编写；\n3、对Linux操作系统有一定了解，会使用基本操作命令；\n4、熟悉Tomcat、Nginx等中间件配置及应用；\n5、熟悉GIS相关原理和技术，熟悉使用ArcGIS软件；\n6、有软件测试经验，熟悉白盒测试、黑盒等功能测试方法；\n7、有性能测试经验，了解loadrunner等性能测试工具使用；\n8、对版本基线计划、缺陷管理有较好的理解，熟悉Git、SVN等代码管理工具；\n9、熟悉软件项目支持流程，有较好的沟通能力，能与研发、项目实施人员良好互动，能够对软件产品功能进行系统讲解和培训。\n职能类别：软件测试\n',
                      '上班地址：武汉市汉阳区芙蓉路1号华中智谷C5栋',
                      '哈工大机器人集团嘉利通科技股份有限公司（证券代码839123）是一家由哈工大参股的***高新技术企业，依托哈工大雄厚的科研技术实力，致力于为中国新型城镇化建设提供整体解决方案，拥有北京西普伟业科技发展有限公司，并在2018年通过招商引资，落户武汉经济开发区，成立哈工智慧（武汉）科技有限公司，业务涵盖公共安全、智能交通、智慧政务、IDC建设等城市精细化管理多个领域。\xa0\xa0哈工大机器人集团嘉利通人践行“耕耘智慧城市，引领人类幸福”的使命，在新型智慧城市建设中坚持以新理念为引领，以数据新要素为驱动，以新技术提升供给能力，以新基础设施为支撑，以新服务为根本，以新治理为重点，探索建设运营新模式，从而持续提升城市核心竞争和提升人们的生活质量和福祉。\xa0\xa0公司拥有自主的知识产权、核心平台软件，采用核心技术充分进行互联网、大数据、人工智能技术与城市建设的深度融合，推进大数据辅助科学决策和社会治理模式的创新。\xa0\xa0公司始终坚持“以人为本”的企业文化，尊重员工个性，努力为员工提供更好的工作环境、职业发展和生活质量。致力于成为社会负责、受人尊重的优质企业，以更加积极、健康的方式为社会贡献力量。未来，哈工大机器人集团嘉利通股份将持续致力于城市建设的发展，为人类幸福生活而耕耘。愿景-----耕耘智慧城市，引领人类幸福使命-----智慧城市解决方案的深度定制专家价值观---诚信、创新、担当、务实；以业务发展为核心。实现客户价值***化；以员工发展为基础，实现企业效益***化'],
        '118746917': ['1-1.5万/月', '', '武汉-洪山区', '3-4年经验', '大专', '招1人', '12-06发布', '软件测试讲师', '武汉辉远信毅科技有限公司',
                      '计算机课程设计\n1、本科及以上学历，有4年以上软件测试技术经验、有测试管理工作经验优先；\n2、掌握C/C或JAVA，掌握SQLServer、Oracle、Mysql中任意一种数据库，有两年以上开发工作经验，掌握Unix或Linux操作系统管理，能够搭建常用的服务；了解软件测试基本概念；\n3、掌握自动化测试理论，熟练使用QTP、LoadRunner之一种，并有相关自动化测试工作经验2年以上；熟悉计算机软硬件知识，熟悉网络基础知识及TCP/IP协议，熟悉Windows或Unix/Linux操作系统的配置和管理，能够搭建常用的服务，了解J2EE或.net架构；\n4.熟悉Linux操作系统基本命令；有2年以上基于Linux操作系统的自动化测试经验；熟练使用脚本语言：Python,Perl,Shell等任意一种；\n5.素质要求：沟通能力，细心，耐心，思考问题思路清楚；\n6.热爱行业，有责任心；\n7.有培训经验者和管理经验者优先！！！\n8.有Python自动化经验者优先！！！\n工作时间：做五休二09:00-12：00下午14:00---18:00\n职能类别：软件测试\n关键字：软件测试讲师\n',
                      '上班地址：洪山区光谷国际广场B座16楼02室',
                      '武汉辉远信毅科技有限公司是一家专注于大数据开发、测试与质量保证领域的专业服务企业，公司成立于2015年，总部位于北京，在石家庄、保定、唐山、沈阳、郑州、武汉、济南、长春、南京分别设立分公司。经过3年多的发展，目前公司在全国7个城市设有交付中心，员工总数已达数百人。公司具备"软件+服务"综合业务能力和强大的纵深服务优势，主营业务覆盖软件技术服务、企业IT解决方案服务、企业IT人才外包服务以及云计算与互联网平台服务四大业务领域。\xa0\xa0\xa0\xa0\xa0\xa0多年来积累了深厚的垂直行业服务经验，帮助客户快速解决业务难题。与诸多客户建立的长期合作关系更保证了自身对行业的深入理解，及服务能力的不断提升。公司发展至今，也得力于一支经验丰富的管理团队，他们对IT领域有着深厚了解，不断追求创新，在动态多变的商业环境中为公司的发展树立了清晰的远景和方向。'],
        '117247880': ['', '', '武汉-洪山区', '无工作经验', '本科', '招10人', '12-04发布', '软件测试 (职位编号：JD-13(武汉))', '北京亚鸿世纪科技发展有限公司',
                      '岗位职责：\n1、负责公司产品版本测试\n2、根据需求编写测试用例，执行测试用例\n3、根据用例制定测试计划、测试方案、测试报告\n4、完成功能测试和性能测试\n5、编写产品业务处理流程图\n任职资格\n1、具有良好的沟通协调和文档撰写能力；\n2、学习能力强，富有团队精神，有强烈的责任感与进取心。工作认真细致，责任心强，良好的语言表达能力；\n3、熟悉测试流程、测试用例与测试计划的编写，熟练使用缺陷管理和测试管理工具；\n4、熟练掌握黑盒测试方法，具备灰盒测试思维；\n5、熟悉linux操作系统，熟悉Oracle、Mysql数据库，熟练掌握SQL语言、熟悉Tomcat、Jboss、Apache等；\n6、熟悉SHELL编程，熟悉网络编程及相关网络协议，了解TCP/IP协议；\n7、对大数据有一定的了解（了解基本的框架hadoop,对hdfs、zookeeper、hive、spark、flume等原理有了解）\n8、有实际研发编码经验、测试脚本编写经验及性能大数据量测试经验者优先。\n\n职能类别：软件测试\n关键字：性能测试功能测试大数据测试\n',
                      '关键字：性能测试功能测试大数据测试',
                      '北京亚鸿世纪科技发展有限公司（以下简称亚鸿公司）是一家专注于互联网空间数据治理、网络与信息安全及数据增值解决方案及服务的高科技公司，2017年7月，亚鸿世纪成为任子行网络技术股份有限公司的全资子公司，完成整体上市。截止到2019年9月，亚鸿公司员工450余人，在北京、深圳和武汉设有研发中心，业务遍及全国30多个省市。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0亚鸿世纪定位于网络空间资源大数据治理专家，是工信部多项互联网安全管理行业标准的制定者，多项***互联网安全管理平台的承建者，省级互联网空间安全治理系统解决方案的引领者，运营商互联网安全解决方案的领跑者。公司致力于构建“国家-省-企业”三层互联网安全管理体系架构并提供领先的整体解决方案，拥有该领域多项专利和软件著作权，并与业界多家知名企业、重点院校以及国家权威机构和专业团体建立了战略合伙伴关系。公司产品多次入选工信部网络安全技术应用试点示范项目和工信部工业互联网专项项目，在工信部省级互联网空间安全大数据治理、运营商互联网安全管理行业市场占有率***。'],
        '114608231': ['12-18万/年', '专业培训|五险一金|通讯补贴|高温补贴|免费班车|包吃|包住宿|带薪年假|定期体检|出国机会|', '武汉-江夏区', '1年经验', '本科', '招4人',
                      '12-03发布', '软件测试工程师（硬件在环)', '博世华域转向系统（武汉）有限公司',
                      '1.分析并评审软件系统需求\nAnalyzeandreviewSoftwareSystemRequirements\n2.根据项目需求修改测试模型\nModifythemodelaccordingtoprojects’specialdemands\n3.创建并评审测试规范\nCreateandreviewtestspecifications\n4.创建测试用例\nCreatetestcases\n5.运行HIL测试\nExecuteHILtests\n6.分析测试结果，解决测试问题\nAnalyzetestresultandfixtestingproblem\n7.在CQ中创建问题报告\nCreateProblemJobinCQ\n8.检入测试结果到CC\nCheckintestresultsinCC\n9.保存并备份测试环境\nSaveandbackuptestenvironment\n\n任职要求：\n\n1、大学本科及以上学历，车辆工程、软件工程等相关专业；\nBachelordegreeorabove，MajorinAutomotiveEngineering,SoftwareEngineeringandsoon;\n2、1-5年汽车电子行业软件测试工作经验；\n1-5yearssoftwaretestexperienceinautomotiveelectronicsindustry\n3、至少熟悉以下一种编程语言：C(C++);Python;Matlab;\nBefamiliarwithatleastoneofthefollowinglanguages:C(C++);Python;Matlab;\n4、正直诚信、踏实勤恳；\nIntegrity,Honesty,SteadfastnessandDiligence\n\n职能类别：软件测试\n关键字：软件测试HIL测试\n',
                      '上班地址：武汉市江夏区金港新区通用大道66号',
                      '博世华域转向系统（武汉）有限公司（原上海采埃孚转向系统（武汉）有限公司，以下简称“公司”）位于武汉市江夏区金港新区通用大道66号，是博世华域转向系统有限公司（以下简称“母公司”）出资成立的全资子公司，注册资本为1.38亿人民币，投资总额达3.51亿人民币。公司主导产品为管柱式电动助力转向系统（EPSc）、双齿轮式电动助力转向系统（EPSdp）以及液压助力转向系统（HPS）和相关零部件等，主要客户为上汽通用（武汉）、东风神龙、上海大众（长沙）、长安福特、上汽通用五菱、沃尔沃中国、一汽大众（成都）等国内知名整车厂。\xa0\xa0\xa0\xa0母公司是由华域汽车系统股份有限公司（占49%股份，隶属于上汽集团，2017年世界500强排名41位）和德国博世转向系统有限公司（51%股份，隶属博世集团，2017世界500强排名76位）共同组建的合资企业，是上海市政府确认的先进技术企业和上海市科委确认的高新技术企业，同时也是中国乘用车转向系统业务规模最大、市场占有率最高、综合能力最强的转向系统专业生产基地。博世华域转向系统（武汉）有限公司于2014年10月正式投厂，在母公司的正确领导，以及当地政府及兄弟工厂、供应商伙伴的大力支持和帮助下，以“依靠不断成长的员工队伍，创新驱动，创造价值”为使命，以“客户导向、创新超越、合作进取、正直诚信”为核心价值观，携手员工共同实现“成为转向系统市场引领者”的企业愿景。与此同时，公司非常重视每位员工的职业发展和培训需求，每位新员工入职后都有一套完整的培训计划，包括上汽和博世的各项业务培训等。除此之外，按照业务需求，员工还有机会外派德国总公司和欧美多个国家地区进行海外培训和交流学习。和谐舒适的工作环境、先进的管理体系、满意的薪资福利、广阔的发展前景是每位有志于汽车工业者的理想之所。公司福利：1、\xa0\xa0\xa0\xa0优秀人才发展计划、武汉居住证办理；2、\xa0\xa0\xa0\xa0为外地单身员工提供酒店式员工宿舍、公司购房补贴；3、\xa0\xa0\xa0\xa0提供免费班车接送、食堂用餐补贴、疗休养津贴、补充医疗保险、弹性休假、工会福利等。应聘简历投递渠道：1.登录前程无忧、智联招聘进入博世华域转向系统（武汉）有限公司2018年校园招聘岗位，线上投递简历；2.登录博世华域转向系统有限公司校园招聘门户网站：http://bshy.zhiye.com/Campus 在线注册后填写简历并提交3. 校园宣讲会现场投递简历。'],
        '118885784': ['1.2-2万/月', '', '武汉-江夏区', '无工作经验', '本科', '招50人', '12-02发布',
                      '校招-软件测试工程师（网络安全、云计算，深圳） (职位编号：MJ000172)', '深信服科技股份有限公司',
                      '岗位描述：\n负责深信服集团母公司旗下虚拟化、云计算、安全产品的软件测试和质量建设工作；在这里，您可以深刻地了解客户的价值和场景，做好缺陷预防，从需求到编码预防缺陷的发生，甚至颠覆需求和设计，让产品方向正确，帮助产品成功；在这里您可以成为产品专家，性能测试专家，测试设计专家，测试架构师，好胆你就来！\n岗位要求：\n1、本科及以上学历，专业不限；\n2、至少熟悉一门编程语言；\n3、熟悉软件研发流程，了解软件测试理论和方法；\n4、除了基本的语言能力，其实我们更看重您得的知识面（网络、操作系统等）和动手能力，您或许并非某一方面的专家，但您接触面广，什么都会一些，愿意动手去尝试做不同的东西，这样的您，是我们最欢迎的伙伴。\n职能类别：软件测试\n',
                      '上班地址：南山区学苑大道1001号南山智园A1栋',
                      '一、公司简介\xa0\xa0\xa0\xa0深信服科技股份有限公司是专注于云计算／虚拟化、网络安全领域的IT解决方案服务商，致力于提供创新的IT基础设施云计算、网络安全建设解决方案，现深信服已成长为国内网络安全龙头，云计算业务成长为国内增速最快的厂商，私有云领域市占率前三。研发实力：公司目前拥有近5000多名员工，其中研发近2000人，每年销售收入的20%投入到研发，在全球已设立深圳、北京、硅谷3大研发中心，专注云计算、网络安全领域，交付的产品包含私有云、公有云、超融合、网络安全等解决方案。\xa0\xa0\xa0\xa0市场实力：公司连续15年保持高速增长，年均增长率近50%，近10年的营收增长超过300倍。目前，深信服在全球共设有55个直属分支机构，其中含国内地主要城市及美国、英国、中国香港、马来西亚、泰国、印尼、新加坡等国家和地区。公司云计算和网络安全产品正在被 24个国家部委、中国区域80%以上的世界500强、90%的省级以上运营商、TOP20银行等 40，000家用户使用。部份荣誉：连续两届被美国《财富》杂志评为“中国卓越雇主”；国内网络安全领域龙头国内私有云领域前三入围全球顶尖网络安全厂商，国内仅6家；入围全球网络安全创新500强，国内仅6家；连续6年获评德勤“中国高科技高成长50强”；连续9年获评德勤“亚太地区高科技高成长500强”；***批国家高新技术企业；国家火炬计划项目单位（国家科技部批准）；中央政府采购协议供货商中国国家信息安全漏洞库CNNVD技术支撑单位；中国反网络病毒联盟ANVA成员单位；连续五年被评为“国家规划布局内重点软件企业；”'],
        '106619673': ['1.2-1.6万/月', '五险一金|年终奖金|弹性工作|免费班车|专业培训|', '武汉-江夏区', '5-7年经验', '大专', '招2人', '11-20发布',
                      '软件测试工程师（高级）', '维书信息科技（上海）有限公司',
                      '1）根据项目需求文档和设计文档，对软件测试项目进行测试设计，编写测试方案；\n2）独立实施软件测试项目，独立编写测试计划、测试用例和测试报告；\n3）及时准确地对项目缺陷进行上报，并与开发人员等相关人员进行有效沟通，保证项目进度和质量；\n4）希望能够根据对项目需求的理解，提出功能测试之外的建议，如用户体验等方面；\n1）根据项目需求文档和设计文档，对软件测试项目进行测试设计，编写测试方案；\n2）独立实施软件测试项目，独立编写测试计划、测试用例和测试报告；\n3）及时准确地对项目缺陷进行上报，并与开发人员等相关人员进行有效沟通，保证项目进度和质量；\n4）希望能够根据对项目需求的理解，提出功能测试之外的建议，如用户体验等方面；\n\n任职要求：\n1）专科及以上学历，计算机相关专业毕业优先；\n2）5年左右软件测试经验；\n3）熟悉软件工程、软件测试流程和规范，精通常用测试方法和手段，熟悉常用的测试工具；\n4）熟悉性能测试、接口测试、Web端测试以及自动化软件测试；\n5）具有良好的沟通能力和团队合作能力；\n6）工作认真负责、积极主动，吃苦耐劳；\n7）具备良好的自学能力，对新技术、新方法充满兴趣；\n\n职能类别：高级软件工程师软件工程师\n关键字：功能接口压力\n',
                      '上班地址：武昌区徐东大街128号联发国际大厦18楼',
                      '维书信息科技（上海）有限公司维书信息科技（上海）有限公司是一家从事软件服务的高新技术企业，为制造业客户提供智能物流、智能工厂、物联网及大数据的解决方案。公司主要业务涉及供应链管理、物流可视化、终端客户及设备管理等方面。互联网的未来发展方向在大数据和物联网。目前，越来越多的传统企业意识到互联网化的重要性，期望通过大数据分析、智能物联等手段，进一步优化传统企业的产品研发、生产、物流及销售等各个环节，降低成本，提高企业的竞争力。维书信息致力于大数据及物联网，为传统的制造业客户提供智能物流、智能工厂、物联网及大数据的解决方案。维书信息一直本着以“注重人才、以人为本”的用人宗旨，力争为员工提供一个具有竞争力的薪酬和广阔的发展空间，让员工与公司共同成长。为实现我们共同的事业和梦想，我们渴望更多志同道合的朋友加入！在这里，您将拥有的不仅仅是良好的工作环境，更是置身于广阔的发展空间之中，在事业的舞台上挥洒我们青春和才智！如果您对未来充满梦想，对成功也充满渴望，那么请让我们携手同行，真诚合作，实现梦想，共创未来！'],
        '92210147': ['1-1.5万/月', '五险一金|员工旅游|餐饮补贴|专业培训|绩效奖金|年终奖金|高温补贴|豪华带薪年假|住房补贴|每年调薪两次|', '武汉-洪山区', '1年经验', '大专',
                     '招若干人', '11-11发布', '软件测试工程师', '武汉华锋惠众科技有限公司',
                     '工作职责：\n1、对客户所提出的需求进行分析，并记录分析过程中所发现的问题，然后和客户方进行协商解决，最终将原始需求整理为可用于软件开发的功能需求，供后续的功能开发使用；\n2、任务分配和进度跟踪：将需进行开发的功能分配给相应的开发人员，制定相应的开发完成计划时间表，然后对开发中所产生的问题进行跟踪、协商和解决，实时跟踪开发的进度，确保项目的进度不拖延，从而做到对项目总体进度的管控；\n3、针对开发完成后的功能进行功能测试（公司暂只要求黑盒测试），并即时的将问题提交至禅道指派给相应的开发人员，然后对解决的问题进行复测即可；\n4、根据测试结果撰写测试报告，包括测试范围、问题清单及状态、问题类型分析等；\n5、整理产品、项目升级包，并对升级包所包含内容进行说明；\n6、产品、项目升级后对升级效果进行跟踪，并提出改善意见；\n7、编写产品、项目的操作文档、FAQ文档，并进行整理归档。\n\n任职要求：\n1、本科以上学历，计算机、机械、汽车覆盖件模具等专业及其相关专业优先；\n2、无工作经验的应届毕业生亦可投递简历，但需配有成绩单、在校参与的活动和所获得各类奖项等；\n3、1年以上测试工作经验（无工作经验者，需：对测试工作感兴趣，逻辑思维严谨，语言表达能力良好，做事踏实、细心、能动性强、学习能力强者亦可）；\n4、能基本使用常用办公软件进行文本编辑，如word、execl、ppt；\n\n加分项：\na、有使用过UG/CATIA等三维设计软件着优先；\nb、有使用过Autoform和Dynaform等CAE软件着优先；\nc、有冲压工艺设计、能够进行曲面造型和熟悉模具结构者优先；\n\n公司薪资及福利体系\n五天八小时，双休；\n公司将按照国家规定为员工缴纳社会保险（养老、医疗、失业、工伤、生育）及住房公积金；\n各类节日、生日、带薪假、生育福利等；\n员工旅游；\n免费提供中午的工作餐（或以餐费补助形式发放）；\n强大的调薪机制以及年终奖福利。\n职能类别：软件工程师测试工程师\n关键字：测试工程师模具工程师模具结构设计需求分析\n',
                     '上班地址：武汉市光谷大道70号现代世贸中心F栋1805',
                     '武汉华锋惠众科技有限公司是为汽车与模具行业提供专业的工程软件产品销售和定制开发服务、冲压模具工艺与结构设计服务、SE工程服务的高新技术企业。目前主要从事冲压模具开发与设计以及相关的 CAD/CAE/CAM软件开发与销售、汽车整车开发阶段的SE工程服务，是目前国内同行业中具有较强竞争力的领先型企业。\xa0\xa0\xa0\xa0公司依托华中科技大学材料成形与模具技术国家重点实验室作为技术支撑，具有强大的市场竞争力。材料成形与模具技术国家重点实验室是我国在模具领域内***的***重点实验室，拥有30余名院士、教授、***等固定研究人员和400多名硕士/博士研究生组成的研发团队，先后承担了包括国家科技攻关项目、973、863、自然科学基金和国际合作等在内的200多项研究课题，并荣获***科技奖励3项、省部级奖励20余项，发表高水平学术论文1500余篇。实验室在CAD/CAE/CAM/ERP软件领域具有国际影响力，研发了一系列达到国际先进水平的软件产品，在国内外汽车、模具等行业拥有超过500家商业客户，累计创造经济效益超过30亿元。\xa0\xa0\xa0\xa0公司现为板料成形与模拟软件FASTAMP产品的总代理。FASTAMP系列软件，是***一款由国内自主研发并拥有完全知识产权的专业金属板料成形仿真系统。目前已经申请了14项软件著作权，并在国内主流汽车与模具企业得到了广泛应用，主要客户包括奇瑞汽车、江淮汽车、上海大众、广州本田、一汽模具、上海赛科利、成飞集成、东风模冲、天汽模及奇瑞瑞鹄等一线汽车与模具企业。\xa0\xa0\xa0\xa0公司现有一支规模超过20人的开发团队，核心成员学历均为硕士以上，核心成员从业经历超过10年，公司多年从事专业CAE软件开发，具备深厚的CAE分析理论基础和丰富的工程分析经验数据积累。可以提供汽车模具制造领域内的专业CAE工程分析。\xa0\xa0\xa0\xa0公司同时可以承接CATIA、NX、Solidworks、Pro/E等主流 CAD 平台的二次开发服务。目前已经在白车身设计、汽车覆盖件工艺设计、汽车覆盖件模具结构设计等相关领域，通过大量的客户化定制实践，积累了丰富的经验，可以快速响应不同客户的不同类型需求，为客户提供***的定制化服务体验。'],
        '116973099': ['', '', '武汉-洪山区', '无工作经验', '本科', '招若干人', '11-11发布', '软件测试工程师 (职位编号：00xz)', '移动设计院湖北分公司',
                      '一、工作内容\n1、编写软件测试计划、搭建测试环境；\n2、编写软件测试需求、软件测试用例；\n3、执行软件测试用例、记录测试结果；\n4、提交测试缺陷，跟踪缺陷关闭；\n5、协助测试团队管理工作。\n二、任职资格\n1、硕士研究生学历或211院校本科以上，计算机科学技术、软件工程等\n2、软件测试、计算机等相关专业专科或以上学历；\n3、熟悉测试理论方法及其原理；\n4、如有实际软件开发经验可优先录取；\n5、精通测试用例设计，掌握自动化性能测试方法；\n6、熟悉相关测试工具（QTP、LoadRunner）；\n7、具备较强的学习能力和良好的沟通能力；\n三、劳动合同签订单位\n中国移动通信集团设计院有限公司\n职能类别：软件工程师\n',
                      '职能类别：软件工程师', '移动设计院湖北分公司诚聘'],
        '117100199': ['1-2万/月', '五险一金|补充医疗保险|餐饮补贴|专业培训|年终奖金|定期体检|', '武汉-洪山区', '3-4年经验', '本科', '招10人', '11-08发布',
                      '高级软件测试工程师-六分科技', '武汉四维图新科技有限公司',
                      '此职位属于四维图新旗下分子公司——北京六分科技有限公司，base武汉\n职位描述\n1、根据测试需求、测试标准，执行测试工作，完成测试用例维护，提交测试报告；\n2、参与完成测试环境的搭建和维护，负责单元测试、功能测试、性能测试、系统测试等；\n3、能够准确地定位并跟踪测试问题，推动问题及时合理地解决；\n4、协助开发人员快速重现和解决产品BUG；\n任职要求\n1、本科及以上学历，计算机软件、通信、信息安全，电子及相关专业，3年以上测试经验；\n2、了解嵌入式软件测试流程，Linux平台应用测试，了解C、C++、Java中的至少2种语言；\n3、积极主动解决相关问题，细致认真，有责任心，有良好的合作性和沟通能力。\n职能类别：高级软件工程师\n',
                      '上班地址：光谷软件园',
                      '武汉四维图新科技有限公司（简称武汉四维）是北京四维图新科技股份有限公司（简称：四维图新，深交所股票代码：002405）在武汉设立的全资子公司，四维图新是中国领先的数字地图内容、车联网及动态交通信息服务、地理位置相关的商业智能解决方案提供商，始终致力于为全球客户提供专业化、高品质的地理信息产品和服务。经过十年多的发展，四维图新已经成为拥有八家全资、六家控股、五家参股公司的大型集团化股份制企业。作为全球第四大、中国最大的数字地图提供商，公司产品和服务充分满足了汽车导航、消费电子导航、互联网和移动互联网、政府及企业应用等各行所需。在全球市场中，四维图新品牌的数字地图、动态交通信息和车联网服务已经获得众多客户的广泛认可和行业的高度肯定。在数字地图领域，公司一直关注大数据时代地理信息数据的整合与发布，通过专注地理信息数据研发，建设地理信息数据云平台，持续深入挖掘数据背后的商业价值。四维图新数字地图已连续11年领航中国前装车载导航市场，获得宝马、大众、奔驰、通用、沃尔沃、福特、上汽、丰田、日产、现代、标致等主流车厂的订单；并通过合作共赢的商务模式在消费电子、互联网和移动互联网市场多年占据50%以上的市场份额，汇聚了腾讯地图、百度地图、搜狗地图、HERE平台、图吧地图、老虎地图、导航犬、天地图等上千家网站地图和众多手机地图品牌，每天通过各种载体访问公司地图数据的用户超过1.5亿。作为全球第三家、中国第一家通过TS16949（国际汽车工业质量管理体系）认证的地图厂商，率先在中国推出行人导航地图产品，并已在语音导航、高精度导航、室内导航、三维导航等新领域实现了技术突破和产品成果化应用。2012年成为目前全球唯一一家掌握NDS标准格式编译技术，提供NDS导航地图数据的公司，在未来争取与国际主流车厂的合作中占据有利地位。在动态交通信息服务领域，四维图新拥有中国覆盖最广、质量最高的服务体系，已建成北、上、广、深等三十余个主要城市的服务网络，高品质服务已连续五年7*24小时可靠运营。凭借在技术和市场的领先优势，依托全国最大浮动车数据平台，集成海量动态交通数据，四维图新可提供交通拥堵、交通事件、交通预测、动态停车场、动态航班信息等丰富的智能出行信息服务，成为中国动态导航时代的领跑者。在车联网服务领域，公司建立了面向乘用车和商用车的车联网应用服务体系，致力于成为国际级Telematics解决方案提供商及国内领先的Telematics服务运营商，全面参与车联网和Telematics的市场竞争。2011年，公司率先在国内推出品牌“趣驾”，依托模块化车联网服务云平台，为客户量身定制平台搭建、内容管理、导航服务、车联网运维及一站式服务解决方案，推动公司由内容提供商向内容和服务提供商转变。目前，公司已经或即将为丰田、奥迪、大众、沃尔沃、长城等国内外主流车厂的车联网项目提供服务，并已在2012年宝马智能驾驶控制系统（iDrive III）中搭载了“趣驾”的部分功能，这是四维图新车联网服务商用化的重要里程碑。依托北京、上海、西安、沈阳四大研发中心，全国35个本地化数据实地采集和技术服务基地，四维图新通过不断自主研发和创新，开发了具有100%自主知识产权的核心技术和工具软件，截至2012年底，已独立承担和参与30余项国家导航标准的编制，申请专利 292 项，已授权 63 项，申报软件著作权登记168项，国家产业化专项3个、863专项2个和核高基专项1个。经过十年来的努力，四维图新已经成为具有现代企业治理结构的多元股份制公司，逐步构建了适应国际竞争的企业管理制度和人力资源管理体系，公司的管理一直与最高水准的国际性企业对标，并通过上市，实现了企业管理上的全面提升。未来，公司将紧紧围绕国家战略性新兴产业的发展机遇，通过打造国内最好的综合地理信息云平台，进一步巩固在行业内的领先地位，借助现有优势快速获取核心技术，形成层次分明、布局合理和可持续发展的公司业务组合，谋取在地理信息服务领域的领先地位；并通过抓住物联网、新能源汽车、北斗导航系统等新兴产业的发展机遇，成为具有国际竞争力、国内最优秀的综合地理信息服务商。'],
        '109429357': ['', '', '武汉-洪山区', '3-4年经验', '本科', '招8人', '11-05发布', '智能驾驶软件测试工程师', '东风汽车集团有限公司技术中心',
                      '\n岗位职责\n\n1.负责智能驾驶系统软件的测试分析工作，负责搭建测试环境和自动化测试框架；\n2.负责智能驾驶软件单元测试方案和测试指标的编制和设计；\n3.负责配合开展智能驾驶软件SIL/HIL测试的工作开展；\n4.负责测试用例的设计和编码实现，负责智能驾驶软件自动化测试的实现，自动化测试脚本的开发、录制、调试、部署、执行；\n5.负责指导和配合开展整车集成测试工作，编制测试用例，整理测试结果制作测试报告\n6.负责分析定位失败用例的结果、配合开发进行优化与修复；\n7.负责根据测试数据与过程，进行分析并编写测试报告。\n\n\n\n\n\n学历：大学本科及以上\n外语要求：具备良好的英语听说读写能力\n工作经历：相关专业年限满3年\n专业背景：\n1.车辆、机电、软件及自动化控制等相关专业，有汽车电子开发背景优先；\n\n\n\n\n素质要求：\n1.具有较强的逻辑分析、判断能力；\n2.具有较强的项目推进能力；\n3.具有跨专业、跨部门沟通协调能力；\n4.具有较强的责任意识和学习能力；\n\n职能类别：汽车设计工程师\n关键字：动力总成试验\n',
                      '上班地址：湖北省武汉市经济技术开发区珠山湖大道663号',
                      '东风汽车集团有限公司技术中心（“东风汽车公司技术中心”）于1983年4月成立，是东风公司的产品开发中心、技术研究中心、技术管理中心，是国家发改委、财政部、税务总局和海关总署认定的国家 级"企业技术中心"，是国家科技部认定的国家一类科研院所，也是国内汽车行业首批国家 级"海外高层次人才创新创业基地"。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0技术中心主要承担东风自主品牌乘用车、军用越野车、新能源汽车、动力总成以及基础和先行技术研究等工作。截至目前，东风汽车公司技术中心共有各类技术人员2800余人，其中硕士研究生及以上学历1023人，高级工程师以上职称人员610人，海外高层次人才近30人，享受国务院政府特殊津贴专家14人，入选国家“千人计划”9人。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0技术中心始终坚持“改进一代、开发一代、预研一代”的产品开发方针，多次荣获国家科技进步奖和东风公司科技进步特等奖，为东风公司和中国汽车工业发展做出了重大贡献。2011年东风公司发布了“乾”D300计划，东风自主品牌汽车销量将达到300万辆，技术中心作为东风自主品牌乘用车产品研发的引领者，在集团“大自主、大协同、大发展”的战略框架下，被赋予了更重大的使命。技术中心将以加速提升乘用车、新能源汽车、动力总成和汽车电子技术研发能力，保持混合动力汽车和高机动越野车开发方面领先优势，促进技术研究、产品开发在国内处于领先地位为整体目标，为东风自主品牌事业发展提供强大的支撑。'],
        '114863528': ['', '', '武汉-洪山区', '无工作经验', '本科', '招若干人', '11-03发布', '软件测试工程师', '东风格特拉克汽车变速箱有限公司',
                      '\n\n岗位职责：\n\nresponsiblefortheSWtestingofseveraltransmissionplatforms\n\n多变速箱平台的软件测试工作\n\nCreate,updateandmaintaintestspecificationsandtestcaseslibrary.\n\n更新和维护测试规范及测试用例库\n\nFinishthetesttasksassignedfromtestleaderontime\n\n完成测试组长分配的测试任务\n\nSupportstheSWdeveloperbyfindingpossiblerootcauseforthefailedtests\n\n失败的测试，支持软件开发人员分析可能的根本原因。\n\nResponsiblefororsupportthewriteandreviewoftestreports\n\n负责或支持编制及评审测试报告\n\n\n\n\n\n任职要求:\n\nSeveralyearsofexperiencewiththeSWdeveloportestoftheautomotivemaincontrolunit\n\n汽车关键控制部件的软件开发或测试经验\n\nSeveralyearsofexperiencewithHiL(Hardware-in-the-Loop)-simulatorsandtestautomationrequired\n\nHIL测试及自动化测试经验\n\nFamiliarwithSWtestprocessandthetestcasedesignmethodsofblackboxtesting\n\n软件测试流程及黑盒测试用例设计方法\n\nBasicknowledgeofTransmissionandAutomotivestructureandprinciple\n\n变速箱和汽车构造及原理知识\n\nFamiliarwithdSPACE/ETAS/NIHILsystem,advancedproficiencyofdSPACEplatform\n\ndSPACE或ETAS或NIHIL系统，优先考虑有dSPACE平台使用经验者\n\nBetterwiththeusingexperienceofthefollowingSWtesttools:ControlDesk,PROVEtechTA,INCA,CANoe,VB/C/C++,etc.\n\n下软件测试工具使用经验:ControlDesk,PROVEtechTA,INCA,CANoe,VB/C/C++等等。\n\nPositiveandgoodatteamwork.\n\n向上，具有团队精神\n\nGoodcommandofbothoralandwrittenEnglish\n\n熟练掌握口语及书面英语\n\n\n职能类别：软件工程师汽车电子工程师\n关键字：汽车电子软件测试\n',
                      '上班地址：武汉经济技术开发区后官湖大道239号',
                      '东风格特拉克汽车变速箱有限公司（简称DGT）,是一家专业从事低扭矩、双离合器汽车变速箱（DCT）研发生产的中德合资企业，DCT代表当今全球最先进的传动技术。公司于2013年3月13日由东风汽车集团与全球最大的独立汽车变速箱企业德国格特拉克各出资50%组建，后者于2016年1月被全球知名的汽车零部件集团麦格纳全资战略收购。东风格特拉克以成为汽车变速箱行业引领者为发展愿景，致力为客户提供技术领先的高品质汽车变速箱产品，以不断满足愉悦驾驶和环保、节能、低碳排放的严苛要求。合资公司成立以来，将打造自主研发和先进制造能力作为优先战略，已快速形成T3级研发能力并向2020年达到T5级目标推进。制造方面先后通过了IATF16949:2016质量认证和ISO14001环境管理、OHSAS18001职业健康安全管理体系认证。目前，公司已开发DCT150和DCT200两款自动变速箱，并成功适配东风汽车集团和上海通用汽车公司等战略客户的众多车型。根据公司战略，东风格特拉克还将依托两家母公司的强大技术和品牌支撑，在不断提升传统汽车变速箱产品的同时积极向新能源汽车拓展，以适应未来更广泛的市场需求和汽车技术变革。作为一个面向行业和未来的高新技术企业，东风格特拉克奉行“诚信、责任、尊重、行必果”的核心价值和开放、合作、共赢的发展理念，将致力“为客户提供价值、为员工创造幸福、为股东获得利润、为社会贡献财富”的企业使命，潜心打造一个行业有地位，员工感自豪的技术DGT、品质DGT、绿色DGT、活力DGT、和乐DGT，不断为汽车事业的进步和利益相关方创造价值。'],
        '116927216': ['1-2.5万/月', '五险一金|交通补贴|餐饮补贴|通讯补贴|专业培训|绩效奖金|年终奖金|定期体检|高温补贴|补充医疗保险|', '武汉-洪山区', '无工作经验', '本科',
                      '招若干人', '10-17发布', '软件测试工程师', '中国移动通信集团设计院有限公司湖北分公司',
                      '一、工作内容\n1、编写软件测试计划、搭建测试环境；\n2、编写软件测试需求、软件测试用例；\n3、执行软件测试用例、记录测试结果；\n4、提交测试缺陷，跟踪缺陷关闭；\n5、协助测试团队管理工作。\n二、任职资格\n1、硕士研究生学历或211院校本科以上，软件测试、计算机等相关专业专科或以上学历；\n2、熟悉测试理论方法及其原理；\n3、如有实际软件开发经验可优先录取；\n4、精通测试用例设计，掌握自动化性能测试方法；\n5、熟悉相关测试工具（QTP、LoadRunner）；\n6、具备较强的学习能力和良好的沟通能力；\n三、劳动合同签订单位\n中国移动通信集团设计院有限公司\n职能类别：软件工程师\n',
                      '上班地址：武汉市',
                      '中国移动通信集团设计院有限公司(China Mobile Group Design Institute Co., Ltd.)，是中国移动通信集团公司直属设计企业，发展历史可以追溯到1952年，是国家甲级咨询勘察设计单位，中国工程咨询协会副会长单位,北京市高新技术企业。'],
        '114542733': ['', '', '武汉-洪山区', '无工作经验', '本科', '招若干人', '10-11发布', '软件测试工程师', '东风格特拉克汽车变速箱有限公司',
                      '工作职责:\nresponsiblefortheSWtestingofseveraltransmissionplatforms\n多变速箱平台的软件测试工作\nCreate,updateandmaintaintestspecificationsandtestcaseslibrary.\n更新和维护测试规范及测试用例库\nFinishthetesttasksassignedfromtestleaderontime\n完成测试组长分配的测试任务\nSupportstheSWdeveloperbyfindingpossiblerootcauseforthefailedtests\n失败的测试，支持软件开发人员分析可能的根本原因。\nResponsiblefororsupportthewriteandreviewoftestreports\n负责或支持编制及评审测试报告\n任职资格:\nSeveralyearsofexperiencewiththeSWdeveloportestoftheautomotivemaincontrolunit\n定的汽车关键控制部件的软件开发或测试经验\nSeveralyearsofexperiencewithHiL(Hardware-in-the-Loop)-simulatorsandtestautomationrequired\n定的HIL测试及自动化测试经验\nFamiliarwithSWtestprocessandthetestcasedesignmethodsofblackboxtesting\n软件测试流程及黑盒测试用例设计方法\nBasicknowledgeofTransmissionandAutomotivestructureandprinciple\n的变速箱和汽车构造及原理知识\nFamiliarwithdSPACE/ETAS/NIHILsystem,advancedproficiencyofdSPACEplatform\ndSPACE或ETAS或NIHIL系统，优先考虑有dSPACE平台使用经验者\nBetterwiththeusingexperienceofthefollowingSWtesttools:ControlDesk,PROVEtechTA,INCA,CANoe,VB/C/C++,etc.\n下软件测试工具使用经验:ControlDesk,PROVEtechTA,INCA,CANoe,VB/C/C++等等。\nPositiveandgoodatteamwork.\n向上，具有团队精神\nGoodcommandofbothoralandwrittenEnglish\n熟练掌握口语及书面英语\n\n职能类别：其他\n',
                      '上班地址：后官湖大道239号',
                      '东风格特拉克汽车变速箱有限公司是东风汽车公司与德国格特拉克国际公司共同出资于2013年3月成立，总投资1.95亿欧元。位于武汉市经济技术开发区。公司各项工作稳步推进，首款联合开发的低扭矩6DCT150双离合自动变速箱，是国际上开发的一款全新产品，双方共同拥有知识产权，在国际市场具有独占性，已于2016年4月在武汉顺利投产。首批签约用户包括东风乘用车、上海通用、神龙汽车等。东风格特拉克按照一次规划、滚动建设、产品分期导入的投资原则，规划到2020年实现产销45万台，吸收就业人员1800人。未来，东风格特拉克将建成年产100万台变速箱的能力和独立自主的变速箱研发中心。'],
        '115784264': ['', '', '武汉-洪山区', '无工作经验', '本科', '招若干人', '08-01发布', '软件测试工程师（武汉）', '上海联影医疗科技有限公司',
                      '工作职责\n1.参与研究、设计和开发高效的测试框架、测试工具、测试平台；\n2.参与推动持续交付全生命周期的落地施行；\n3.协助解决各产品线遇到的疑难测试问题。\n任职要求\n1.计算机相关专业，硕士及以上学历；\n2.熟练掌握C/C++/Java/python中的任意一种开发语言，具备较好的代码编写能力；\n3.掌握关系型及非关系型数据库的原理和基本操作；\n4.熟悉WINDOWS、Linux操作系统的基本命令，会常用的Bat或者Shell命令；\n5.掌握一般的软件研发流程，对敏捷开发有所了解者优先；\n6.逻辑思维清晰，沟通表达能力佳。\n\n职能类别：研究生\n',
                      '职能类别：研究生',
                      '联影医疗技术集团有限公司是一家全球领先的医疗科技企业，致力于为全球客户提供高性能医学影像、放疗产品及医疗信息化、智能化解决方案。公司于2011年成立，总部位于上海，同时在美国休斯敦、克利夫兰、康科德、波士顿和国内武汉、深圳、常州、贵州等地设立子公司及研发中心。联影拥有一支世界级人才团队，包括140余位海归科学家，500余位深具行业研发及管理经验的专业人士。目前，联影人才梯队总数达3600多人，其中40%以上为研发人员。截至目前，联影已向市场推出掌握完全自主知识产权的63款产品，包括全景动态扫描PET-CT（2米PET-CT）、“时空一体”超清TOF PET/MR、光梭3.0T MR、160层北斗CT、一体化CT-linac等一批世界首创和中国首创产品，整体性能指标达到国际一流水平，部分产品和技术实现世界范围内的引领。\xa0\xa0\xa0\xa0目前，联影产品已进驻美国、日本等全球18个国家和地区的3300多家医疗及科研机构，包括350多家***医院。2016-2018年，联影PET-CT及中高端DR在国内新增市场的产品份额持续3年位列***。基于uCloud联影智慧医疗云，联影结合移动互联网、云计算、人工智能、大数据分析等前沿技术，为政府、医院、科研机构和个人量身定制一系列云端智能化解决方案。2014年至今，联影助力上海、安徽、福建、贵州、湖北等19个省市的地方政府搭建分级诊疗体系，覆盖医院超过1700家，覆盖人群超过1亿。基于uAI智能平台，联影致力于打造“全栈全谱”的跨模态AI解决方案，贯穿疾病成像、筛查、随访、诊断、治疗、评估各环节，为医疗设备和医生赋能，让成像更好、更快、更安全、更经济，大幅提升医生诊断效率和精准度。2017年9月，联影以333.33亿元估值完成A轮融资，融资金额33.33亿元***，成为中国医疗设备行业***单笔私募融资。以“成为世界级医疗创新引领者”为愿景，“创造不同，为健康大同”为使命，联影正在构建一个以预防、诊断、治疗、康复全线产品为基础，以uCloud联影智慧医疗云为桥梁，以第三方精准医学诊断服务为入口，以大数据为智慧，由智能芯片与联影uAI人工智能平台全面赋能的全智能化医疗健康生态。通过与全球高校、医院、研究机构及产业合作伙伴的深度协同，持续提升全球高端医疗设备及服务可及性，为客户创造更多价值。'],
        '110061445': ['1-1.5万/月', '五险|交通补贴|餐饮补贴|通讯补贴|绩效奖金|年终奖金|加班费|', '武汉-硚口区', '3-4年经验', '大专', '招1人', '12-09发布',
                      '嵌入式软件工程师', '湖北地创三维科技有限公司',
                      '1、负责嵌入式软件项目的概要设计和详细设计工作，参与具体项目的方案设计；\n2、负责嵌入式软件项目的开发和调试工作，负责代码的单元测试和整机测试，配合硬件工程师及测试工程师进行调测；\n3、负责产品测试设备及监控、标定软件设计；\n4、编制规范的软件设计及开发文档，协助制度软件测试流程及产品测试流程；\n5、嵌入式产品软件的后期维护和支持。\n任职资格：\n1、26-35岁，男女不限，电力、电子或自动化控制等相关专业，本科及以上学历，3年以上工作经验；\n2、精通C语言；\n3、熟悉STM32,单片机开发，或嵌入式软件开发；\n4、熟悉有关步进电机控制的运动算法的优先考虑；\n5、熟悉Marlin,Repetier或其他3D打印机固件中的一款的优先考虑；\n6、熟悉FreertosUcos等操作系统的优先考虑。\n职能类别：嵌入式软件开发(Linux/单片机/PLC/DSP…)软件工程师\n',
                      '上班地址：简易路50号',
                      '湖北地创三维科技有限公司成立于2017年，是一家具有国资背景和深圳市创想三维科技有限公司联合成立的国有高新技术企业。公司主要从事3D打印机、3D扫描仪设计、研发、生产、销售等业务。公司总部位于湖北武汉，并在东莞、深圳、上海、山东、北京等地设有分公司。同时与多所高校建立产学研教学实习基地。业务遍及全球三十多个国家和地区，拥有丰富的OEM/ODM配合经验和高效严谨的配合机制，并通过中国著名品牌、ISO9001、CE、FCC、ROHS等多项专业认证。地创三维通过深入的调查研究、严格的生产管理、专业的技术服务，为客户带去满意度最高的产品。地创三维致力于推广3D打印技术，将继续秉承：“专业，专注，创新，品质”的品牌精神，践行客户至上的服务理念，持续提供稳定优质的产品和细致周到的服务，以产业布道者的精神让千家万户享受科技带来的便捷。'],
        '118919135': ['1-1.5万/月', '', '武汉-硚口区', '无工作经验', '本科', '招若干人', '12-09发布', '系统测试工程师', '武汉海兰信数据科技有限公司',
                      '岗位职责：1.负责公司智能船产品的系统级测试工作，包括物理测试环境搭建，自动化测试环境构建，测试用例设计与执行等工作；2.对算法领域建立测试体系和度量标准，推动其优化和完善；3.负责日常项目及需求测试，确保项目正常进行；4.参与技术架构设计和测试的评审工作，提出改进意见和可测试性建议；5.跨团队沟通和协作，推进整个项目的测试效率；岗位要求：1.计算机或航海相关专业本科及以上学历优先；2.5年左右软件测试经验，精通测试理论、测试策略、测试用例设计方法等相关测试技术；3.具备白盒测试或自动化测试框架等开发经验优先；4.具备丰富的大型复杂系统的测试经验，以及项目管理经验；5.熟练使用LoadRunner、jmeter等测试开发工具，熟悉java/PHP/Python等至少一种编程语言；6.有大数据平台开发或测试经验优先，有船舶综合导航相关产品测试经验优先；7.追求完美，良好的沟通能力和团队协作精神，严谨的工作态度与高质量意识；\n职能类别：系统测试\n',
                      '上班地址：东湖高新区国采中心', '武汉海兰信数据科技有限公司诚聘'],
        '117292478': ['', '', '武汉-硚口区', '无工作经验', '本科', '招若干人', '12-09发布', '测试工程师', '武汉光谷联合集团有限公司',
                      '本科及以上学历，计算机相关专业。\n职能类别：软件测试\n', '职能类别：软件测试',
                      '武汉光谷联合集团有限公司，香港上市公司名称为中电光谷联合控股有限公司（股份代码：00798.HK），简称中电光谷，公司组建于2004年，是香港联交所主板上市的产业园区运营集团。***大股东为中国电子信息产业集团（中央直接管理的国有特大型骨干企业）。\xa0\xa0\xa0\xa0作为产业资源共享平台，公司以全生命周期园区智能管理系统为基础，提供适合的科技产业园区投资、开发、招商、运营整体解决方案，为各类创新企业提供理想的办公、科研、生产场所和服务。搭建了产业投资、规划建设、招商运营、企业服务四位一体产业资源共享体系的业务结构，形成了全方位产业园区开发运营服务能力。\xa0\xa0\xa0\xa0目前，中电光谷拥有园区开发、建筑规划设计、建筑工程总包、装饰工程设计与施工、机电工程、物业管理等八个专业方面的一级资质。已在全国26个城市开发运营各类主题产业园30多个，运营面积3000万平方米，服务企业及各类技术创新机构逾6300家，园区就业人群超42万人。拥有软件园、金融港、信息港、物联港、生物城、科技城、芯谷、智谷、研创中心、创意天地等不同类型园区产品线体系。并组建多支产业投资基金，完成50余家科技企业的股权投资，形成以物联网、北斗应用、文创、军民融合为特色的产业生态。荣获1个***双创示范基地、6个***众创空间、3个***创新孵化基地等荣誉称号。\xa0\xa0\xa0\xa0未来，中电光谷将以“产城融合、军民融合、科技艺术融合、生产生活生态协调共生”的规划理念，以“换道超车、联合创新、产业生态”为发展战略，推动中电光谷发展成为中国领先的产业资源共享平台。'],
        '116650171': ['', '', '武汉-硚口区', '无工作经验', '本科', '招若干人', '12-09发布', '测试工程师（武汉）', '武汉中原电子集团有限公司',
                      '熟悉常用软件测试理论、方法、流程及规范，并具备一定编程能力；能熟练操作各仪器仪表；具备无线通信基础知识及一定电路基础；\n有通信电子类产品研发、测试经验者优先。\n\n\n\n\n职能类别：软件工程师算法工程师\n',
                      '职能类别：软件工程师算法工程师',
                      '武汉中原电子集团有限公司（国营第710厂），于1949年创建于上海，1957年内迁武汉，2011年搬迁至武汉“中国光谷”东湖新技术开发区。公司隶属于中国电子信息产业集团有限公司（CEC）控股子公司中国长城科技集团股份有限公司（上市公司，股票代码：000066），是一家大型高科技通信产业集团。公司主营业务涵盖高新电子、应用电子、电池能源，主要科研生产产品包括战术通信系统、战术通信装备、卫星定位导航、无人车、无人机、模拟训练/维修检测、通信装备附件、北斗应用、汽车电子、智能电网、锂一次电池、锂二次电池、铅酸电池等。公司分布在武汉和长沙两地，10家二级公司，现有员工4000余人，研发团队1000余人，拥有2个院士专家工作站和2个博士后科研工作站。公司70年历史，曾获得***发明奖300余项，质量银质奖，全国科技大会奖，国家、部、省、市各级科技进步奖150余项，是“全国质量工作先进单位”和“全国五一劳动奖”获得者，参与国家重大军事演习和重大工程以及阅兵保障，是国民经济建设和国防信息化主战场。'],
        '116644534': ['1-1.5万/月', '', '武汉-硚口区', '无工作经验', '本科', '招10人', '12-09发布', '硬件工程师', '武汉华中数控股份有限公司',
                      '1.负责产品硬件开发，包含技术调研、需求分析、方案规划、器件选型、图纸设计等；\n2.跟踪项目进度，编写产品开发过程中相关过程及技术文档；负责审核其输出；\n3.协助解决部门产品的技术问题，按阶段提交完整的设计输出，指导相关配套硬件、软件测试验证工作；\n专业要求：电子信息相关专业\n发展方向：电路设计工程师、嵌入式工程师、FPGA固件开发工程师\n\n\n职能类别：硬件工程师\n',
                      '职能类别：硬件工程师', '武汉华中数控股份有限公司诚聘'],
        '116467100': ['', '', '武汉-硚口区', '无工作经验', '本科', '招若干人', '12-09发布', '开发测试工程师（武汉）', '中望软件',
                      '岗位职责：1、根据软件设计需求制定测试计划，设计测试数据和测试用例，并执行提交测试报告；2、负责测试文档编写（测试计划、测试用例、测试报告、技术培训文档，帮助文档）；3、完成对产品的集成测试与系统测试，对产品的软件功能、性能及其它方面的测试；4、参与产品的需求开发；完成测试工具的定制开发或产品部分独立功能的研发。岗位要求：1、本科以上学历，计算机科学与技术、软件工程、机械工程及自动化等工科相关专业；2、熟练掌握C/C++编程语言，熟练掌握Windows平台下各种常用开发、调试工具及知识；3、熟悉软件测试的基本方法、流程和规范，可以独立完成测试分析和测试案例设计。\n职能类别：储备干部\n',
                      '职能类别：储备干部',
                      '1、公司简介广州中望龙腾软件股份有限公司（简称“中望软件”）是国际领先的CAD/CAM/CAE软件与服务提供商，是国内***同时拥有二维CAD，高端三维CAD/CAM及CAE完全自主知识产权的国际化软件企业，致力于为全球用户提供世界级技术水平的可信赖的CAD/CAM/CAE产品与服务，帮助用户以合理成本解决正版化的同时，借助可信赖的CAx解决方案，帮助企业提升综合竞争力。2、整体概况自1998成立至今，600+员工，筹备上市。总部广州，布局北京、上海、武汉、重庆，营盘南京、青岛，遥控佛罗里达、越南。3、技术、服务与产品技术：三大研发中心（广州、武汉、佛罗里达），超25年经验的世界级研发团队。服务：致力于为用户提供核心二、三维基础设计、行业专属设计、个性化定制及更多CAx拓展应用的整体解决方案。依托先进的CAD/CAM/CAE技术，中望软件可为广大院校提供创新工具、课程资源、师资培训、竞赛活动、创客空间等解决方案。产品：ZWCAD、ZW3D、CAD云服务、中望教育、中望仿真软件。4、全球发展客户涵盖国电集团、国投集团、中交集团、宝钢集团、中国船舶、中国移动、南方电网、华润地产、保利地产等；拥有15种语言版本的软件产品，畅销全球90多个国家和地区，全球合作伙伴超过260家，正版授权用户数突破90万。目前已与全国3000多所院校建立深层次合作，3万所学校注册3D创客教育社区，近1200万人次在使用中望教育产品；培训发展：* 新员工入职培训；* 在职一对一帮辅指导；* 专业技能培训；* 定向管理能力培训；* 外部培训机会* 出国培训学习机会福利简介：* 公司5天上班制，每天工作7.5小时，弹性上班制；* 免费提供午餐或餐补，下午茶点；* 购买五险一金额外购买商业意外险；* 从优的薪酬，全面的福利；文娱生活：* 每周组织羽毛球、篮球、足球活动；* 设立部门活动基金，定期组织团队活动及户外拓展；* 其他多种关怀员工的内部活动；* 崇尚快乐工作，快乐生活。'],
        '115821791': ['1-1.5万/月', '做五休二|周末双休|带薪年假|五险一金|绩效奖金|节日福利|专业培训|住房补贴|', '武汉-江岸区', '5-7年经验', '本科', '招1人',
                      '12-09发布', '测试经理', '武汉东天红数字科技有限公司',
                      '1、根据项目实际情况，制定和推进测试策略、测试计划和测试方法；\n2、参与项目需求和功能设计评审，保证产品的可测试性；\n3、参与测试效果评估和软件质量核查；\n4、通过测试相关流程、策略、方法和工具等创新，努力提升测试的质量和效率，完善公司测试流程；\n5、负责测试团队的组建和管理工作，带领团队完成产品的测试工作和质量保证，推动开发团队提高测试能力和认识。\n\n任职要求：\n1、计算机或相关专业，本科及以上学历；\n2、三年以上软件测试团队管理经验；\n3、熟悉各种测试工具和方法，具备良好的业务沟通和理解能力\n4、能独立建立部门的测试流程规范，具备对测试人员进行招聘，培训和指导的能力；\n5、熟悉快速原型法和迭代式开发法的相关管理方式。\n6、有高度的工作热情、积极性和责任心强。\n7、团队管理协作能力强，具有较强的独立工作能力和解决问题的能力。\n职能类别：软件测试\n',
                      '上班地址：湖北省武汉市江岸区新长江传媒大厦',
                      '竹叶山集团、思科瑞新资本、上海真祥、已在武汉注册成立武汉东天红数字科技有限公司，初始注册资本 1 亿元。新公司将作为未来事业的总部，立足湖北武汉，以此为平台，投入 50 亿元，进行全国范围内重点城市龙头二手车交易市场的并购整合，并以此为基础，导入科技属性的新服务，推动二手车产业整体革新升级，成为中国二手车产业创新领导者，引领二手车产业向标准化、智能化变革发展，打造汽车消费新文化。'],
        '117849157': ['1-1.5万/月', '五险一金|补充医疗保险|员工旅游|餐饮补贴|通讯补贴|专业培训|定期体检|年终奖金|', '武汉-洪山区', '3-4年经验', '本科', '招5人',
                      '12-09发布', '测试开发工程师(J10486)', '深圳市汇顶科技股份有限公司',
                      '工作职责:\n岗位职责：\n1.负责搭建和改进公司的自动化测试平台，提高产品自动化测试的覆盖度\n2.负责新产品测试需求梳理、测试方案设计、测试计划制定、执行\n3.负责测试工具或脚本的开发\n4.研究探索前沿测试技术，对团队成员进行技术分享\n任职资格:\n职位要求：\n1.电子信息、计算机、通信等相关专业本科及以上学历\n2.两年以上测试平台开发或者测脚本开发经验，有NFC/RFID、金融卡产品开发经验优先\n3.熟练掌握C/C++、Java、Python中的至少一种编程语言\n4.有强烈的责任心和主动性，热爱挑战和学习，具有良好的沟通能力和团队意识\n\n职能类别：软件测试\n关键字：自动化测试\n',
                      '上班地址：中部创意城',
                      '汇顶科技成立于2002年，经过持续的努力和技术积累，目前已经成为全球领先的人机交互技术与解决方案提供商。以“创新技术，丰富生活”为愿景，专注基于客户需求的创新。汇顶科技在包括手机、平板电脑和可穿戴产品在内的智能移动终端人机交互技术领域构筑了领先的优势。目前，产品和解决方案广泛应用在华为、联想、OPPO、vivo、中兴、酷派、魅族、乐视、HTC、金立、TCL、三星显示、JDI、诺基亚、东芝、松下、宏碁、华硕、戴尔等国际国内知名终端品牌，服务全球数亿人群。\xa0\xa0\xa0\xa0作为***高新技术企业和触控与指纹识别的全球领导品牌，汇顶科技重视核心技术的持续研发积累，坚信满足并超越客户需求是所有技术开发的源动力，陆续推出了拥有自主知识产权的多项全球领先技术，包括单层多点触控技术、Goodix-Link、IFSTM指纹识别与触控一体化技术等。这些先进的技术正通过性能卓越的芯片产品、完善的整体解决方案以及周到快捷的技术服务给各品牌整机终端注入勃勃生机。\xa0\xa0\xa0\xa0作为管理规范的股份有限公司，汇顶科技深刻理解客户的成功来源于创新的技术和卓越的产品，而这些均凝结着员工的汗水与智慧。汇顶科技致力于给员工提供施展才华的空间和舞台，促进员工能力的持续发展，帮助员工获得事业的成就，并通过员工持股的方式与员工共享发展成果。\xa0\xa0\xa0\xa0作为中国本土的高科技企业，汇顶科技积极承载可持续发展的社会责任。持续努力推动中国移动互联网产业技术前进，促进人机交互技术的革新，驱动中国制造转型为中国创造，助力中国创新型科技社会的进步。公司愿景：创新技术 丰富生活（Vision：Enrich Your Life through Innovation）公司使命：成为受人尊敬的世界一流的创新科技公司（Mission：To be respected world-leading innovative corporation）管理理念：以人为本，视员工为事业伙伴遵循科学，追求理性核心价值观：用心、团队、绩效、 创新企业荣誉：国家高新技术企业深圳市高新技术企业通过国际标准化协会ISO9001-2000质量体系认证\xa0薪酬待遇：\xa0\xa0\xa0正值公司高速成长之际，公司求贤若渴，高薪诚聘专业人才。一经录用，将提供具有行业竞争力的薪酬，并给予核心骨干人才诱人的股权激励。企业福利：1、五天7.5小时工作制：上午9:00-12:30，下午14:00-18：002、购买五险一金，解除您的后顾之忧 !3、额外购买人身意外保险，增加双重人身保障！4、提供中餐、晚餐以及点心，让您乐享工作！5、每年提供员工高额的、全面的健康体检，让您得到工作与健康平衡！6、缤彩纷呈的员工活动：年度旅游、户外拓展、社团活动、部门聚会活动、年度晚会等等，让您感受团队的温暖与力量！7、法定节假日之外的带薪假期：带薪年假。8、提供多元化的培训与在职进修机会，不断提升您的软硬实力！9、神秘的生日礼物、贴心的节日礼品、浪漫的结婚大礼包，给您惊喜连连！公司网址：www.goodix.com    简历投递：zhaopin@goodix.com公司总部地址：深圳市福田保税区腾飞工业大厦B座13层\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0海到无边天做岸，山登绝顶我为峰。汇顶正与合作伙伴一起，以澎湃的激情和无限的创造力投入到移动互联网迅猛发展的浪潮中，征服下一座高峰。'],
        '111462661': ['1.2-1.7万/月', '五险一金|绩效奖金|补充医疗保险|定期体检|', '武汉-洪山区', '3-4年经验', '本科', '招2人', '12-09发布', '全栈开发工程师',
                      '武汉天喻信息产业股份有限公司', '\n职能类别：高级软件工程师\n关键字：全栈前端后端\n', '上班地址：武汉市东湖开发区华中科技大学科技园天喻楼',
                      '武汉天喻信息产业股份有限公司(股票代码SZ：300205)注册资本4.3亿元，于2011年4月在创业板上市，是一家专业从事智能卡及相关附件产品、行业系统平台产品及解决方案为主营业务的高新技术企业，业务涉及数据安全、移动互联、支付服务、税务服务、O2O电商服务。作为公司支柱业务，数据安全业务目前涵盖了卡、系统、终端、服务，广泛应用于金融、通信、交通、政府应用等领域，以硬件安全、软件安全、体系安全保障国计民生各种领域的安全。天喻信息近年来先后成为国家创新型企业、国家发展规划布局内重点软件企业、软件收入前百家企业，国家火炬计划重点高新技术企业，湖北省首批创新型企业、湖北省高新技术企业、湖北省重点软件企业(已通过CMMI5)，湖北省首批计算机信息系统集成一级资质的企业，首批入选武汉市“黄鹤白云计划”和东湖新技术开发区“3551光谷人才计划”。截至到2014年12月底，天喻信息共申请123项国内专利，获得授权专利108项；国外申请专利2项，获得授权专利 2项；承担各级科研课题50余项，其中，国家课题15项，湖北省课题20项。企业使命：创造安全智慧的信息化生活。天喻信息为员工提供：（1）科学的考核体系、具竞争优势的薪酬制度！（2）“六险一金”（养老、医疗、失业、工伤、生育险、商业医疗保险及公积金）让员工无后顾之忧！（3）人性化的培训管理制度、一对一的指定帮助人让员工快速融入并成长！（4）法定节假日之外的带薪事假、年休假，让员工与家人共享美好生活！（5）户外拓展、旅游、体检、生日礼物、节日津贴等让员工体验家的温馨！请符合条件者将个人简历、学历证、学位证、身份证等复印件邮寄、传真或发邮件到所述地址。'],
        '110629762': ['1-1.5万/月', '周末双休|带薪年假|五险一金|绩效奖金|节日福利|年底双薪|福利体检|国内外旅游|新生代|福利补贴|', '武汉-江夏区', '5-7年经验', '本科', '招2人',
                      '12-09发布', '软件培训讲师', '武汉正厚软件技术有限公司',
                      '1．根据教学计划完成教学任务，不断优化课程教学方法和教学课程体系安排；\n2．解决学员提出的一些技术性问题，组织并指导学生完成项目实战。\n3.完成开学之前的班级准备工作；\n4.负责学员日常工作的管理，包括学员考勤的统计，请假单的收集整理，学员情绪反馈等日常管理工作；\n5．配合其他部门的工作：招生、就业面试的技术支持；协助企业服务部进行部分职业素质课程的教学工作，就业推荐工作以及收集学员详细信息。\n\n岗位要求：\n1.熟悉软件开发测试流程，能编写测试计划、设计测试方案、测试用例，有至少8年以上测试工作经验；\n2.掌握C/C++或JAVA，掌握SQLServer、Oracle、Mysql中任意一种数据库，有开发经验者优先；\n3.掌握自动化或性能测试理论，熟练使用QTP、Selenium、LoadRunner、Jmeter之一种，有相关自动化测试工作经验者优先；\n4.熟悉Linux操作系统基本命令；熟练使用脚本语言：Python,Perl,Shell，Ruby等任意一种；\n5.良好的沟通能力，细心，耐心；思考问题思路清楚，口头表达能力强。\n职能类别：培训讲师职业技术教师\n关键字：软件测试讲师测试工程师IT培训讲师计算机培训讲师培训讲师软件测试\n',
                      '上班地址：光谷金融港',
                      '正厚软件是一家综合性的软件公司，主营软件产品研发、专业技能提升、人力资源整合、就业平台专供以及高校专业共建等。经过行业十五年的沉淀和成长，南京正厚软件技术有限公司（简称：正厚软件南京中心）于2017年正式运营，注册资金1000万，总公司坐落于南京鼓楼区湖南路16号，面积1000+平方。2018年，武汉正厚软件技术有限公司（简称：正厚软件武汉中心）开始正式投入运营。公司自运营以来一直秉持「正己守道」、「厚德载物」之旨，以客户实际业务需求为导向，为客户提供完善的信息化应用解决方案，在软件行业赢得了良好的口碑和影响力。'],
        '116529612': ['1.2-1.5万/月', '周末双休|带薪年假|五险一金|节日福利|做五休二|', '武汉-洪山区', '5-7年经验', '大专', '招1人', '12-09发布',
                      'Java高级开发工程师', '上海通天晓信息技术有限公司',
                      '1.参与产品的架构设计，明确负责开发部分的设计需求\n2.按照设计要求和源代码编写规范编写程序代码，对其质量、性能负责\n3.编写相关技术文档，负责进行开发阶段的软件测试，包括：单元测试、集成测试\n4.产品上线后，保障运营平台的稳定，解决相关技术问题\n\n职位要求：\n1.计算机或相关专业，大专或以上学历，具有5年以上（不含实习）Java开发经验；\n2.有电商订单管理系统或者物流行业OMS/ERP相关经验优先；\n3.JAVA基础扎实，熟悉io、多线程、集合等基础框架、熟悉并精通制定各种网络协议，熟悉分布式、缓存、消息、搜索等机制，了解Groovy，Scala，Python等语言优先；\n4.熟练掌握SpringMVC，熟悉RestfulAPI设计与开发；\n5.熟练掌握JavaScript，熟悉CSS，了解B/S架构，了解HTTP协议；\n6.熟悉Sqlserver、Oracle、Mysql等主流数据库，对负载均衡有比较深的了解，精通MySql数据库，拥有较好的数据库设计能力；\n7.了解微服务，有SpringBoot经验优先；\n8.熟悉分布式缓存（Redis、memcached）、负载均衡（Lvs,Haproxy,Keepalive，Nginx中的任一）、消息（RabbitMQ,kafka,Active中的任一）、搜索（Solr，ElasticSearch）等机制者优先\n9.熟悉Linux环境以及操作，SVN，git的使用，熟悉Tomcat，Jetty，Nginx等开源的服务器，***使用过Jenkins，Docker\n10.具有较强的逻辑思维以及数据结构和算法基础，良好的编程风格，能快速学习和掌握新技术，具有强烈的责任意识和开放的心态，同时，事业心强，勤奋好学，有团队精神。\n职能类别：高级软件工程师\n关键字：JavaSpringMVCJavaScript\n',
                      '上班地址：喻路889号光谷国际广场B座1401室',
                      '上海通天晓信息技术有限公司(TTX) 2011年成立于中国上海，是一家由资深国内外软件专家和行业顾问组成的、致力于提升中国电商物流和供应链管理信息化水平的公司。公司自主研发的成熟的X-WMS仓库管理系统、X-BMS物流计费系统，Cybertrans平台以及X-AIS物流接口平台，能灵活满足电子商务、第三方物流、快速消费品、医药等客户的差异化需求以及企业对物流管理方面严谨、高效的追求，被广大用户广泛认同和采纳。公司自成立以来，仅几年的时间，就凭借专业行业技术、产品成熟稳定的性能，以及丰富的实践经验，跃居成为专业物流解决方案领域的佼佼者，拥有一大批如聚美优品、伊藤忠物流、顶通物流、汉维供应链、杭州悠可化妆品等行业领先客户。通天晓助力其在双十一等海量订单活动下取得了突出的成绩和效果，在业界享有盛誉，正如总经理吴煜先生受邀在中国电商与物流协同发展大会上的演讲称：“通天晓不只是卖产品，我们更注重服务，让客户感受到专业系统以外所带来的价值，并伴随客户不断持续增长！”“Technology to excellence”是通天晓（TTX）的口号，更是公司的理念与服务的宗旨，并已成为每一位通天晓员工的座右铭。同时，通天晓非常注重团队的培养与建设，我们始终认为，只有提供更广阔的发展平台、加强团队成员之间的协作精神，了解员工，关心、热爱他们，才能激发员工的潜能、发挥团队的能量。公司更注重员工的福利待遇，不仅薪资处于同行业领先水平，每位员工还将享受五险一金的缴纳、十天带薪年假、生日party、各种补贴、员工体检、员工意外伤害险、以及各种丰富有趣的外出旅游团建活动，应有尽有，绝对让你乐不停。'],
        '111883832': ['1.1-1.5万/月', '五险一金|补充医疗保险|通讯补贴|定期体检|餐饮补贴|弹性工作|绩效奖金|专业培训|', '武汉-洪山区', '5-7年经验', '本科', '招1人',
                      '12-09发布', '资深测试工程师(012618) (职位编号：digitalchina012618)', '神州数码（中国）有限公司',
                      '岗位职责:\n1、负责公司企业级wlan产品（AP、AC等）的项目测试工作。\n2、针对无线接入、负载均衡、网络优化等热点方向对产品进行测试\n\n任职资格:\n1、通信、计算机相关专业，本科以上学历。本科三年、硕士二年以上无线产品软件测试工作经验\n2、精通并熟练运用tcp/ip，MQTT，802.11，Vlan，NAT，IPV6等网络知识，熟悉网络抓包和数据分析\n3、熟悉无线通信产品硬件基带，射频，可靠性等测试原理和测试标准\n4、精通网络设备软件实现原理，测试方法和测试流程。擅长设计功能测试，集成测试，系统测试方案。\n5、熟悉使用至少1-2种自动化测试工具，如Postman，LoadRunner，JMeter等\n6、熟悉至少一种编程语言:C，Python，Shell，Java，Javascript等\n有以下技能者优先考虑：\n1、熟悉云产品测试\n2、有独立搭建无线测试实验室经验，对网络并发和稳定性保障有专业的设计经验\n3、有传输仪表/性能测试仪表使用经验者优先、能够使用无线测仪表优先\n职能类别：高级软件工程师\n',
                      '上班地址：光谷大道金融港光谷智慧园',
                      '2015年，为迎击“互联网+”时代浪潮，神州控股（00861.HK）出售分销和系统业务，神州数码集团正式独立起航。2016年4月，神州数码集团成功登陆A股，股票代码000034.SZ。神州数码集团始终秉承数字化中国的理想与使命，坚持持续创新，先后荣获***火炬计划重点高新技术企业称号、北京市高新技术企业称号、中关村高新技术企业称号，软件开发获得CMMI4级认证，软件服务水平通过ISO20000和ISO27001认证，并在北京和武汉建成两个大型研发中心，是北京市“十百千工程”中，四家千亿核心企业之一。神州数码集团一直是国内外产品技术以及服务的提供商在中国的重要合作伙伴，与300余家国际顶尖供应商展开精诚合作，并建成覆盖全国860个城市、30000余家渠道伙伴的中国***的IT营销网络之一，累计拥有超过4项***标准认证、150余项发明专利、100余项软件著作权认证以及超过500项解决方案，在为广大的消费者用户提供丰富的电子产品的同时，神州数码集团已累计为超过100万家中国企业提供信息化所需的产品、解决方案和服务。如今，全新的神州数码集团致力于在国家自主可控政策的指引下，充分利用互联网、云计算、大数据等新型技术，为中国广大企业用户和个人用户提供云到端的产品、技术解决方案及服务，打造中国***的IT领域新生态。神州数码集团将作为这一新生态体系的建设者和运营者，同时也是技术支持和服务的提供者，与全球顶尖供应商和众多合作伙伴聚合在一起，再次引领产业的变革。面向未来，神州数码集团将继续通过专业化与多元化的IT产品和服务，释放信息技术的力量，把信息技术价值转化为客户价值，推动中国信息化建设进程。人才理念"把个人的追求融入到企业的追求中去，倡导员工与公司共同成长"，是神州数码始终坚持的核心价值观，基于这样的企业文化，我们根据员工职业发展周期和规律的不同特点，把一个员工进入企业的发展分为三个阶段，帮助员工顺利完成三个阶段的转换，最终实现员工与企业共同成长。围绕这样一个基本理念，我们设计了"选、用、育、留、记"的完整的人才发展机制：\xa0选：德才兼备、以德为先十余年来，神州数码始终坚持寻找"志同道合的同路人"，我们的员工来自不同的行业与企业，既有社会人才、应届精英，更有从海外归来的技术专家与管理专家。用：发挥优势、追求卓越为了帮助每一名员工充分发挥与展现自己的能力，神州数码建立了清晰的岗位工作与业绩管理体系，提供便捷的经营运作平台、数字化的办公网络与充足的资源支持，使你们能够充分发挥自己的能力与潜力，一展所长。育：成长加油站神州数码始终相信企业的高绩效来源于员工的持续学习与发展，而给予你们充分的学习与培训是保证组织与个人能力提升的必要手段之一。因此，在你们每一个成长阶段，我们都准备了丰富多彩的培训课程，为你们的成长不断加油助威。留：公司因你而精彩神州数码希望每一个员工都能够在这个舞台上成就组织与个人共同的理想与目标，为此我们始终坚持"待遇留人、感情留人和事业留人"。记：成长轨迹神州数码相信，每一位员工取得的每一次成功与进步都是非常宝贵的财富，为了系统地记录与保存你们在神州数码的发展历程，我们帮助每一位员工建立了成长和发展的轨迹档案，使人才成为公司可以流动的最活跃、最有价值的共享资源。'],
        '119035668': ['1-2万/月', '五险一金|员工旅游|绩效奖金|弹性工作|年终奖金|定期体检|', '武汉-洪山区', '5-7年经验', '本科', '招1人', '12-09发布', '测试科长',
                      '电装光庭汽车电子（武汉）有限公司',
                      '任职条件：\n1.5年以上软件测试经验，有汽车仪表软件测试经验；\n2.能够独立的根据需求文档完成测试用例设计；\n3.熟悉软件测试流程并能在工作中严格遵守；\n4.能独立按计划完成测试任务并提交测试报告；\n5.熟悉仪表各个功能模块如表头，报警信息，行程电脑，诊断，网络管理等的测试；\n6.能熟练使用测试工具，如CAN工具、信号发生器、示波器、万用表、电阻箱等；\n7.能熟练运用CAN，总线相关知识，能使用CAPL语言编写测试脚本；\n8.有10人以上团队管理经验优先考虑。\n9.加分项：日语N2及以上级别。\n职能类别：软件测试\n关键字：汽车仪表测试\n',
                      '上班地址：湖北省武汉市东湖新技术开发区软件园中路4号光谷E城4号楼5F',
                      '企业简介：电装光庭汽车电子（武汉）有限公司，是一家由电装和光庭合资成立的，面向中国市场，集研发、生产、制造为一体的汽车电子企业，注册资本1亿人民币。公司致力于为中国市场的汽车厂商提供包括仪表、智能座舱等产品，后续也会进入其他汽车电子领域。公司本着结合电装的品质经验，以及光庭的研发速度和成本控制能力，为丰田等在中国的合资车厂，以及中国本土车厂提供适合中国市场的产品和服务。'],
        '116418678': ['1.2-2万/月', '', '武汉-江汉区', '3-4年经验', '大专', '招10人', '12-09发布', '测试工程师', '广州华钧软件科技有限公司',
                      '岗位职责：\n1、跟进并协调项目进度；\n2、负责测试环境的部署维护;\n3、协助测试主管分析测试需求；并设计有效的测试用例，根据具体情况，用多种手段进行项目测试，\n4、项目测试完成，负责发布测试报告；\n5、负责上线部署跟进。\n岗位要求：\n1、专科，计算机相关专业毕业，有3年的软件测试或开发经验；\n2、具有快速阅读代码的能力；\n3、熟悉数据库读写操作，熟悉SQL语句，使用过Oracle，SQLServer、mysql任意一种数据库；\n4、对软件测试感兴趣，富有责任心和工作激情；\n5、具备优秀的沟通和书写能力，具有较强的逻辑分析能力，有较强团队协作精神；\n6、掌握自动化、性能、安全性等工具者优先，如LoadRunner、qtp、jmeter、appscan、selenium等。\n7、对自动化测试有了解，熟悉使用自动化测试相关工具，有开发过测试框架经验者优先。\n职能类别：测试员软件测试\n关键字：测试工程师\n',
                      '上班地址：武汉江汉区青年路185号新业大厦',
                      '广州华钧软件科技有限公司是位于广州高新技术产业开发区的高科技软件企业 。 作为一家专业定位于教育信息化服务的高新科技企业，始终 遵循“以人为本，以产品开发为中心，以价值管理为手段，实现社会价值***化”的企业管理理念，为我国教育、学校、学生实现教育信息现代化而努力耕耘。基于我国教育业和教育的发展状况和实际需求，公司提供华钧教育与教育信息化建设全面解决方案： 包括教育软件、系统集成、校园网解决等教育信息化的基础建设；教育信息服务进校校通工程即解决教育信息化最后一公里问题；服务各级教育政府部门的信息化建设的 教育电子政务管理系统；提供教育信息化技术服务的校校通即服务系统；服务教育局、中小学校、教育机构、等教育服务单位的校校通系列解决方案等。广州华钧软件科技有限公司集中了一大批具有丰富计算机工作经验和教育知识背景的复合型高科技人员，其中硕士研究生及以上学历的占 40%，高级工程师占30%。 他们在广东省计算机学界权威人士的直接带领下，依托华南师范大学、广东工业大学等重点高等院校，借助国内外众多知名计算机软 、硬件厂商的密切合作，通过多年来教育应用管理项目的开发 积累了 丰富的教育信息化实战经验，对教育信息化建设精神有了更深刻的理解和认识，项目实施过程得到教育政府部门和中小学校的积极反馈和肯定。'],
        '118250096': ['1-2万/月', '五险一金|年终奖金|定期体检|免费工作餐|免费住宿|节假日福利|交通补贴|周末双休|', '武汉-江夏区', '1年经验', '本科', '招1人', '12-09发布',
                      '上位机软件工程师', '武汉元丰汽车电控系统有限公司',
                      '1.负责公司生产检测、实验标定及客户定制的上位机软件及界面开发；\n2.对软件测试和运行过程中出现的BUG进行分析和解决；\n3.维护和改进已有的软件项目，并完善相关规范化工作；\n4.负责上位机软件需求分析、架构设计、开发维护等软件开发全生命周期管理；\n5.完成上级交办的其它工作。\n\n能力要求\n1.英语四级以上，具有良好的英文阅读能力；\n2.了解Windows平台下的多线程开发技术,熟悉各种总线协议和通讯接口，如RS232、485、CANBus、TCP/IP等；\n3.熟悉软件开发过程中需求分析、概要设计、详细设计、代码编写、单元测试、集成测试、系统测试的各个环节及相应的技能要求；\n5.具备手机相关软件设计及优化经验者优先。\n职能类别：电子软件开发(ARM/MCU...)机械工程师\n',
                      '上班地址：武汉市东湖新技术开发区光谷大道299号',
                      '武汉元丰汽车电控系统有限公司成立于2007年2月，是一家专门研发和生产汽车制动防抱死系统（ABS）与电子稳定程序（ESC）的高新技术企业。公司注册资本5000万元，占地142亩，具备年产55万套的制造能力。公司立足于技术领先型企业发展路线，与清华大学汽车工程研究院合作成立“清华元丰汽车电控技术研究所”，为公司发展提供了强有力的技术保证。公司拥有自主知识产权的ABS和ESC，具有世界先进水平的调节器和控制器的设计和制造能力。元丰电控的宗旨是依靠高起点、高效率的制造系统，以民族品牌汽车为目标市场，在细分市场内确立领先优势，与国内主机厂共同发展、壮大，并最终实现民族品牌汽车、本土零部件占领中国汽车主流市场的目标。'],
        '118904543': ['', '', '武汉-东湖新技术产业开发区', '无工作经验', '本科', '招3人', '12-09发布', 'BIOS/EC测试工程师',
                      '诚迈科技（武汉分公司）—武汉诚迈科技有限公司',
                      '负责PC项目BIOS/EC测试\n\n职位要求：\n1、本科学历，3年以上BIOS/EC测试/开发经验\n2、能够看懂英文版本的BIOS/ECSPEC,器件datasheet,测试方案\n3、熟练使用Intel/AMD和第三方常见测试工具\n4、熟练使用RW工具查看，修改各种寄存器\n5、熟练使用80portdebugcard,串口线采集日志\n6、故障现场日志采集能力（BSODfulldump设置，BIOSROMdump，各种寄存器dump）\n7、基本的自动化脚本开发能力\n职能类别：软件测试测试工程师\n关键字：PCWindowsbios测试EC测试笔记本电脑\n',
                      '上班地址：:武汉东湖高新区高新大道武汉未来科技城C2-11楼',
                      '诚迈科技（南京）有限公司成立于2006年9月，2017年1月20日公司成功上市，是一家专业从事软件产品设计、代码开发、质量保证及技术支持等全流程服务的软件服务提供商，致力于提供全球化的专业软件研发服务，专注于移动设备及无线互联网行业软件研发及咨询等服务。诚迈科技总部位于中国南京。经过多年的发展，规模已超过2000人，在加拿大、芬兰及日本设立销售体系，在北京、上海、深圳、武汉、广州和西安设有分支机构，业务覆盖全球，在中国（内地及台湾）、北美、欧洲、日本、韩国等地广泛开展业务。Archermind Technology (Nanjing) Co. Ltd., established in September, 2006, was listed on the stock market on 20 January,2017,is a professional software service provider specializing in software product design, code development, quality assurance, technology support, etc.. The company is devoting to providing specialized world-wide software R&D service and focusing on R&D and consult service in the field of mobile facilities and wireless internet software. The headquarters of Archermind is in Nanjing. After four years’ development, the company has more than 2,000 employees, sales systems in Canada, Finland, and Japan and branch offices in Beijing, Shanghai, Shenzhen and Wuhan. Now, the company extends its service to lots of places in the world, such as China including mainland and Taiwan, North America, Europe, Japan and Korea.诚迈科技作为行业的领军者，在全球范围内为国内外客提供一流的软件研发和测试服务。专业的研发团队凭借多年的项目经验掌握了行业核心技术，可提供Android行业软件解决方案（车载系统、TV、eBook等）；移动互联网软件解决方案（浏览器、APP Store、运营商定制等）；云终端解决方案及企业应用和云计算解决方案。在嵌入式测试方面，诚迈科技专业的软件测试团队在测试方法、测试策略、测试标准方面有着丰富的经验，精通手机终端设备中的手机操作系统、手机应用软件等测试。目前，诚迈科技已经与世界级的客户建立了长期友好的合作关系，主要客户广泛分布于终端设备制造商、世界级芯片制造商、运营商及软件公司。As a leader in the field, Archermind is dedicating to provide top software R&D and test service to domestic and oversea customers. The professional R&D group who have years’ project experience, have professional core technology and can provide total solution for Android software (Car System, TV, eBook, etc.); for mobile internet software(Browser, APP Store, Custom Operators, etc.); and provide solution for cloud terminal, enterprise application and cloud computing. On the aspect of embedded test, the software test groups are experienced in test method, test strategy and test standard. They are proficient in test of mobile operating system and mobile application software in mobile terminal equipment. Now, Archermind has established long-term cooperative relationship with world-class customers, who are from the top terminal equipment manufacturers, chip manufacturers, operators and software companies.如果您崇尚奋斗，渴望创新，并希望同公司一起成长，请加入我们的团队，您可以应对不同的挑战，以激发个人潜能。我们将长期提供多方面的发展机会，并对成绩突出的员工给予职位晋升和物质奖励。If you like striving, innovation and growing up with the company, please join us! Here you have the opportunity to meet different challenges to motivate your potential. We will provide kinds of development opportunities. If you work hard and outstandingly, we will give you promotion and rewards.您还将享受完善的员工福利制度，包括：弹性工作时间，各项激励奖金，养老保险，医疗保险，失业保险，工伤、生育保险，住房公积金，员工俱乐部，各种员工活动，员工心灵关怀和健康关怀计划，特别节日假期，带薪年假，集体户口（如需要）等。You can also benefit from the employee welfare system, which includes flexible working time, pension insurance, medical insurance, unemployment insurance, industrial injury assurance and maternity insurance, housing fund, employee club, a variety of employee activities, employee spiritual care and health care programs, particularly holidays, paid annual leave, collective household  account(if need), etc..处于高速发展和扩张期的诚迈科技诚邀有志之士与公司同仁一起共创一个伟大的软件企业！Archermind, who is in the period of rapid development and expansion, sincerely invites the ones who are looking forward to create a great software industry with the us.公司网址：www.archermind.com若您希望在以下城市工作，可按以下邮件地址投递：南 京：hr@archermind.com武 汉：hr_wh@archermind.com上 海：hr_sh@archermind.com深 圳：hr_sz@archermind.com北 京：hr_bj@archermind.com广 州：hr_gz@archermind.com'],
        '103118891': ['1-2万/月', '五险一金|员工旅游|餐饮补贴|绩效奖金|定期体检|专业培训|年终奖金|', '武汉-东湖新技术产业开发区', '1年经验', '本科', '招3人', '12-09发布',
                      'Software engineer', '苏州联讯仪器有限公司',
                      '1.参与功能需求定义及评估，并配合测试工程师执行SVT/DVT．\n2.针对项目需求定制化开发及维护产品固件firmware．主要针对光模块产业链应用,产品涵盖光模块/光器件老化测试系统,高速误码仪,高速示波器等产品.\n3.代码规范化管理,参与制定/执行测试方案和用例．\n4.协助开发人员快速重现和解决产品功能问题及缺陷．\n5.负责研发资料,测试文档,自动化测试案例及报告撰写．\n职位要求：\n1.大学本科以上学历，计算机/电子工程/通信工程/软件工程专业．英语4级以上．\n2.3年以上工作经验，优秀应届生也可，具备ARM/C51平台开发经验,熟悉主流IDE环境开发,如Eclipse/KeilMDK/IAR等.\n3.具有一定的上位机软件开发经验,能够独立开发简易的产品测试人机界面．\n4.精通C语言编程,熟练掌握C++/C#编程。光通信行业产品开发经验优先考虑.\n5.熟悉Labview/Python编程优先考虑．\n6.良好的团队协作意识，严谨的工作态度,较强的学习能力。\n\n职能类别：软件工程师高级软件工程师\n关键字：软件工程师软件测试研发工程师软件开发测试工程师C++C#\n',
                      '上班地址：苏州高新区湘江路1508号1号楼',
                      '苏州联讯仪器有限公司（Stelight Instrument）成立于2017年，由一批从事光通信技术研究多年的研发团队创办，致力于光通信测试设备的研发、生产、销售与服务,包括高速误码仪，采样示波器，光谱仪，可调光源，数字源表，高速数据采集卡，芯片老化测试系统等，并提供包括测试硬件及软件系统整体方案，是一家集科研、设计、制造、销售、服务为一体的创新型企业。公司先后获批苏州高新区科技创新创业领军人才、苏州市姑苏创新创业领军人才、苏州高新区重点创业团队、江苏省民营科技企业、优秀科技人才工作企业等荣誉称号。\xa0\xa0\xa0\xa0“创新，将新技术转化为生产力”是联讯仪器的核心竞争力。公司拥有专业的研发和管理团队，在上海设有研发中心，在华南、华东、西南、台湾等地设有分销点，技术支持和服务覆盖国内主要区域，以做到对客户需求的快速响应，迅速满足市场不断涌现的新需求，凭借对高频测试设备和光通信行业的深刻理解，将独特的产品理念和丰富的产品开发经验相结合，帮助全球客户实现低成本、高效率、高性能、高度集成和自动化的系统测试目标。 公司产品快速抢占国内市场的同时，还远销美国、中国台湾等地区，在行业内已发展成为国内外具有影响力的光通信测试整体解决方案供应商之一。\xa0\xa0\xa0\xa0Stelight Instrument的愿景是通过全体成员不断完善和自身奋斗，成为世界一流的测试设备制造商。我们注重企业和员工职业发展的同步成长，为员工提供能充分发挥个人能力和价值的平台，倡导以人为本和合作共赢的管理理念。我们用心、努力作好每一件事，满怀信心迎接每一次挑战。欢迎您加入Stelight Instrument！工作时间：9：00-5：30，双休，享有五险一金、节假日福利、年度健康体检、旅游、年终奖等。'],
        '115549137': ['1.2-2万/月', '五险一金|交通补贴|餐饮补贴|专业培训|绩效奖金|年终奖金|定期体检|', '武汉-东湖新技术产业开发区', '5-7年经验', '本科', '招1人',
                      '12-09发布', '测试主管', '武大吉奥信息技术有限公司',
                      '岗位职责：\n1.负责建立有效的测试流程，持续推进测试流程的优化；\n2.负责搭建测试环境，保证测试环境的独立和维护测试环境的更新；\n3.负责测试的技术体系建设与维护，以及团队技能培养，如：自动化测试、性能测试、安全测试等；\n4.对现有产品进行性能或安全性测试，并能进行结果分析；\n5.测试团队日常工作的管理、监督测试团队的工作，并进行人员培养。\n任职要求：\n1.统招本科及以上学历，硕士优先；5年或以上测试工作经验，从事GIS、云计算和大数据行业测试经验者优先；\n2.软件知识结构全面，通晓软件工程、软件测试理论、方法和过程；\n3.熟悉主流操作系统及数据库，熟练使用sql语句，熟练使用相关测试工具(Jmeter、LR、gTest、jUnit、jenkins、selenium等)；\n4.较强的文档撰写能力，完成测试计划、测试设计、测试报告等文档；\n5.良好的分析能力，表达能力和综合协调能力，且能有效解决问题；\n6.有丰富的测试团队管理经验。\n职能类别：质量管理/测试主管(QA/QC主管)\n',
                      '上班地址：东湖新技术开发区大学园路武大科技园吉奥大厦',
                      '武大吉奥信息技术有限公司成立于1999年，是武汉大学科技成果转化企业。作为中国领先的地理智能、大数据技术研发及服务企业，公司拥有20年地理信息实践与管理经验，业务体系涵盖自然资源、城市治理、智慧城市和军民融合等行业领域。目前公司在北京、江西、广西、广州、深圳、西安、无锡等地设立了分支机构，服务区域遍布我国29个省及400多个县市。\xa0\xa0\xa0\xa0\xa0\xa0公司拥有业内领先、自主可控的GIS产品—“吉奥之星”系列软件，以地理信息基础平台GeoGlobe、地理智能服务平台GeoSmarter、云管理平台GeoStack三大产品为核心，构建云生态的产品应用服务体系，聚焦城市大数据治理，致力于成为时空大数据治理的领航者。\xa0\xa0\xa0\xa0\xa0未来，武大吉奥坚持以客户为中心，秉承“挖掘数据价值，服务数字中国”的理念，建立以业务驱动协同化、数据驱动平台化的双轮驱动模式，打造大数据治理的新引擎。公司实行每天8小时工作双休制，一经录用，我们将为您提供：一、完备的福利措施1.社会保险（养老、医疗、失业、工伤、生育）2.住房公积金3.车贴、餐贴4.集体出游、年度体检5.各种贺礼、慰问金6.国家法定节假日、带薪年假、带薪病假7.婚假、产假以及围产假、丧假……二、健全的培训机制1.培训体系：新进人员培训、专业技能类培训、综合素质培训、管理类培训、外部培训和进修；2.培训形式：内训、派外训练、在职进修；3.公司鼓励并且组织员工参加各类认证考试、相关培训，考试等费用均由公司承担；4.对于员工自行参加的各类认证考试，符合公司奖励政策的，还可另行奖励。三、完善的职业晋升通道公司构建完善的员工职业发展通道，鼓励员工从管理、专业技术等多个方向进行选择性地职业发展，建立包括企业后备接班人、后备干部、后备梯队在内的企业内部不同层次的人才培养机制，鼓励员工积极进取，将个人的职业发展与企业的发展进行有效地结合。公司地址：武汉东湖新技术开发区大学园路武大科技园吉奥大厦 (邮编：430223)公司官网：http://www.geostar.com.cn'],
        '116535741': ['1-1.5万/月', '水果早餐|补充医疗保险|绩效奖金|定期体检|专业培训|', '武汉-洪山区', '3-4年经验', '本科', '招若干人', '12-09发布',
                      'SDK测试工程师(J10320)', '北京腾云天下科技有限公司',
                      '工作职责:\n1．负责SDK产品的日常迭代工作\n2．负责测试方案设计、计划制定、跟踪实施及测试优化\n3．在项目中发现线下/线上问题并进行分析，探索更多测试手段提升研发/测试整体质量和效率\n任职资格:\n1．本科及以上计算机或相关专业学历，1年以上SDK测试经验\n2．熟练掌握Appium、并能熟练使用至少一开发语言完成自动化脚本的开发，熟悉Android/iOS/H5/小程序开发者优先\n3．熟悉自动化测试和终端常用测试工具，对互联网软件开发、测试过程、项目把控具有丰富的实践经验，有较强的沟通协作能力\n4.熟悉软件开发测试流程和规范，具备扎实的测试常识，有良好的质量和风险意识\n5．有较强的逻辑分析能力和学习能力，有较强的测试敏感度，有强烈的责任心和团队精神\n职能类别：软件测试\n',
                      '上班地址：新发展大厦',
                      'TalkingData 成立于2011年，是国内领先的第三方数据智能平台。借助以SmartDP为核心的数据智能应用生态为企业赋能，帮助企业逐步实现以数据为驱动力的数字化转型。我们的愿景TalkingData 成立以来秉承“数据改变企业决策，数据改善人类生活”的愿景，逐步成长为中国领先的数据智能服务商。以开放共赢为基础，TalkingData凭借领先的数据智能产品、服务与解决方案，致力于为客户创造价值，成为客户的“成效合作伙伴”，帮助现代企业实现数据驱动转型，加速各行业的数字化进程，利用数据产生的智能改变人类对世界以及对自身的认知，并最终实现对人类生活的改善。企业责任感TalkingData不仅专注于数据智能应用的研发和实践积累，同时也在积极推动大数据行业的技术演进。早在2011年成立初始，TalkingData就组建了数据科学团队，将机器学习等人工智能技术引入海量数据的处理、加工流程中。通过几年来的不断发展，TalkingData已在大数据、人工智能领域拥有多项国家专利。此外，TalkingData还开源了大规模机器学习算法库Fregata、UI组件库iView、地理信息可视化框架inMap等项目，在海内外得到广泛支持与认可，使用者和贡献者遍布全球。目前TalkingData设立了包括硅谷边缘计算实验室、人本实验室在内的多个大数据、人工智能实验室，并与MIT媒体实验室、斯坦福人工智能实验室、加州理工航天技术实验室等国际顶尖学府、研究机构展开合作，共同加速大数据、人工智能相关技术的探索和演进，并将国际前沿技术引入高速发展的中国市场，与国内丰富的应用场景相结合，驱动新技术的落地应用与行业的飞跃发展。'],
        '117782126': ['1-2万/月', '五险一金|交通补贴|年终奖金|员工旅游|绩效奖金|带薪年假|', '武汉-洪山区', '5-7年经验', '本科', '招1人', '12-09发布',
                      '软件工程师（AUTOSAR）', '华砺智行（武汉）科技有限公司',
                      '1.基于AUTOSAR标准使用相关工具设计软件架构，完成V2X基础软件配置；\n2.完成应用层软件、算法层软件、协议栈底层驱动的集成；\n3.负责撰写软件架构设计详细文档，并给出软件测试方案。\n岗位要求：\n1、熟悉汽车电子软件开发流程；\n2、精通嵌入式C软件编程；\n3、熟悉了解ISO26262相关规范；\n4、有过ECU单元、网关等零部件AUTOSAR软件开发经验优先；\n5、熟悉UDS诊断及DTC相关协议（ISO14229/ISO15765/ISO15031）等优先考虑；\n苏州高铁新城/武汉\n\n职能类别：高级软件工程师\n',
                      '上班地址：经济技术开发区神龙大道18号太子湖文化数字创意产业园创谷启动区B101号',
                      '华砺智行（武汉）科技有限公司是一家专业从事智能网联汽车智能终端、智能交通行业应用的高新技术企业，在无线通信、协议栈、SDK软件开发包、交通应用、云平台等方面具有国际先进水平的研发实力。公司致力于打造车联网运营的智能基础设施平台，为智能驾驶、智慧城市提供软硬件综合解决方案。公司经营理念：为客户创造价值，让员工展现价值，与合作伙伴分享价值。公司核心团队成员来自美国斯坦福大学、加州大学伯克利分校、清华大学、华为等国内外著名高校和知名企业，拥有车联网通信设备、智能交通系统的丰富研究和工程实施经验。公司采用国际化运作方式，提倡高效协同融洽的工作氛围，在这里能为每一位成员打开新的视野。秉承“开放、共享、迭代”的文化理念，注重把员工的个人的职业生涯规划与企业的发展相结合，并以“让出行更智慧”为愿景，不断坚持技术创新。公司坐落于武汉经济开发区美丽的南太子湖畔旁，毗邻地铁站与购物中心。一经录用，您将获得有竞争力的薪酬待遇和完善的员工福利，包括：年终奖金，五险一金，例行体检，集体旅游，法定休假。联系HR:027-84218656邮箱：hr@huali-tec.com'],
        '118458453': ['1-1.5万/月', '', '武汉-洪山区', '无工作经验', '本科', '招30人', '12-09发布', '研发工程师', '桂林长海发展有限责任公司',
                      '\n\n算法工程师：信息对抗、通信电子类专业；熟练掌握matlab编程；熟悉常用的雷达工作体制及工作原理，有雷达信号处理经验，熟悉跟踪、分类与识别等算法。\n\n软件工程师：计算机类、电子信息类专业；方向：Java、C++、数据库设计、WEB前端、UI美工、手机APP、软件测试。\n\n电路工程师：信息对抗、电路与系统、通信电子类专业；熟练掌握电子对抗知识，有较强的电路分析与设计能力；具有硬件设计经验，掌握Protel、DXP等电路设计软件。\n\n天线工程师：电磁场与微波技术、天线与电波等专业；具备扎实的电磁场、微波技术、天线设计的理论基础；掌握HFSS、CST、FEKO等一种或多种电磁场仿真能力，具有宽带天线设计经验者优先；掌握天线测试方法及相关仪表的使用。\n\n简历投递邮箱：675926900@qq.com\n职能类别：高级软件工程师通信技术工程师\n关键字：电子通信软件\n',
                      '上班地址：广西桂林市长海路3号',
                      '桂林长海发展有限责任公司位于山水甲天下的国际旅游名城——桂林市，公司占地面积1200余亩，注册资金1.9亿元，是央企中国电子信息产业集团（全球500强）的重点二级企业。\xa0\xa0\xa0\xa0公司秉承“致力军工，心系员工，造福社会”的企业宗旨，致力于发展我国国防科技工业。公司以军工电子产品为主业，同时大力发展民品业务，涉及船用视频监视和闭路电视系统、天气雷达产品、智能安防产品等广阔领域，力争在“十三五”期间成为国内一流军工电子企业。在生产经营稳步发展的同时，公司坚持“以人文本”的管理理念，关心人才、尊重人才，为人才成长特别是年轻人才的成长提供了良好的工作、生活环境，为各类人才提供发挥聪明才智、展现青春风采的平台。\xa0\xa0\xa0\xa0我们竭诚欢迎有识之士加盟，与我们一起在军工企业的大舞台上施展才华，成就我们共同的理想与事业！\xa0\xa0\xa0\xa0我们确信，长海因为有您而骄傲，您将为加入长海而自豪！电话： (0773)2691496邮箱：675926900@qq.com'],
        '116865207': ['1-1.5万/月', '五险一金|餐饮补贴|交通补贴|绩效奖金|年终奖金|定期体检|员工旅游|', '武汉-江夏区', '5-7年经验', '大专', '招1人', '12-09发布',
                      '测试工程师', '武汉福禄网络科技有限公司',
                      '岗位职责：\n1.负责项目的所有业务流程，对于已上线的功能要做到比产品经理还要熟悉，能解答需求方、产品提出的各种疑问\n2.快速学习新业务流程，尽可能全的考虑各种业务场景，快速进行用例的设计\n3.针对项目有自己的见解，能够参与项目的整体方案讨论，给出合理建议\n4.熟练掌握测试方法，独立完成项目的整体测试，给出评估报告\n5.根据测试进展，合理分配时间，安排好测试项目的具体进程\n6.带队制定测试计划、测试策略，领导团队成员一起按时保质的完成测试\n7.对生产环境发现的问题，能快速准确的定位问题级别，分析问题的产生原因，配合开发快速给出合理的应急措施\n8.遇到较严重的问题或风险及时向上级汇报\n9.完成领导安排的其它工作任务\n\n任职资格：\n1、IT相关专业本科以上学历；\n2、5年以上企业应用软件测试经验；\n3、精通B/S应用的测试；熟悉测试流程、Bug管理流程；\n4、掌握软件测试理论、测试方法及测试规范，具有软件功能测试/黑盒测试/移动端测试等方面的经验；\n5、有Android/IOS的测试经验；有自动化测试、性能测试、接口测试、Python经验者优先；\n6、工作认真负责，有耐心，具有敏锐的思维能力，良好的沟通能力和团队协作精神。\n\n上班时间：9:30-18:00；周末双休\n职能类别：系统测试软件测试\n关键字：自动化性能测试接口测试Python\n',
                      '上班地址：光谷金融港B27栋16楼',
                      '【关于福禄】福禄网络（武汉福禄网络科技有限公司）是中国领先的虚拟服务提供商。面向C端，提供便民充值服务，覆盖通信、游戏、视频、音乐、音频、知识付费、阅读、生活八大品类，几乎涉足日常文娱生活所需的一切；面向B端，提供充值技术支持、营销与大数据服务等增值服务，帮助企业创新服务，深挖用户价值。多元化先发布局已经形成规模效益，打通上下游产业链的服务能力形成强壁垒。近十年锤炼发展，福禄年交易额超百亿，累积独立用户达2亿，受到腾讯、阿里巴巴、百度、完美世界、盛大游戏、巨人网络，及招商银行、农业银行、移动、联通、电信等上千家客户的青睐。目前，福禄正深度探索B2B虚拟增值服务，以在充值、营销、大数据等领域形成完整的价值链。【员工成长】优秀平台，和一流人才同行福禄网络目前拥有超过400名小伙伴，其中技术、运营、产品等岗位骨干成员来自腾讯、阿里、华为等一线大厂，拥有丰富的行业经验，欢迎有梦想、有热情的你加入我们。福禄网络服务于腾讯视频、爱奇艺、滴滴、喜马拉雅、招商银行等众多行业TOP级企业，在这里，你可以接触一流的人才队伍和丰厚的行业资源。真正扁平化管理，让工作简单我们倡导简单高效的工作方式、结果导向的工作机制。没有低效率无结果的公司会议，也没有新人专背的职场黑锅。在这里，用能力衡量价值，有才华的你一定不会被埋没。丰厚福利，不是说说而已我们还拥有行业内具有竞争力的薪酬，完善的五险一金、宽松舒适的办公环境和各种福利补贴，绝不会让认真工作的你受到亏待。【产品介绍】福禄开放平台福禄开放平台是福禄网络依托十年虚拟服务行业沉淀，打造的全产业链虚拟增值服务平台，致力于帮助企业创新服务，深挖用户价值，带来真实业绩增长。整合虚拟充值、游戏服务、营销、大数据等优势资源，福禄开放平台深度服务行业上下游，在上游为互联网内容商提供渠道分发、电商运营、知识产权保护等服务，在下游帮助流量渠道企业提升流量变现、用户运营效率，助力企业客户创造新的业绩增长点。福禄充值App——话费流量特价快充神器一款基于移动端的充值app，支持各大运营商话费充值、热门大型客户端游戏和手游、页游、网娱，致力为用户提供更优质更便捷的充值体验。福禄网游数卡专营店——福禄网络天猫旗舰店福禄旗下电商店铺，专注虚拟充值服务，年交易额超百亿元。【相关链接】公司官网 http://www.fulu.com/福禄开放平台 http://open.fulu.com/微博 @福禄网络微信  福禄网络/福禄微招聘招聘邮箱 zhaopin@fulu.com'],
        '112492792': ['', '', '武汉-江夏区', '3-4年经验', '本科', '招若干人', '12-09发布', '功能测试工程师', '九江银行股份有限公司',
                      '岗位职责：\n1.负责组织项目测试，编制测试计划，分析制定测试策略，测试用例设计及组织用例评审，缺陷深入定位跟踪及解决，协助开发分析解决问题；\n2.跟进项目迭代、推进测试进度；\n3.能对测试流程进行改进，提高测试效率、测试覆盖和质量。\n任职条件：\n1.初始学历为全日制本科（不含定向委培、专升本）及以上，计算机相关专业；\n2.年龄32周岁及以下(1987年1月1日后出生)，特别优秀者可适当放宽年龄条件\n3.具有4年及以上功能测试相关工作经验；精通测试理论及测试用例设计、白盒黑盒测试方法；熟悉oracle数据库、websphere中间件；掌握并熟悉java、python等至少一种编程语言\n4.同等条件下，具有银行核心系统、支付系统、渠道等测试工作经验者优先。\n职能类别：软件测试系统测试\n',
                      '上班地址：光谷大道77号光谷金融港B13栋',
                      '九江银行创立于2000年11月18日，总部位于江西省九江市，目前下设广州、合肥、南昌等13家分行和广东自贸试验区南沙支行、九江辖内33家直属支行，主发起设立20家村镇银行。截止2018年12月，系统网点达到300余家，资产总额突破3000亿元，在江西省乃至全国银行业金融机构中具有良好的品牌形象和竞争优势。2018年7月10日，在香港联合交易所主板成功上市。在2018年英国《银行家》杂志发布的组织排名中跃居372位，中国银行业中排名第62位。九江银行已发展成为一家充满活力的区域性股份制上市银行。'],
        '116336958': ['1-1.8万/月', '做五休二|周末双休|五险一金|绩效奖金|全勤奖|节日福利|专业培训|通讯补贴|', '武汉-江夏区', '无工作经验', '本科', '招1人', '12-09发布',
                      '飞控算法工程师', '易瓦特科技股份公司',
                      '岗位职责：\n1、负责飞控系统建模仿真、优化设计、测试验证和硬件集成，以及数据分析等工作；\n2、负责组合导航算法设计，包括多传感器数据表决融合、位置姿态估计等；\n3、负责飞行控制算法，包括导航制导解算、避障路径规划、自动驾驶仪、位置姿态控制、内环增稳控制、控制分配、故障重构等；\n4、负责控制系统测试和验证，包括模型测试、软件测试和硬件测试，虚拟闭环和半实物仿真验证，并配合系统联调和试飞；\n5、负责飞控系统适配到相应的无人机型号，并排查和解决可能遇到的问题；\n6、负责整理撰写相关设计方案、设计报告、论文专利，形成详细技术文档；\n7、参与无人机型号协作开发和技术交流，以及无人机的总体设计和论证；\n\n任职资格：\n1、本科及以上学历，自动控制、控制工程、导航制导、飞行器设计、飞行力学、飞行仿真等专业，对飞行器、控制理论和组合惯导有深刻理解和应用，具有飞控开发经验者优先；\n2、熟悉飞行动力学基础，了解常用飞行传感器、四元数旋转、六自由度运动方程、操纵性稳定性、飞行器总体设计等；\n3、熟悉GNSS/INS导航原理，掌握传感误差标定与补偿等算法，熟练运用EKF滤波进行多传感器表决融合和位置姿态估计；\n4、熟悉飞行控制原理，掌握线性控制、滤波器设计、自抗扰控制、智能控制、自适应鲁棒控制、动态逆和控制分配、系统模型识别、稳定性分析等；\n5、熟练运用Simulink/Stateflow进行控制系统建模仿真，了解基于模型设计流程，包括建模仿真、测试验证、代码生成和嵌入集成等；\n6、具备较强复杂C/C++代码阅读和修改能力，能够顺利阅读英文资料以及英语口语交流；\n职能类别：算法工程师\n',
                      '上班地址：江岸区兴业路石桥一路6号科技创业中心2号楼1层',
                      '易瓦特科技股份公司成立于2010年，是世界领先的民用无人机系统制造商，自主研发了全系列无人机产品，业务涵盖产业链各环节，包括无人机系统研发、生产、销售、培训、技术与飞行服务等，综合实力位居行业前列。现拥有中国第一家无人机驾驶员培训学院，以及在建的全球最大民用无人机研发生产基地。公司固定翼无人机、多旋翼无人机和大载荷无人直升机等产品已广泛用于新闻影视、物流配送、农林植保、婚庆旅游、警用消防、国土测绘、能源巡检、电力巡线等10多个领域，并不断融入新的行业应用。以市场为导向，以智能创造为根本理念，易瓦特组建了一只极富开拓精神的国际化团队，吸引了一批来自北美、欧洲及本土的顶尖人才。并在美国、中国香港分别设立分公司，以迅猛而稳健的步伐迈向国际市场。“智创无限可能”，易瓦特以开创航空领域技术革命为远大目标，以科技创新为生产力，以为客户提供一流产品与全方位优质服务为己任，向着更远大的目标扬帆起航，共创共赢美好未来。'],
        '78817674': ['1-1.8万/月', '五险一金|补充医疗保险|补充公积金|员工旅游|餐饮补贴|专业培训|年终奖金|定期体检|', '武汉-洪山区', '3-4年经验', '本科', '招4人',
                     '12-09发布', '嵌入式软件开发工程师', '深圳市有为信息技术发展有限公司',
                     '岗位职责：\n1、能根据项目需求独立完成程序设计、文档编写以及代码编写、调试、自测等工作；\n2、与项目团队和管理团队紧密配合，良好的沟通理解能力，确保产品高质量成功交付；\n3、完成产品的开发及相关文档编写工作，确保开发工作按时保质完成。\n\n岗位要求：\n1、具备扎实的嵌入式开发基础及C/C++基础，熟练掌握嵌入式开发环境和调试技巧，3年以上工作经验；；\n2、熟悉linux/android系统开发；\n3、熟悉软件测试策略、方法及流程，能独立完成测试方案、测试计划、测试用例与实施；\n4、良好的文档编写能力，能够编写开发文档、用户手册与测试文档；\n5、良好的沟通与协调能力，良好的团队合作意识及责任感；\n6、有算法开发、移植经验的优先\n7.善于沟通，能承担较大工作压力。\n职能类别：软件工程师高级软件工程师\n关键字：C语言开发嵌入式软件linux系统\n',
                     '上班地址：光谷大道金融港B22栋401室',
                     '深圳市有为信息技术发展有限公司成立于2005年，注册资本4000万，公司长期专注于卫星定位车载无线通讯监控管理系统的研发、生产、服务，在卫星定位车载无线通讯产品和系统方面有着深厚的技术沉淀，拥有独到领先的技术产品和最为广泛的市场应用。\xa0\xa0\xa0\xa0十多年稳定的研发核心团队，严谨的科研态度，厚积薄发致力于打破行业缺乏创新的格局。在车载卫星定位监控、汽车行驶记录仪、多媒体移动监控、行业管理平台软件系统领域全面出击，倾心打造“有为信息”的行业质量口碑。\xa0\xa0\xa0\xa0作为卫星监控行业最早从事卫星定位车载无线通讯监控管理系统软硬件产品研发、生产和技术服务于一体的国家高新技术企业，公司拥有核心的自主知识产权，在无线通讯模块、车载卫星定位无线终端和多媒体汽车行驶记录仪方面具有一定的领先技术优势，能够为用户提供从产品设计，二次开发、产品生产和售后服务全套的服务。\xa0\xa0\xa0\xa0有为信息拥有现代化的生产基地，多条生产线和全套车载终端产品综测设备。按照现代企业的要求，建立了完善的质量管理体系，通过了国际ISO9001:2008质量体系认证和ISO/TS16949:2009质量体系认证。\xa0\xa0\xa0\xa0有为信息坚守“技术先行、质量为本”的原则，获得“中国卫星导航产业十佳产品供应商”、 “ITS产品金狮奖”、 “公共交通信息化推进优秀供应商”、“中国优秀方案提供商”、“深圳市优秀软件企业”、“中国智能交通30强企业”、“交通运输行业最受欢迎车联网品牌产品”、“全国交通运输企业诚信品牌”、“中国卫星导航和位置服务十佳产品供应商”、 “推动产业发展杰出贡献奖”、“北斗行业应用示范奖”等奖项。\xa0\xa0\xa0“合作、诚信、创新、发展”是公司始终秉持的经营理念 。本着“质量、共赢”的服务宗旨，我们致力于为用户提供技术先进、性能一流、质量可靠、价格合理、服务完善和信誉优异的产品和技术服务。\xa0\xa0\xa0“有为者·有位”欢迎各位有识之士加入有为信息!\xa0\xa0\xa0\xa0公司具备完善的福利体系，具体有：\xa0\xa0\xa01、全面的保险保障\xa0\xa0\xa0\xa0六险一金：\xa0\xa0\xa0（1）我们为员工量身定制了完善的保障计划，其中包含：购买五险（养老保险、医疗保险、工伤保\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0险、失业保险、生育保险）+一金（住房公积金）；\xa0\xa0\xa0（2）为保障员工的人身安全，我们为其购买商业意外保险；\xa0\xa0\xa02、竞争力的薪酬\xa0\xa0\xa0（1）年终奖金；\xa0\xa0\xa0（2）每年及时调整薪资政策，已保证具有竞争力的薪资水平；\xa0\xa0\xa0（3）全勤奖励、中餐补贴、加班餐补；\xa0\xa0\xa0（4）各类荣誉、奖励及激励（如优秀员工、优秀新人、优秀团队等）；\xa0\xa0\xa03、踏实的传帮带文化\xa0\xa0\xa0\xa0促进新人积极融入公司文化及工作节奏、流程，公司实行导师引领方式，倡导传帮带文化；\xa0\xa0\xa04、带薪休假\xa0\xa0\xa0\xa0我们为员工提供人性化的福利休假：婚假、产假、陪产假等，另法定假日：春节、清明、五一、端\xa0\xa0\xa0\xa0午、中秋、国庆、元旦均按国家政策要求放假；\xa0\xa0\xa05、定期的健康体检\xa0\xa0\xa0\xa0为了保障员工的身体健康，公司定期会组织员工进行全面体检；\xa0\xa0\xa06、丰富的后勤保障\xa0\xa0\xa0\xa0生日礼品/party&节日慰问礼品；\xa0\xa0\xa07、多彩的员工活动\xa0\xa0\xa0（1）员工俱乐部：公司成立了各种俱乐部，旨在丰富员工生活，提高员工生活品质。包括篮球、足\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0球、羽毛球、乒乓球、瑜伽等；\xa0\xa0\xa0（2）公司每年组织旅游；\xa0\xa0\xa08、落户深圳\xa0\xa0\xa0\xa0为符合深圳入户政策及公司落户政策的员工办理落户手续。'],
        '116064076': ['1-1.4万/月', '五险一金|股票期权|定期体检|年终奖金|餐饮补贴|通讯补贴|员工旅游|周末双休|带薪年假|节日福利|', '武汉-洪山区', '3-4年经验', '本科', '招1人',
                      '12-09发布', '高级硬件测试工程师', '任子行网络技术股份有限公司',
                      '1、负责产品的质量保障工作，制定测试计划、测试方案、测试用例，以及相应的执行和质量评估工作；\n2、保证被测系统的质量，并通过测试流程和方法创新，努力提升产品质量和交付效率；\n3、跟踪定位产品中的缺陷或问题，与项目相关人员就业项目进度和问题进行沟通；\n任职要求：\n1，具备通信背景，熟悉网络设备或者通信设备的基础知识，熟悉基本的网络知识，熟悉TCP/IP的基础知识，熟悉常见的网络协议，如HTTP、FTP等。\n2，熟练操作linux系统，会使用常用的linux命令进行安装软件、配置网络、查看日志等。\n3，熟悉LTE核心网组网架构，熟悉核心网信令接口业务过程。\n4，熟悉软件测试方法和流程，能根据项目实际情况提高测试效率。\n5、会编写自动化脚本；执行自动化优先；\n6、熟悉分组交换、TCP/IP、VoIP等通信标准和协议，熟悉以太网交换机、路由器等数通类产品中的一种或几种，熟悉网络知识能够熟练应用思博伦、IXIA等公司的数通类测试仪表，能够熟练使用抓包工具，有数通类产品实际测试工作经验者优先录用，有运营商选型招标测试经验者优先录用；\n职能类别：其他\n',
                      '上班地址：武汉光谷软件园F3栋11楼',
                      '任子行网络技术股份有限公司（以下简称任子行,证券代码：300311）成立于2000年5月，注册资金2.99亿元，是中国最早涉足网络信息安全领域的企业之一，致力于为国家管理机构、运营商、企事业单位和个人网络信息安全保驾护航。成立十余年，任子行在深圳、北京、武汉建立4大研发基地，参与多项国家公安部、工信部等部委网络信息安全行业标准的制定，拥有40余项信息安全核心技术，承担30多项网络安全重大课题研发，拥有130多项行业准入资质，获得200多项重大荣誉，具备网络审计与监管领域最全产品线和解决方案。作为国内领先的、拥有完全自主知识产权的网络内容与行为审计和网络监管解决方案综合提供商，被业界誉为“网络应用审计专家”。'],
        '109397800': ['1-1.5万/月', '五险一金|专业培训|周末双休|加班少|出国机会|定期体检|员工旅游|年终奖金|', '武汉-江夏区', '无工作经验', '本科', '招1人', '12-09发布',
                      'Mobile APP 自动化测试', '博彦科技股份有限公司',
                      '1.3年以上自动化经验，2年以上手机App自动化测试经验。\n2.精通Android/iOSApp自动化测试\n3.熟练使用Appium等自动化测试工具\n4.能够搭建和维护手机App自动化测试框架\n5.熟练使用Java或者Python\n6.熟练使用数据库\n7.良好的沟通能力\n\n8.较强的学习能力\n职能类别：软件测试\n关键字：IOSAndroidapp自动化\n',
                      '上班地址：武汉市江夏区光谷大道金融港A9棟',
                      '博彦科技（深交所上市公司：002649）是亚洲领先的全方位IT咨询、服务及行业解决方案提供商。全球三大洲的六个国家设有超过30个分支机构和交付中心，具备全球范围的交付能力和灵活多样的交付方式。深厚的行业专长和成熟的行业实践，国际化的精英团队和完善的人才管理，完备的全球化交付和无缝的客户服务网络'],
        '118969247': ['1-1.5万/月', '五险一金|补充医疗保险|员工旅游|餐饮补贴|年终奖金|定期体检|弹性工作|', '武汉-洪山区', '无工作经验', '本科', '招5人', '12-09发布',
                      '系统测试工程师', '博为科技有限公司',
                      '岗位职责:\n1.负责测试嵌入式宽带终端产品，产品支持10GPON，VOIP、IPTV和WiFi等功能；\n2.负责测试相关文档、测试用例的编写工作，以及测试流程的制定；\n3、负责海外招标测试；\n3.负责测试系统的搭建，业务的测试，以及测试问题和测试报告的输出；\n4.分析测试中出现的问题并提供解决方案；\n5.为开发和产品维护团队提供技术支持；\n任职要求：\n1.具有E/GPON、VOIP、Wifi,交换机中的一项或多项经验，熟悉宽带接入技术以及相关应用场景；\n2.熟悉以太网相关的业务（Vlan,Qos,IGMP），并且有相关的测试经验；\n3.能熟练使用TestCenter，SmartBits，Ixia，Abacus等测试仪器。；\n4.有终端WiFi测试经验，且熟悉WiFi6技术者优先；\n5.有在电信领域3年以上的测试工作经验；\n6.较好的英语说、写能力；\n\n7.大学本科及以上学历，通讯，电子或计算机等相关专业毕业。\n职能类别：软件测试\n',
                      '上班地址：汤逊湖北路33号华工科技园创新基地9栋3楼',
                      '博为科技有限公司是一家致力于研发提供下一代超高速光纤以及无线智能宽带互联网接入终端解决方案的研发型高技术互联网企业。公司集产品设计、研发、生产、销售为一体，产品和解决方案主要面向北美、南美、欧洲以及亚太等中高端市场，最终客户涵盖政府、金融、商业企业等企业光网络市场客户、电信运营商客户（高速互联网宽带光纤接入市场以及移动高速微基站数据回传市场）。公司具有较强的核心技术竞争力，注重为客户提供差异化竞争需要的产品和解决方案，同时也是行业中少有的具有全方位研发设计生产能力，以及能够独立研发下一代10G及40G超高速光纤接入产品和解决方案的领先宽带智能终端公司。Bowei Technology Company Limited (“BFW Solutions” or “BFW”) is a high-tech company dedicating ourselves to develop the next generation Internet Broadband Access CPE solutions, including high-speed fiber access, smart technologies and wireless technologies.    Our business covers design, development, manufacturing, marketing and sales.  Our products and solutions target mid to high end market in North America, South America, Europe and Asia Pacific.  In the enterprise optical LAN market, our products and solutions are deployed in government, corporate, financial institutes and etc.  In the Telecom market, they are used in network providers’ Fiber To The Home access and mobile backhaul markets.  We differentiate ourselves, from the competitors, in our strong R&D capabilities and services.  We emphasize in developing customized products and solutions for our customers.  Meanwhile, we are one of few companies in this market to provide complete solutions to our customers, including developing the next generation 10G/40G fiber access and smart products and solutions.'],
        '62584854': ['1-1.5万/月', '五险一金|通讯补贴|餐饮补贴|', '武汉-东湖新技术产业开发区', '3-4年经验', '本科', '招1人', '12-09发布', 'GNSS算法工程师',
                     '湖北高通空间技术有限责任公司',
                     '工作职责：\n1.GNSS高精度定位算法研究工作；\n2.GNSS理论的软件实现工作；\n3.GNSS算法软件的日常维护工作；\n4.GNSS算法软件测试工作。\n\n职位要求：\n1.测量工程，自动控制或相关专业本科生以上学历；\n2.精通C/C++，熟悉.net或java语言；\n3.熟悉GNSS精密定位定轨理论；\n4.有工作热情，勇于挑战难题；\n5.有独立的解决问题能力，较强的沟通能力；\n6.有GNSS算法软件开发经验者优先。\n\n公司地址：武汉市东湖高新技术开发区华师园路5号华师科技园2号楼2楼201号\n公交站点：810（华丽环保工业园站）、902或732（顾庄村站）\n职能类别：数据通信工程师\n',
                     '上班地址：华师园路5号 华师科技园2号楼2楼',
                     '湖北高通空间技术有限责任公司（以下简称湖北高通），始终坚持以自主研发、技术创新作为企业的核心竞争力，致力于发展信息数据采集、传输、分析处理技术，是集产品研发、生产、服务于一体的高新技术企业。湖北高通常年专注地理信息监测领域，紧密结合应用需求，在GNSS核心技术的基础上，集成了地质灾害、气象、水文、大坝等多元数据的采集与处理技术，拥有多项软件著作权和专利，并能根据用户需求量身定制全面、系统的管理方案。\xa0\xa0\xa0\xa0湖北高通与武汉大学、中国地质大学（武汉）、三峡地区灾害与环境协同创新中心等单位建立了紧密的合作机制，主要产品和服务涵盖高精度测量型GNSS接收机、GIS数据采集终端、环境综合因素采集设备、水质监测系列设备、形变监测系统以及相关软件应用开发；产品广泛应用于国土、水利、交通、电力、数字城市、国防、环境监测及综合治理等诸多领域。'],
        '103064461': ['1-1.5万/月', '五险一金|年终奖金|带薪年假|专业培训|餐饮补贴|弹性工作|交通补贴|绩效奖金|', '武汉-东湖新技术产业开发区', '2年经验', '本科', '招2人',
                      '12-09发布', '电力电子软件工程师', '武汉海亿新能源科技有限公司',
                      '\n岗位职责：\n1、进行燃料电池系统用中大功率DC/DC变换器底层软件功能开发；\n2、基于DC/DC电路及开环传递函数设计闭环控制算法并仿真验证;\n3、C或C++语言编程及基于系统建模工具进行的控制功能开发;\n4、编写软件需求分析书及设计任务书，完成软件设计；\n5、模块功能调试、软件测试、运行维护及项目现场调试；\n6、项目文件资料编写和专利申报相应工作；\n7、撰写技术文档，指导、培训相关生产工艺环节，为其他部门提供技术支持。\n8、对产品需要的某项技术进行专项研究与开发。\n\n任职资格：\n1、电力电子基本知识，了解中、大功率（≥10kW）DC/DC变换器与DC/AC逆变器基本拓扑结构及工作原理；2、有中、大功率（≥10kW）DC/DC变换器实际项目控制算法设计及仿真经验；\n3、熟悉TI公司28系列DSP的编程，FPGA/CPLD开发，熟悉VerilogHDL语言；\n4、从事过燃料电池变换器、电动汽车充电桩、风力变流器以及光伏逆变器等项目优先，具备中、大功率变换器或逆变器的调试与开发经验；5、有3年及以上DC/DC、DC/AC电源、变频器等产品的开发工作经验者优先；\n6、熟悉电力电子产品研发和生产全过程，能够把握行业技术发展趋势和业务发展动向，对关键技术有自己独到的见解。\n\n\n职能类别：电力工程师/技术员软件工程师\n',
                      '上班地址：东湖新技术开发区关山大道598号',
                      '武汉海亿新能源科技有限公司创立于2017年，是一家致力于新能源氢燃料电池系统、燃料电池汽车整车动力系统技术平台和相关电力电子产品的研发和产业化的高科技初创企业。海亿新能由留美电子工程海归博士、长期从事燃料电池系统和汽车动力系统的著名大学教授和国内知名高新产业投资专家等联合创立。作为国内氢燃料电池车关键技术研发最早的一批探路人，海亿新能的核心技术团队自2001年以来先后承担了国家“863”计划中多个关于燃料电池汽车的重大专项课题，积累了深厚的实践经验，具有了成熟的技术储备，并取得了多项创新成果。当前团队拥有多项自主知识产权专利技术，形成了国内领先、国际先进的燃料电池系统及汽车动力系统的技术力量。公司现核心产品包括氢燃料电池发动机系统、氢燃料电池汽车动力系统总成技术平台、燃料电池升压变换器、燃料电池主控制器、燃料电池单片电压巡检仪等；并提供多类型氢燃料电池汽车的动力系统集成、动力系统优化控制、工程服务的完整解决方案。公司将围绕燃料电池系统及汽车动力系统坚持技术创新，打造核心技术链。联合产业链上下游各个关键节点，为我国新能源汽车发展作出卓越贡献，推动我国向全面资源节约型、环境友好型社会健康前进。注：我们的岗位非常适合期望在创业公司里有巨大成长空间的优秀人才。'],
        '117357789': ['1-1.8万/月', '五险一金|定期体检|免费班车|绩效奖金|年终奖金|', '武汉-东湖新技术产业开发区', '5-7年经验', '本科', '招1人', '12-09发布',
                      '测试主管（武汉）', '武汉精测电子集团股份有限公司',
                      '工作职责:\n职责描述：\n1、负责测试团队建设和管理（硬件、软件测试）\n2、主导分解新项目的测试需求和测试方案制定\n3、主导测试标准和规范制定\n4、指导组内成员分析和解决技术问题，负责组织技术难题攻关；\n5、主导详细测试方案的审核，主导对测试结果的审核\n6、负责团队成员培养，协调内部工作\n7、参与专项团队制度和体系建设\n任职资格:\n任职要求：\n1、本科及以上学历，5年以上测试相关经验，3年团队管理经验，有过独立带项目的经验，为项目负责人或主管完成某个研发项目\n2、具有良好的组织和沟通能力，有团队管理经验\n3、熟悉标准化的专项功能设计开发流程\n4、具有较高的技术敏感度，具备专项技术创新能力\n5、良好的文档编写能力\n职能类别：品质经理\n',
                      '上班地址：东湖高新技术开发区流芳园南路22号',
                      '武汉精测电子集团股份有限公司创立于2006年4月，旗下拥有苏州精濑、昆山精讯、台湾宏濑、武汉精能、武汉精立、武汉精毅通、武汉精鸿、精测香港、精测美国等子公司并在韩国设立研发中心，是一家在显示面板、半导体、新能源等先进制造领域提供“光、机、电、软、算”一体化系统测试方案的高科技上市企业（股票代码300567）。公司Module制程检测系统的产品技术已处于行业领先水平，技术优势明显，产品包括模组检测系统、面板检测系统、OLED检测系统、AOI光学检测系统和平板显示自动化设备，并通过ISO9000-2008质量管理体系认证、CE欧盟产品认证。产品已在京东方、三星、夏普、华星光电、中电熊猫、富士康、友达光电等知名企业批量应用，并于2017年取得苹果公司的供应商资格。公司秉承“科技成就未来、品质赢得信任”的宗旨，坚持“以客户为中心，以创新为驱动”的产品开发战略，聚焦行业技术发展趋势与市场需求，积极引进专家和优秀人才并与国内知名科研院所展开合作，持续在光学检测、自动化控制以及信号检测技术领域的研发投入，使核心产品拥有自主知识产权，整体技术达到国际先进水平，同时以严格的品质管控和快速有效的服务不断提升产品市占率，确保公司业绩高速发展。截至2017年度末，公司研发人员占总人数48%以上；研发投入占营业收入13.08%；公司已取得300多项专利权，其中发明专利113项，同时获得“国家技术创新示范企业”和“国家知识产权示范企业”两项殊荣。未来，精测集团将依托上市公司资本平台，以业界领先的“光、机、电、软、算”一体化技术为基点，积极布局全球营销网络，整合全球研发资源，努力将公司打造成为世界一流的的“光、机、电、软、算”一体化系统提供商。武汉精测正处于高速发展期，为员工提供富有竞争力的薪酬、完善的福利以及良好的发展平台，致力于创造一个尊重知识、尊重人才、开放包容的公司氛围，为客户创造更大价值，为员工和股东创造更多财富。公司期待有兴趣的有志之士加盟，大展身手。'],
        '117255710': ['10-15万/年', '五险一金|专业培训|餐饮补贴|交通补贴|通讯补贴|定期体检|', '武汉-洪山区', '无工作经验', '本科', '招若干人', '12-09发布', '测试工程师',
                      '武汉长江通信产业集团股份有限公司',
                      '岗位职责：\n1.根据产品需求制定功能测试用例和测试脚本的编写，并根据用例进行功能测试；2.提交BUG，对BUG修复情况进行跟踪和回归测试，直到BUG解决；3.制定性能测试方案，编写必要的测试脚本，根据方案进行性能测试，收集结果并给出简单分析；4.根据产品测试情况编写测试报告以及相关文档。\n\n要求：相关专业本科及以上学历，三年及以上相关经验。\n\n职能类别：软件测试\n',
                      '上班地址：武汉东湖高新技术开发区关东工业园文华路2号',
                      '武汉长江通信产业集团股份有限公司（简称“长江通信”）是1996年设立并通过国家科技部、中国科学院认证的高科技上市公司（股票代码：600345）。总部基地设立于国家自主创新示范区武汉东湖新技术开发区。2014年，成为烽火科技集团（武汉邮电科学院）旗下三大上市公司之一，是国家光电子信息产业基地——“武汉光谷”的重要骨干企业。\xa0\xa0\xa0\xa0长江通信专注于移动物联网、节能照明、光通信等产业的投资、研发、制造和销售，产品涵盖卫星定位、视频监控、移动通信、LED照明、光纤光缆、光通信设备、信息系统集成和技术服务以及平台软件开发等多个领域，是行业内重要的信息技术产品及服务提供商，连续多年获得“中国光通信最具竞争力企业10强”荣誉。\xa0\xa0\xa0\xa0长江通信拥有多项自主知识产权的产品，并长期承担国家“863”计划、省市等多个科技项目的开发与研究。企业还投资组建了***“博士后工作站”和“院士工作室”，为创新搭建了优质的技术平台和人才平台。\xa0\xa0\xa0\xa0未来，长江通信将秉承“责任、进取、绩效、和谐”的企业理念，以烽火科技集团完善的机制和行业地位为依托，专注信息电子技术产品与服务一个主业；聚焦物联网和通信配套材料两个领域；打造物联网核心技术与产品开发能力、物联网核心软件与整体解决方案应用能力、通信配套材料细分市场核心产品化产业化能力三种能力；实现集团发展方式转变、经营规模增长、股东回报提升、员工与企业共同发展四个目标。'],
        '118565607': ['1-1.5万/月', '五险一金|补充医疗保险|专业培训|通讯补贴|餐饮补贴|交通补贴|年终奖金|股票期权|定期体检|', '武汉-东湖新技术产业开发区', '2年经验', '本科',
                      '招1人', '12-09发布', '测试工程师', '杭州海康威视数字技术股份有限公司', '职能类别：软件测试\n关键字：JavaPython\n', '上班地址：光谷软件园F4',
                      '【公司介绍】海康威视是以视频为核心的智能物联网解决方案和大数据服务提供商。2011-2017全球视频监控市占率第1（IHS）2016-2018“全球安防50强”第1位（a&s《安全自动化》）2017-2018 年Brand Finance“全球科技品牌百强榜”2018年中国软件业务收入百强第6位，2018中国大数据企业50强央视财经论坛暨中国上市公司峰会 “2016&2018 CTV中国十佳上市公司”\xa0【公司实力】人员规模：34000+员工，？16000+研发和技术服务人员（截止2018年底）产业布局：主营业务版块包括大数据服务、行业智慧应用解决方案、综合安防解决方案、安防全系列产品；创新业务覆盖互联网业务\\机器人业务\\汽车电子\\智慧存储、海康微影、慧影科技等其他拓展业务。研发实力：1所研究院、国内8大研发基地，海外2大研发中心，2809项已授权专利、881软件著作权、参与制定标准298项、多项全球竞赛大奖营销网络：32家国内省级业务中心/一级分公司及44家境外分支机构，产品和解决方案覆盖全球150多个国家及地区。【薪酬福利】海康威视倡导凭借价值贡献获取回报，并为员工提供有竞争力的薪酬、完善的福利保障、全球工作机会、明晰完善的职业发展和培训体系。假期：带薪年假、全薪病假、母婴照顾假、婚假等；外派：国内与海外有住房、生活、艰苦区域补贴，补充商业险，探亲福利及高额奖励；补贴：交通补贴/总部免费停车场、补充商业险、通讯补贴、过节福利、现金医疗补贴、荣誉奖励、工会福利、免费手机、杭州市人才引进津贴等；乐活：餐饮补贴、免费早餐、免费零食、生日蛋糕、总部园区生态圈（食堂、便利店、健身中心等）、年度体检、弹性工作制、医务室等；安居：人才落户政策。【加入我们】请关注海康威视招聘官网了解更多公司及岗位信息http://talent.hikvision.com/'],
        '114915028': ['1.1-1.8万/月', '五险一金|年终奖金|弹性工作|定期体检|周末双休|专业培训|员工旅游|下午茶|绩效奖金|通讯补贴|', '武汉-东湖新技术产业开发区', '2年经验', '本科',
                      '招1人', '12-09发布', 'STM32软件工程师', '武汉依迅电子信息技术有限公司',
                      '1、根据项目具体要求，承担软件开发任务，按计划完成任务目标；2、完成软件系统以及模块的测试方案、文档的编写，软件测试；3、参与公司TBOX、部标一体机、部标分体机等产品的调试，并对调试中出现的软件问题的进行实施、跟踪及汇总。\n任职要求：1、电子、通信、软件工程等相关专业，本科及以上学历，2年以上的工作经验；2、熟悉ARM微控制器架构，具备STM32微控制器的软件设计及开发经验；3、精通C语言嵌入式编程，熟悉FreeRTOS实时操作系统；4、熟悉KEIL开发环境，掌握altiumdesigner等软件查看原理图；5、有良好的英语阅读能力，能够快速阅读并准确理解各种英文技术文档；6、具有TBOX、车载导航、行车记录仪、车载监控、车载中控等产品相关开发经验者优先。\n职能类别：高级软件工程师\n',
                      '上班地址：武大科技园航域二期A1栋2层',
                      '武汉依迅电子信息技术有限公司（简称：依迅电子）是一家多级国有基金参股专注于北斗卫星导航应用的军民融合高新技术企业集团。主要业务涵盖国防军工、智能交通、智慧城市、精准农业四大版块；在北斗高精度组合制导、北斗原子钟授时、视觉测距与识别等领域拥有国际领先的核心技术。在美国硅谷、中国光谷分别建有研发中心，与武汉大学、武汉理工大学等高校共建“教学科研实习基地”、“博士后流动工作站”，公司现为中国国防工业军民融合产业联盟副理事长单位，军工资质、生产资质齐全，在全国拥有100多家紧密型合作伙伴及多家分子公司，市场占有率连续多年居行业之前列，连续5年被行业协会评选为中国卫星导航产业“十佳产品供应商、十佳运营服务商”。\xa0\xa0\xa0公司位于中国光谷，现有员工平均年龄28岁，其中学士学位员工占到80%，技术研发员工占到60%以上。2007年公司与武汉大学、武汉理工大学等高校共建“教学科研实习基地”以及“博士后流动工作站”，构建出以产业为主导、企业为主体、技术为依托、产学研相结合、软硬件集成一体化的现代高科技企业体系。\xa0\xa0\xa0\xa0依迅电子坚持“政府推动，市场导向，科技支撑”的发展道路，不断提高自主创新能力，如今已拥有一支由该领域知名专家、教授及高工组成的研发队伍，并相继通过了ISO9001:2008质量管理体系认证、CCC产品认证、欧盟CE认证等国内外权威认证。\xa0\xa0\xa0依迅电子在全国拥有100多家紧密型合作伙伴，市场覆盖30多个省、直辖市，市场占有率连续3年居行业之前列。依迅以技术创新、应用创新带动导航与位置服务产业创新发展为着力点，积极探索市场机制，加速推进导航与位置服务产业的关键技术、核心部件和重大产品创新，公司具有自主知识产权的系列产品广泛销售于国内外，赢得了用户的一致好评，并获得了“2009年度行业创新奖”。公司的北斗系列产品、车载3G终端，特别是北斗及CDMA制式终端的市场占有率多年来一直保持行业领先地位。\xa0\xa0\xa0目前公司已拥有国家专利7项，软件著作权19项，公司承担国家创新基金支持项目1项，公司现为“武汉东湖高新技术企业” 、“中国全球定位系统及时应用协会会员单位” 、“双软认证企业” 、“国家地球空间信息产业基地会员单位” 、“国家创新基金扶持项目承担单位” 、“中国物流与采购联合会员单位”、“湖北省软件协会理事单位”“2011年、2012年和2013年中国十佳卫星导航产业供应商”、2013年武汉市东湖高新区“瞪羚企业”等。\xa0\xa0\xa0\xa0武汉依迅定位于“位置服务集成商及运营服务提供商”，秉承“自主创新、产业报国”的理想，依迅人以“推动我国导航与位置服务产业可持续发展”为己任。未来，武汉依迅将矢志成为位置产品及服务领域领先企业，在大力发展以自主卫星导航系统为基础的导航与位置服务产业的同时，为服务我国经济建设、社会发展和公共安全全面提升我国导航与位置服务产业核心竞争力不懈努力。公司提供：\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0五险一金；\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0周末双休；\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0法定节假日休息，带薪年假，春节额外5天以上带薪年假（春节假期12-15天）；\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0提供假日礼品、福利，员工生日福利，免费饮料（咖啡、奶茶、橙汁）和下午茶点，每年2次旅游等；\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0良好的职业发展空间。'],
        '116565043': ['1.1-1.4万/月', '五险一金|餐饮补贴|通讯补贴|定期体检|绩效奖金|年终奖金|', '武汉-东湖新技术产业开发区', '5-7年经验', '本科', '招1人', '12-09发布',
                      '高级测试工程师 (MJ000788)', '神州数码信息服务股份有限公司',
                      '岗位职责：\n1.负责测试资源协调，需求的沟通确认以及项目进度汇报工作；\n2.负责测试任务分配，测试案例编写，测试案例审核等；\n3.负责项目日常管理，控制测试执行进度，检查测试执行质量，测试执行，缺陷跟踪以及测试风险汇报；\n4.负责测试结束后操作手册编写、汇总整理、审核，需要下发各分行的PPT及通知的编写，参与电视电话会议等上线前工作；\n岗位要求：\n1.熟练掌握软件测试理论、测试流程及测试方法，熟悉软件项目，能熟练编写和执行测试用例、编写测试报告、能快速发现并定位缺陷；\n2.熟悉软件生命周期、开发流程、双V及瀑布模型；\n3.熟悉质量管理体系，了解CMMI过程改进标准；\n4.能熟练操作数据库及SQL语言：Oracle、MS-SQLServer、PostgreSQL、MySql；\n5.熟练使用配置管理工具CVS、SVN及FireFly，了解配置管理的环境搭建和基线变更流程；\n6.能够熟练使用测试工具如QualityCenter、Bugfree、SecureCRT、SSH等；\n7.熟悉WINDOWS、Linux操作系统，了解TCP/IP协议，了解RAID磁盘阵列的搭建；\n8.参与过多个项目的测试，工作认真负责、积极主动、团队合作能力强、接受新知识快、真诚待人；\n最重要：有银行测试经验！\n职能类别：软件工程师\n',
                      '上班地址：武汉市黄陂区汉口北大道众邦银行',
                      '神州数码信息服务股份有限公司，中文简称：神州信息，英文简称：DCITS，股票代码：000555.SZ ；作为金融科技全产业链综合服务商，拥有三十余年行业信息化建设经验，是国内信息化产业领导者和数字中国的践行者，依托深厚的自主研发能力，融合科技与业务，赋能行业发展，推动中国数字化升级，支撑数字中国的使命。聚焦金融科技，以人工智能、区块链、云计算与分布式、大数据、物联网、以及量子通信等新兴技术的应用，驱动软件及服务产品智能化迭代，助力金融机构安全合规地推进基础架构转型及业务创新；融合金融、政企、运营商、农业等行业数据及场景资源，创新金融场景，打造新的服务平台并提供运营服务，赋能金融行业数字化转型，打造产业融合新生态。'],
        '100706538': ['10-20万/年', '五险|定期体检|双休|交通补贴|员工旅游|年终奖金|餐饮补贴|绩效奖金|', '武汉-东湖新技术产业开发区', '3-4年经验', '本科', '招2人',
                      '12-08发布', '资深硬件开发工程师 (职位编号：01)', '武汉岩海工程技术有限公司',
                      '岗位职责：\n1.基于市场和产品团队的需求，编写优化设计方案；\n2.器件选型，完成符合功能和性能要求的原理图设计；\n3.完成多层PCB设计工作；\n4．整理调测方案，开发文档；\n5.负责产品研发，调试电路和问题解决，指导并配合软件测试以及验证；\n5.产品研发过程中的成本控制、风险及质量控制等。\n\n任职要求：\n1、正规重点大学本科（含）以上学历，有一定工作经验；\n2、通信、电子信息工程、电气自动化、测控技术等计算机、电子相关类专业；\n3、熟悉SPI，UART，I2C,485等接口；\n4具有丰富的FPGA/ARM嵌入式系统板级软硬件设计和调试经验；\n5、可熟练阅读并理解英文技术文档，学习能力强；\n6、具有良好的团队合作精神，诚实守信，坚韧不拨，有强烈的实现自我价值的愿望。\n7、具3年以上项目独立研发经验,熟悉软、硬件开发者优先\n职能类别：高级硬件工程师\n关键字：硬件工程师\n',
                      '上班地址：武汉市洪山区光谷大道62号光谷总部国际2号楼27层28层',
                      '岩海公司是在武汉市东湖高新区管委会直接支持下于1992年3月成立的一家专门从事工程检测技术研究开发的高新技术企业，现有员工60余名，80％以上具有本科以上学历，具有硕士、博士学位和高级技术职称员工十多名。公司成立二十多年来，一直致力于工程检测技术的研究开发，涉足微电子技术、计算机技术、数学力学、岩土工程、工程物探等多学科领域，先后研制出基桩动测仪、非金属超声检测仪、基桩静荷载检测仪、成孔(槽)质量检测仪、工程地震仪、井下电视、裂缝宽度检测仪、超磁发射机、桥梁结构应力检测系统及相关传感器等系列具有自主知识产权的产品，已获得发明专利三项、实用新型专利两项、正在申请的专利一项；近年又与南京大学合作研制出钢筋笼长度测试仪，解决了灌注桩钢筋笼长度测试难题；与浙江省台州市建设局合作研制出无线数据传输仪，实现现场测试过程的实时无线监控。\xa0\xa0岩海已成为国内工程检测领域较有影响的研发中心之一，其RS系列产品均畅销全国，在建筑工程、公路工程、铁路工程、水利水电、国防工程等各个基础建设领域均得到广泛应用，研究成果也多次获得省部级科技进步奖及科技成果推广奖；其中部分产品已打入国际市场，销量连续多年稳居国内同行榜首；各种现场考核和对比试验表明，部分产品的性能指标已达到或超过国外同类仪器水准。岩海群英荟萃，人才济济，年轻而富有朝气，在仪器研制、方法研究、工程测试等交叉领域协同发展，取得了令人瞩目的成绩。省、市及行业领导也多次来公司视察，勉励科技人员不断研发新成果、新技术。国家科委成果办、国家建筑工程质量监督检验测试中心、中国深基础工程协会检测委员会、中国工程建设标准化协会、同济大学、浙江大学、中国地质大学、湖南大学、青海大学及一些省市质检总站或行业协会都多次举办会议，推广岩海产品，交流与岩海产品相关的工程测试技术。“以诚为本，用户至上”是岩海人的宗旨，多年来，我们急用户所急，想用户所想，不断进行广泛的售前售后门到门的服务，并因此而赢得了良好口碑和用户信任。\xa0\xa0\xa0\xa0我们将不懈努力，研制出更多更先进、更适用、更好用、更耐用的检测设备为广大工程技术人员服务。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0公司网址：www.rocksea.net.cn'],
        '79714827': ['1-1.2万/月', '五险一金|免费班车|交通补贴|餐饮补贴|通讯补贴|绩效奖金|', '武汉-东湖新技术产业开发区', '无工作经验', '本科', '招2人', '12-06发布',
                     '嵌入式软件开发工程师（五险一金+节日福利+年终奖金）', '武汉飞流智能技术有限公司',
                     '岗位职责\n(1)独立完成嵌入式程序开发，能够快速实现基于嵌入式平台的软件功能。能够快速学习和实现基于标准通信接口的程序开发任务；\n(2)参与嵌入式软件测试及调试，产品维护等工作；\n(3)参与产品的需求和技术可行性分析\n(4)编写软件模块开发文档、协助制定测试文档。\n\n任职要求\n(1)计算机、电子通信、自动化等相关专业本科或以上；本科及以上学历。往应届毕业生均可。\n(2)有独立完成STM32项目开发经验者优先（含在校期间项目）。\n(3)熟练使用C语言进行嵌入式软件编程。\n(4)熟悉STM32的功能特性，能够独立使用STM32完成调试和开发工作。\n(5)有8位或32位单片机、多核处理器等设备的开发经验；\n(6)熟悉I2C、SPI、CAN、USB、UART等外设接口；\n(7)熟悉嵌入式操作系统，ucos、freertos等；\n(8)具有良好的代码编写及管理习惯，熟悉svn、git等软件版本管理工具；\n(9)具备较强的沟通协调能力，良好的职业素质和团队合作精神，对工作认真负责。\n三、福利\n1.国家法定节假日休假。\n2.缴纳五险一金（养老保险、失业保险、工伤保险、生育保险、医疗保险、住房公积金）；\n3.公司福利：节假日过节费、结婚礼金、带薪年休假、年度调薪、年终奖金等各项福利。\n职能类别：嵌入式软件开发(Linux/单片机/PLC/DSP…)电子软件开发(ARM/MCU...)\n关键字：嵌入式\n',
                     '上班地址：武汉东湖高新创业街留学生创业园',
                     '飞流智能是一家专注于人工智能技术在工业自动化监测领域深度应用的高科技公司，结合各类机器视觉、深度学习与神经元等算法提供大数据采集处理与应用分析服务，并提供自动化控制、信息化及运维问题解决方案，拥有大量自主知识产权。全资子公司飞流智控提供自动驾驶智能控制模组、通信数据链核心模组、环境感知导航定位模组（融合激光雷达、毫米波雷达与视觉）及各类探测传感器模组；全资子公司飞流智航提供专业化的工业无人机、行走类机器人、悬挂类机器人及各类工业自动化监测设备。公司研发中心位于武汉光谷核心区域的科技园-武汉留学生创业园，已通过ISO9001:2008质量管理体系认证，是“光谷3551人才计划”企业，具备优秀的产品技术研发实力和业务拓展能力。公司生产测试与培训基地位于鄂州梧桐湖开发区，交通便利，设施齐全，可同时容纳200人的交付培训。\xa0\xa0\xa0公司建立了完整的智能自动化系统研究、开发、生产、销售及服务链，拥有近50人的高水平研发团队，技术实力雄厚，先后研发了【源|Origin4】、【源|Origin6】、【源|Origin6Pro】和【源|Origin8】多旋翼系列无人机，【弦|MelodyEM】和【弦|MelodyPM】复合固定翼系列无人机，以及约20种适配于不用场景下使用的应用载荷。公司产品已成功应用于电力、环保、测绘、消防等多个领域，为客户创造了良好的经济效益；公司同时与华中科技大学、武汉大学、中国地质大学、海军工程大学、空军预警学院、火箭军指挥学院等院所共建产学研与工程实践平台，创造了良好的社会价值。'],
        '107160175': ['1-1.2万/月', '五险一金|员工旅游|餐饮补贴|专业培训|绩效奖金|年终奖金|股票期权|弹性工作|定期体检|', '武汉-洪山区', '无工作经验', '本科', '招2人',
                      '12-06发布', '测试开发工程师', '广州中望龙腾软件股份有限公司',
                      '1、设计执行测试用例，保障产品品质；\n2、编写自动化测试脚本；\n3、开发测试工具，提高测试过程自动化程度；\n4、使用英语与国外团队沟通测试项目。\n\n\n任职资格\n1、软件工程、计算机科学与技术、机械、土木、建筑、电子、数学、应用数学及相关专业，本科学历及以上；\n2、熟悉软件测试的基本方法、流程和规范，可以独立完成测试分析和测试案例设计；\n3、熟悉常用软件测试工具,熟悉测试分析技术,有较强的逻辑分析能力和总结能力；\n4、能够服从工作安排，有上进心，乐于接受挑战；\n5、具备团队思维，与人友善；\n6、系统学习过任意一种程序语言(C++\\Java\\C#\\Python等)；\n7、具备实际设计、编程、测试工作经验优先；\n8、能熟练使用英语进行书面及口头交流者优先。\n职能类别：软件工程师软件测试\n关键字：测试开发\n',
                      '上班地址：珞喻东路佳园路慧谷时空',
                      '广州中望龙腾软件股份有限公司（简称“中望软件”）是国际领先的CAD/CAM解决方案供应商，国内唯一同时拥有完全自主知识产权二维中望CAD、高端三维CAD/CAM软件中望3D的国际化软件企业，致力于为全球用户提供世界级技术水平的高性价比CAD/CAM产品与服务，帮助用户以合理成本解决正版化的同时，最大化发挥正版CAD/CAM软件的应用效益。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0截止目前，中望系列软件产品已经畅销全球80多个国家和地区，正版用户突破55万，并赢得了宝钢股份、海马汽车、保利地产、中国移动等中国乃至世界知名企业的认可，全球正版授权用户数突破55万。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0中望软件一直致力于CAD/CAM软件技术的研发与创新，在广州、武汉和美国佛罗里达设有三大CAD研发中心，拥有一支超过25年CAD/CAM研发经验的世界一流技术研发队伍；此外，还积极与国际ODA、Partsolution零件库等组织合作，融合国际领先技术，不断提升中望系列软件产品的技术水平。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0中望软件总部位于广州，在北京、上海、武汉、美国佛罗里达设有分公司。凭借20多年的研发经验，中望软件可迅速响应用户需求，提供快捷、专业的本土化服务及更具针对性的研发级技术支持，满足用户CAD功能定制、专业插件移植等个性化需求，进一步拓展CAD/CAM应用边界，从而帮助用户轻松提高软件应用效益。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0中望自2004年开始海外拓展，首开民族CAD软件出口海外的先河，并连续多年实现海外销售额增长超过50%，海外业务拓展成绩斐然。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa02008年9月，中望龙腾长坑希望小学在广东兴宁正式开学；2009年11月，第二所中望龙腾希望小学在湖北红安建成；2009年以来多次参加政府扶贫开发“双到”工作，踊跃捐款……作为一家有着强烈社会责任感的企业，中望在未来将继续通过多种形式承担起更多的社会责任，回报社会。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0随着公司的快速发展，我们对高素质的国际化人才需求与日俱增，公司提供极具竞争力的薪酬和全面的福利，欢迎优秀的您加盟中望，与我们一起成长，一起收获，一起创造CAD软件的辉煌明天!（有关公司更为详细情况请参见网址www.zwcad.com）\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa02017年5月26日，我公司经全国中小企业股份转让系统有限公司责任公司批准，正式在全国中小企业股份转让系统（即新三板）挂牌。培训发展：公司为员工提供完善的培训发展平台，包括新员工入职培训、在职一对一帮辅指导、专业技能培训、定向管理能力培训等，研发部门定期购买书籍供员工学习，鼓励员工学习深造，优秀研发人员可获得去美国弗罗里达研发中心学习工作机会。福利代遇：公司5天上班制，每天工作7.5 小时，实行弹性上班制，提供免费午餐（补贴）和下午茶点，员工享有五险一金以及国家规定的各类带薪假期，公司定期组织团队活动和户外旅游，真正让员工快乐工作，快乐生活。'],
        '88188442': ['1-1.5万/月', '五险一金|交通补贴|年终奖金|餐饮补贴|定期体检|高温假|', '武汉-洪山区', '无工作经验', '本科', '招10人', '12-06发布', '高级软件工程师',
                     '中国船舶重工集团公司第七0九研究所',
                     '岗位职责：\n1、从事软件设计与开发工作，包含底层软件开发和嵌入式软件开发；\n2、从事计算机软件体系结构研究；\n3、从事软件可靠性和软件测试研究。\n\n任职要求：\n1、硕士研究生及以上学历，计算机应用技术、计算机软件与理论、软件工程等相关专业；\n2、热爱国防事业，愿意长期从事国防科研工作，具有很强的保密意识；\n3、团结协作，善于沟通。\n职能类别：高级软件工程师\n',
                     '上班地址：武汉市东湖新技术开发区凤凰产业园藏龙北路1号',
                     '中国船舶重工集团公司第七○九研究所（以下简称七○九所）成立于1956年，隶属于中国船舶重工集团公司，是中央在汉事业单位和国防军工重要科研院所，现有两大院区，其中光谷院区地处“武汉·中国光谷”核心商业区，交通便利，繁华腹地；藏龙岛新区地处东湖新技术开发区，正全力打造一流的军工科技和民品科技产业园。七○九所是融数理理论、计算机、控制技术和系统集成于一体的国家重点综合性研究所，主要从事指挥控制系统、计算机加固技术、容错技术、并行处理技术以及网络技术与软件工程、图形图像处理、机电一体化等专业的研究与开发工作。七○九所以高新技术研究为中心，研制的系统和各类设备填补多项国内空白，为国防现代化和信息化作出了巨大贡献。随着全球信息技术的飞速发展和国防信息化建设力度不断加大，七○九所把握机遇，主动出击，力争建成为国内领先、国际知名的军民融合电子信息行业高科技企业集团。'],
        '85855805': ['13-20万/年', '五险一金|补充医疗保险|交通补贴|餐饮补贴|专业培训|绩效奖金|年终奖金|定期体检|', '武汉-洪山区', '3-4年经验', '本科', '招5人',
                     '12-06发布', '驱动工程师', '中船重工（武汉）凌久电子有限责任公司', '职能类别：软件工程师\n', '上班地址：珞喻路718号709所',
                     '中船重工（武汉）凌久电子有限责任公司（简称凌久电子），是中国船舶重工集团公司第七〇九研究所控股的高新技术企业。\xa0\xa0\xa0\xa0凌久电子从事并行处理技术的研究始于1983年，是我国最早开展并行处理研究的三家单位之一，从“七五”起到现在的“十三五”，先后承担了一系列国家有关并行处理的重点预研项目，取得了一批具有国际先进水平、国内领先的科研成果，获得了多项***和省部级科技进步奖。\xa0\xa0\xa0公司以嵌入式实时信号处理与高性能计算技术为基础,面向船舶、航空、航天、兵器等国防电子领域及轨道交通、海工装备、能源电力、半导体制造等民用高科技领域提供芯片级、模块级、设备级、系统级等软硬件产品；面向科研院所、部队及军校提供作战指挥决策、军事训练、装备论证、战法研究等定制化军事仿真服务。\xa0\xa0\xa0加入我们，我们将给予您：公平的晋升机制——“技术晋升”+“管理晋升”双通道发展，老带新导师赋能完善的个人培养体系--岗前培训  内部培训  短期外培  外聘讲师  考察学习等健全的福利关怀--  带薪年假   高温假  高温补贴  社团活动餐费补贴    保密补贴  交通补贴工会福利   节日福利     生日卡  电影票  劳保福利  工作服等  五险一金   商业保险   定期体检地址：湖北省武汉市洪山区珞喻路718号709所网址：http://www.csic-lincom.cn凌久电子微信公众号：LINCOM_CSIC'],
        '84204448': ['1-2万/月', '五险一金|绩效奖金|年终奖金|员工旅游|专业培训|出国机会|带薪年假|', '武汉-洪山区', '2年经验', '本科', '招3人', '12-06发布',
                     'C/C++研发工程师', '武汉卓讯互动信息科技有限公司',
                     '（1）熟练掌握Windows,Linux/Unix平台的C/C++语言和开发工具，并能熟练使用其开发相应的开发，调试工具；\n（2）参与项目需求分析，完成模块的概要设计和详细设计，主动跟踪软件测试结果和BUG分析及修改；\n（3）对已有的项目进行维护和迭代；\n（4）开发各种内容测试使用DEMO程序。\n任职要求：\n（1）本科及以上学历；计算机或相关专业,2年以上工作经验；\n（2）掌握C/C++，深刻理解面向对象思想；\n（3）熟悉Service，SDK，DLL库的设计与开发。\n\n我们是一家处于上升期的互联网游戏公司\n你想要的我们都能给你\n高大上的工作环境\nOPEN的沟通氛围\nNICE的老板\n善解人意的HR\n任性的红包雨\n一群志同道合的伙伴\n我们缺的就只有你~\n\n完善的福利：\n五险一金、商业保险、项目提成、年终奖、住房补贴、丰富可口的加班餐点、带薪年假、入职体检\n优秀的你还能获得晋升、年度调薪、带薪外训、节假日特色礼品or购物卡…\n\n团队建设：\n月度生日会团队趣味拓展…\n海鲜大餐年度旅游\n单身的你个人问题也交给我们好啦\n\n我们的宗旨你来开开心心的工作其他的问题都交给我们解决\n职能类别：高级软件工程师互联网软件开发工程师\n关键字：CC++C语言C++研发软件工程师\n',
                     '上班地址：关山大道保利国际中心写字楼33层',
                     '武汉卓讯互动信息科技有限公司，于2012年在武汉东湖新技术开发区登记成立，是武汉市高新技术企业，东湖高新区瞪羚企业，湖北省双软企业，截止2018年，累计纳税过亿元。公司在移动端游戏及应用开发及运营，大数据分析与挖掘上具有领先的优势。利用互联网创新思维，融合互联网技术和人工智能，打造音乐与在线教育相结合的功能性游戏。同时公司致力于广电云媒体服务，在中国广播电视网络有限公司领导下，集聚广电优势力量，由中国有线、华栖云、卓讯互动、岩华传媒强强联合，成立了“中广云媒网络技术有限公司”。通过开展差异化的媒体云、融合媒体中心、智慧云教等核心业务，为全国各广电网络公司提供全新融合媒体服务。2018年在国家应急部指导下，由中国职业健康安全协会、新华社旗下新华通网络及卓讯互动共同发起成立了全国性智慧用电灾害监控预警管理平台，利用物联网大数据、云平台数据，实现高并发、大数据、数据可视化功能，建立以物联网大数据为核心的综合数据业务服务体系，为灾前预警、灾时协助、灾后排查提供技术支撑及解决方案。'],
        '98466633': ['10-15万/年', '', '武汉-江夏区', '5-7年经验', '本科', '招若干人', '12-05发布', '高级java研发工程师', '武汉联宇技术股份有限公司',
                     '1、负责公司软件产品架构设计、系统设计、功能设计及核心代码的编码工作；\n2、协助初级工程师解决各种编程难题，配合测试人员完成系统测试及改进工作，配合编写项目各种文档；\n3、与产品经理做好紧密沟通，制定详细的工作计划，跟踪业界新的开发技术；\n4、把控整个项目团队的开发进度、风险评估，对于团队管理有自己的认识及理解并可高效的执行落地；\n5、组织并监督技术评审、质量保证、软件测试、项目实施等相关工作。\n\n任职资格：\n1、国家统招本科以上学历（985、211毕业优先），5年工作经验以上，有水利信息化行业工作经验者、有高级职称者优先；本岗位同时招收2019年应届统招一本毕业生；\n2、精通Struts2，Spring，SpringMVC,myBatis框架，精通HTTP/HTTPS协议，熟悉分布式计算、分布式文件系统；\n4、至少精通三种常用的关系型数据库如sqlserver、mysql、oracle，精通memcache、redis等缓存技术或具备海量数据处理的能力；\n5、有项目管理经验者，精通SVN、maven等版本管理软件；\n6、较强的逻辑思维能力、学习能力,有良好的沟通和团队协作能力，具备独立完成工作和创新的能力，能快速适应新的工作环境。\n薪酬福利：\n1、企业为员工提供具有竞争力的薪酬体系、职业发展空间；\n2、企业定期为员工提供免费培训；\n3、按照国家规定办理社会保险；\n4、五天工作制，双休；\n5、员工享受国家法定节假日、带薪年假、工龄奖、全勤奖、年终奖及节日福利、生日福利等。\n\n\n职能类别：高级软件工程师\n关键字：软件架构设计系统设计功能设计核心代码编码把控项目团队Struts2SpringSpringMVCmyBatis\n',
                     '上班地址：东湖新技术开发区东一产业园流芳园北路9号',
                     '武汉联宇技术股份有限公司成立于2003年4月，是一家专门从事水利和水环境信息化的高新技术企业，公司主营业务涉及灌区、水库、泵站、水电站、堤防、山洪灾害防治、防汛抗旱、中小河流治理和水资源优化调度等信息化系统集成及相关软、硬件的研发、生产和销售；兼营水环境、水土保持、水厂、污水处理、城市排水等监测系统的软、硬件研发及系统集成，是湖北省信息化骨干企业、新三板上市企业（证券代码：430252），信息化技术水平处于行业领先地位。公司总部位于武汉东湖新技术开发区，拥有自建总面积约14000平米的研发大楼，并在全国约20多个省、市、自治区及直辖市设立办事处。\xa0\xa0\xa0\xa0公司自成立以来，研发水平逐步提高，业务范围不断扩大，覆盖全国20多个省份，主要完成了以下工程项目：灌区信息化工程40项，水库信息化工程31项，泵站、电站信息化工程40项，山洪灾害防治工程130项，水资源管理、中小河流治理、流域综合治理信息化工程44项，水闸监控与自动化控制工程4项，水利设计项目18项，供水工程自动化及饮水工程12项，安防监控工程18项。\xa0\xa0\xa0\xa0欢迎立志从事水资源、水环境保护领域业务的软件、硬件工程师、产品经理、销售人员及物联网建设领域的项目管理等优秀人才，加入公司共同发展。'],
        '118192576': ['1-1.5万/月', '五险一金|补充医疗保险|通讯补贴|餐饮补贴|包住|绩效奖金|年终奖金|牛人团队|股票期权|', '武汉-洪山区', '3-4年经验', '本科', '招1人',
                      '12-05发布', 'Java开发工程师', '鄂尔多斯市煤易宝网络科技有限公司',
                      '薪资福利：月薪10K—15K+五险一金+双休+年度旅游+年度体检+带薪年假+节日福利+年终奖+股份\n\n加入我们，您将获得：\n1、雄厚的资金保障：煤易宝自有煤矿资源，款项现结模式，伊泰、汇能等煤矿龙头企业背书，保证了公司有稳定的资金链；\n2、有竞争力的薪酬福利：全员持股！入职越早，越优先分配！五险一金，还享受年度体检、年度旅游、出差补助、节日福利、结婚生子贺礼、年终奖等各种福利！\n3、完善的休假：周末双休、国家法定节假日、婚假、产假、陪产假、带薪年假；\n4、丰富的团建活动：聚餐、K歌、兴趣俱乐部、户外拓展、旅游……应有尽有；\n5、以人为本：弹性作息、尊重员工个性发展；\n6、牛人团队：京东、高德、顺丰、良品铺子、明源云、斑马快跑、陕煤、伊泰、大同煤矿……煤易宝已吸纳大量知名互联网和煤矿企业人才，牛人带你飞！\n7、发展空间：公司刚完成工商注册就有3000万投资到账，还有超3亿的投资意向正在洽谈，计划2023年在港股或创业板上市！全员持股，根据入职时间和岗位分配，加入我们一起“闷声发大财”吧！\n\n岗位职责：\n1、根据公司产品项目需要，能独立完成设计与编码\n2、优化系统，保证所完成功能模块的可用性和稳定性\n3、能解决负责模块的关键问题和技术难题\n4、协助并完成其他各类技术开发任务\n5、理解业务、识别需求，能与团队组员友好协作与沟通，保证产品研发进度和质量\n\n任职要求：\n1、统招二本及以上学历，985、211高校优先，计算机相关专业，3年以上Java开发经验；\n2、熟悉Spring、SpringcloudorDubbo、mybatis等开源框架（框架提供的特性及其实现原理）\n3、熟悉MySQL等数据库的使用；熟练使用SQL语句，熟悉数据库性能优化\n4、熟悉WEB应用服务器的配置与使用，如Tomcat，Jboss\n5、了解OOD、OOP、DDD以及设计模式等基本设计方法，熟悉UML\n6、对数据缓存技术有一定了解，如Memcached、Redis等\n7、了解NoSQL（如MongoDB、Hbase）数据库\n8、理解乐观锁，对JVM原理及垃圾回收机制有一定的了解\n\n煤易宝对优秀人才的定义是：\n#专业、职业、靠谱\n#高效、协作、诚信\n#使命必达、自我驱动\n#持续学习、拥抱变化\n#初心不改、仍怀梦想\n如果你有无处安放的才能和智慧想尽情发挥，我们为你提供施展才华的舞台！\n职能类别：互联网软件开发工程师软件工程师\n关键字：软件测试JavaSQLSpringDubboMySQL\n',
                      '上班地址：虎泉街五环天地1号楼（杨家湾地铁站D出口前行200米）1901—1904室',
                      '鄂尔多斯市煤易宝网络科技有限公司，成立于2018年，注册资金1000万元，是武汉物易云通网络科技有限公司（司机宝）和煤问题（内蒙古）电子商务有限责任公司的合资控股企业。\xa0\xa0\xa0\xa0公司旗下的煤易宝供应链管理平台是集交易、物流、供应链金融服务为一体的产业互联网平台，专注于煤炭领域，为企业客户提供一票到站的供应链综合服务。目前公司的主营业务有：一票到站、无车承运、代客叫车、坑口代发。我们提供煤炭行业采、运、销各环节一站式服务，保障货物高效送达。\xa0\xa0\xa0\xa0公司拥有强大的软硬件自主研发能力，研发团队位于武汉光谷高新科技产业园，拥有来自于美团、京东、高德、顺丰、平安科技、海航、斗鱼、唯品会、明源云、良品铺子等知名企业的技术人员，涵盖了物流、金融、供应链、大数据等技术背景。\xa0\xa0\xa0\xa0煤易宝运营团队在煤炭领域深耕多年，对行业有着深刻的理解，通过专业的操作流程和规范保障服务质量。愿景：成为中国市场上专业的精益煤炭供应链管理平台使命：通过互联网+科技的手段提升煤炭供应链效能价值观：精进 专业 创新 共赢加入我们，您将获得：1、财富：\xa0\xa0\xa0只要你有能力、有渴望，除了岗位工资、各项补贴、绩效奖金、五险一金、节日福利、评优奖金、年终奖等基本的薪酬福利，成为持股员工享受分红权、投票权、处置权，是我们敢于给你的认可和信任2、团队：\xa0\xa0\xa0—董事长拥有银行和美团、航班管家、司机宝创始人等丰富的背景，战略眼光毒辣，超强大脑、有趣的灵魂就是这样有魅力！\xa0\xa0\xa0—总经理具备丰富的销售实战经验，拉起乐队去北漂那都不在话下，如果你干练又聪明，你们是一路人！\xa0\xa0\xa0—销售副总俗称“煤炭活地图”，在煤炭行业深耕多年，想在煤炭行业忽悠到他，还真得有两把刷子！\xa0\xa0\xa0—首席财务官，请自行百度“姬志福”，伊泰集团传奇人物，最年轻的高管！\xa0\xa0\xa0—产品研发核心人员，来自高德、顺丰、京东、美团、明源云、斗鱼、唯品会、海航科技、平安科技、良品铺子等知名互联网企业，不用我们吹，做出来的产品，那就是硬实力！3、事业：我们正在踏踏实实做的这件事——打造煤炭供应链管理平台，注定成为中国产业互联网进程上辉煌的篇章。4、人才培养发展通道：从上到下全力发掘优秀人才，专业序列和管理序列双通道晋升；煤易宝大学开设“新人训练营”、通用素质能力、专业知识技能、领导力、管理知识和技能等培训，全面提升人才综合能力'],
        '112873490': ['1-1.8万/月', '五险一金|交通补贴|年终奖金|绩效奖金|定期体检|专业培训|员工旅游|', '武汉-洪山区', '5-7年经验', '本科', '招1人', '12-04发布',
                      '嵌入式软件工程师（应用方向）', '武汉能钠智能装备技术股份有限公司',
                      '岗位职责：\n1.负责产品软件的应用软件需求分析、方案设计协助制定具体项目研发计划；\n2.负责从事信号采集板卡应用软件的开发工作，主要完成windows平台上的上位机软件开发；\n3.负责完成windows平台软件测试、验证工作；\n4负责完成项目相关报告、文档编制工作；\n\n任职要求：\n1、大学本科以上学历，3年以上工作经验，电子、计算机、通讯类专业毕业；\n2、精通linux、windows下的C/C++编程及调试；熟练linux、windows下的多线程、TCP/UDP、多进程等方面的开发，熟悉常用通信协议和数据库应用优先；\n3、有丰富的实时嵌入式操作系统开发经验，具有高速信号处理、电子对抗、通信相关行业算法优化经验者优先；\n4、熟悉DSP/ARM/PowerPC/GPU硬件架构体系要求优先；\n5、英语四级以上，具备良好的外文文献阅读能力。\n6、良好的沟通与表达能力，思路清晰，较强的动手能力与逻辑分析能力；\n7、较好的英语读写能力，可轻松读懂专业英文文档；\n8、具备较强的学习能力、抗压能力，能够与下位机团队良好沟通；\n9、具备多种操作系统平台开发经验优先。\n职能类别：嵌入式软件开发(Linux/单片机/PLC/DSP…)\n关键字：软件开发linuxwindowsARM\n',
                      '上班地址：江夏区藏龙岛开发区研创中心25号楼',
                      '武汉能钠智能装备技术股份有限公司成立于2009年，是致力于军用特种计算机系统的设计、开发、生产、销售及系统集成一体化的高新技术企业，公司先后通过了***高新企业认证、湖北省双软企业认证、并建立省级技术中心，具备全套军工科研生产资质。公司占地面积约2000平米，公司拥有先进的研发技术和大批高尖端技术人才。研发团队占总人数65%以上，公司创始人及核心团队均为具有***军工科研院所经验的技术人员组成，有着10多年的技术积累和丰富的行业经验。公司专注于军用及特种嵌入式计算机系统设计，提供高性能计算平台、信息处理平台解决方案和设备，立足于提供自主知识产权的数字模块业务平台。在嵌入式计算平台、模块化计算平台、移动计算、国产化计算平台、数字信号处理平台等多个领域具有完整的产品线，具备CPCI、VPX、存储、信号处理等领域的产品的专业开发团队，可为客户提供高性能和国产化信息系统的设计开发等定制化产品服务。公司拥有基于军用嵌入式计算机系统的整体解决方案，研制出一系列基于X86、PowerPC等处理器平台的嵌入式模块化产品以及基于龙芯、飞腾、申威的国产化处理器平台的系统级解决方案，达到国内领先水平。公司拥有基于CPCI标准总线系列产品、VPX标准总线系列产品、高可靠性控制计算机系列、抗恶劣环境加固计算机系列、固态存储系列等5大系列产品，可为军工、轨道交通、航空航天、能源装备等行业领域提供完善、全面的嵌入式系统解决方案。客户遍及中船重工、中国兵器、航天科工、中电科、中国南车、国家核电等各大企业，并成功配套国家多项重点型号任务及技术改造项目。公司以“质量就是生命”为宗旨，以“服务客户，提升客户满意度”为根本出发点。公司先后通过了GB/T19001-2008质量管理体系及GJB9001B-2009武器装备质量管理体系的认证。以总经理为代表的管理团队亲抓产品质量和服务，不断提升产品质量，并向客户提供7天24小时服务。'],
        '116050651': ['1-1.3万/月', '周末双休|带薪年假|五险一金|绩效奖金|全勤奖|节日福利|通讯补贴|', '武汉-洪山区', '无工作经验', '本科', '招1人', '12-04发布',
                      '高级测试工程师', '武汉兴图新科电子股份有限公司',
                      '岗位职责：\n1、负责公司产品/系统需求评审，测试方案设计，测试用例评审等工作；\n2、负责产品/系统测试工具和手段提升，解决测试过程中遇到的难点问题；\n3、对所负责产品/系统测试产出件质量负责，对所负责产品最终交付质量负责；\n4、协助部门主管提升部门测试能力（如测试方法，测试效率等）；\n5、协助部门主管提升中级/初级工程师测试能力；\n技能要求：\n1、本科学历，至少5年以上测试经验；\n2、熟练掌握测试理论基础和日常研发测试流程；\n3、熟练编写测试计划，系统测试方案，测试用例，测试报告等；\n4、熟练掌握JAVA、PYTHON语言中的一种，能够开发测试工具优先；\n5、熟练掌握一种性能或者自动化测试工具使用；\n6、熟悉oracle数据日常使用和性能调优；\n7、熟悉linux操作系统日常操作和调优；\n8、有性能测试，可靠性测试、稳定性测试等相关工作经验优先；有音视频行业相关工作经验者优先；\n9、可适应短期出差。\n职能类别：系统测试软件测试\n',
                      '上班地址：武汉市东湖高新技术开发区光谷软件园C3栋8层',
                      '公司简介武汉兴图新科电子股份有限公司是专业从事音视频综合业务网络应用平台研发的高新技术企业和双软认证企业，公司总部位于世界五百强云集的“中国.光谷”,并在华东、华中、华南、西北、西南等地设有办事处或子公司，形成辐射全国的营销服务网络。公司拥有4000平米的研发中心。现有员工500余人， 技术研发人员占比高达75%。公司拥有ISO9001:2008 质量管理体系认证证书、软件研发CMMI-III级国际认证证书、ITSS信息技术服务运行维护标准三级等多项行业认证资质。公司成立10余年来，始终围绕企业使命和愿景开展技术及产品创新。创造性提出音视频中间件概念，采用先进的面向服务体系技术架构，开发完成了openVone音视频一体化中间件平台。未来，兴图公司将在公共突发事件应急指挥、城市建设、安全生产及现场指挥调度等领域，大力拓展民用市场，同时依托互联网和5G技术的高速发展，在智能安居、智慧养老、智慧办公等领域全面开拓“音视频+互联网”新产品、新业务，形成新产业布局。我们视员工为公司最宝贵的财富，因人而宜，量才适用，人尽其才，才尽其能。让想干事的人有机会，能干事的人有舞台；我们用心经营工作，真诚对待同事和客户，把大家当成亲人和朋友，实现工作与生活的完美结合，愉快工作，快乐生活。兴图新科欢迎您的加入！薪酬：具有市场竞争力的宽带薪酬，丰厚的绩效奖金，每年定期调薪，工龄工资每年递增；提供研发人员项目奖金、销售人员提成奖金、员工合理化建议及新产品构思奖金。福利：1、办理五险一金（养老、医疗、失业、工伤、生育保险、住房公积金）；2、双休、法定节假日、带薪年休假、国家规定的婚、产、丧假及相应补贴；3、丰富的企业文化及团队建设活动，设篮球、足球、羽毛球俱乐部，配置固定活动经费；事业：1、居于行业领先的市场地位：为行业持续提供领先的音视频应用产品和解决方案；2、富于协作的学习型组织：完善规范的流程制度与自由交流的技术沙龙统一互补；3、个性化的职业发展路线：针对员工特点提供不同职业发展规划，创造广阔的发展空间和自由施展才华的人生际遇；4、充分的培训机会：完善的内部培训体系与在职/脱产的外训结合，达成技术能力、个人职业素养全面提升。\xa0\xa0应聘人员发送简历请不要以附件形式发送！\xa0\xa0兴图新科招聘1群：244470542\xa0\xa0简历投递邮箱：zhaopin@xingtu.com\xa0\xa0微信：13429832589（张晓亮）'],
        '111009216': ['1-1.5万/月', '五险一金|带薪年假|专业培训|补充医疗保险|员工旅游|餐饮补贴|定期体检|年终奖金|绩效奖金|', '武汉-洪山区', '3-4年经验', '本科', '招若干人',
                      '12-03发布', 'QA工程师', '台达电子企业管理（上海）有限公司武汉分公司',
                      '\n\n岗位职责：\n\n负责大型Java系统或者大型分散式应用系统软件的测试，具体内容包括功能测试、集成测试、系统测试、性能测试、国际化测试等\n根据系统需求规格编写测试计划，设计测试用例\n编写高品质的测试用例和测试脚本，并准确执行测试用例，并验证测试结果，书写测试报告\n与开发人员合作沟通，协调测试额准备、执行和bug追踪及最终解决\n维护和升级已有的测试用例和脚本，满足新业务实现要求\n\n任职要求：\n\n计算机相关专业本科以上，硕士优先，985和211大学优先\n三年以上测试经验，其中两年以上Web功能测试经验，和一年以上开发或自动化测试经验，同时满足为基本条件\n熟悉敏捷项目开发模式\n有性能测试经验、外企（英文工作环境）、知名公司成熟项目工作经历有加分\n熟悉至少一门开发语言，需要在实际项目中使用过，JAVA优先\n熟悉测试框架TestNG&Junit，LinuxShell编程有加分\n\n\n职能类别：软件测试\n',
                      '上班地址：东湖高新区光谷大道77号金融港B22栋',
                      "台达创立于 1971 年，为电源管理与散热解决方案的领导厂商，并在多项产品领域居世界级重要地位。面对日益严重的气候变迁议题，台达秉持「环保 节能 爱地球」的经营使命，运用电力电子核心技术，整合全球资源与创新研发，深耕三大业务范畴，包含「电源及零组件」、「自动化」与「基础设施」。同时，台达积极发展品牌，持续提供高效率且可靠的节能整体解决方案。台达营运据点遍布全球，在中国台湾、中国大陆、美国、泰国、日本、新加坡、墨西哥、印度、巴西以及欧洲等地设有研发中心和生产基地。近年来，台达陆续荣获多项国际荣耀与肯定。自2011年起，连续六年入选道琼永续指数(Dow Jones Sustainability Indexes, 简称DJSI) 之「世界指数」(DJSI World)，2016年CDP(国际碳揭露项目)年度评比，台达从超过5,800家回复CDP问卷的全球大型企业中，获得气候变迁「领导等级」的评级。台达集团的详细资料，请参见：http://www.delta-china.com.cn/\xa0About DeltaDelta, founded in 1971, is a global leader in power and thermal management solutions and a major player in several product segments such as industrial automation, displays, and networking. Its mission statement, “To provide innovative, clean and energy-efficient solutions for a better tomorrow,” focuses on addressing key e***ironmental issues such as global climate change. As an energy-saving solutions provider with core competencies in power electronics and innovative research and development, Delta's business categories include Power Electronics, Automation, and Infrastructure. Delta has 153 sales offices, 61 R&D centers and 40 manufacturing facilities worldwide.Throughout its history, Delta has received many global awards and recognition for its business achievements, innovative technologies and dedication to corporate social responsibility. Since 2011, Delta has been selected as a member of the Dow Jones Sustainability? World Index (DJSI World) for 6 consecutive years. In 2016, Delta was selected out of 5,800 large companies by CDP (formerly the Carbon Disclosure Project) for its Climate Change Leadership Level.For detailed information about Delta, please visit: http://www.delta-china.com.cn/"],
        '110284101': ['12-35万/年', '免费班车|员工旅游|交通补贴|通讯补贴|五险一金|周末双休|带薪年假|年底十三薪|包吃包住|', '武汉-洪山区', '1年经验', '大专', '招1人',
                      '12-03发布', '测试工程师', '武汉长兴集团有限公司',
                      '选择长兴集团，亮点在这里：\n1、万亿市场规模，在国家“一带一路”战略的推动下，随着我国电网投资规模的不断增加，我国电力装备企业将迎来巨大的市场发展空间；\n2、长兴集团制造业根基深厚，30年发展历程，年均10亿＋的销售额，华中地区最具影响力的国内一流配电设备制造企业之一；\n3、知名企业，武汉100强企业，公司平台大、管理规范、社会资源丰富，有机会接触更多大项目、大人物，发展快速；\n4、多元化发展，3家高新技术企业，12家子公司，经营状态稳定，工作相对稳定；\n岗位职责：\n1、负责公司智能配电、用电产品的软件测试及硬件测试；\n2、依据产品需求，完成产品的测试计划及测试用例的设计和编制；\n3、搭建测试环境，按照测试计划及测试用例，完成产品的软、硬件功能及性能测试；\n4、对测试结果进行分析总结，编写测试报告，并对缺陷进行跟踪，推动问题及时解决；\n5、产品生产过程的技术支持；\n6、用户现场的产品技术答疑和技术沟通。\n任职要求：\n1、1年以上电力自动化产品或用电信息采集或电力仪表等行业的工作经验；\n2、电气工程、自动化、电力电子或相关专业专科及以上学历；\n3、了解基础的EMC测试；\n4、具备国网用电信息采集设备或故障指示器软、硬件测试工作的相关经验，熟悉相关技术规范者优先；\n5、具备良好的逻辑思维能力和分析复杂问题的能力，能够快速定位缺陷并深入分析查找原因；\n6、工作认真，责任心强，积极主动，具有良好的团队合作精神。\n福利待遇：\n1、花园式的办公环境：办公地点位于金银湖生态旅游区，宽敞舒适的办公环境，单纯的人际关系，自由平等，无障碍的沟通方式；\n2、公司免费提供住宿；\n3、享受国家法定节假日、带薪年假、婚丧假、产假、陪产假等福利假期；\n4、节日礼品：端午节、中秋节、春节等节日公司公司会派发节日慰问物资；\n5、工会活动：每季度至少一次员工活动，生日会、出游、拓展训练、运动会、聚餐、唱歌等各种各样的活动；\n6、免费的职工活动中心：设有影视厅、图书馆、电子阅览室、茶吧、健身房、瑜伽室、桌球厅、兵乓球室、篮球场、足球场等休闲娱乐场所，员工可免费使用；\n7、出国旅游：公司不定期安排员工出国旅游、学习考察；\n8、享受标准五险（养老保险、生育保险、医疗保险、失业保险、工伤保险）福利保障；\n\n只要你愿意，长兴集团就是让你展现自己的舞台，真诚期待你的加入！！！\n求职小贴士：如果您对我们公司提供的岗位有意向，可来电话询83247802/83372616我们会优先为您安排面试！\n职能类别：测试工程师软件工程师\n关键字：EMC测试测试工程师软件测试硬件测试高级测试\n',
                      '上班地址：湖北省武汉市东西湖吴家山经济技术开发区（***）海口电力工业园海口二路',
                      '武汉长兴集团有限公司始创于1992年，总部位于武汉市东西湖区吴家山经济技术开发区（金山大道）海口工业园，占地10万余平方米，注册资本1.46亿元，在职员工千余人，是湖北省以研发、生产、销售和服务为一体的，以35kv及以下的电气配电设备、35kv及以下的中低压开关、户内户外断路器、直流牵引配电设备、牵引直流开关、直流综合微机保护、电力工程总包及施工安装、钣金机柜制造等为主导产业的企业集团。\xa0\xa0\xa0\xa0\xa0\xa0\xa0企业实施集团化管理体制和运行模式，在集团董事会确立的以工业电器制造为主业，创造品牌化、多元化经营战略思想的指导下，集团以武汉长兴电器发展有限公司、武汉中直电气股份有限公司、武汉倍诺德开关股份有限公司为工业制造核心企业，并带动集团下属的武汉兴源达电力工程安装有限公司、武汉泰易德钣金机柜有限公司等工业子公司的发展。公司始终坚持科技创新，工艺创新，质量至上，打造品牌企业。多年来不断探索研发新产品，并进入智能电气设备高新产品的研发领域，成熟精湛的生产工艺和完备的技术装备，工业电器制造作为主导产业是长兴集团得以不断发展壮大的坚实基础。\xa0\xa0\xa0\xa0\xa0\xa0\xa0长兴集团在做好工业主业的同时，积极拓展房地产、生态农业、园林、度假休闲、物流、商贸、项目投资等二、三产业。先后成立了武汉四海通房地产有限公司、武汉春景园林工程有限公司、十堰长能电器有限公司、武汉源兴科技有限公司、红安桃花塔生态农业有限公司等多家子公司。所涉及的各个行业已逐渐形成一条和谐而可持续发展的产业链，使集团的资源得到了充分有效利用，形成产业多元化，发展规模化、经营专业化、业务区域化、管理差异化的产业格局。\xa0\xa0\xa0\xa0\xa0\xa0\xa0长兴集团通过加强企业党建、工会、科协等组织平台的建设，坚持制度创新、管理创新的同时，坚持“以人为本、和谐长兴”的文化理念，不断探索并努力寻求建设具有长兴特色的企业文化，建立起高效率的管理团队和员工队伍。秉承“个人与企业的发展融为一体，坦诚、高效、持续发展，既让个体生命展现光华，也使企业快速成长，塑造高素质人才，创建中国民族品牌”的企业愿景，以“做强做大”为宗旨，持续引进高新技术，优化生产管理和人力资源管理，扩大研发生产规模，且根据自身特点建立并完善“以人为本”的现代化管理制度，以一流的技术、质量、服务、信誉，积极参与国内、国际高新技术领域的竞争，着力打造民族品牌，为社会稳定和经济发展做出更大贡献，实现属于我们长兴人的“长兴梦”——“走持续发展之路，创百年长兴企业”。公司地址：湖北省武汉市东西湖吴家山经济技术开发区海口电力工业园海口二路邮政编码：430040公司网站：http://www.whcxdq.com联系电话：83247802'],
        '118358324': ['1-1.5万/月', '五险一金|免费班车|员工旅游|餐饮补贴|专业培训|绩效奖金|年终奖金|', '武汉-武汉经济开发区', '无工作经验', '本科', '招1人', '12-02发布',
                      '产品测试工程师', '武汉神动汽车电子电器股份有限公司',
                      '1、依据产品需求，负责项目的测试方案，测试用例，测试报告输出\n2、掌握测试基本理论，搭建测试平台，按照测试计划，完成产品测试任务\n3、对测试结果进行分析总结，编写测试报告，并对缺陷进行跟踪，推动问题及时解决；\n4、能够积极主动与客户现场人员沟通问题，协助研发准确定位排查问题\n\n任职要求：\n1、全日制本科及以上学历，电子信息、计算机、通信、测控、机电一体化、电气自动化等相关专业。\n2、有较强责任心以及兜底意识、有较强的团队合作意识和抗压能力，有较强的自我驱动力，能接受短期出差。\n3、有较强的沟通协调能力，逻辑性强。\n4、熟悉至少一种缺陷管理工具，熟悉汽车行业电器产品相关标准。\n职能类别：软件测试\n',
                      '上班地址：枫树新路8号',
                      '武汉神动汽车电子电器股份有限公司（以下简称神动公司）成立于2009年1月，神动公司的主营业务为汽车电子电器、车载电源、汽车配件的制造与销售（国家有专项规定项目的经审批后或凭有效许可证方可经营）。神动公司于2010年通过ISO/TS16949认证并形成批量生产能力，截至2016年形成年产汽车传感器200万只的产能规模。现已成为集研发、生产和销售于一体的专业化汽车电子及传感器系列产品的湖北省高新技术企业。武汉神动以自身发展潜力，以及企业在业界内的广泛好评，吸引各类人才和投资者。2016年8月新三板挂牌成为上市公司，股票代码8383214.\xa0\xa0\xa0\xa0武汉斯马特益电子技术有限公司（以下简称斯马特益）是由武汉神动控股发起、一汽专家加盟、国内知名投资人参与、于2017年11月注册成立的、专业从事车载电源产品、车载储能产品和智能网络传感器产品研发的高科技公司。斯马特益秉持“科技创新、以人为本”的经营理念，热忱欢迎车载电源行业专家的加盟，为成就公司事业、助力我国新能源汽车产业发展而激扬创新！'],
        '115439380': ['1-1.5万/月', '五险一金|', '武汉-黄陂区', '5-7年经验', '本科', '招1人', '12-02发布', '质量经理 (MJ000626)',
                      '神州数码系统集成服务有限公司深圳分公司',
                      '岗位职责：\n1、能熟练编写项目测试计划和测试用例，至少熟悉一种缺陷管理软件；\n2、熟悉软件工程、软件测试理论和方法，熟悉常用的测试方法、测试工具、测试流程与测试文档规范，较强的分析问题的能力；\n3、熟练指定软件质量保证计划，参与软件项目评审、确认工作；\n4、逆向思维及对缺陷的敏感性、沟通，计划及执行力较强，擅长团队管理工作；\n5、良好的职业操守逻辑思维能力强，良好的沟通表达能力。\n岗位要求：\n1.计算机专业本科以上学历，具4年以上软件测试经验，2年以上团队管理经验；\n2.熟悉软件测试的流程，掌握基本的软件测试方法，熟练编写各类测试相关文档；\n3.熟练掌握接口测试、数据库测试、系统测试、性能测试方法；\n4.具备Loadrunner、Jmeter等工具或框架的使用经验；\n5.熟悉Oracle、MySQL数据库，并能熟练使用sql语句进行数据操作；\n6.熟悉Linux常用命令，有一定的测试环境搭建及环境维护能力；\n7.性格开朗乐观，责任心强，积极主动，善于沟通，具有良好的团队精神。\n\n熟悉银行业务，有核心业务测试经验者优先；\n职能类别：软件测试\n关键字：质量经理测试经理银行\n',
                      '上班地址：湖北省武汉市黄陂区盘龙城经济开发区汉口北大道88号汉口北国际商品交易中心D2区1-2层、22-23层众邦银行',
                      '公司简介神州数码信息服务股份有限公司，中文简称：神州信息；英文简称：DCITS；股票代码：000555.SZ ；三十余年的发展历程，国内最早参与行业信息化建设的企业之一，以业务模式和技术产品创新引领和推动中国信息化进程和信息服务产业的发展，支撑数字中国的使命。依托云计算、大数据、量子通信等技术，面向金融、政企、电信、农业、制造等行业提供规划咨询、应用软件设计与开发、技术服务、云服务、数据服务、量子通信等服务内容，以数据赋能行业创新升级，助力产业升级、价值重塑。'],
        '118129292': ['1-2万/月', '五险一金|补充医疗保险|员工旅游|绩效奖金|年终奖金|弹性工作|', '武汉-武昌区', '5-7年经验', '本科', '招1人', '12-02发布',
                      'QA主管/QA Lead', '广州澳图美德信息科技有限公司',
                      '岗位职责：\n1、根据规范和要求制定并执行测试计划，测试计划和脚本；\n2、开发和执行手动测试用例；\n3、开发自动化测试脚本；\n4、支持和与开发团队紧密协作；\n5、及时提交问题报告和测试报告；\n6、提供反馈意见以改善可交付成果的质量以及质量检查流程；\n7、遵循文档，版本控制，质量保证，问题管理等中定义的***实践和程序。\nJobResponsibilities\ni.Developandexecutetestschedules,testplans,andscriptsbasedonspecificationsandrequirement\nii.Developandexecutemanualtestcase\niii.Developautomationtestscript\niv.Supportandcoordinatecloselywiththedevelopmentteams\nv.Issuereportingandtestreport\nvi.ProvidefeedbacktomakeimprovementinthequalityofdeliverablesaswellastheQAprocess\nvii.Followbestpracticesandproceduresdefinedindocumentation,versioncontrol,qualityassurance,issuemanagementetc.\n\n职位要求：\n1、IT或相关专业的本科毕业；\n2、至少6年的测试用例准备经验；\n3、具有测试自动化方面的工作经验并熟悉Selenium，熟悉Java+Selenium；\n4、熟悉Java和SQL，具有Python基本知识；\n5、负责任，有动力，头脑细心，有条理和积极主动；\n6、有Scrum经验将会优先考虑；\n7、良好的分析和沟通能力；\n8、良好的英文读写能力；\nJobRequirements\ni.DegreeHolderinITorrelatedfields\nii.Atleast6years’experienceintestcasepreparation\niii.WorkingexperienceintestautomationandfamiliarwithSelenium\niv.BasicknowledgeinJava,Python,SQL\nv.Beresponsible,motivated,detailedminded,organizedandpro-active\nvi.ExperienceinScrumwouldbeanadvantage\nvii.GoodInterpersonal,Analytical&CommunicationSkills\nviii.GoodcommandofwrittenEnglish\n\n备注：ASL是香港集团公司，目前有意向在武汉拓展业务开设子公司，因此需开展招聘。\n目前中国大陆地区主要子公司在广州（广州澳图美德信息科技有限公司），所以刚开始的招聘工作会从广州出发，请留意来自广州的固话来电，我们会提及有需要跟香港部门经理进行视频面试或者部门经理去到武汉进行面试。此属于我们公司正规内部操作，务必放心！\n职能类别：软件测试\n',
                      '上班地址：丁字桥路',
                      '广州澳图美德信息科技有限公司（Guangzhou Automated System）广州澳图美德信息科技有限公司是自动系统集团有限公司(ASL)在大陆地区的全资子公司，成立于2006年底，主要负责ASL在大陆地区的业务。ASL自1973年成立于香港，1997年于香港联交所上市（SEHK：771）。在香港地区服务逾35年，客户遍及各行各业，拥有丰富的行业知识和经验，是业界领先的信息科技供应商，员工总数超过1300人，业务主要包括：系统集成、应用开发及外包、软硬件产品的销售、服务外包、专家及顾问服务、咨询及培训、数据中心托管、维护支持等。你有本领，我们有舞台，ASL期待你的加入！更多信息请浏览官网：http://www.ASL.com.hk/'],
        '114574719': ['1-1.3万/月', '交通补贴|餐饮补贴|弹性工作|出国机会|绩效奖金|', '武汉-洪山区', '3-4年经验', '大专', '招4人', '12-02发布', '测试工程师',
                      '武汉伺动科技有限公司',
                      '岗位职责：\n1、根据项目计划制定测试用例并实施，保证项目质量和进度；\n2、跟踪定位产品项目中的缺陷或问题，与项目相关人员就项目进度和问题进行沟通；\n3、参与程序架构和代码的评审工作，并提出改进意见和可测试性建议；\n4、根据项目设计与实现有关自动化测试的代码与用例；\n5、根据项目特点,开发合适测试工具或自动化解决方案，提高测试效率。\n6、负责产品测试技术文档积累。\n任职要求：\n1、工科、计算机或其他相关专业专科以上学历；\n2、有3年以上软件测试经验，\n3、精通软件测试理论、方法和过程，熟悉常用的测试策略、测试用例设计方法等；\n4、熟悉Linux或Unix操作系统；\n5、熟悉Oracle/Sqlserver/MySQL等常用数据库系统的操作，能熟练编写SQL语句；\n6、掌握编程语言Java和Python；\n7、掌握常见的Web测试框架，如RobotFramework、Selenium、Jmeter等；\n8、对软件测试有浓厚的兴趣和丰富的经验，有很强的分析能力和定位问题的能力；\n9、有很强的责任心，做事严谨，有良好的的沟通、团队协作意识及多任务协调能力。\n职能类别：软件测试\n',
                      '上班地址：光谷资本大厦4楼',
                      '武汉伺动科技有限公司成立于2015年11月，注册资本200万。公司在移动营销平台开发基础上，通过多元化的应用场景实现“移动互联网+”的落地经营。在教育领域，通过软硬结合来解决学校或者机构遇到的各类问题。 移动互联网是当下互联网发展的大趋势，手机应用成为众多企业关注的热点，伺动科技通过将设计创新、产品研发与已有的传统标准流程相结合的方式，成功帮助客户部署了移动应用并在市场拓展、品牌传播方面取得了巨大成效。主要合作企业及项目有，武汉工程大学云阅卷系统，郑州铁路局铁路运营教学仿真系统，宁夏智慧城市呼叫中心标段，湖北蜂之宝蜂业电商运营，湖北石首经济开发区扩区调区咨询等等……。2016年参与武汉市智慧园区建设标准编制的整个流程（招投标及标准制定）。'],
        '45021829': ['1-1.5万/月', '五险一金|绩效奖金|员工旅游|餐饮补贴|年终奖金|专业培训|', '武汉-江汉区', '5-7年经验', '本科', '招3人', '12-02发布', '项目开发经理',
                     '武汉长达系统工程有限公司', '职能类别：项目经理项目主管\n关键字：B/SC/S.NET架构分析设计测试项目开发管理PMP\n',
                     '上班地址：武汉市汉口发展大道166号江锋大厦A座12楼（汉口火车站斜对面，紧挨武汉科技局旁）',
                     '企业简介\xa0\xa0\xa0\xa0\xa0武汉长达系统工程有限公司成立于1992年7月，是国内最早从事全国城市环境综合治理、省建设大数据平台、省房地产大数据监测平台、省城乡污水治理大数据平台、省垃圾治理大数据平台、市政工程项目管理、建筑业、信息化、房屋维修资金、住房公积金等建设领域信息化研发的高新技术企业。30年来公司完成了全国城市污水处理信息管理系统、国家水质检测网信息系统、全国城市环境综合整治考核系统、全国城市（县城、村镇）建设统计年报、中国西部小城镇环境基础设施经济适用技术示范信息系统（国际合作项目）、全国市政公用利用外资信息系统、国家统计局《中国城市建设年鉴》、交通部全国成品油管理信息系统、全国质量安全信息管理平台、全国建筑节能管理系统、全国建筑业统计月报、全国建筑业快速调查、全国建设行政许可动态管理系统（施工、监理、招标代理、物业、园林、建造师、监理工程师、造价师、物业管理师等）、国家安居工程统计、全国住宅AAA级认定系统、江苏省建设领域全行业经济运行信息平台、黑龙江省建设领域全行业经济运行信息平台、安徽省重大危险源动态管理系统、湖北省建设大数据整合共享平台、湖北省房地产大数据监测平台等一批重点项目，并承担了住建部“城市建设统计指标体系研究”、“建筑业统计指标体系研究”、“城市建设主要指标月度快速调查研究”、“住房公积金管理信息系统”、“房屋维修资金管理信息系统”等国家研究课题项目16个，目前已拥有核心技术相关的知识产权65件，先后取得ISO9001、ISO27001、ISO20000和ITSS三级、AAA级信用企业等各种资质和认证。\xa0\xa0\xa0\xa0作为一个27年的企业，凭借雄厚的技术实力和完善的服务体系，长达获得了客户的一致赞誉，我们正在努力把自己变得更有趣，更迷人，每项工作都要用最具创新的方式来实现。我们拒绝所有形式上的浮夸，以周为单位，衡量自己和团队的成长，我们希望你拥有如下特质：1、对世界充满好奇，强烈的求知欲望；2、拥有冒险精神，乐于挑战自己，挑战权威；3、认为学习是终生命题，喜爱阅读，特爱科学；4、追求自由，不随波逐流，不盲目跟从；5、再有一点浪漫主义情怀，热爱生活，乐观积极；\xa0\xa0\xa0\xa0我们不要大牛，只靠汗水，需要志同道合的你的加入，你将是其中很重要的角色！别人有的我们都有，别人没有的我们也有,面试了解更多：福利待遇1、五天八小时工作制，轻松的工作环境和一群乐观正能量满满的小伴们；2、五险一金，这个必须得有；3、带薪假期，提供国家规定的法定节假日，以及公司年假；4、只要你善于学习、诚实努力，就会得到无限的上升空间和成长机会；我们的薪酬原则是待遇和能力成正比；5、boss主张扁平化的管理风格；6、超酷团建，户外outing、漂流、cs、爬山烧烤、球类比赛欢乐多；最重要的是，如果你想开开心心地coding & working，那么，快加入我们吧！有意者请将个人简历（中、英文均可）、薪资要求发送e-mail至公司专用招聘邮箱（公司会对应聘人的个人资料保密，请勿来访，资料恕不奉还）。应聘邮箱：85617711cd@163.com/hr@cdkj.net，欢迎猛戳！联系人：付***、联系电话：027-85617711'],
        '116235388': ['1.2-3.5万/月', '五险一金|年终奖金|绩效奖金|', '武汉-江汉区', '5-7年经验', '本科', '招20人', '11-27发布', '电池+电驱动+热管理（广州）',
                      '武汉高起企业管理咨询有限公司',
                      '要求学历本科，工作地点广州南沙区，WX：308054947\n电池系统集成经理\n电池系统开发工程师\n电池试验试制工程师\n电池系统试制工程师\n充电及高压系统经理\n充电及高压系统工程师\n低压系统工程师\n电池系统高级经理\n充电系统集成资深工程师\n电池系统集成高级经理\n电池系统开发经理\n控制管理高级经理\n系统开发经理\n系统功能开发与集成工程师\n策略开发经理\n控制策略开发工程师\n基础软件开发工程师\n整车标定主任工程师\n整车性能标定工程师\n控制策略开发高级经理\n电力电子系统工程师\n减速器主任/资深工程师\n系统集成与验证经理\n悬置与NVH开发工程师\n电驱动高级经理电机\n电磁设计工程师\n电驱动总成NVH工程师\n电驱动资深硬件工程师\n电驱动资深软件工程师\n电机控制软件工程师\n电机控制软件测试工程师\n热管理分析验证工程师\n空调产品工程师\n空调空气质量工程师\n整车热管理系统资深工程师\n整车热管理控制器工程师\n整车空调及热管理功能开发工程师\n整车热管理控制资深工程师\n整车冷却模块资深工程师\n整车冷却系统附件工程师\n三电热管理性能匹配仿真工程师\n空调系统CFD仿真工程师\n电池包热管理系统仿真工程师\n职能类别：汽车设计工程师\n',
                      '上班地址：南沙区',
                      'COAHR（高起）一直只专注于汽车领域的管理咨询与培训服务。COAHR是“CAR”、“COACH”、“HR”的组合，英文含义为：汽车业人力资源教练。高起的中文含义为：我们提供每一次服务都成为客户发展的更高起点！\xa0\xa0\xa0\xa0COAHR的顾问团队COAHR的顾问团队由多年从事汽车销售与服务、汽车维修与技术等方面的四十余位杰出职业经理人或优秀管理经营者组成，成为汽车领域***的的专家团队之一。均有良好的教育背景、骄人的工作与经营业绩。都接受过严格的培训师、咨询师资格训练，能确保一流服务水准。 80%的专家均获得过国内汽车公司总部授权培训或咨询资格。同时具备现场调研、设计开发、培训辅导的综合实力！COAHR的服务特点我们的定位是：研究型汽车培训咨询机构。培训咨询课题全部针对客户核心业务需要。通过培训引导“员工行为产生行为”，通过咨询促进“企业提升整体绩效”。我们一直在认真研究中国汽车领域的每一个细微动向，细心捕捉每一家客户不同的“管理文化表现”，加以科学整理分析，最终结合顾问的职业素质、丰富经验、专业智慧顺利达成“管理者代表”的期望目标！COAHR的成绩经过多年努力，COAHR已为国内六十余家汽车主机厂提供营销与服务管理咨询、培训服务，涉及中国23个省市的1200余家经销商与服务站，学员数量累计12000余人。'],
        '118481203': ['1.2-1.8万/月', '', '武汉-武昌区', '3-4年经验', '本科', '招1人', '11-27发布', 'Java中级开发工程师',
                      '北京捷泰天域信息技术有限公司武汉分公司', '\n\n职能类别：高级软件工程师\n关键字：javaSpring分布式容器云计算GIS\n', '上班地址：中南路2-6号中建广场B座24楼F室',
                      'GISUNI（北京捷泰天域信息技术有限公司）成立于2011年12月，是一家空间信息领域的国家高新技术企业，是国内领先的地理平台全面解决方案与服务提供商。目前公司总部位于北京，在上海、广州、武汉、成都等地设有分公司和办事处，拥有近150人的技术研发和咨询服务团队。公司获得ISO9001质量管理体系认证、ISO27000信息安全管理体系认证，及互联网地图服务甲级测绘资质。GISUNI以“用地理的智慧帮助他人”为企业经营理念，针对地理大数据、云计算、移动互联网、人工智能等应用需求的爆发式增长，研发了多项具有自主知识产权的系列产品，并拥有多项核心专利技术。公司拥有平台产品、工具产品和数据产品以及全面的解决方案，广泛应用于智慧城市、政府、金融、地产、零售、汽车、物流、传媒、教育等20余个行业，***限度帮助用户提升地理信息的应用价值。地理平台一体化解决方案GISUNI作为全球领先的GIS平台软件及服务提供商——Esri公司在中国的战略合作伙伴，通过在产品层面、业务层面的深度合作，为覆盖数十个行业的用户及多家合作伙伴，提供地理平台一体化解决方案，涵盖数据生产、数据管理、快速制图、GIS 服务发布与管理、成果共享与交换、云GIS平台搭建和资源管理、平台运维保障等各个环节，能有效地帮助用户提高开发效率、优化资源管理和降低建设成本。位置智能平台解决方案GISUNI凭借深厚的GIS技术背景及多年行业应用经验，打造了国内领先的位置智能平台——智图GeoQ（www.geoq.cn），提供地理大数据分析与智能化的解决方案。GeoQ位置智能平台提供可靠的地理大数据、可拓展的开发接口以及精美的数据可视化方案。无论是政府、企业、互联网、媒体、高校，或是地图爱好者、开发者，都能够轻松获得数据可视化工具和地图相关的数据服务资源。通过专业地理大数据分析模型与用户业务数据的结合，GeoQ位置智能平台可为政府数据开放、商业选址、物流配送、经营分析、市场营销、媒体传播等多个应用领域提供综合解决方案。'],
        '84733450': ['10-15万/年', '五险一金|补充医疗保险|免费班车|餐饮补贴|专业培训|定期体检|绩效奖金|年终奖金|', '武汉-江夏区', '无工作经验', '本科', '招6人',
                     '11-26发布', '协议测试工程师', '武汉虹信通信技术有限责任公司',
                     '岗位职责\n1、负责5G设备系统功能与性能测试工作；\n2、负责我司5G设备的开通调测及日常外场测试工作；\n3、负责运营商组织的5G实验室和外场测试工作。\n\n任职要求：\n1、5G或LTE等制式基站、核心网、终端等产品协议栈测试或开发经验；\n2、熟悉3GPP系列规范，对NAS/RRC/PDCP/RLC/MAC/物理层、S1、X2、S6a、S10等协议有深入理解；\n3、熟悉TCP/IP网络协议和以太网络配置，熟悉测试环境的搭建，具有一定的问题定位能力；\n4、能适应加班和出差，有主动性和强烈的责任心，良好的团队协作意识和较强的沟通能力。\n职能类别：系统测试软件测试\n',
                     '上班地址：谭湖二路1号',
                     '烽火科技集团（原武汉邮电科学研究院）是中国优秀的信息通信领域产品的综合解决方案提供商，“武汉·中国光谷”的核心企业，直属国务院国有资产监督管理委员会管理，是中央直属的117家央企之一。集团目前已形成覆盖光纤通信技术、无线通信技术、数据通信技术、与智能化应用技术四大产业的发展格局。武汉虹信通信技术有限责任公司系烽火科技集团第二大全资骨干企业，是烽火科技集团无线通信领域的核心平台企业，旗下子公司包括武汉虹旭信息技术有限责任公司、武汉虹信技术服务有限责任公司、深圳市虹远通信有限责任公司、武汉虹捷信息技术有限公司。公司秉承“专业提升无线网络价值”的核心使命，以公网无线通信产品应用领域为主，向专网无线技术应用、软件及增值业务等领域发展，成为“国内一流、国际知名”的无线通信领域整体方案提供商。\xa0\xa0\xa0\xa0虹信通信是国内领先的无线通信整体方案提供商和系统集成服务商，现有员工4000余人，公司在武汉设有核心研发中心，并在北京、深圳分设有研发机构。已在全国建立了31个省级代表处以及108个二级代表处，在海外建立了常驻代表处，形成了覆盖全国，面向世界的市场营销和工程服务网络。公司网址：www.hxct.com【发展历程】●2G时代（1998-2008）：成功研制国内首台“移动通信直放站光纤传输设备”，国内首创移动通信室内、室外分开覆盖的解决方案，国内首个GSM网络室内覆盖系统公司：北京国贸大厦，国内无线网优覆盖行业的领军者。●3G时代（2008-2013）：产业链不断延伸，产品类型持续丰富：网优设备、RF器件、天线、数字微波、无线宽带接入、通信电源、软件及移动增值业务等，建设遍布全球数以百万计的无线网优覆盖精品工程提供无线网优的整体解决方案。●4G时代（2013-2016）：LTE基站主设备全面入围三大运营商集采，公司转型成为无线通信领域主流解决方案提供商；无线服务拓展至通信一体化服务领域，覆盖全国30个省份的电信基础建设和网络运维，同时拓展移动互联网络安全、智慧建筑和信息服务业务，更好地为未来综合智能信息服务提供支撑。●5G时代（2016至今）：启动5G预研，有序推进5G网络的研发和实验工作，对5G各项关键技术进行研究和论证，推进NB-IOT、天线增强技术、波束成型、3D MIMO的研发和实验工作， 2020年将启动5G网络商用。\xa0\xa0\xa0公司的发展需要源源不断的人才加盟，真诚邀请优秀的您加盟虹信公司，共创美好未来。\xa0\xa0\xa0请关注虹信招聘（微信公众号：FH_HONGXIN），我们将随时发布最新招聘信息。'],
        '116639044': ['1-1.5万/月', '五险一金|补充医疗保险|补充公积金|专业培训|绩效奖金|年终奖金|员工旅游|定期体检|交通补贴|通讯补贴|', '武汉-武昌区', '2年经验', '大专',
                      '招1人', '11-21发布', 'IT运维工程师', '武汉路成电力设备工程有限公司',
                      '1、负责项目现场内部网络和应用的日常维护、技术评估，包括网络交换机、路由器、防火墙、网络监控系统、终端等。\n2、对项目现场数据机房，信息系统及设施的日常检查、监控、运维分析。\n3、负责项目现场业务服务器的资源调配和系统安全、数据备份；负责各项数据的监控，如流量、负载等；\n4、负责项目现场会议系统支撑和保障。\n5、制定技术培训方案，对项目现场人员进行培训。\n\n岗位要求：\n1、计算机或网络相关专业，具有计算机信息系统集成项目、IT运维工作经验优先考虑。\n2、熟练掌握计算机软、硬件及网络技术知识，能够灵活运用，准确判断项目用户需求和问题所在，提出解决方案。\n3、熟悉主流厂商网络、安全设备安装、配置、维护、故障排除。\n4、具备良好的服务意识、沟通协调能力和团队合作精神。\n5、具有网络工程师认证证书、ITSS证书者优先。\n6、熟悉计算机分级保护项目者优先。\n职能类别：项目主管软件测试\n',
                      '上班地址：中南路路口',
                      '武汉路成电力设备工程有限公司成立于2014年9月18日，主要从事为国家电网、南方电网下属各省电力公司提供电力、通信、视频和自动化仪器仪表等设备的销售、安装、维护服务等业务。公司注册资本500万元。公司总部位于上海，同时在上海、湖南、江西、山东四省设立了分公司。公司作为世界著名通信设备生产厂商华为、诺基亚上海贝尔、烽火等公司的产品代理商，不断将业务拓展到全国电力市场。公司主要销售产品包括交换机、光传输设备、宽带接入设备、数据网络设备、软交换系统、综合复用设备、微波通信系统、通信网管系统等大型专业通信系统，在国内的电力通信行业有着骄人的销售业绩，良好的信誉和售后服务让我们赢得了客户广泛的信任。公司目前拥有员工近1000人，其中本科以上学历者占多数，为公司的发展奠定了良好基础。'],
        '118480910': ['1.2-1.8万/月', '五险一金|补充医疗保险|交通补贴|餐饮补贴|通讯补贴|定期体检|年终奖金|', '武汉-武昌区', '3-4年经验', '本科', '招若干人',
                      '11-21发布', 'Java开发工程师', '易智瑞（中国）信息技术有限公司武汉分公司',
                      '1、负责公司GIS中台相关工具及平台的设计和优化方案制定，并参与定制化开发。\n2、负责公司基于容器云平台的设计，功能开发，产品的落地实施；设计并开发生命周期管理、发布部署、任务调度、监控运维等自动化子产品，并支撑公司的业务应用开发和部署。\n3、独立完成模块代码的编写以及代码质量控制。\n4、系统调优及协助系统调试、软件测试工作。\n任职要求：\n1、3年及以上开发工作经验，熟练运用java开发语言，熟悉sprintboot，springcloud；熟练掌握mysql数据操作；熟悉linux环境；熟悉maven等编译部署工具。\n2、对云计算(IaaS、PaaS、SaaS)及DevOps、CI/CD有一定的实战和见解；熟练Docker的使用，有kubernates、DockerSwarm至少一种资源编排工具开发运维经验。\n3、熟悉分布式服务架构设计，对redis、zookeeper、RabbitMQ、ActiveMQ、kafka有一定的深入了解和分析。\n4、思路清晰，思维敏捷，有快速的学习能力。\n5、具备良好的分析、解决问题的能力，良好的沟通能力和团队协作精神。\n职能类别：软件工程师互联网软件开发工程师\n',
                      '上班地址：中建广场B座',
                      'Esri中国信息技术有限公司（Esri China Information Technology Co. Ltd.，简称：Esri中国）是Esri公司在中国大陆的***分支机构，是具有独立法人资格的独资企业，目前拥有7家分公司，近100人的高素质服务团队，为客户提供基于地理信息技术的系统设计咨询、技术支持、教育培训等服务。公司还与“中国科学院国家资源与环境信息重点试验室”联合建立了“ArcGIS中国培训中心”，并与国内200多家单位和专业机构建立了合作伙伴业务关系，为用户提供全方位的解决方案。Esri中国自成立之初就一直致力于推动中国空间信息产业发展，将国外先进的GIS技术、理念和应用引进国内，帮助用户充分挖掘数据的潜在价值，提升服务能力和水平，降低成本；同时还积极投身环保、减灾等公益事业，不遗余力地参与中国GIS教学和科研建设，促进人才的培养和应用水平的提升。目前，ArcGIS平台软件已成为中国用户群体***，应用领域***的GIS平台。今后，Esri中国将继续为用户的数字化转型和创新发展提供最先进的解决方案，帮助用户用地图更好地管理业务、辅助决策、创造更美好的未来。 同时，公司还为中国大陆地区用户提供Exelis公司的 ENVI/IDL遥感图像处理系统和SARscape高级雷达图像处理软件的销售和技术支持服务，传播和推广遥感技术和应用。'],
        '112008229': ['1-2万/月', '周末双休|带薪年假|五险一金|全勤奖|节日福利|交通补贴|餐饮补贴|通讯补贴|', '武汉-东湖新技术产业开发区', '2年经验', '本科', '招3人',
                      '11-20发布', '开发测试工程师', '武汉睿智视讯科技有限公司',
                      '岗位职责：\n1、负责视频/图片识别的相关应用平台的测试；\n2、编写自动化测试用例或自动化测试脚本。\n\n任职要求：\n1、熟悉linux系统2、至少熟练使用shell\\python\\java等其中一种编程语言3、具备定位bug的能力4、有压力测试经验者5、有自动化测试经验2年及以上者\n加分项：1、能熟练使用postman2、能熟练使用抓包工具3、熟悉Elasticsearch、kafka、redis、hadoop、mysql等\n\n【工作时间】\n9：00---18：00午休时间：12：00--13：30\n周六日双休、国家法定节假日休息\n\n\n福利待遇：五险一金、午餐补助、通讯补助、节假日福利、旅游拓展、部门不定期聚餐、团建、结婚礼金、年终奖金、年度体检、茶话会等\n\n\n联系方式：027-59320695\n工作地点：武汉市江夏区光谷大道当代光谷梦工厂5号楼8-9楼\n招聘流程：投递简历→简历筛选→专业面试→综合面试→发放录取通知书→入职\n职能类别：软件测试脚本开发工程师\n',
                      '上班地址：当代光谷梦工厂5号楼8-9楼',
                      '武汉睿智视讯科技有限公司隶属北京深瞐科技有限公司（原北京华富睿智科技有限公司）旗下全资子公司及武汉研发中心。北京深瞐科技有限公司成立于2012年，研发中心武汉睿智视讯科技有限公司成立于2013年，是由企业家、投资人、海外留学归国技术专家共同创立的高新技术企业，专注于人工智能、机器视觉等领域，拥有多项国际领先的自主核心算法和发明专利。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0深瞐科技面向安防与智能交通领域推出车辆特征识别系统、车辆标志物识别系统、驾驶员行为分析系统、动态人脸识别系统、视频质量诊断系统灯多套视频图像分析技术与产品，广泛推广应用于公安、交通、国安、环保、停车场管理、小区车辆管理等多个行业领域。公司始终坚持自主研发和技术创新，在全球首家提出“车脸”识别概念，利用深度学习技术推出业界领先的“车脸”识别、视频结构化等系列产品，已广泛应用于公共安防、海关、边检、高速等领域，取得了良好的经济效益和社会效益。深瞐科技立足安防，积极拓展海关、边检、金融、交通等应用领域，同时积极布局海外业务，实现中国技术服务全球。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0深瞐科技秉承"聚集人才、积累技术、面向应用、实现价值"的价值理念，力争成为全球领先的视频图像分析技术、产品与服务提供商。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0核心团队\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0深瞐科技坚持以人为本，自始至终以技术研究和创新为导向，聚集了国内外在机器视觉领域深耕的多位专家学者。公司在北京和武汉分设两个研发中心，研发团队超过100人，其中硕士占比30%，博士占比20%，及2位微软亚洲学者。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0企业文化\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0理念：让机器理解我们所见\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0使命：成为全球机器视觉行业领先的智能图像信息化解决方案供应商\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0文化：诚信、创新、共赢'],
        '117426579': ['1-1.5万/月', '五险一金|员工旅游|专业培训|绩效奖金|年终奖金|定期体检|', '武汉-东湖新技术产业开发区', '无工作经验', '本科', '招若干人', '11-20发布',
                      'Java开发工程师', '湖北国铁轨道交通研究院有限公司',
                      '1.负责用户需求调研；实施软件项目的开发，完成系统/模块的代码编写，填写开发日志，包括数据库、主要算法。2.根据方案书制定测试计划，实施软件测试，编写测试文档及报告；根据方案书及实际开发，编写技术文档及使用手册；项目交予客户进行验收，并提供技术指导。3.参与企业项目或者相关技术的交流讨论；完成领导交给的其他任务。\n职能类别：高级软件工程师\n关键字：java\n',
                      '上班地址：武汉市洪山区花城大道9号',
                      '湖北国铁轨道交通研究院有限公司于2017年成立，坐落于武汉软件新城，注册资金2300万元，实缴资金为2300万元。主营业务为铁路和轨道交通定向研发、检测及服务；软件开发及运用；铁路和轨道交通专业维保；航空、航天非标试验装备定向研发制造及服务，为襄阳国铁全资子公司。公司具备原创性自主研发的能力，先后开发了有轨电车清扫车、智能健康管理系统、安全联锁装置、基于北斗导航的轨道交通智能运维装备、超声波驱鸟器等。拥有专利13个，其中实用新型8个，软著5个，1个发明专利正在受理过程中。公司具备研发需要的各项基础设施与实验条件，现有技术研发场地面积5300㎡。研发设备主要包括路轨及电子化系统、L型公铁车及电气系统、轨道健康管理系统、北斗RTK差分定位系统等，均为国内或世界先进水平的配置。公司与武汉大学成立合作公司，就北斗定位系统展开全方位更紧密更深层次的产学研合作，形成较为完备的产学研合作体系和企业技术创新体系。'],
        '116159883': ['1-1.5万/月', '五险一金|补充医疗保险|年终奖金|', '武汉-洪山区', '8-9年经验', '本科', '招1人', '11-18发布', '高级测试工程师',
                      '武汉锦益慧通网络科技有限公司',
                      '\n\n岗位职责：\n\n1、参与产品需求评审、制定测试计划、测试方案、设计测试用例及测试实施，跟进问题并输出报告。\n\n2、负责构建测试体系，管理测试人员，优化测试流程。\n\n3、对项目生命周期内的质量问题进行全面跟踪。\n\n任职资格：\n\n1、计算机相关专业，5年以上测试工作经验。\n\n2、能独立搭建测试环境。\n\n3、精通web和小程序测试。\n\n4、熟悉性能测试工具jmeter，能搭建自动化测试平台，熟悉一门编程语言。\n\n5、有团队管理经验，能负责资源的协调和解决测试过程中的问题。\n\n6、控制项目进度、控制和解决产品和技术的风险。\n\n7、具备良好的自我驱动能力，强大的推动和沟通协同能力能，通过协同达到团队和个人目标。\n\n\n职能类别：软件测试系统测试\n关键字：性能测试\n',
                      '上班地址：光谷app广场3栋702室',
                      '北京锦益网络科技有限公司是一家致力于用零售重新定义美好生活的公司。武汉锦益慧通为其全资控股子公司，公司目前的主要业务集中在生鲜和一般食品的运营、销售。公司核心团队操盘过某一线知名零售新业态，受到业内同行和消费者的广泛认同。基于推动零售领域深入变革的强大使命，我们选择重新出发，现需要优秀的新鲜血液加入。核心团队诸多成员有世界500强公司丰富的工作、管理经验，团队尤其注重快速学习和整体进步，我们相信员工的进步是企业发展的重要动力。公司非常注重对员工贡献的及时肯定，在奖金分配上，透明公正，不让老实人吃亏。我们提倡团队胜则举杯相庆，败则拼死相救的精神。公司在起步阶段就受到国内、国际一线资本的追逐，未来行业、市场发展空间巨大。投身于新零售行业，让人们的生活变得更加愉悦美好。'],
        '110663775': ['1-1.3万/月', '五险一金|交通补贴|通讯补贴|年终奖金|定期体检|营养午餐|别墅轰趴|婚/育红包|逢节必过|', '武汉-洪山区', '3-4年经验', '大专', '招1人',
                      '11-13发布', '测试主管', '武汉垂定网络科技有限公司',
                      '1、参与项目或产品需求分析和评审，提出有价值的建议\n2、进行测试工具选型，负责公司研发产品的各项测试，并对结果负责\n3、编写测试方案、测试用例和测试数据\n4、搭建测试环境，执行测试之后输出测试报告\n5、测试领城新技术、方法的研究、应用与推广提升测试团队技术影响力\n6、积极总结测试经验，并在内部进行分享\n\n岗位要求：\n1、计算机相关专业本科及以上学历\n2、三年及以上测试工作经验，深刻了解软件测试知识体系，有编写测试方案的能力\n3、新悉常用中间件、数据库和Linux操作系统，能独立在Linux环境下搭建测试环境\n4、学习能力强，有较强的分析和定位问题能力，沟通协调能力强\n5、有大型项目的测试经验者优先\n6、会使用自动化测试工具selenium、Loadrunner的使用经验优先\n职能类别：软件测试\n',
                      '上班地址：武汉市江岸区永清小路20号永青汇6楼',
                      '武汉垂定网络科技有限公司（Tradedge），成立于2017年，是国内领先的新零售系统技术服务平台，目前产品已覆盖全国30多个省份及自治区，为超过1000个城市提供服务。通过对技术的不断革新、新零售模式的深入了解实现了社群商家从后端供应链，到直营、代理的社群运营，再到终端消费者之间的全流程管控。持续为用户创造价值，释放运营时间，提升商家销量。\xa0\xa0\xa0\xa0\xa0每一个垂定人都喜欢创新、高速的互联网文化“垂直交易，定义未来”在垂定团队中，你能感受到思维的碰撞、创意的激发，在平等、轻松的工作氛围中尽情释放自己的才能，与各领域人才共同定义发展，领跑未来。'],
        '82424003': ['1-1.5万/月', '五险一金|员工旅游|餐饮补贴|专业培训|绩效奖金|年终奖金|弹性工作|', '武汉-江夏区', '无工作经验', '本科', '招1人', '11-08发布',
                     '嵌入式软件开发', '武汉高思光电科技有限公司',
                     '工作职责:\n1．负责嵌入式产品软件的需求分析、整体方案设计；\n2．负责嵌入式产品程序的代码设计和开发；\n3．根据公司技术文档规范编写相应的技术文档；\n4．制定软件测试方案，完成软件基本测试，配合项目组完成最终测试；\n5．参与硬件和软件的联合调试。\n\n\n任职资格:\n1．本科及以上学历，计算机、电子或相关理工科专业，嵌入式软件1年以上工作经验；\n2．具有扎实的C语言功底，有过C语言编写经验，熟悉嵌入式开发，能够完成嵌入式软件开发、调试等任务；能独立完成产品软件设计，能熟练阅读各种英文芯片资料；\n3．熟悉STM32、FPGA及其开发环境，熟悉常用外部设备接口，如CAN、USB、I2C、UARI、SPI、EEPROM、UART等，并有相关项目开发经验；\n4．熟悉基本硬件调试工具，如Jlink、示波器、信号源等，能理解电路原理图；\n5．有强烈的责任心、较强的上进心和敬业精神，有良好的沟通能力、拼搏奋斗精神和团队合作意识。\n职能类别：电子软件开发(ARM/MCU...)\n',
                     '上班地址：流芳园横路三号凌云光电产业园L5号楼2楼',
                     '高思光电成立于2008年，目前是光纤传感行业的主要光电模块供应商，客户包括多家上市公司，员工人数过百人，主要业务包括三大模块：光电器件的生产，光测试仪表开发，生产和销售，光传感器的开发，生产和销售。\xa0\xa0\xa0\xa0主要产品包括：激光雷达相关器件，模块，光接近传感器，光源，光功率计，误码仪，可调谐光源，光传感解调模块等。\xa0\xa0\xa0\xa0为加快公司的发展速度，提升公司的市场占有率，现招聘销售经理，高级硬件工程师，嵌入式软件工程师，光学工程师，自动化工程师，生产主管，生产技工等，期待各类人才加盟，共创美好明天！'],
        '118367289': ['1-1.5万/月', '五险一金|交通补贴|餐饮补贴|通讯补贴|专业培训|绩效奖金|股票期权|弹性工作|节日福利|体检|', '武汉-东湖新技术产业开发区', '无工作经验', '本科',
                      '招若干人', '11-07发布', '测试工程师（WAF）(J10871)', '绿盟科技',
                      '工作职责:\n负责网络安全产品的测试工作，包括：\n1.测试环境搭建；\n2.独立编写测试用例，独立执行测试，定位缺陷；\n3.独立制定测试计划和测试方案。\n任职资格:\n1.计算机相关专业。2年以上测试经验。有安全产品、网络设备测试经验者优先。\n2.熟悉项目开发过程、熟悉软件测试方法、熟悉用例设计方法。\n3.熟悉Linux操作系统，熟悉网络协议、网络设备应用。熟悉python，shell脚本语言优先。\n4.熟练使用avalanche、bps等测试仪表，熟悉安全测试工具优先。\n\n职能类别：其他\n',
                      '上班地址：光谷软件园A9座',
                      '一、公司介绍绿盟科技（nsfocus），成立于2000年4月，公司专注于网络安全的行业，面向全球提供基于自身核心竞争力的企业级网络安全解决方案。\xa0\xa0现有员工1600多人，在全国主要省会城市设有7个分公司、31个办事处和联络处，另在日本和美国建有子公司。自2000年成立，基于我们领先的安全漏洞研究实力、强大的产品研发和创新能力，我们始终保持高速稳健的发展，我们期待更多精英的加入！二、我们的优势1、卓越雇主品牌： 财富fortune 和华信惠悦watsonwyatt授予“卓越雇主：中国最适宜工作的公司”。2、持续快速的增长：成立10年来，公司业务规模保持持续快速的增长，年平均人员增长率为45%。3、一流的基础研究实力，保证在行业始终保持竞争优势：我们是中国网络安全行业的技术领导者，10年来我们协助microsoft、sun、cisco 等公司解决了大量系统安全漏洞问题 。4、强大的研发能力及成功的市场拓展战略。5、具有国际竞争力的安全产品、解决方案： 绿盟科技的安全产品与解决方案覆盖全面，其中的绿盟远程安全评估系统是英国西海岸实验室认证的“全球第六、亚太***”的漏洞扫描产品。6、完善的专业安全服务体系和专业安全服务方法论：绿盟科技在国内率先开展专业安全服务业务，具备国内***安全服务资质。7、国际化发展：基于自身的技术优势，从2008年开始启动国际化发展步伐，我们正稳步前进。三、加入绿盟科技您可以获得什么1、行业领先的薪酬福利水平：绿盟科技尊重并承认每个员工的价值所在，一直致力于提供具有行业竞争力的薪酬福利。\xa0\xa0\xa0加入绿盟，您将获得有竞争力的薪资、全面的法定保障“五险一金”、60万元高额商业保险、以及带薪年假、年度体检等13项周到细致的员工关怀计划。2、专业化的培养体系和方案：绿盟独有的技术氛围，不断健全的内部培训体系，多元化的交流平台让每个员工都有展示才能、分享知识、全面锻炼和提高的机会。3、令人向往的工作环境和团队氛围：“融洽的气氛、良好的团队协作精神和凝聚力、浓厚的学习氛围、乐于分享、充满活力”，在每年的员工满意度调查中，这是绿盟员工经常提到的词语。'],
        '118140323': ['1-1.5万/月', '五险一金|餐饮补贴|弹性工作|定期体检|交通补贴|年终奖金|补充医疗保险|', '武汉-东西湖区', '3-4年经验', '本科', '招2人', '11-02发布',
                      '高级测试工程师（武汉）(J11046)', '北京天融信科技有限公司',
                      '工作职责:\n1.参与软件产品的需求分析和设计评审负责测试计划制定；\n2.负责软件产品的测试方案和用例设计；\n3.根据测试计划搭建和维护测试环境；\n4.执行具体测试任务并确认测试结果，完成测试报告以及测试结果分析；\n5.进行项目测试报告的编写及审核。\n6.负责内部项目使用培训文档的编写\n7.独立完成产品的各类型测试，保证产品满足质量标准；\n任职资格:\n1.计算机相关专业毕业，3年以上测试工作经验，有安全行业相关经验优先；\n2.网络技术，知晓二三层交换路由原理，熟悉交换机配置（思科/华为等），了解TCP/IP各协议和应用层协议，能定位排查网络故障；\n3.熟悉常用网络协议ftp、http、https、TCP/IP等协议\n4.熟悉linux系统，可熟练应用Linux系统常用命名，熟悉系统基本配置，可在Linux系统下独立搭建应用环境。\n5.熟悉vpn相关技术、认证知识以及密码学知识的优先考虑；\n6.性能测试技术，接触过一种以上硬件性能测试工具（BPS/IXIA/avalanche等），了解基本配置以及使用方法。\n7.熟练掌握常用测试框架和测试工具;\n8.热爱软件测试工作，具有良好的沟通与表达能力，踏实敬业，责任心强，在快速迭代环境中工作与项目成员进行快速有效的沟通\n\n职能类别：其他\n',
                      '上班地址：五环大道416号网安大厦B座25层',
                      '一、\xa0\xa0\xa0\xa0公司简介天融信科技集团创始于1995年，是中国领先的网络安全、大数据与安全云服务提供商。于2017年在A股上市（股票代码：002212）。天融信坚持自主创新，连续19年位居中国网络安全防火墙市场***，并在安全硬件、整体网络安全市场处于领导地位。面对大、智、移、云、物时代的安全挑战，天融信构建了整体的可信网络安全架构，并在人工智能、物联网安全、工业互联网安全、下一代互联网安全等新技术领域进行了前瞻布局并保持高强度研发投入，不断推出创新产品与服务，在多个行业得到应用与落地。二、加入我们的理由1.选择一个极具吸引力和发展前景的行业数字经济时代，网络安全关系国家安全、企业安全和个人安全！顺势而为，来和我们一起站在风口！2.公司行业领先、实力不凡（1）专注网络安全行业24年，是中国领先的网络安全、大数据与安全云服务提供商；（2）技术为本，员工4000+名，技术研发人员占比超过80%；（3）获得国家科技进步二等奖（连续两年）等多项荣誉，连续19年位居中国网络安全防火墙市场***。3.关注员工发展和成长我们致力于建设更好的学习发展环境，通过天融信大学、一对一导师制等助力员工成长，并鼓励员工通过学习获得行业技术及职业认证（CISP、CISSP、PMP），保持公司持续创新的DNA。三、学习发展1.天融信大学我们拥有知识体系完善的知识共享平台——天融信大学，涵盖丰富的产品知识、行业知识、业务技能知识，针对各个岗位的不同特点设置针对性的学习内容，帮助员工实现职业生涯的华丽变身。培训内容涵盖新员工培训（校招岗前培训/社招入职培训），专业能力培训（营销体系培训/产品技术培训/运营体系培训/岗位资质与职称认证培训/项目管理培训）、通用素质能力培训、管理与领导力发展等项目，赋能员工成长，支持业务发展，推动战略落地。2.1V1导师制新员工入职后，业务部门会给新员工安排一对一导师，导师由绩优骨干员工担任，以帮助新员工了解公司文化，学习掌握内部工作交流平台和公司各种管理制度，使新员工具备相应岗位任职资格及岗位技能，顺利通过试用期考核转正。3.多元内部学习活动公司以员工发展为中心，各业务体系都设有专人负责体系内的业务技能培训工作，培训活动内容丰富、形式多样，给员工带来有价值的行业信息及技术干货；另外，内部学习和竞赛、读书会等多种学习形式丰富员工业余生活。4.持续学习公司鼓励和支持员工不断学习，为员工提供免费的外部学习机会，通过学习获得行业技术及职业认证（如CISP、CISSP、PMP等），提升自身技术能力、职业素养，提高企业与员工的综合竞争力。四、薪酬福利1.薪资体系：基本薪资（12个月）、绩效奖金（0-12个月）、股权激励；2.福利体系：七险一金（含重疾险、意外险）、补充医疗险、饭补/话补/交补；3.员工关怀：春节假期11天、带薪年假、年度体检、节日礼物、团建活动、员工旅游；4.奖励机制：年度个人/团体评优、员工持续服务奖励、即时激励和内部表彰。五、联系我们天融信以国际化的视野招贤纳士，真诚期待您的加盟。欢迎登陆我们的网站http://www.topsec.com.cn或关注天融信招聘公众号了解更多的信息。'],
        '111084404': ['1-1.5万/月', '五险一金|补充医疗保险|交通补贴|餐饮补贴|通讯补贴|弹性工作|定期体检|节日福利|生日party|', '武汉-东西湖区', '3-4年经验', '本科',
                      '招1人', '10-31发布', '测试工程师', '恒宝股份有限公司',
                      '1、完成软件系统的整体测试，功能测试；\n2、根据需求说明完成相关测试工作，以及生成相应测试报告；\n3、能独立完成系统性能测试，并提供相关性能测试报告\n4、分析并协助开发人员解决测试中发现的bug；\n1、最少3年以上测试相关经验。\n2、搭建测试框架，并具备基本的JAVA语言基础，能用java编写测试用例；\n3、熟悉常用性能测试工具，以及分析工具；\n4、熟悉使用Oracle、Mysql等数据库；\n5、熟悉使用Tomcat等应用服务器；\n6、工作踏实、责任心强，敢于独立分析和解决问题。\n7、有良好的团队协作精神，乐于分享，共同进步。\n\n职能类别：软件测试\n',
                      '上班地址：武汉',
                      '恒宝股份公司成立于1996年， 2007年在深交所成功上市（股票代码：002104），目前注册资本71350.4万元。\xa0\xa0\xa0\xa0公司面向金融、通信、税务、交通、保险、安全、市政建设等多个行业致力于提供高端智能产品及解决方案，主导产品和业务包括金融IC卡、通信IC卡、移动支付产品、互联网支付终端、磁条卡、密码卡、票证、物联网、平台系统及信息安全服务业务和解决方案等。历经十余年的发展，已成为集服务、研发、生产和销售为一体，业内领先的国家重点高新技术企业。\xa0\xa0\xa0\xa0\xa0公司构建了以北京作为管理、研发、营销中心，以江苏丹阳作为生产基地的两大运营体系。公司实行"股东大会、董事会、监事会"三位一体的现代企业治理结构，设有研发、生产及营销三大业务中心，围绕客户需求和核心竞争力，不断延展公司的价值链，提升产品的技术含量和附加值。\xa0\xa0\xa0\xa0公司现有员工1500余人，不同专业背景，不同地域文化的交流融合塑造了公司多元、开放、充满活力的企业文化，塑造了作为一家行业领先的高新技术企业独特的前瞻性与注重实际应用相结合的技术风格。\xa0\xa0\xa0\xa0公司在"珍惜奋斗后的成功，致力成功后的奋斗"理念指导下，坚持不懈地把"诚信为本，用户至上"的经营方针化为现实，坚持以优质的产品、优良的技术和优秀的服务回报社会，把"追求卓越"的恒宝价值观回馈给***大的用户、合作伙伴和公司员工。 "一流的服务、一流的技术、一流的管理"将推动着我们的事业不断前进。'],
        '83106848': ['1.2-1.5万/月', '五险一金|绩效奖金|定期体检|', '武汉-洪山区', '3-4年经验', '本科', '招若干人', '10-31发布', '嵌入式软件工程师-便携式仪器',
                     '武汉市农业科学技术研究院农业环境安全检测研究所',
                     '1.基于ARM的Linux环境下嵌入式软件开发；\n2.分为两个方面：一、负责Linux底层驱动开发和网络应用开发，熟悉JAVA语言；\n二、负责GUI交互界面的开发及嵌入式Android产品软件开发；\n两个方面熟悉其中一块即可。\n3.负责相关开发文档的编写工作；\n4.负责软件测试、发布和维护\n任职要求：\n1.本科以上学历，电子、计算机、控制、自动化等相关专业；\n2.两年以上Android产品应用开发经验，有良好的代码风格；\n或精通JAVA语言，Linux系统开发、能进行高性能的应用程序开发；\n或Linux内核移植、驱动开发，有单片机或ARM基础，熟悉常用UART,SPI,IIC,IIS,USB等，\n3.具备良好的工作态度、沟通能力及团队协作精神，能吃苦耐劳；\n4.具有食品安全仪器或医疗仪器软件开发经验者优先。\n职能类别：嵌入式软件开发(Linux/单片机/PLC/DSP…)\n',
                     '上班地址：白沙洲大道（青菱乡）张家湾特1号（凌吴墩车站附近）',
                     '武汉市农业科学技术研究院农业环境安全检测研究所简介\xa0\xa0\xa0\xa0\xa0\xa0\xa0武汉市农业科学技术研究院农业环境安全检测研究所（简称武汉市农科院农环检测所）成立于2015年6月，是一所从事农业环境、农产品和食品安全检测技术研究、成果转化和三农服务的武汉市公益一类事业单位。\xa0\xa0\xa0\xa0\xa0\xa0\xa0武汉市农科院农环检测所发展目标是：针对日益严峻的农业环境污染和食品安全现状，建立系列污染物（食源性致病微生物、农药和兽药残留、生物毒素、环境激素、重金属等）快速检测新技术，研制污染物检测试剂盒和仪器，构建污染物溯源物联网信息化平台，建设第三方检测中心。研究所设有六个实验室，包括质谱色谱检测实验室、侧向层流检测实验室、酶联免疫检测实验室、生物传感器实验室、仪器研发实验室和物联网信息化实验室。打造由多名教授和博士组成的具有持续创新能力的高水平研发队伍，逐步建成省级、***科研平台，面向环境和食品污染物快速检测重大国家需求和市场需求，形成一个完整的技术开发-应用研究-成果转化-行业服务创新发展模式，推进农业环境、农产品和食品安全检测产业的发展，服务三农，保障食品安全和生命健康。'],
        '95924091': ['1-2万/月', '五险一金|餐饮补贴|通讯补贴|年终奖金|弹性工作|定期体检|节日福利|', '武汉-洪山区', '3-4年经验', '本科', '招1人', '10-24发布',
                     '视频测试工程师-武汉', '北京小鱼易连科技有限公司',
                     '工作职责：\n1、整理并快速跟进产品需求，意见反馈，客户问题。\n2、协同研发和产品团队定义功能，实现，前期评估和对比测试，日常产品/测试问题整理和跟进。\n3、制定并执行测试计划，测试用例；管理问题报告和问题追踪。\n4、基于客户问题和新特性，不断改进测试用例，优化测试流程，组织高效有针对性的测试。\n5、客户技术服务支持和前期产品技术咨询。\n\n职位要求：\n1、计算机或通信相关背景；\n2、三年以上软件/系统测试经验；\n3、一年以上音视频产品或iOS/安卓App或网络相关测试经验；\n4、具备计算机，网络，通信，软件，系统相关的知识和工作技能；\n5、具备丰富的测试计划，测试用例，问题报告，问题追踪，与开发和产品高效协作的经验；\n6、具备强烈的责任心，耐心，细心，求知欲，复现问题和定位追踪的能力；\n7、较强的理解力，沟通力和快速学习的能力，具有良好的团队合作意识；\n8、深刻理解产品质量和用户体验；\n9、有一定的抗压能力，在日常的快速迭代中，和团队一起高效地加班奋战，严格保控产品质量；\n10、热爱测试工作！\n\n优先条件：\n1、丰富的音视频产品测试经验；\n2、丰富的虚拟化部署测试经验；\n职能类别：软件测试\n',
                     '上班地址：洪山区光谷APP广场3号楼1207',
                     '小鱼易连隶属北京小鱼易连科技有限公司，起步于2014年3月，通过构建全球互联的云视频通讯平台，致力打造“云端+终端+服务+业务”的生态体系。公司利用全球首创的智能硬件产品终端、 世界领先的音视频算法、运营商级的SaaS服务三大核心优势，提供云视频会议、远程教育、远程医疗、远程政务等服务，实现人务互联，让世界零距离。\xa0\xa0\xa0\xa0\xa0\xa0公司投资者包括创新工场、光速中国、成为资本、富士康、真格基金、真成基金，已经完成Pre-A、A、B轮超过3亿元人民币的融资。核心团队均为来自音视频行业从业多年的业内精英，掌握并创新互联网音视频核心技术。 截至目前，每一天在全球近百个国家、近千座城市，有数十万个企业/个人用户使用小鱼易连视频会议。'],
        '115633857': ['1-1.5万/月', '弹性工作|五险一金|员工旅游|专业培训|定期体检|', '武汉-洪山区', '无工作经验', '本科', '招1人', '10-24发布', '测试开发工程师',
                      '北京风行在线技术有限公司',
                      '工作职责：\n\n1.负责系统的手工测试和自动化测试，保证发布产品的质量\n\n2.为智能电视系统设计测试用例并执行测试，实现测试用例的自动化\n\n3.开发基于Java平台的自动化测试框架和自动化测试工具，包括功能、压力、稳定性测试等\n\n4.不断对项目开发流程优化，提高测试和整个项目的交付效率\n\n5.学习和研究新技术以提高测试的效率和质量，满足质量保证的需求\n\n任职要求：\n\n1.具有1年以上的测试经验，熟悉Linux和Android，熟练使用相关测试工具\n\n2.具有后台系统测试经验者或智能电视测试经验者优先\n\n3.具备良好的团队沟通能力，较强的学习能力\n\n4.能熟练应用以下一门或几门技术：\n\nJava/Linuxshell编程\n\nPython/Perl/Lua/PHP\n\nJavaScript/Ajax/MySql及相关数据库技术\n职能类别：软件测试\n关键字：SQL、postman\n',
                      '上班地址：武汉市东湖新技术开发区光谷智慧园17栋',
                      '北京风行在线技术有限公司，2005年9月成立，是国内领先的全渠道内容运营服务商。风行秉承“让内容流动更简单”的使命，依托个人与家庭、大屏与小屏等内容消费场景，专注于为产业链上下游、广告主及用户提供横跨PC、移动及电视等多渠道的内容运营服务，并让客户、用户、供应商、合作伙伴、员工、股东等各类参与者都能享受到因内容充分流动而增加的商业价值、成长价值及体验价值，最终成为面向全球的专业的全渠道内容运营服务商。如果想更多的了解风行的情况，请访问我们的网站http://www.fun.tv纯正的互联网精神——梦想与激情，工作的乐趣和成果的共享，是所有互联网传奇的必备，风行不是传奇的旁观者，而是新机遇下的缔造者。如果你有一颗激情澎湃的创新之心；如果你不安于为稻粱谋的平淡工作；如果你乐于享受高手间脑力激荡的乐趣；如果你渴望享受成功后的从容归隐；那么，加入我们风行的大家庭吧！我们不把风行的经历当成一份工作，更视之为自我实现的舞台，和我们一起成长，一起分享梦想和成功，一起风行天下，在生命中留下绚烂的一笔！我们真诚的期待你的加入！公司地址：北京海淀区知春路6号锦秋国际大厦B座12层，邮编：100088'],
        '116271296': ['', '', '武汉-洪山区', '无工作经验', '本科', '招1人', '10-15发布', '测试开发管培生', '武汉今天梦想商贸有限公司',
                      '岗位职责：\n1、负责所属产品线的功能测试必要时要进行性能测试；2、根据需求编写测试用例并且执行测试用例；3、准确、详细的描述bug产生过程、bug的现象，准确地定位并跟踪问题，协助开发人员解决问题。\n\n任职资格：\n1、2020届985、211院校本科及以上学历，计算机软件相关专业；2、熟练掌握软件工程基础知识，熟悉软件测试理论及方法；3、有良好的计算机理论基础知识，熟悉操作系统及网络的基本原理，至少掌握一门编程语言；4、具备扎实的代码走读能力，熟悉各类常用debug工具；5、逻辑思维能力强，工作认真细致，具备良好的学习能力和适应能力。\n\n工作时间：\n早上9:00-12:00，下午13:00-18:00，周末双休\n福利待遇：\n五险一金、带薪休假、免费体检、团建基金\n\n\n职能类别：培训生\n',
                      '职能类别：培训生',
                      'Today便利店于2008 年在南宁创立。2014 年，总部迁至武汉。经过十一年的发展，企业规模不断壮大，并以创新的模式与赋能形态，不断刷新中国便利店的历史。截至2019 年9月，Today 在武汉、南宁、长沙共设有400 家门店，其中武汉门店突破300 家。从2017年底开始，Today组建超过100人的技术中心，重构了一套基于云的“前台——中台——后台”新技术架构，实现互联网技术的全面支撑。2018年9月，Today自主研发的新零售云平台正式上线，逐步实现了由传统便利店向科技新零售公司的转型。2014年至2018年，Today先后获得红杉资本、信中利资本、泛大西洋资本的投资，估值超过30亿。公司官网：http://www.today36524.com/'],
        '109556147': ['1.3-1.8万/月', '', '武汉-硚口区', '5-7年经验', '本科', '招1人', '10-14发布', '测试经理', '北京爱康云医疗科技有限公司',
                      '\n1、负责测试小组质量管理体系的建设、团队管理、绩效考核、年度计划制定；负责自动化测试技术规划、创新和应用，提高整体测试技术水平及工作效能；\n2、负责具体项目质量保障工作，解决测试工作中出现的问题，保证测试工作顺利开展；\n3、引导开发部门进行系统优化，提供高效合理的解决方案，主导测试需求实现，配合项目顺利完成，并进行跨部门协调等工作；\n4、根据公司产品发展方向，及时追踪、收集软件测试和硬件测试新技术、新动态的资料，通过技术培训、交流等方式，建立测试团队，提高测试团队的技术和业务能力；\n5、负责测试部门和其他部门的协调工作，监控分析达成本部门质量目标的达成、提升本部门工作效率；\n6、评估测试方案、测试策略和相关测试报告，完成测试小组成员的项目绩效考核；\n7、培养指导软件测试工程师，并组织相关培训工作，保证测试团队能力的持续提高。\n\n任职要求：\n1五年以上测试经验，两年以上团队管理经验，统招本科以上学历，有APP测试管理经验\n2.熟练掌握主流测试工具和故障定位工具的使用方法；扎实的软件开发和测试技术，精通及具备自动化测试（重点）、性能测试、容量测试、兼容性测试、稳定性测试、安全测试等专业知识和经验，熟练掌握主流测试工具。\n3.至少熟悉shell、Python、JavaScript等其中一种脚本语言；\n4.至少熟悉Mysql、SQLServer、Oracle其中一种数据库，熟练使用SQL语句。\n5.熟悉大型软件架构，熟悉操作系统和数据库理论和应用，具备丰富的大型复杂系统的测试经验；\n6.熟悉流行的开源测试工具和框架，具备二次开发能力，能够做代码走查和一般问题定位；\n7.出色的团队领导能力和管理能力，有丰富的团队建设经验，有能力吸引和发展杰出人才。\n职能类别：软件测试\n关键字：自动化测试\n',
                      '上班地址：解放大道航空路新世界中心写字楼B座',
                      '北京爱康云医疗科技有限公司隶属于母公司北京爱康医疗集团，秉承“用我们的爱创造一个生命平等的医疗环境”的服务理念，于2017年正式成立。北京爱康医疗投资控股集团始创于1993年，系一家致力于医疗投资、医院管理、证券基金、房地产等多元化经营的大型集团公司，已在北京、武汉、黄石及北美地区成立了四大总部。经过10多年的运营，旗下拥有20多家全资控股的各级医院，并跟武汉华中科技大学附属同济医院联合成立了同济爱康医院管理有限公司，专注从事医院的运营管理事业；随着爱康医疗集团的业务升级和服务延伸，北京爱康云医疗科技有限公司应运而生。北京爱康云医疗科技公司的主营业务是帮助医院构建院后管理部、互联网诊疗中心和患者管理中心（Patient Care Center），借助先进的互联网工具，开发一系列患者管理相关的软件、硬件设备和权威患教内容（管理处方）于一体的患者管理终端产品；借助分级诊疗模式构建医患朋友圈，形成患者诊前、诊中、诊后于一体的患者全病程随访与康复管理的创新模式。现今随着“健康中国”国家战略的实施和中国医改逐步走入深水区，实体医院的经营也面临着从传统的“被动地等着患者来就医、出院就放羊”的运营模式向“实体+互联网”的主动管理患者的服务模式转型。北京爱康云医疗科技公司在爱康集团强大的医院运营平台上孕育而生，旨在应用先进的互联网工具和医疗智能可穿戴设备，在医院院内建设患者管理中心，构建起患者院外的长期随访管理的创新模式，并逐步在全国其他医院复制。这不仅符合国家的分级诊疗政策和医改大方针，而且也造福广大患者，是一项利国利民的医疗创新工程。北京爱康云医疗科技公司在北京中关村科技园区注册成立，享受国家高新技术企业的优惠政策，并在爱康集团控股的湖北、湖南、安徽的各级医院里孵化。公司总部设在湖北武汉，现面向武汉招聘一批有志向从事医疗科技和患者康复管理事业的医疗和技术人才，诚邀各位精英的加盟，共创伟业。'],
        '116884763': ['1-1.5万/月', '做五休二|五险一金|带薪年假|节日福利|餐饮补贴|交通补贴|', '武汉-硚口区', '3-4年经验', '本科', '招3人', '10-11发布', '测试工程师',
                      '上海顺益信息科技有限公司',
                      '工作职责\n1.负责需求分析、测试计划制定、测试用例设计、测试执行，协助项目经理保证项目质量与进度；\n2.负责公司各产品线的质量保证工作；\n3.负责测试相关平台、工具的设计与开发，提升工作效率与效果；\n4.跟踪定位产品中的缺陷或问题，与项目相关人员就项目进度和问题进行沟通。\n5.参与项目的需求和迭代开发计划的讨论和评审；\n6.制定项目的测试计划并设计测试用例；\n7.搭建测试环境、测试设计、执行及bug的定位、跟踪和管理；\n8.设计UI、接口自动化脚本或性能测试脚本，并执行自动化脚本；\n9.项目上线后，对产生线上Incident事件或技术缺陷进行case_study分析；\n10.通过总结、对外交流、技术钻研和培训，进行测试过程和测试方法的持续改进。\n职位要求\n1、本科及以上学历，计算机相关专业；\n2、具有4年以上测试或开发经验（测试经验不低于2年）；\n3、熟悉测试理论、流程与方法，熟练使用主流的功能或性能测试工具；\n4、具备一定的业务分析，沟通表达能力和综合协调能力，工作积极主动；\n5、良好的沟通能力和团队协作能力，具备高度责任感；\n6、具备强大的逻辑思辨能力，谈判能力和冲突管理能力者优先。\n7、能够基本掌握一门开发语言，java/php/.net；\n8、熟悉Oracle/SqlServer/Mysql/MongoDB等至少一种数据库管理系统，能够熟练编写SQL语句；\n职能类别：软件工程师软件测试\n关键字：测试\n',
                      '上班地址：武汉市江汉区泛海国际soho城 6栋',
                      '上海顺益信息科技有限公司是完全市场化运作的软件开发和运营管理的高科技企业，是中国报关协会副会长单位。顺益公司运营管理的——“通关网”（www.hscode.net）是海关总署和中国报关协会指定的全国预归类服务平台。所有进出口商品报关前可通过平台完成商品预归类，以便利通关。该网在海关总署和中国报关协会的领导下，积极参与海关重大业务改革，充分利用信息化的手段,创新管理模式，力求打造服务社会、服务海关、服务企业的智慧型物流生态链。通过全国预归类服务平台，遵照海关总署在预归类服务基础上推进“三预”，即“预归类、预审价、原产地预确认”的要求，以预归类商品数据库为核心，运营全国预归类平台的基础上，整合仓储、运输等关联物流行业的服务需求,最终形成以物流为核心的电子商务网站平台。2014年公司借助通关网平台致力于跨境电子商务通关服务，紧跟互联网浪潮。目前，公司正与上海市政府及海关总署指定的上海跨境电子商务平台——“跨境通”合作，共同建设跨境信息平台，并参与自贸区信息平台的设计和建设。同时，公司积极开拓跨境电商直邮业务，与国内外知名跨境电商大力合作，美国亚马逊、中国敦煌网等均为公司重要战略客户。公司正紧锣密鼓的打造跨境电子商务的***信息平台，在当今互联网的大潮下，未来两到三年是巨大的机遇期，公司将纳入大批的人才加入到我们这个开创性的事业中来。现诚邀您的加入！'],
        '110010833': ['1-1.5万/月', '做五休二|五险一金|带薪年假|节日福利|餐饮补贴|交通补贴|', '武汉-硚口区', '3-4年经验', '本科', '招3人', '10-11发布', '测试工程师',
                      '上海顺益信息科技有限公司',
                      '工作职责\n1.负责需求分析、测试计划制定、测试用例设计、测试执行，协助项目经理保证项目质量与进度；\n2.负责公司各产品线的质量保证工作；\n3.负责测试相关平台、工具的设计与开发，提升工作效率与效果；\n4.跟踪定位产品中的缺陷或问题，与项目相关人员就项目进度和问题进行沟通。\n5.参与项目的需求和迭代开发计划的讨论和评审；\n6.制定项目的测试计划并设计测试用例；\n7.搭建测试环境、测试设计、执行及bug的定位、跟踪和管理；\n8.设计UI、接口自动化脚本或性能测试脚本，并执行自动化脚本；\n9.项目上线后，对产生线上Incident事件或技术缺陷进行case_study分析；\n10.通过总结、对外交流、技术钻研和培训，进行测试过程和测试方法的持续改进。\n职位要求\n1、本科及以上学历，计算机相关专业；\n2、具有4年以上测试或开发经验（测试经验不低于2年）；\n3、熟悉测试理论、流程与方法，熟练使用主流的功能或性能测试工具；\n4、具备一定的业务分析，沟通表达能力和综合协调能力，工作积极主动；\n5、良好的沟通能力和团队协作能力，具备高度责任感；\n6、具备强大的逻辑思辨能力，谈判能力和冲突管理能力者优先。\n7、能够基本掌握一门开发语言，java/php/.net；\n8、熟悉Oracle/SqlServer/Mysql/MongoDB等至少一种数据库管理系统，能够熟练编写SQL语句；\n职能类别：软件工程师软件测试\n关键字：测试\n',
                      '上班地址：武汉市江汉区泛海国际soho城 6栋',
                      '上海顺益信息科技有限公司是完全市场化运作的软件开发和运营管理的高科技企业，是中国报关协会副会长单位。顺益公司运营管理的——“通关网”（www.hscode.net）是海关总署和中国报关协会指定的全国预归类服务平台。所有进出口商品报关前可通过平台完成商品预归类，以便利通关。该网在海关总署和中国报关协会的领导下，积极参与海关重大业务改革，充分利用信息化的手段,创新管理模式，力求打造服务社会、服务海关、服务企业的智慧型物流生态链。通过全国预归类服务平台，遵照海关总署在预归类服务基础上推进“三预”，即“预归类、预审价、原产地预确认”的要求，以预归类商品数据库为核心，运营全国预归类平台的基础上，整合仓储、运输等关联物流行业的服务需求,最终形成以物流为核心的电子商务网站平台。2014年公司借助通关网平台致力于跨境电子商务通关服务，紧跟互联网浪潮。目前，公司正与上海市政府及海关总署指定的上海跨境电子商务平台——“跨境通”合作，共同建设跨境信息平台，并参与自贸区信息平台的设计和建设。同时，公司积极开拓跨境电商直邮业务，与国内外知名跨境电商大力合作，美国亚马逊、中国敦煌网等均为公司重要战略客户。公司正紧锣密鼓的打造跨境电子商务的***信息平台，在当今互联网的大潮下，未来两到三年是巨大的机遇期，公司将纳入大批的人才加入到我们这个开创性的事业中来。现诚邀您的加入！'],
        '104659950': ['1-1.2万/月', '五险一金|年终奖金|弹性工作|免费班车|专业培训|', '武汉-硚口区', '5-7年经验', '大专', '招2人', '11-20发布', '高级软件测试工程师',
                      '维书信息科技（上海）有限公司',
                      '1）根据项目需求文档和设计文档，对软件测试项目进行测试设计，编写测试方案；\n2）独立实施软件测试项目，独立编写测试计划、测试用例和测试报告；\n3）及时准确地对项目缺陷进行上报，并与开发人员等相关人员进行有效沟通，保证项目进度和质量；\n4）希望能够根据对项目需求的理解，提出功能测试之外的建议，如用户体验等方面；\n\n任职要求：\n1）专科以上学历，计算机相关专业毕业优先；\n2）5年左右软件测试经验；\n3）熟悉软件工程、软件测试流程和规范，精通常用测试方法和手段，熟悉常用的测试工具；\n4）熟悉性能测试、接口测试、Web端测试以及自动化软件测试；\n5）具有良好的沟通能力和团队合作能力；\n6）工作认真负责、积极主动；\n7）具备良好的自学能力，对新技术、新方法充满兴趣；\n\n\n职能类别：高级软件工程师系统工程师\n关键字：功能测试接口测试jmeterloadrunner\n',
                      '上班地址：江夏区通用大道',
                      '维书信息科技（上海）有限公司维书信息科技（上海）有限公司是一家从事软件服务的高新技术企业，为制造业客户提供智能物流、智能工厂、物联网及大数据的解决方案。公司主要业务涉及供应链管理、物流可视化、终端客户及设备管理等方面。互联网的未来发展方向在大数据和物联网。目前，越来越多的传统企业意识到互联网化的重要性，期望通过大数据分析、智能物联等手段，进一步优化传统企业的产品研发、生产、物流及销售等各个环节，降低成本，提高企业的竞争力。维书信息致力于大数据及物联网，为传统的制造业客户提供智能物流、智能工厂、物联网及大数据的解决方案。维书信息一直本着以“注重人才、以人为本”的用人宗旨，力争为员工提供一个具有竞争力的薪酬和广阔的发展空间，让员工与公司共同成长。为实现我们共同的事业和梦想，我们渴望更多志同道合的朋友加入！在这里，您将拥有的不仅仅是良好的工作环境，更是置身于广阔的发展空间之中，在事业的舞台上挥洒我们青春和才智！如果您对未来充满梦想，对成功也充满渴望，那么请让我们携手同行，真诚合作，实现梦想，共创未来！'],
        '85435329': ['1-1.5万/月', '五险一金|年终奖金|免费班车|员工旅游|定期体检|餐饮补贴|', '武汉-硚口区', '3-4年经验', '本科', '招3人', '12-09发布',
                     '电气设计工程师', '武汉高德红外股份有限公司',
                     '岗位职责：1.参与系统及飞行器电气方案的论证工作；\n2.根据总体及技术要求，开展电气分系统设计工作，材料的选型及调研，电路的测试、联调及排故工作；\n3.开展相应部件的嵌入式软件设计、测试工作；\n4.根据系统需求，开展全弹研制过程中相关分系统的测试系统设计工作；\n5.配合开展的各种系统测试、联调及试验工作\n任职要求：\n1.本科2年以上，硕士1年以上工作经历。\n2.掌握STM32、TI系列DSP或FPGA电路设计技术，熟悉电子产品设计开发流程。\n3.熟练运用电路设计工具，精通C语言。\n4.能运用工具独立完成封装制作、PCB布局、布线、PCB制板文件制作及检查者优先。\n5.有过软件测试工作经验者；\n6.具有优秀的团队意识，善于组织协调开展工作，具有较强的抗压能力。\n职能类别：电气工程师/技术员\n',
                     '上班地址：湖北省武汉市东湖开发区黄龙山南路6号',
                     '武汉高德红外股份有限公司创立于1999年，是规模化从事红外探测器、红外热像仪、大型光电系统、防务类系统研发、生产、销售的高新技术上市公司。公司总市值超过200亿元，员工总数2300余人，其中研发团队近1000多人，营销服务网络遍布全球70多个国家和地区，并在比利时成了欧洲分公司。公司产品广泛应用于电力、冶金、石化、建筑、消防、执法、检验检疫、安防监控、车载夜视等民用领域。公司正以红外焦平面探测器产业化为契机，积极推进红外热成像产品的“消费品化”。\xa0\xa0\xa0\xa0\xa0\xa02010年公司顺利登陆深圳A股主板市场，股票代码：002414。'],
        '85549528': ['1-1.5万/月', '五险一金|餐饮补贴|定期体检|免费班车|员工旅游|年终奖金|', '武汉-硚口区', '2年经验', '本科', '招2人', '12-09发布',
                     '跟踪器（DSP方向）', '武汉高德红外股份有限公司',
                     '1.根据技术要求，开展跟踪器的方案设计\n2.开展跟踪器硬件电路设计，芯片的选型及调研，硬件电路的测试、联调及排故工作；\n3.配套开展相应部件的嵌入式软件设计、测试工作；\n4.配合其他部门进行系统测试、联调及试验工作；\n5.编写技术文档。\n\n1.有硬件电路设计、PCB制板设计或嵌入式系统设计工作经验者优先；\n2.精通至少一种DSP的硬件或相关软件设计并熟悉相关设计工具；\n3.熟练掌握C语言程序设计，能够进行简单的汇编程序设计；\n4.有过软件测试工作经验者优先；\n5.具有优秀的团队意识，善于组织协调开展工作，具有较强的抗压能力。\n职能类别：嵌入式软件开发(Linux/单片机/PLC/DSP…)\n',
                     '上班地址：湖北省武汉市东湖开发区黄龙山南路6号',
                     '武汉高德红外股份有限公司创立于1999年，是规模化从事红外探测器、红外热像仪、大型光电系统、防务类系统研发、生产、销售的高新技术上市公司。公司总市值超过200亿元，员工总数2300余人，其中研发团队近1000多人，营销服务网络遍布全球70多个国家和地区，并在比利时成了欧洲分公司。公司产品广泛应用于电力、冶金、石化、建筑、消防、执法、检验检疫、安防监控、车载夜视等民用领域。公司正以红外焦平面探测器产业化为契机，积极推进红外热成像产品的“消费品化”。\xa0\xa0\xa0\xa0\xa0\xa02010年公司顺利登陆深圳A股主板市场，股票代码：002414。'],
        '118904295': ['', '', '武汉-东湖新技术产业开发区', '无工作经验', '本科', '招2人', '12-09发布', 'Beta测试组织工程师', '诚迈科技（武汉分公司）—武汉诚迈科技有限公司',
                      '1、Beta测试活动组织（包括宣传策划，项目运维，线下专项活动策划组织等）\n2、Beta用户人员运营（Beta用户活跃度及组织气氛调动，用户纳新及优质用户维护，Beta用户粘性维护等）\n\n职位要求：\n1、本科学历，有测试经验，性能温和，脑子灵活，开朗活泼，能与组员和睦相处\n2、组织能力强，情商高，有想法，爱表达\n3、细心，耐心，大度\n4、熟练掌握office办公工具，熟练掌握PS\n\n\n职能类别：项目执行/协调人员软件测试\n关键字：Beta测试沟通组织\n',
                      '上班地址：:武汉东湖高新区高新大道武汉未来科技城C2-11楼',
                      '诚迈科技（南京）有限公司成立于2006年9月，2017年1月20日公司成功上市，是一家专业从事软件产品设计、代码开发、质量保证及技术支持等全流程服务的软件服务提供商，致力于提供全球化的专业软件研发服务，专注于移动设备及无线互联网行业软件研发及咨询等服务。诚迈科技总部位于中国南京。经过多年的发展，规模已超过2000人，在加拿大、芬兰及日本设立销售体系，在北京、上海、深圳、武汉、广州和西安设有分支机构，业务覆盖全球，在中国（内地及台湾）、北美、欧洲、日本、韩国等地广泛开展业务。Archermind Technology (Nanjing) Co. Ltd., established in September, 2006, was listed on the stock market on 20 January,2017,is a professional software service provider specializing in software product design, code development, quality assurance, technology support, etc.. The company is devoting to providing specialized world-wide software R&D service and focusing on R&D and consult service in the field of mobile facilities and wireless internet software. The headquarters of Archermind is in Nanjing. After four years’ development, the company has more than 2,000 employees, sales systems in Canada, Finland, and Japan and branch offices in Beijing, Shanghai, Shenzhen and Wuhan. Now, the company extends its service to lots of places in the world, such as China including mainland and Taiwan, North America, Europe, Japan and Korea.诚迈科技作为行业的领军者，在全球范围内为国内外客提供一流的软件研发和测试服务。专业的研发团队凭借多年的项目经验掌握了行业核心技术，可提供Android行业软件解决方案（车载系统、TV、eBook等）；移动互联网软件解决方案（浏览器、APP Store、运营商定制等）；云终端解决方案及企业应用和云计算解决方案。在嵌入式测试方面，诚迈科技专业的软件测试团队在测试方法、测试策略、测试标准方面有着丰富的经验，精通手机终端设备中的手机操作系统、手机应用软件等测试。目前，诚迈科技已经与世界级的客户建立了长期友好的合作关系，主要客户广泛分布于终端设备制造商、世界级芯片制造商、运营商及软件公司。As a leader in the field, Archermind is dedicating to provide top software R&D and test service to domestic and oversea customers. The professional R&D group who have years’ project experience, have professional core technology and can provide total solution for Android software (Car System, TV, eBook, etc.); for mobile internet software(Browser, APP Store, Custom Operators, etc.); and provide solution for cloud terminal, enterprise application and cloud computing. On the aspect of embedded test, the software test groups are experienced in test method, test strategy and test standard. They are proficient in test of mobile operating system and mobile application software in mobile terminal equipment. Now, Archermind has established long-term cooperative relationship with world-class customers, who are from the top terminal equipment manufacturers, chip manufacturers, operators and software companies.如果您崇尚奋斗，渴望创新，并希望同公司一起成长，请加入我们的团队，您可以应对不同的挑战，以激发个人潜能。我们将长期提供多方面的发展机会，并对成绩突出的员工给予职位晋升和物质奖励。If you like striving, innovation and growing up with the company, please join us! Here you have the opportunity to meet different challenges to motivate your potential. We will provide kinds of development opportunities. If you work hard and outstandingly, we will give you promotion and rewards.您还将享受完善的员工福利制度，包括：弹性工作时间，各项激励奖金，养老保险，医疗保险，失业保险，工伤、生育保险，住房公积金，员工俱乐部，各种员工活动，员工心灵关怀和健康关怀计划，特别节日假期，带薪年假，集体户口（如需要）等。You can also benefit from the employee welfare system, which includes flexible working time, pension insurance, medical insurance, unemployment insurance, industrial injury assurance and maternity insurance, housing fund, employee club, a variety of employee activities, employee spiritual care and health care programs, particularly holidays, paid annual leave, collective household  account(if need), etc..处于高速发展和扩张期的诚迈科技诚邀有志之士与公司同仁一起共创一个伟大的软件企业！Archermind, who is in the period of rapid development and expansion, sincerely invites the ones who are looking forward to create a great software industry with the us.公司网址：www.archermind.com若您希望在以下城市工作，可按以下邮件地址投递：南 京：hr@archermind.com武 汉：hr_wh@archermind.com上 海：hr_sh@archermind.com深 圳：hr_sz@archermind.com北 京：hr_bj@archermind.com广 州：hr_gz@archermind.com'],
        '118904135': ['', '', '武汉-东湖新技术产业开发区', '2年经验', '本科', '招3人', '12-09发布', '音频测试工程师', '诚迈科技（武汉分公司）—武汉诚迈科技有限公司',
                      '负责PC项目音频类测试\n\n职责要求：\n1、本科学历，2年以上PC音频类测试经验，经验合适可以放宽至大专\n1.具备音乐发烧友潜质，懂得分辨什么是”好的音质“。\n2.具备良好的动手能力，了解基本的音频设备，能够熟练使用音频测试设备，如声卡、功放、播放器、音响等。\n3.具备基本的视频和音频剪辑经验，能够使用会声会影，爱剪辑，AdobeAudition等软件。\n职能类别：测试工程师软件测试\n关键字：PC音频Audition测试产品测试\n',
                      '上班地址：:武汉东湖高新区高新大道武汉未来科技城C2-11楼',
                      '诚迈科技（南京）有限公司成立于2006年9月，2017年1月20日公司成功上市，是一家专业从事软件产品设计、代码开发、质量保证及技术支持等全流程服务的软件服务提供商，致力于提供全球化的专业软件研发服务，专注于移动设备及无线互联网行业软件研发及咨询等服务。诚迈科技总部位于中国南京。经过多年的发展，规模已超过2000人，在加拿大、芬兰及日本设立销售体系，在北京、上海、深圳、武汉、广州和西安设有分支机构，业务覆盖全球，在中国（内地及台湾）、北美、欧洲、日本、韩国等地广泛开展业务。Archermind Technology (Nanjing) Co. Ltd., established in September, 2006, was listed on the stock market on 20 January,2017,is a professional software service provider specializing in software product design, code development, quality assurance, technology support, etc.. The company is devoting to providing specialized world-wide software R&D service and focusing on R&D and consult service in the field of mobile facilities and wireless internet software. The headquarters of Archermind is in Nanjing. After four years’ development, the company has more than 2,000 employees, sales systems in Canada, Finland, and Japan and branch offices in Beijing, Shanghai, Shenzhen and Wuhan. Now, the company extends its service to lots of places in the world, such as China including mainland and Taiwan, North America, Europe, Japan and Korea.诚迈科技作为行业的领军者，在全球范围内为国内外客提供一流的软件研发和测试服务。专业的研发团队凭借多年的项目经验掌握了行业核心技术，可提供Android行业软件解决方案（车载系统、TV、eBook等）；移动互联网软件解决方案（浏览器、APP Store、运营商定制等）；云终端解决方案及企业应用和云计算解决方案。在嵌入式测试方面，诚迈科技专业的软件测试团队在测试方法、测试策略、测试标准方面有着丰富的经验，精通手机终端设备中的手机操作系统、手机应用软件等测试。目前，诚迈科技已经与世界级的客户建立了长期友好的合作关系，主要客户广泛分布于终端设备制造商、世界级芯片制造商、运营商及软件公司。As a leader in the field, Archermind is dedicating to provide top software R&D and test service to domestic and oversea customers. The professional R&D group who have years’ project experience, have professional core technology and can provide total solution for Android software (Car System, TV, eBook, etc.); for mobile internet software(Browser, APP Store, Custom Operators, etc.); and provide solution for cloud terminal, enterprise application and cloud computing. On the aspect of embedded test, the software test groups are experienced in test method, test strategy and test standard. They are proficient in test of mobile operating system and mobile application software in mobile terminal equipment. Now, Archermind has established long-term cooperative relationship with world-class customers, who are from the top terminal equipment manufacturers, chip manufacturers, operators and software companies.如果您崇尚奋斗，渴望创新，并希望同公司一起成长，请加入我们的团队，您可以应对不同的挑战，以激发个人潜能。我们将长期提供多方面的发展机会，并对成绩突出的员工给予职位晋升和物质奖励。If you like striving, innovation and growing up with the company, please join us! Here you have the opportunity to meet different challenges to motivate your potential. We will provide kinds of development opportunities. If you work hard and outstandingly, we will give you promotion and rewards.您还将享受完善的员工福利制度，包括：弹性工作时间，各项激励奖金，养老保险，医疗保险，失业保险，工伤、生育保险，住房公积金，员工俱乐部，各种员工活动，员工心灵关怀和健康关怀计划，特别节日假期，带薪年假，集体户口（如需要）等。You can also benefit from the employee welfare system, which includes flexible working time, pension insurance, medical insurance, unemployment insurance, industrial injury assurance and maternity insurance, housing fund, employee club, a variety of employee activities, employee spiritual care and health care programs, particularly holidays, paid annual leave, collective household  account(if need), etc..处于高速发展和扩张期的诚迈科技诚邀有志之士与公司同仁一起共创一个伟大的软件企业！Archermind, who is in the period of rapid development and expansion, sincerely invites the ones who are looking forward to create a great software industry with the us.公司网址：www.archermind.com若您希望在以下城市工作，可按以下邮件地址投递：南 京：hr@archermind.com武 汉：hr_wh@archermind.com上 海：hr_sh@archermind.com深 圳：hr_sz@archermind.com北 京：hr_bj@archermind.com广 州：hr_gz@archermind.com'],
        '118877518': ['', '', '武汉-东湖新技术产业开发区', '无工作经验', '本科', '招3人', '12-09发布', 'Camera测试工程师', '诚迈科技（武汉分公司）—武汉诚迈科技有限公司',
                      '负责PC项目Camera测试\n\n职位要求：\n1、统招本科学历，光学，光电，图像处理，电子，自动化，计算机等专业\n2、2年以上Camera相关测试/开发经验，了解Camera成像原理，图像质量基础知识，会调试图像显示效果，经验合适学历可放宽至大专\n3、熟悉图像分析软件如faststone,DXO,Imatest等，熟悉使用Camera测试设备，如DXO、IE灯箱、QC灯箱，Aebox等仪器\n4、要求非色盲、色弱，摄影爱好者优先\n\n职能类别：软件测试测试工程师\n关键字：Camera测试PCWindows\n',
                      '上班地址：:武汉东湖高新区高新大道武汉未来科技城C2-11楼',
                      '诚迈科技（南京）有限公司成立于2006年9月，2017年1月20日公司成功上市，是一家专业从事软件产品设计、代码开发、质量保证及技术支持等全流程服务的软件服务提供商，致力于提供全球化的专业软件研发服务，专注于移动设备及无线互联网行业软件研发及咨询等服务。诚迈科技总部位于中国南京。经过多年的发展，规模已超过2000人，在加拿大、芬兰及日本设立销售体系，在北京、上海、深圳、武汉、广州和西安设有分支机构，业务覆盖全球，在中国（内地及台湾）、北美、欧洲、日本、韩国等地广泛开展业务。Archermind Technology (Nanjing) Co. Ltd., established in September, 2006, was listed on the stock market on 20 January,2017,is a professional software service provider specializing in software product design, code development, quality assurance, technology support, etc.. The company is devoting to providing specialized world-wide software R&D service and focusing on R&D and consult service in the field of mobile facilities and wireless internet software. The headquarters of Archermind is in Nanjing. After four years’ development, the company has more than 2,000 employees, sales systems in Canada, Finland, and Japan and branch offices in Beijing, Shanghai, Shenzhen and Wuhan. Now, the company extends its service to lots of places in the world, such as China including mainland and Taiwan, North America, Europe, Japan and Korea.诚迈科技作为行业的领军者，在全球范围内为国内外客提供一流的软件研发和测试服务。专业的研发团队凭借多年的项目经验掌握了行业核心技术，可提供Android行业软件解决方案（车载系统、TV、eBook等）；移动互联网软件解决方案（浏览器、APP Store、运营商定制等）；云终端解决方案及企业应用和云计算解决方案。在嵌入式测试方面，诚迈科技专业的软件测试团队在测试方法、测试策略、测试标准方面有着丰富的经验，精通手机终端设备中的手机操作系统、手机应用软件等测试。目前，诚迈科技已经与世界级的客户建立了长期友好的合作关系，主要客户广泛分布于终端设备制造商、世界级芯片制造商、运营商及软件公司。As a leader in the field, Archermind is dedicating to provide top software R&D and test service to domestic and oversea customers. The professional R&D group who have years’ project experience, have professional core technology and can provide total solution for Android software (Car System, TV, eBook, etc.); for mobile internet software(Browser, APP Store, Custom Operators, etc.); and provide solution for cloud terminal, enterprise application and cloud computing. On the aspect of embedded test, the software test groups are experienced in test method, test strategy and test standard. They are proficient in test of mobile operating system and mobile application software in mobile terminal equipment. Now, Archermind has established long-term cooperative relationship with world-class customers, who are from the top terminal equipment manufacturers, chip manufacturers, operators and software companies.如果您崇尚奋斗，渴望创新，并希望同公司一起成长，请加入我们的团队，您可以应对不同的挑战，以激发个人潜能。我们将长期提供多方面的发展机会，并对成绩突出的员工给予职位晋升和物质奖励。If you like striving, innovation and growing up with the company, please join us! Here you have the opportunity to meet different challenges to motivate your potential. We will provide kinds of development opportunities. If you work hard and outstandingly, we will give you promotion and rewards.您还将享受完善的员工福利制度，包括：弹性工作时间，各项激励奖金，养老保险，医疗保险，失业保险，工伤、生育保险，住房公积金，员工俱乐部，各种员工活动，员工心灵关怀和健康关怀计划，特别节日假期，带薪年假，集体户口（如需要）等。You can also benefit from the employee welfare system, which includes flexible working time, pension insurance, medical insurance, unemployment insurance, industrial injury assurance and maternity insurance, housing fund, employee club, a variety of employee activities, employee spiritual care and health care programs, particularly holidays, paid annual leave, collective household  account(if need), etc..处于高速发展和扩张期的诚迈科技诚邀有志之士与公司同仁一起共创一个伟大的软件企业！Archermind, who is in the period of rapid development and expansion, sincerely invites the ones who are looking forward to create a great software industry with the us.公司网址：www.archermind.com若您希望在以下城市工作，可按以下邮件地址投递：南 京：hr@archermind.com武 汉：hr_wh@archermind.com上 海：hr_sh@archermind.com深 圳：hr_sz@archermind.com北 京：hr_bj@archermind.com广 州：hr_gz@archermind.com'],
        '118877249': ['', '', '武汉-东湖新技术产业开发区', '5-7年经验', '本科', '招3人', '12-09发布', 'PC Windows测试经理',
                      '诚迈科技（武汉分公司）—武汉诚迈科技有限公司',
                      '1、负责项目的实施、协调、监督与交付，把握测评实施服务进度与质量。\n2、负责项目实施案例整理及成果提炼，形成可复制的知识；对项目实施方法、策略以及方案进行持续优化和建议，确保项目实施的持续化改进。\n3、负责项目的风险管理，包括对完成项目可能出现的各种风险的识别和评估、风险防范策略的制定及对风险的有效监控。\n\n职位要求：\n1、5年以上PCWindows产品测试经验，其中具备3年以上PC测试管理经验，沟通、推动能力强。\n2、有很强的业务理解能力和测试分析建模能力，同时具备很强的技术档撰写能力；掌握质量改进方法。\n3、独立管理测试团队，根据客户进度制定测试计划，分配测试任务，执行测试任务，整理检查并反馈组内成员输出结果，确保所有测试结果的正确性及有效性。\n职能类别：项目经理软件测试\n关键字：PCWindows测试经理项目经理管理\n',
                      '上班地址：:武汉东湖高新区高新大道武汉未来科技城C2-11楼',
                      '诚迈科技（南京）有限公司成立于2006年9月，2017年1月20日公司成功上市，是一家专业从事软件产品设计、代码开发、质量保证及技术支持等全流程服务的软件服务提供商，致力于提供全球化的专业软件研发服务，专注于移动设备及无线互联网行业软件研发及咨询等服务。诚迈科技总部位于中国南京。经过多年的发展，规模已超过2000人，在加拿大、芬兰及日本设立销售体系，在北京、上海、深圳、武汉、广州和西安设有分支机构，业务覆盖全球，在中国（内地及台湾）、北美、欧洲、日本、韩国等地广泛开展业务。Archermind Technology (Nanjing) Co. Ltd., established in September, 2006, was listed on the stock market on 20 January,2017,is a professional software service provider specializing in software product design, code development, quality assurance, technology support, etc.. The company is devoting to providing specialized world-wide software R&D service and focusing on R&D and consult service in the field of mobile facilities and wireless internet software. The headquarters of Archermind is in Nanjing. After four years’ development, the company has more than 2,000 employees, sales systems in Canada, Finland, and Japan and branch offices in Beijing, Shanghai, Shenzhen and Wuhan. Now, the company extends its service to lots of places in the world, such as China including mainland and Taiwan, North America, Europe, Japan and Korea.诚迈科技作为行业的领军者，在全球范围内为国内外客提供一流的软件研发和测试服务。专业的研发团队凭借多年的项目经验掌握了行业核心技术，可提供Android行业软件解决方案（车载系统、TV、eBook等）；移动互联网软件解决方案（浏览器、APP Store、运营商定制等）；云终端解决方案及企业应用和云计算解决方案。在嵌入式测试方面，诚迈科技专业的软件测试团队在测试方法、测试策略、测试标准方面有着丰富的经验，精通手机终端设备中的手机操作系统、手机应用软件等测试。目前，诚迈科技已经与世界级的客户建立了长期友好的合作关系，主要客户广泛分布于终端设备制造商、世界级芯片制造商、运营商及软件公司。As a leader in the field, Archermind is dedicating to provide top software R&D and test service to domestic and oversea customers. The professional R&D group who have years’ project experience, have professional core technology and can provide total solution for Android software (Car System, TV, eBook, etc.); for mobile internet software(Browser, APP Store, Custom Operators, etc.); and provide solution for cloud terminal, enterprise application and cloud computing. On the aspect of embedded test, the software test groups are experienced in test method, test strategy and test standard. They are proficient in test of mobile operating system and mobile application software in mobile terminal equipment. Now, Archermind has established long-term cooperative relationship with world-class customers, who are from the top terminal equipment manufacturers, chip manufacturers, operators and software companies.如果您崇尚奋斗，渴望创新，并希望同公司一起成长，请加入我们的团队，您可以应对不同的挑战，以激发个人潜能。我们将长期提供多方面的发展机会，并对成绩突出的员工给予职位晋升和物质奖励。If you like striving, innovation and growing up with the company, please join us! Here you have the opportunity to meet different challenges to motivate your potential. We will provide kinds of development opportunities. If you work hard and outstandingly, we will give you promotion and rewards.您还将享受完善的员工福利制度，包括：弹性工作时间，各项激励奖金，养老保险，医疗保险，失业保险，工伤、生育保险，住房公积金，员工俱乐部，各种员工活动，员工心灵关怀和健康关怀计划，特别节日假期，带薪年假，集体户口（如需要）等。You can also benefit from the employee welfare system, which includes flexible working time, pension insurance, medical insurance, unemployment insurance, industrial injury assurance and maternity insurance, housing fund, employee club, a variety of employee activities, employee spiritual care and health care programs, particularly holidays, paid annual leave, collective household  account(if need), etc..处于高速发展和扩张期的诚迈科技诚邀有志之士与公司同仁一起共创一个伟大的软件企业！Archermind, who is in the period of rapid development and expansion, sincerely invites the ones who are looking forward to create a great software industry with the us.公司网址：www.archermind.com若您希望在以下城市工作，可按以下邮件地址投递：南 京：hr@archermind.com武 汉：hr_wh@archermind.com上 海：hr_sh@archermind.com深 圳：hr_sz@archermind.com北 京：hr_bj@archermind.com广 州：hr_gz@archermind.com'],
        '118294805': ['1-2万/月', '五险一金|交通补贴|餐饮补贴|专业培训|绩效奖金|年终奖金|定期体检|', '武汉-东湖新技术产业开发区', '5-7年经验', '本科', '招1人',
                      '12-09发布', '测试组长', '武大吉奥信息技术有限公司',
                      '岗位职责：\n1.负责建立有效的测试流程，持续推进测试流程的优化；\n2.负责搭建测试环境，保证测试环境的独立和维护测试环境的更新；\n3.负责测试的技术体系建设与维护，以及团队技能培养，如：自动化测试.性能测试.安全测试等；\n4.对现有产品进行性能或安全性测试，并能进行结果分析；\n5.测试团队日常工作的管理.监督测试团队的工作，并进行人员培养。\n任职要求：\n1.统招本科及以上学历，硕士优先；5年或以上测试工作经验，从事GIS.云计算和大数据行业测试经验者优先；\n2.软件知识结构全面，通晓软件工程.软件测试理论.方法和过程；\n3.熟悉主流操作系统及数据库，熟练使用sql语句，熟练使用相关测试工具(Jmeter.LR.gTest.jUnit.jenkins.selenium等)；\n4.较强的文档撰写能力，完成测试计划.测试设计.测试报告等文档；\n5.良好的分析能力，表达能力和综合协调能力，且能有效解决问题；\n6.有丰富的测试团队管理经验。\n\n职能类别：高级软件工程师软件工程师\n',
                      '上班地址：东湖新技术开发区大学园路武大科技园吉奥大厦',
                      '武大吉奥信息技术有限公司成立于1999年，是武汉大学科技成果转化企业。作为中国领先的地理智能、大数据技术研发及服务企业，公司拥有20年地理信息实践与管理经验，业务体系涵盖自然资源、城市治理、智慧城市和军民融合等行业领域。目前公司在北京、江西、广西、广州、深圳、西安、无锡等地设立了分支机构，服务区域遍布我国29个省及400多个县市。\xa0\xa0\xa0\xa0\xa0\xa0公司拥有业内领先、自主可控的GIS产品—“吉奥之星”系列软件，以地理信息基础平台GeoGlobe、地理智能服务平台GeoSmarter、云管理平台GeoStack三大产品为核心，构建云生态的产品应用服务体系，聚焦城市大数据治理，致力于成为时空大数据治理的领航者。\xa0\xa0\xa0\xa0\xa0未来，武大吉奥坚持以客户为中心，秉承“挖掘数据价值，服务数字中国”的理念，建立以业务驱动协同化、数据驱动平台化的双轮驱动模式，打造大数据治理的新引擎。公司实行每天8小时工作双休制，一经录用，我们将为您提供：一、完备的福利措施1.社会保险（养老、医疗、失业、工伤、生育）2.住房公积金3.车贴、餐贴4.集体出游、年度体检5.各种贺礼、慰问金6.国家法定节假日、带薪年假、带薪病假7.婚假、产假以及围产假、丧假……二、健全的培训机制1.培训体系：新进人员培训、专业技能类培训、综合素质培训、管理类培训、外部培训和进修；2.培训形式：内训、派外训练、在职进修；3.公司鼓励并且组织员工参加各类认证考试、相关培训，考试等费用均由公司承担；4.对于员工自行参加的各类认证考试，符合公司奖励政策的，还可另行奖励。三、完善的职业晋升通道公司构建完善的员工职业发展通道，鼓励员工从管理、专业技术等多个方向进行选择性地职业发展，建立包括企业后备接班人、后备干部、后备梯队在内的企业内部不同层次的人才培养机制，鼓励员工积极进取，将个人的职业发展与企业的发展进行有效地结合。公司地址：武汉东湖新技术开发区大学园路武大科技园吉奥大厦 (邮编：430223)公司官网：http://www.geostar.com.cn'],
        '107816950': ['1-1.4万/月', '五险一金|年终奖金|弹性工作|免费班车|专业培训|', '武汉-东湖新技术产业开发区', '5-7年经验', '大专', '招2人', '12-09发布',
                      '自动化测试工程师', '维书信息科技（上海）有限公司',
                      '1、编写自动化测试用例，开展自动化测试。\n2、负责自动化测试脚本(selenium+Java)的编写与维护；\n3、根据性能测试的需求，设计性能测试的场景，数据，脚本；\n4、使用主流性能测试工具，产出标准的测试文档；\n5、独立完成自动化测试任务，根据工作需要开发测试工具、测试脚本、监控脚本等。\n\n任职资格：\n1、专科及以上学历，至少2~3年自动化测试项目经验；\n2、能够熟练使用selenium+Java进行自动化测试脚本的开发；\n3、精通性能测试场景设计，掌握系统性能测试方法；\n4、熟练掌握主流性能测试工具Jmeter、loadrunner；\n5、熟悉自动化测试，接口测试，白盒测试，压力测试的设计原则和流程；\n\n\n职能类别：软件测试测试工程师\n关键字：测试自动化pythonJavaJmeterloadrunner\n',
                      '上班地址：江夏区通用大道',
                      '维书信息科技（上海）有限公司维书信息科技（上海）有限公司是一家从事软件服务的高新技术企业，为制造业客户提供智能物流、智能工厂、物联网及大数据的解决方案。公司主要业务涉及供应链管理、物流可视化、终端客户及设备管理等方面。互联网的未来发展方向在大数据和物联网。目前，越来越多的传统企业意识到互联网化的重要性，期望通过大数据分析、智能物联等手段，进一步优化传统企业的产品研发、生产、物流及销售等各个环节，降低成本，提高企业的竞争力。维书信息致力于大数据及物联网，为传统的制造业客户提供智能物流、智能工厂、物联网及大数据的解决方案。维书信息一直本着以“注重人才、以人为本”的用人宗旨，力争为员工提供一个具有竞争力的薪酬和广阔的发展空间，让员工与公司共同成长。为实现我们共同的事业和梦想，我们渴望更多志同道合的朋友加入！在这里，您将拥有的不仅仅是良好的工作环境，更是置身于广阔的发展空间之中，在事业的舞台上挥洒我们青春和才智！如果您对未来充满梦想，对成功也充满渴望，那么请让我们携手同行，真诚合作，实现梦想，共创未来！'],
        '116519192': ['1-1.5万/月', '水果早餐|补充医疗保险|绩效奖金|定期体检|专业培训|', '武汉-东湖新技术产业开发区', '5-7年经验', '本科', '招若干人', '12-09发布',
                      '高级测试工程师(J10319)', '北京腾云天下科技有限公司',
                      '工作职责:\n1、负责公司相关项目产品的测试，包括但不限于功能、接口、性能测试。按时保质交付项目。\n2、与开发、产品紧密沟通，协同测试小组，进行项目测试过程质量把控，推进项目进展，及时反馈测试进度和风险。\n3、和自动化工具小组进行有效沟通和衔接，进行项目测试过程质量把控，推进项目进展，及时反馈测试进度和风险；\n4、保障项目测试质量、完成项目顺利上线、进行线上质量保障及反馈等；\n5、梳理并对项目相关的流程标准进行适当裁剪和梳理规范；\n任职资格:\n1、计算机相关专业毕业，本科以上，工作年限5年以上\n2、有良好的质量意识，扎实的测试理论基础，很强的责任感和相关风险意识；\n3、2年以上团队管理经验，有实际的项目质量过程控制经验和自动化测试经验，有性能经验者优先；\n4、熟悉C++/java/python/go等任意语言，熟悉主流数据库的操作和相关使用；\n5、熟悉大数据相关的技术或相关测试经验者优先\n\n职能类别：软件测试\n',
                      '上班地址：新发展大厦',
                      'TalkingData 成立于2011年，是国内领先的第三方数据智能平台。借助以SmartDP为核心的数据智能应用生态为企业赋能，帮助企业逐步实现以数据为驱动力的数字化转型。我们的愿景TalkingData 成立以来秉承“数据改变企业决策，数据改善人类生活”的愿景，逐步成长为中国领先的数据智能服务商。以开放共赢为基础，TalkingData凭借领先的数据智能产品、服务与解决方案，致力于为客户创造价值，成为客户的“成效合作伙伴”，帮助现代企业实现数据驱动转型，加速各行业的数字化进程，利用数据产生的智能改变人类对世界以及对自身的认知，并最终实现对人类生活的改善。企业责任感TalkingData不仅专注于数据智能应用的研发和实践积累，同时也在积极推动大数据行业的技术演进。早在2011年成立初始，TalkingData就组建了数据科学团队，将机器学习等人工智能技术引入海量数据的处理、加工流程中。通过几年来的不断发展，TalkingData已在大数据、人工智能领域拥有多项国家专利。此外，TalkingData还开源了大规模机器学习算法库Fregata、UI组件库iView、地理信息可视化框架inMap等项目，在海内外得到广泛支持与认可，使用者和贡献者遍布全球。目前TalkingData设立了包括硅谷边缘计算实验室、人本实验室在内的多个大数据、人工智能实验室，并与MIT媒体实验室、斯坦福人工智能实验室、加州理工航天技术实验室等国际顶尖学府、研究机构展开合作，共同加速大数据、人工智能相关技术的探索和演进，并将国际前沿技术引入高速发展的中国市场，与国内丰富的应用场景相结合，驱动新技术的落地应用与行业的飞跃发展。'],
        '115698060': ['1-2万/月', '五险一金|补充医疗保险|通讯补贴|餐饮补贴|定期体检|地铁周边|不打卡|扁平化管理|领导NICE|免费零食|', '武汉-洪山区', '5-7年经验', '本科',
                      '招1人', '12-09发布', '测试经理', '北京腾赋网络科技有限公司',
                      '岗位职责：\n1.负责建立和维护一个有效的测试流程；\n2.负责测试团队的日常管理工作；\n3.负责制定和安排测试计划、测试工作；\n4.带领测试团队进行程序测试工作、按照制定的测试计划执行，并监督和控制测试工作的进程；\n5.负责测试用例的质量，开发高效的测试用例；\n6.负责与其他部门的人员沟通协作，例如与开发人员和项目管理人员进行沟通，共同推动项目的顺利进行；\n\n任职要求：\n1、计算机、通信等相关专业本科以上学历；\n2、有5年以上产品测试经验，具有独力安装使用自动测试与压力测试工具能力;具备良好的管理、组织和协调能力；\n3、熟悉主流的测试方法与理论，掌握主流的测试及管理工具；\n4、有3年以上，5人以上测试团队管理的工作经历；\n5、有电商行业或者零售行业工作经验者优先。\n职能类别：品质经理软件测试\n',
                      '上班地址：武汉市洪山区街道口理工大孵化楼 - B座17楼1701',
                      '公司福利：1）五险一金，人身意外险、补充医疗保险；2）午餐餐补、晚餐补贴、打车费报销、通讯补贴；3）办公区免费零食、水果、下午茶；4）法定节假日礼品；5）不定期组织培训、交流分享会，助力员工成长与发展；6）年度员工体检；7）不定期的组织团建或聚会；8）更多惊喜等你来发现~~用人准则：人品、责任心、学习能力！公司简介：新零售领域第三方独立服务商资深零售行业专家和互联网技术精英组成的创业团队致力于新零售领域实体零售商的各种创新业务突破各种壁垒进而高度融合从门到门、端到端O+O，形成闭环并真正为各方带来切实的价值成立两年已上线数千家实体门店（包括京客隆，欧尚，新华都，美特好，正大优鲜等多个知名企业客户）与美团外卖、饿了么、京东到家、百度外卖等互联网平台深度合作'],
        '100640736': ['1-1.5万/月', '五险一金|年终奖金|绩效奖金|', '武汉-江夏区', '无工作经验', '本科', '招若干人', '12-09发布', '自动化测试工程师',
                      '博彦科技股份有限公司',
                      '-熟练使用Java、python或者有较强的其他语言编程能力，有较强的代码运用能力；\n-良好的英语听说读写能力：英语读写熟练，口语流利者尤佳；\n-具有数据库使用经验；\n-可以独立编写测试计划，设计测试用例；\n-有自动化测试脚本开发及框架开发经验；\n-良好的交流沟通能力。能吃苦耐劳，应对复杂的工作需求。\n\n职能类别：软件测试软件工程师\n关键字：javapython自动化英语coding\n',
                      '上班地址：武汉市江夏区光谷大道金融港A9棟',
                      '博彦科技（深交所上市公司：002649）是亚洲领先的全方位IT咨询、服务及行业解决方案提供商。全球三大洲的六个国家设有超过30个分支机构和交付中心，具备全球范围的交付能力和灵活多样的交付方式。深厚的行业专长和成熟的行业实践，国际化的精英团队和完善的人才管理，完备的全球化交付和无缝的客户服务网络'],
        '111219215': ['1-1.5万/月', '周末双休|带薪年假|五险一金|绩效奖金|节日福利|年底双薪|福利体检|国内外旅游|新生代|福利补贴|', '武汉-江夏区', '5-7年经验', '本科', '招2人',
                      '12-09发布', '软件培训讲师+周末双休', '武汉正厚软件技术有限公司',
                      '1．根据教学计划完成教学任务，不断优化课程教学方法和教学课程体系安排；\n2．解决学员提出的一些技术性问题，组织并指导学生完成项目实战。\n3.完成开学之前的班级准备工作；\n4.负责学员日常工作的管理，包括学员考勤的统计，请假单的收集整理，学员情绪反馈等日常管理工作；\n5．配合其他部门的工作：招生、就业面试的技术支持；协助企业服务部进行部分职业素质课程的教学工作，就业推荐工作以及收集学员详细信息。\n\n岗位要求：\n1.熟悉软件开发测试流程，能编写测试计划、设计测试方案、测试用例，有至少8年以上测试工作经验；\n2.掌握C/C++或JAVA，掌握SQLServer、Oracle、Mysql中任意一种数据库，有开发经验者优先；\n3.掌握自动化或性能测试理论，熟练使用QTP、Selenium、LoadRunner、Jmeter之一种，有相关自动化测试工作经验者优先；\n4.熟悉Linux操作系统基本命令；熟练使用脚本语言：Python,Perl,Shell，Ruby等任意一种；\n5.良好的沟通能力，细心，耐心；思考问题思路清楚，口头表达能力强。\n职能类别：培训讲师职业技术教师\n关键字：软件测试讲师测试工程师IT培训讲师计算机培训讲师培训讲师软件测试\n',
                      '上班地址：光谷金融港',
                      '正厚软件是一家综合性的软件公司，主营软件产品研发、专业技能提升、人力资源整合、就业平台专供以及高校专业共建等。经过行业十五年的沉淀和成长，南京正厚软件技术有限公司（简称：正厚软件南京中心）于2017年正式运营，注册资金1000万，总公司坐落于南京鼓楼区湖南路16号，面积1000+平方。2018年，武汉正厚软件技术有限公司（简称：正厚软件武汉中心）开始正式投入运营。公司自运营以来一直秉持「正己守道」、「厚德载物」之旨，以客户实际业务需求为导向，为客户提供完善的信息化应用解决方案，在软件行业赢得了良好的口碑和影响力。'],
        '110603544': ['1-1.5万/月', '周末双休|带薪年假|五险一金|绩效奖金|节日福利|年底双薪|福利体检|国内外旅游|新生代|福利补贴|', '武汉-江夏区', '5-7年经验', '本科', '招2人',
                      '12-09发布', '测试讲师', '武汉正厚软件技术有限公司',
                      '岗位职责：\n1、根据教学计划完成教学任务，不断优化课程教学方法和教学课程体系安排；\n2、解决学员提出的一些技术性问题，组织并指导学生完成项目实战。\n3、完成开学之前的班级准备工作；\n4、负责学员日常工作的管理，包括学员考勤的统计，学员情绪反馈等日常管理工作；\n5、配合其他部门的工作：招生、就业面试的技术支持；\n任职要求：\n1、计算机相关专业，本科及以上学历，至少8年以上测试相关工作；\n2、熟悉软件测试流程，能编写测试计划、设计测试方案、测试用例；\n3、掌握C/C++或JAVA，掌握SQLServer、Oracle、Mysql中任意一种数据库，有开发经验者优先；\n3.掌握自动化或性能测试理论，熟练使用QTP、Selenium、LoadRunner、Jmeter之一种，有相关自动化测试工作经验者优先；\n4.熟悉Linux操作系统基本命令；熟练使用脚本语言：Python,Perl,Shell，Ruby等任意一种；\n5.良好的沟通能力，细心，耐心；思考问题思路清楚，口头表达能力强。\n职能类别：培训讲师职业技术教师\n关键字：软件测试讲师培训讲师职业技术讲师IT培训讲师\n',
                      '上班地址：光谷金融港',
                      '正厚软件是一家综合性的软件公司，主营软件产品研发、专业技能提升、人力资源整合、就业平台专供以及高校专业共建等。经过行业十五年的沉淀和成长，南京正厚软件技术有限公司（简称：正厚软件南京中心）于2017年正式运营，注册资金1000万，总公司坐落于南京鼓楼区湖南路16号，面积1000+平方。2018年，武汉正厚软件技术有限公司（简称：正厚软件武汉中心）开始正式投入运营。公司自运营以来一直秉持「正己守道」、「厚德载物」之旨，以客户实际业务需求为导向，为客户提供完善的信息化应用解决方案，在软件行业赢得了良好的口碑和影响力。'],
        '102356421': ['1-1.5万/月', '五险一金|年终奖金|带薪年假|餐饮补贴|弹性工作|交通补贴|绩效奖金|通讯补贴|', '武汉-江夏区', '2年经验', '本科', '招2人', '12-09发布',
                      '电力电子工程师', '武汉海亿新能源科技有限公司',
                      '岗位描述\n1、进行燃料电池系统用中大功率DC/DC变换器强弱电主回路的设计、元器件选型与调试；\n2、根据产品需要进行配套中小功率DC/AC逆变器的设计与开发；3、电路原理、PCB设计、调试；\n4、编写软件需求分析书及设计任务书，完成软件设计；\n5、模块功能调试、软件测试、运行维护及项目现场调试；\n6、项目文件资料编写和专利申报相应工作；\n7、撰写技术文档，指导、培训相关生产工艺环节，为其他部门提供技术支持；\n8、对产品需要的某项技术进行专项研究与开发。\n\n\n岗位要求\n1、熟悉多种拓扑结构的中大功率（≥10kW）DC/DC变换器与DC/AC逆变器主回路硬件电路设计、调试与开发；\n2、熟悉电力电子主电路系统参数计算、状态分析、主要部件优化选型及工程化设计；3、熟悉IGCT、IGBT、IPM、MOSFET模块设计；4、熟悉运用控制系统仿真软件至少一种；\n5、熟悉DSP的结构及编程，或精通FPGA/CPLD开发，熟悉VerilogHDL语言；\n6、具备以下项目之一经验者优先：电动汽车充电桩、燃料电池变换器、风力变流器、光伏逆变器、DC/DC、DC/AC、变频器开发等。\n职能类别：电力工程师/技术员电气工程师/技术员\n关键字：DC/DCDC/AC电力电子电力传动\n',
                      '上班地址：东湖新技术开发区关山大道598号',
                      '武汉海亿新能源科技有限公司创立于2017年，是一家致力于新能源氢燃料电池系统、燃料电池汽车整车动力系统技术平台和相关电力电子产品的研发和产业化的高科技初创企业。海亿新能由留美电子工程海归博士、长期从事燃料电池系统和汽车动力系统的著名大学教授和国内知名高新产业投资专家等联合创立。作为国内氢燃料电池车关键技术研发最早的一批探路人，海亿新能的核心技术团队自2001年以来先后承担了国家“863”计划中多个关于燃料电池汽车的重大专项课题，积累了深厚的实践经验，具有了成熟的技术储备，并取得了多项创新成果。当前团队拥有多项自主知识产权专利技术，形成了国内领先、国际先进的燃料电池系统及汽车动力系统的技术力量。公司现核心产品包括氢燃料电池发动机系统、氢燃料电池汽车动力系统总成技术平台、燃料电池升压变换器、燃料电池主控制器、燃料电池单片电压巡检仪等；并提供多类型氢燃料电池汽车的动力系统集成、动力系统优化控制、工程服务的完整解决方案。公司将围绕燃料电池系统及汽车动力系统坚持技术创新，打造核心技术链。联合产业链上下游各个关键节点，为我国新能源汽车发展作出卓越贡献，推动我国向全面资源节约型、环境友好型社会健康前进。注：我们的岗位非常适合期望在创业公司里有巨大成长空间的优秀人才。'],
        '114465453': ['1-1.5万/月', '五险一金|专业培训|绩效奖金|定期体检|员工旅游|做五休二|', '武汉-东湖新技术产业开发区', '3-4年经验', '本科', '招3人', '12-09发布',
                      '高级STM32嵌入式软件开发工程师', '武汉依迅电子信息技术有限公司',
                      '1、根据项目具体要求，承担软件开发任务，按计划完成任务目标；\n2、完成软件系统以及模块的测试方案、文档的编写，软件测试；\n3、参与公司TBOX、部标一体机、部标分体机等产品的调试，并对调试中出现的软件问题的进行实施、跟踪及汇总；\n\n任职要求：\n1、电子、通信、软件工程等相关专业，本科及以上学历，2年以上的工作经验；\n2、熟悉ARM微控制器架构，具备STM32微控制器的软件设计及开发经验；\n3、精通C语言嵌入式编程，熟悉FreeRTOS实时操作系统；\n4、熟悉KEIL开发环境，掌握altiumdesigner等软件查看原理图；\n5、有良好的英语阅读能力，能够快速阅读并准确理解各种英文技术文档；\n6、具有TBOX、车载导航、行车记录仪、车载监控、车载中控等产品相关开发经验者优先\n职能类别：电子软件开发(ARM/MCU...)\n关键字：STM32TBOX车载\n',
                      '上班地址：武大科技园航域二期A1栋2层',
                      '武汉依迅电子信息技术有限公司（简称：依迅电子）是一家多级国有基金参股专注于北斗卫星导航应用的军民融合高新技术企业集团。主要业务涵盖国防军工、智能交通、智慧城市、精准农业四大版块；在北斗高精度组合制导、北斗原子钟授时、视觉测距与识别等领域拥有国际领先的核心技术。在美国硅谷、中国光谷分别建有研发中心，与武汉大学、武汉理工大学等高校共建“教学科研实习基地”、“博士后流动工作站”，公司现为中国国防工业军民融合产业联盟副理事长单位，军工资质、生产资质齐全，在全国拥有100多家紧密型合作伙伴及多家分子公司，市场占有率连续多年居行业之前列，连续5年被行业协会评选为中国卫星导航产业“十佳产品供应商、十佳运营服务商”。\xa0\xa0\xa0公司位于中国光谷，现有员工平均年龄28岁，其中学士学位员工占到80%，技术研发员工占到60%以上。2007年公司与武汉大学、武汉理工大学等高校共建“教学科研实习基地”以及“博士后流动工作站”，构建出以产业为主导、企业为主体、技术为依托、产学研相结合、软硬件集成一体化的现代高科技企业体系。\xa0\xa0\xa0\xa0依迅电子坚持“政府推动，市场导向，科技支撑”的发展道路，不断提高自主创新能力，如今已拥有一支由该领域知名专家、教授及高工组成的研发队伍，并相继通过了ISO9001:2008质量管理体系认证、CCC产品认证、欧盟CE认证等国内外权威认证。\xa0\xa0\xa0依迅电子在全国拥有100多家紧密型合作伙伴，市场覆盖30多个省、直辖市，市场占有率连续3年居行业之前列。依迅以技术创新、应用创新带动导航与位置服务产业创新发展为着力点，积极探索市场机制，加速推进导航与位置服务产业的关键技术、核心部件和重大产品创新，公司具有自主知识产权的系列产品广泛销售于国内外，赢得了用户的一致好评，并获得了“2009年度行业创新奖”。公司的北斗系列产品、车载3G终端，特别是北斗及CDMA制式终端的市场占有率多年来一直保持行业领先地位。\xa0\xa0\xa0目前公司已拥有国家专利7项，软件著作权19项，公司承担国家创新基金支持项目1项，公司现为“武汉东湖高新技术企业” 、“中国全球定位系统及时应用协会会员单位” 、“双软认证企业” 、“国家地球空间信息产业基地会员单位” 、“国家创新基金扶持项目承担单位” 、“中国物流与采购联合会员单位”、“湖北省软件协会理事单位”“2011年、2012年和2013年中国十佳卫星导航产业供应商”、2013年武汉市东湖高新区“瞪羚企业”等。\xa0\xa0\xa0\xa0武汉依迅定位于“位置服务集成商及运营服务提供商”，秉承“自主创新、产业报国”的理想，依迅人以“推动我国导航与位置服务产业可持续发展”为己任。未来，武汉依迅将矢志成为位置产品及服务领域领先企业，在大力发展以自主卫星导航系统为基础的导航与位置服务产业的同时，为服务我国经济建设、社会发展和公共安全全面提升我国导航与位置服务产业核心竞争力不懈努力。公司提供：\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0五险一金；\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0周末双休；\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0法定节假日休息，带薪年假，春节额外5天以上带薪年假（春节假期12-15天）；\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0提供假日礼品、福利，员工生日福利，免费饮料（咖啡、奶茶、橙汁）和下午茶点，每年2次旅游等；\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0良好的职业发展空间。'],
        '113512376': ['1-2万/月', '包吃|包住宿|五险一金|补充公积金|交通补贴|餐饮补贴|绩效奖金|股票期权|', '武汉-洪山区', '无工作经验', '本科', '招5人', '12-07发布',
                      '测试开发工程师', '武汉蓝星科技股份有限公司',
                      '岗位描述：\n\n1、设计执行测试用例，保障产品品质；\n2、编写自动化测试脚本；\n3、开发测试工具，提高测试过程自动化程度。\n\n任职要求：\n1、软件工程、计算机科学与技术、机械、建筑、数学、应用数学及相关专业，本科学历及以上；\n2、熟悉软件测试的基本方法、流程和规范，可以独立完成测试分析和测试案例设计；\n3、熟悉常用软件测试工具,熟悉测试分析技术,有较强的逻辑分析能力和总结能力；\n4、能够服从工作安排，有上进心，乐于接受挑战；\n5、具备团队思维，与人友善；\n6、系统学习过任意一种程序语言(包含但不限于C\\C++\\C#)；\n7、具备实际设计、编程、测试工作经验优先\n职能类别：软件测试\n',
                      '上班地址：东二产业园黄龙山东路',
                      '武汉蓝星科技股份有限公司是2002年经湖北省人民政府批准成立的股份制企业，注册资本金13369万元。公司专注于LINUX嵌入式操作系统、图形软件系统等基础软件研发，在嵌入式操作系统、操作系统开发工具、系统平台等领域拥有完整自主知识产权，技术成果主要面向嵌入式市场，可广泛应用于医疗医美、航天军工、智能制造、AI智能、消费电子、电教设备、车辆信息化、智慧农业等行业领域，是领域内知名高新技术企业。\xa0\xa0\xa0全球LINUX基金会银牌会员\xa0\xa0\xa0开源车载系统平台联盟AGL银牌成员\xa0\xa0\xa0与华中科技大学建立联合实验室《嵌入式图形图像及计算机视觉联合实验室》\xa0\xa0\xa0《GB/T 26775-2011 车载音视频系统通用技术条件》国家标准起草单位\xa0\xa0\xa0《车载无线通信设备通用技术条件》行业/国标主任起草单位\xa0\xa0\xa0\xa0湖北省省级企业技术中心。。。。。。。。公司立足自主创新，研发人员占总人数70%。研发中心下辖可视图形计算事业群、OS 事业群、终端设计事业群和技术支持事业群等四个事业群。公司拥有深厚的技术积累，产业方向符合国家战略规划，正处于高速上升期，欢迎您的加入，共创美好明天'],
        '115604874': ['1-1.2万/月', '五险一金|免费班车|员工旅游|餐饮补贴|通讯补贴|专业培训|绩效奖金|年终奖金|出国机会|', '武汉-东湖新技术产业开发区', '3-4年经验', '大专',
                      '招1人', '12-06发布', '射频测试工程师（WH）', '深圳市卓翼科技股份有限公司',
                      '岗位要求：\n1、电子技术、通信工程、计算机、射频/微波相关专业毕业，大专及以上学历\n2、5年以无线宽带与家庭终端产品（CPE/E5/无线路由器/XDSL终端/XPON终端）射频测试相关工作经验\n3、能独立输出产品的射频测试策略与计划、测试用例、测试报告\n4、熟悉allegro/powerpcb,orcad相关EDA软件的使用\n5、熟悉WiFiIEEE802.11a/b/g/n/ac，EN300328，FCCPart15C相关无线指标测试标准与测试方法（基础要求）；\n6、熟悉手机产品2/3/4G等相关无线指标测试标准与测试方法（加分项）；\n7、熟悉蓝牙BDR,EDR,BLE测试标准与测试方法\n8、熟悉天线指标测试，S参数测试，OTA测试方法\n9、熟悉手机综测仪、Litepoint/R&S射频测试仪、Agilent信号分析仪、频谱仪、网络分析仪、信号源、无线功率计等相关测试仪器的使用\n\n岗位职责：\n1、负责网通产品（无线路由器/XDSL终端/XPON终端/CPE）的WIFI射频指标、性能、天线指标测试工作，根据产品需求规格、产品质量目标制定相应的射频测试策略、测试计划、测试用例\n2、根据产品的测试计划、测试用例及相应的测试规范执行测试，测试内容包括但不限于射频发送指标、射频接收指标、天线无源指标、天线有源指标、OTA性能、产品整机WIFI覆盖性能、DFMA测试、器件一致性测试等，测试完成后提交规范的测试报告\n3、对在测试的过程中发现的的问题提交信息完整、描述清晰的缺限报告或问题单，并能提供初步的缺限修改建议，协助及跟踪开发工程师最终解决问题；\n4、参加原理图、PCBLayout评审，测试可行性评审，测试策略、测试报告、测试用例等评审。\n职能类别：硬件测试软件测试\n关键字：CPEE5路由射频测试\n',
                      '上班地址：光谷未来科技城',
                      '深圳市卓翼科技股份有限公司（以下简称“卓翼科技”）创始于2004年，2010年3月在深交所挂牌上市（证券简称：卓翼科技，证券代码：002369）。卓翼科技专业从事通讯、计算机、消费类电子等3C产品的研发、制造与销售。在移动终端、网络通信、智能家居、可穿戴、自动化及消费产品领域，卓翼科技向全球客户提供设计、开发、生产、技术支持等优质服务。凭借强大的技术优势、开拓进取的专业态度和尽善尽美的服务精神，卓翼科技一直处于市场领先地位，与全球诸多顶尖客户精诚合作，共创未来。\xa0\xa0\xa0卓翼科技在全球拥有约10000名员工，在深圳、厦门、西安设有研发中心，在深圳、天津设有两个高度自动化的生产基地。依托自身研发、制造能力，卓翼科技可提供优秀的产品设计、完善的供应链管理以及专业的柔性智能制造，帮助客户把产品更快地投入市场，提高其成本效率。2015年起，卓翼科技在美国硅谷设立技术服务公司，重点扶持跟卓翼科技产业方向吻合的创新公司，助力全球智能硬件创新。作为全球领先的产品和服务解决方案提供商，卓翼科技坚持加大前沿技术驱动的创新投入，不断优化产品结构，逐步扩大生产自动化的应用，从规模驱动转变为效率驱动的行业领先企业。\xa0\xa0\xa0卓翼科技通过ISO9001标准化质量管理体系、ISO14001环境管理体系、OHSAS18001职业健康安全管理体系以及SA8000-2008社会责任管理体系的认证。卓翼科技相继获得深圳市工业500强、南山区民营领军企业、南山区纳税百强企业、中小企业诚信榜AAA上榜企业等各项荣誉。取得国家高新技术企业、深圳市市级研究开发中心等资质。\xa0\xa0\xa0面对滚滚而来的万物互联浪潮，卓翼科技将一如既往地肩负科技使命，心怀梦想，憧憬未来。努力抓住物联网时代提供的慷慨成长机遇，构筑产品、制造、创业加速为一体的综合服务平台；力争成为中国智能制造的标杆和创新创业合作的理想平台，成为一流的科技服务型企业。'],
        '118192225': ['1-1.8万/月', '五险一金|补充医疗保险|通讯补贴|餐饮补贴|包住|绩效奖金|年终奖金|牛人团队|股票期权|', '武汉-洪山区', '3-4年经验', '本科', '招1人',
                      '12-05发布', '测试主管（自动化测试）', '鄂尔多斯市煤易宝网络科技有限公司',
                      '薪资福利：月薪10K—18K+五险一金+周末双休+年度旅游+年度体检+带薪年假+节日福利+年终奖+全员持股\n\n加入我们，您将获得：\n1、雄厚的资金保障：煤易宝有自己的煤矿资源，款项现结模式，伊泰、汇能等煤矿龙头企业背书，保证了公司有稳定的资金链；\n2、有竞争力的薪酬福利：全员持股！入职越早，越优先分配！还享受五险一金、年度体检、年度旅游、出差补助、节日福利、年终奖等各种福利；\n3、完善的休假：周末双休、国家法定节假日、婚假、产假、陪产假、带薪年假；\n4、丰富的团建活动：聚餐、K歌、兴趣俱乐部、户外拓展、旅游……应有尽有；\n5、以人为本：弹性作息、尊重员工个性发展；\n6、牛人团队：京东、高德、顺丰、良品铺子、明源云、斑马快跑、陕煤、伊泰、大同煤矿……煤易宝已吸纳大量知名互联网和煤矿企业人才，牛人带你飞！\n7、发展空间：公司刚完成工商注册就有3000万投资到账，还有超3亿的投资意向正在洽谈，计划2023年在港股或创业板上市！\n\n岗位职责:\n1、参与项目需求、产品定义、研发计划的评审\n2、负责公司软件产品的测试\n3、编写测试计划、测试方案、测试用例、提交测试报告，满足产品和业务需求\n4、对测试中发现的问题进行详细分析和准确定位，协助研发人员定位或复现问题，从测试角度提出优化意见\n5、确保软件质量达标，对软件质量负责\n\n任职资格:\n1、统招本科及以上学历，计算机相关专业，4年以上软件产品测试经验，1年以上自动化测试经验及测试小组管理经验\n2、熟悉移动端抓包工具charles,性能测试工具例如JMeter\n3、熟悉自动化测试框架,会ruby或python脚本编程\n4、熟悉问题管理工具（如Jira,禅道）\n5、了解至少一种常见自动化测试工具及其原理，比如QTP、Selenium、Watir、VSTest等\n6、具备良好的语言表达、沟通和团队协作能力，必须具备严谨、负责的态度，精益求精，确保产品质量\n\n煤易宝对优秀人才的定义是：\n#专业、职业、靠谱\n#高效、协作、诚信\n#使命必达、自我驱动\n#持续学习、拥抱变化\n#初心不改、仍怀梦想\n如果你有无处安放的才能和智慧想尽情发挥，我们为你提供施展才华的舞台！\n职能类别：软件测试系统测试\n关键字：测试主管自动化测试PythonJmeterSeleniumQTP\n',
                      '上班地址：虎泉街五环天地1号楼（杨家湾地铁站D出口前行200米）1901—1904室',
                      '鄂尔多斯市煤易宝网络科技有限公司，成立于2018年，注册资金1000万元，是武汉物易云通网络科技有限公司（司机宝）和煤问题（内蒙古）电子商务有限责任公司的合资控股企业。\xa0\xa0\xa0\xa0公司旗下的煤易宝供应链管理平台是集交易、物流、供应链金融服务为一体的产业互联网平台，专注于煤炭领域，为企业客户提供一票到站的供应链综合服务。目前公司的主营业务有：一票到站、无车承运、代客叫车、坑口代发。我们提供煤炭行业采、运、销各环节一站式服务，保障货物高效送达。\xa0\xa0\xa0\xa0公司拥有强大的软硬件自主研发能力，研发团队位于武汉光谷高新科技产业园，拥有来自于美团、京东、高德、顺丰、平安科技、海航、斗鱼、唯品会、明源云、良品铺子等知名企业的技术人员，涵盖了物流、金融、供应链、大数据等技术背景。\xa0\xa0\xa0\xa0煤易宝运营团队在煤炭领域深耕多年，对行业有着深刻的理解，通过专业的操作流程和规范保障服务质量。愿景：成为中国市场上专业的精益煤炭供应链管理平台使命：通过互联网+科技的手段提升煤炭供应链效能价值观：精进 专业 创新 共赢加入我们，您将获得：1、财富：\xa0\xa0\xa0只要你有能力、有渴望，除了岗位工资、各项补贴、绩效奖金、五险一金、节日福利、评优奖金、年终奖等基本的薪酬福利，成为持股员工享受分红权、投票权、处置权，是我们敢于给你的认可和信任2、团队：\xa0\xa0\xa0—董事长拥有银行和美团、航班管家、司机宝创始人等丰富的背景，战略眼光毒辣，超强大脑、有趣的灵魂就是这样有魅力！\xa0\xa0\xa0—总经理具备丰富的销售实战经验，拉起乐队去北漂那都不在话下，如果你干练又聪明，你们是一路人！\xa0\xa0\xa0—销售副总俗称“煤炭活地图”，在煤炭行业深耕多年，想在煤炭行业忽悠到他，还真得有两把刷子！\xa0\xa0\xa0—首席财务官，请自行百度“姬志福”，伊泰集团传奇人物，最年轻的高管！\xa0\xa0\xa0—产品研发核心人员，来自高德、顺丰、京东、美团、明源云、斗鱼、唯品会、海航科技、平安科技、良品铺子等知名互联网企业，不用我们吹，做出来的产品，那就是硬实力！3、事业：我们正在踏踏实实做的这件事——打造煤炭供应链管理平台，注定成为中国产业互联网进程上辉煌的篇章。4、人才培养发展通道：从上到下全力发掘优秀人才，专业序列和管理序列双通道晋升；煤易宝大学开设“新人训练营”、通用素质能力、专业知识技能、领导力、管理知识和技能等培训，全面提升人才综合能力'],
        '118887378': ['1.2-2万/月', '', '武汉-洪山区', '无工作经验', '本科', '招50人', '12-02发布', '校招-测试开发工程师（深圳研究所） (职位编号：MJ000173)',
                      '深信服科技股份有限公司',
                      '本科年薪19万+，硕士22万+\n岗位描述：\n负责深信服集团母公司旗下虚拟化、云计算、安全、企业级移动应用产品的软件测试和质量建设工作；\n在这里，您可以深度参与到工程生产力团队里面，开发平台和工具，让测试工作更轻松，让研发过程更高效；您可以审查代码，发现深层次的逻辑问题，指导白盒测试，帮助软件开发过程持续集成；在这里您可以成为测试开发专家，工具开发专家，自动化测试高手，测试架构师，有胆你就来！\n岗位要求：\n1、本科及以上学历，专业不限；\n2、熟悉使用并掌握C/C++/Python/Shell中的一门或多门语言，有较强的开发能力和较多的项目开发经验；\n3、喜欢钻研技术，有广泛的技术视野，具备很强的学习能力和解决问题的能力。\n职能类别：软件测试\n',
                      '上班地址：南山区学苑大道1001号南山智园A1栋',
                      '一、公司简介\xa0\xa0\xa0\xa0深信服科技股份有限公司是专注于云计算／虚拟化、网络安全领域的IT解决方案服务商，致力于提供创新的IT基础设施云计算、网络安全建设解决方案，现深信服已成长为国内网络安全龙头，云计算业务成长为国内增速最快的厂商，私有云领域市占率前三。研发实力：公司目前拥有近5000多名员工，其中研发近2000人，每年销售收入的20%投入到研发，在全球已设立深圳、北京、硅谷3大研发中心，专注云计算、网络安全领域，交付的产品包含私有云、公有云、超融合、网络安全等解决方案。\xa0\xa0\xa0\xa0市场实力：公司连续15年保持高速增长，年均增长率近50%，近10年的营收增长超过300倍。目前，深信服在全球共设有55个直属分支机构，其中含国内地主要城市及美国、英国、中国香港、马来西亚、泰国、印尼、新加坡等国家和地区。公司云计算和网络安全产品正在被 24个国家部委、中国区域80%以上的世界500强、90%的省级以上运营商、TOP20银行等 40，000家用户使用。部份荣誉：连续两届被美国《财富》杂志评为“中国卓越雇主”；国内网络安全领域龙头国内私有云领域前三入围全球顶尖网络安全厂商，国内仅6家；入围全球网络安全创新500强，国内仅6家；连续6年获评德勤“中国高科技高成长50强”；连续9年获评德勤“亚太地区高科技高成长500强”；***批国家高新技术企业；国家火炬计划项目单位（国家科技部批准）；中央政府采购协议供货商中国国家信息安全漏洞库CNNVD技术支撑单位；中国反网络病毒联盟ANVA成员单位；连续五年被评为“国家规划布局内重点软件企业；”'],
        '118356639': ['', '', '武汉-洪山区', '3-4年经验', '本科', '招若干人', '11-21发布', '电控功能安全工程师', '东风汽车集团有限公司技术中心',
                      '职责概述：\n1、负责整车级功能安全需求分解\n2、承担分系统功能安全需求制定\n3、承担VCU、EMS功能安全软件方案制定\n4、负责VCU、EMS功能安全的软件设计与开发\n5、负责VCU、EMS功能安全的软件测试\n\n学历、职称：全日制本科或以上学历\n外语要求：具备良好的英语听说读写能力\n工作经历：相关专业5年以上\n专业背景：电子类、电气类、计算机类、通信类等相关专业\n\n素质要求\n1、熟悉ISO26262标准\n2、熟悉汽车理论相关知识\n3、熟悉整车功能安全的开发流程\n4、掌握FMEA或者FTA分析方法\n5、具备功能安全开发的相关经验\n6、熟练使用功能安全相关的工具\n\n职能类别：汽车电子工程师电气/电器工程师\n',
                      '上班地址：湖北省武汉市经济技术开发区珠山湖大道663号',
                      '东风汽车集团有限公司技术中心（“东风汽车公司技术中心”）于1983年4月成立，是东风公司的产品开发中心、技术研究中心、技术管理中心，是国家发改委、财政部、税务总局和海关总署认定的国家 级"企业技术中心"，是国家科技部认定的国家一类科研院所，也是国内汽车行业首批国家 级"海外高层次人才创新创业基地"。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0技术中心主要承担东风自主品牌乘用车、军用越野车、新能源汽车、动力总成以及基础和先行技术研究等工作。截至目前，东风汽车公司技术中心共有各类技术人员2800余人，其中硕士研究生及以上学历1023人，高级工程师以上职称人员610人，海外高层次人才近30人，享受国务院政府特殊津贴专家14人，入选国家“千人计划”9人。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0技术中心始终坚持“改进一代、开发一代、预研一代”的产品开发方针，多次荣获国家科技进步奖和东风公司科技进步特等奖，为东风公司和中国汽车工业发展做出了重大贡献。2011年东风公司发布了“乾”D300计划，东风自主品牌汽车销量将达到300万辆，技术中心作为东风自主品牌乘用车产品研发的引领者，在集团“大自主、大协同、大发展”的战略框架下，被赋予了更重大的使命。技术中心将以加速提升乘用车、新能源汽车、动力总成和汽车电子技术研发能力，保持混合动力汽车和高机动越野车开发方面领先优势，促进技术研究、产品开发在国内处于领先地位为整体目标，为东风自主品牌事业发展提供强大的支撑。'],
        '118356607': ['', '', '武汉-洪山区', '无工作经验', '本科', '招若干人', '11-21发布', '电控系统基础软件工程师', '东风汽车集团有限公司技术中心',
                      '职责概述：\n根据软件开发流程进行基础软件架构设计、编码、仿真测试和代码集成，进行软件功能验证和可靠性设计，代码评审，工作内容如下：\n1、负责电控系统基础软件开发工作，包含MCU底层驱动、OSEK网络管理、诊断协议栈、标定协议栈等底层基础软件开发；\n2、负责符合AUTOSAR标准的基础软件开发，使用AUTOSAR工具软件配置基础软件相关功能模块；\n3、负责基础软件测试工作；\n4、负责基础软件相关文档编写工作；\n5、负责基础软件维护及升级工作。\n\n学历、职称：全日制本科或以上学历\n外语要求：具备良好的英语听说读写能力\n工作经历：相关专业3年以上\n专业背景：电子类、电气类、计算机类、通信类等相关专业\n\n素质要求：\n1、三年以上汽车电子软件开发工作经验，熟悉嵌入式软件、MCAL开发；\n2、具有EMS/VCU控制器开发经验优先；\n3、精通C语言，有扎实的编程功底，掌握单片机系统开发知识，具有一定的软件架构，系统调度，底层驱动，诊断开发能力；\n4、熟悉bootloader开发，Flash驱动，CAN驱动，I2C/SPI驱动；\n5、熟悉python语言优先。\n\n职能类别：其他\n',
                      '上班地址：湖北省武汉市经济技术开发区珠山湖大道663号',
                      '东风汽车集团有限公司技术中心（“东风汽车公司技术中心”）于1983年4月成立，是东风公司的产品开发中心、技术研究中心、技术管理中心，是国家发改委、财政部、税务总局和海关总署认定的国家 级"企业技术中心"，是国家科技部认定的国家一类科研院所，也是国内汽车行业首批国家 级"海外高层次人才创新创业基地"。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0技术中心主要承担东风自主品牌乘用车、军用越野车、新能源汽车、动力总成以及基础和先行技术研究等工作。截至目前，东风汽车公司技术中心共有各类技术人员2800余人，其中硕士研究生及以上学历1023人，高级工程师以上职称人员610人，海外高层次人才近30人，享受国务院政府特殊津贴专家14人，入选国家“千人计划”9人。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0技术中心始终坚持“改进一代、开发一代、预研一代”的产品开发方针，多次荣获国家科技进步奖和东风公司科技进步特等奖，为东风公司和中国汽车工业发展做出了重大贡献。2011年东风公司发布了“乾”D300计划，东风自主品牌汽车销量将达到300万辆，技术中心作为东风自主品牌乘用车产品研发的引领者，在集团“大自主、大协同、大发展”的战略框架下，被赋予了更重大的使命。技术中心将以加速提升乘用车、新能源汽车、动力总成和汽车电子技术研发能力，保持混合动力汽车和高机动越野车开发方面领先优势，促进技术研究、产品开发在国内处于领先地位为整体目标，为东风自主品牌事业发展提供强大的支撑。'],
        '118356510': ['', '', '武汉-洪山区', '3-4年经验', '本科', '招若干人', '11-21发布', '电控系统测试工程师', '东风汽车集团有限公司技术中心',
                      '岗位职责：\n根据开发流程，进行电控系统的代码测试、台架测试、HIL测试、实车测试，进行软件功能测试和可靠性验证，工作内容如下：\n1、负责电控系统软件静态代码测试；\n2、电控系统的HIL测试；\n3、负责电控系统测试计划编制、测试用例设计、测试结果分析与报告编写；\n4、负责电控系统实车测试（功能/性能/故障）计划与测试用例，测试结果分析与报告编写；\n5、针对测试过程问题缺陷进行分析和反馈，协助开发工程师完成改善验证；\n\n学历、职称：全日制本科或以上学历\n外语要求：具备良好的英语听说读写能力\n工作经历：相关专业2年以上\n专业背景：汽车类、电子类、自动化类、计算机类、通信类等相关专业\n\n素质要求：\n\n1、二年以上汽车电子软件测试经历，熟悉C语言,具备基本硬件电路知识；\n2、熟悉电控系统原理、HIL测试理论及测试方法\n3、熟悉CANoe、ValueCAN等CAN调试工具的使用；\n4、熟悉CCP/XCP协议、ISO15765、ISO14229协议优先；\n5、熟悉python语言优先。\n\n职能类别：汽车设计工程师\n',
                      '上班地址：湖北省武汉市经济技术开发区珠山湖大道663号',
                      '东风汽车集团有限公司技术中心（“东风汽车公司技术中心”）于1983年4月成立，是东风公司的产品开发中心、技术研究中心、技术管理中心，是国家发改委、财政部、税务总局和海关总署认定的国家 级"企业技术中心"，是国家科技部认定的国家一类科研院所，也是国内汽车行业首批国家 级"海外高层次人才创新创业基地"。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0技术中心主要承担东风自主品牌乘用车、军用越野车、新能源汽车、动力总成以及基础和先行技术研究等工作。截至目前，东风汽车公司技术中心共有各类技术人员2800余人，其中硕士研究生及以上学历1023人，高级工程师以上职称人员610人，海外高层次人才近30人，享受国务院政府特殊津贴专家14人，入选国家“千人计划”9人。\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0技术中心始终坚持“改进一代、开发一代、预研一代”的产品开发方针，多次荣获国家科技进步奖和东风公司科技进步特等奖，为东风公司和中国汽车工业发展做出了重大贡献。2011年东风公司发布了“乾”D300计划，东风自主品牌汽车销量将达到300万辆，技术中心作为东风自主品牌乘用车产品研发的引领者，在集团“大自主、大协同、大发展”的战略框架下，被赋予了更重大的使命。技术中心将以加速提升乘用车、新能源汽车、动力总成和汽车电子技术研发能力，保持混合动力汽车和高机动越野车开发方面领先优势，促进技术研究、产品开发在国内处于领先地位为整体目标，为东风自主品牌事业发展提供强大的支撑。'],
        '106619895': ['1-1.3万/月', '五险一金|年终奖金|弹性工作|免费班车|专业培训|', '武汉-江夏区', '5-7年经验', '大专', '招2人', '11-20发布', '高级测试工程师',
                      '维书信息科技（上海）有限公司',
                      '职位描述：\n1）根据项目需求文档和设计文档，对软件测试项目进行测试设计，编写测试方案；\n2）独立实施软件测试项目，独立编写测试计划、测试用例和测试报告；\n3）及时准确地对项目缺陷进行上报，并与开发人员等相关人员进行有效沟通，保证项目进度和质量；\n4）希望能够根据对项目需求的理解，提出功能测试之外的建议，如用户体验等方面；\n\n\n任职要求：\n1）专科科以上学历，计算机相关专业毕业优先；\n2）5年左右软件测试经验；\n3）熟悉软件工程、软件测试流程和规范，精通常用测试方法和手段，熟悉常用的测试工具；\n4）熟悉性能测试、接口测试、Web端测试以及自动化软件测试；\n5）具有良好的沟通能力和团队合作能力；\n6）工作认真负责、积极主动，吃苦耐劳；\n7）具备良好的自学能力，对新技术、新方法充满兴趣；\n\n职能类别：软件工程师项目主管\n关键字：性能功能接口压力\n',
                      '上班地址：通用大道',
                      '维书信息科技（上海）有限公司维书信息科技（上海）有限公司是一家从事软件服务的高新技术企业，为制造业客户提供智能物流、智能工厂、物联网及大数据的解决方案。公司主要业务涉及供应链管理、物流可视化、终端客户及设备管理等方面。互联网的未来发展方向在大数据和物联网。目前，越来越多的传统企业意识到互联网化的重要性，期望通过大数据分析、智能物联等手段，进一步优化传统企业的产品研发、生产、物流及销售等各个环节，降低成本，提高企业的竞争力。维书信息致力于大数据及物联网，为传统的制造业客户提供智能物流、智能工厂、物联网及大数据的解决方案。维书信息一直本着以“注重人才、以人为本”的用人宗旨，力争为员工提供一个具有竞争力的薪酬和广阔的发展空间，让员工与公司共同成长。为实现我们共同的事业和梦想，我们渴望更多志同道合的朋友加入！在这里，您将拥有的不仅仅是良好的工作环境，更是置身于广阔的发展空间之中，在事业的舞台上挥洒我们青春和才智！如果您对未来充满梦想，对成功也充满渴望，那么请让我们携手同行，真诚合作，实现梦想，共创未来！'],
        '116139231': ['1-1.5万/月', '', '武汉-东湖新技术产业开发区', '2年经验', '本科', '招1人', '11-12发布', '云计算测试工程师', '杭州海康威视数字技术股份有限公司',
                      '职能类别：软件测试\n', '上班地址：光谷软件园F4',
                      '【公司介绍】海康威视是以视频为核心的智能物联网解决方案和大数据服务提供商。2011-2017全球视频监控市占率第1（IHS）2016-2018“全球安防50强”第1位（a&s《安全自动化》）2017-2018 年Brand Finance“全球科技品牌百强榜”2018年中国软件业务收入百强第6位，2018中国大数据企业50强央视财经论坛暨中国上市公司峰会 “2016&2018 CTV中国十佳上市公司”\xa0【公司实力】人员规模：34000+员工，？16000+研发和技术服务人员（截止2018年底）产业布局：主营业务版块包括大数据服务、行业智慧应用解决方案、综合安防解决方案、安防全系列产品；创新业务覆盖互联网业务\\机器人业务\\汽车电子\\智慧存储、海康微影、慧影科技等其他拓展业务。研发实力：1所研究院、国内8大研发基地，海外2大研发中心，2809项已授权专利、881软件著作权、参与制定标准298项、多项全球竞赛大奖营销网络：32家国内省级业务中心/一级分公司及44家境外分支机构，产品和解决方案覆盖全球150多个国家及地区。【薪酬福利】海康威视倡导凭借价值贡献获取回报，并为员工提供有竞争力的薪酬、完善的福利保障、全球工作机会、明晰完善的职业发展和培训体系。假期：带薪年假、全薪病假、母婴照顾假、婚假等；外派：国内与海外有住房、生活、艰苦区域补贴，补充商业险，探亲福利及高额奖励；补贴：交通补贴/总部免费停车场、补充商业险、通讯补贴、过节福利、现金医疗补贴、荣誉奖励、工会福利、免费手机、杭州市人才引进津贴等；乐活：餐饮补贴、免费早餐、免费零食、生日蛋糕、总部园区生态圈（食堂、便利店、健身中心等）、年度体检、弹性工作制、医务室等；安居：人才落户政策。【加入我们】请关注海康威视招聘官网了解更多公司及岗位信息http://talent.hikvision.com/'],
        '117259291': ['1-2万/月', '五险一金|员工旅游|通讯补贴|餐饮补贴|定期体检|年终奖金|', '武汉-洪山区', '无工作经验', '本科', '招若干人', '11-11发布',
                      '测试开发工程师（武汉）(J10455)', '深圳市汇顶科技股份有限公司',
                      '工作职责:\n1.负责搭建和改进公司的自动化测试平台，提高产品自动化测试的覆盖度\n2.负责新产品测试需求梳理、测试方案设计、测试计划制定、执行\n3.负责测试工具或脚本的开发\n4.研究探索前沿测试技术，对团队成员进行技术分享\n任职资格:\n1.电子信息、计算机、通信等相关专业本科及以上学历\n2.两年以上测试平台开发或者测脚本开发经验，有NFC/RFID、金融卡产品开发经验优先\n3.熟练掌握C/C++、Java、Python中的至少一种编程语言\n4.有强烈的责任心和主动性，热爱挑战和学习，具有良好的沟通能力和团队意识\n\n职能类别：软件工程师高级软件工程师\n',
                      '上班地址：中部创意城',
                      '汇顶科技成立于2002年，经过持续的努力和技术积累，目前已经成为全球领先的人机交互技术与解决方案提供商。以“创新技术，丰富生活”为愿景，专注基于客户需求的创新。汇顶科技在包括手机、平板电脑和可穿戴产品在内的智能移动终端人机交互技术领域构筑了领先的优势。目前，产品和解决方案广泛应用在华为、联想、OPPO、vivo、中兴、酷派、魅族、乐视、HTC、金立、TCL、三星显示、JDI、诺基亚、东芝、松下、宏碁、华硕、戴尔等国际国内知名终端品牌，服务全球数亿人群。\xa0\xa0\xa0\xa0作为***高新技术企业和触控与指纹识别的全球领导品牌，汇顶科技重视核心技术的持续研发积累，坚信满足并超越客户需求是所有技术开发的源动力，陆续推出了拥有自主知识产权的多项全球领先技术，包括单层多点触控技术、Goodix-Link、IFSTM指纹识别与触控一体化技术等。这些先进的技术正通过性能卓越的芯片产品、完善的整体解决方案以及周到快捷的技术服务给各品牌整机终端注入勃勃生机。\xa0\xa0\xa0\xa0作为管理规范的股份有限公司，汇顶科技深刻理解客户的成功来源于创新的技术和卓越的产品，而这些均凝结着员工的汗水与智慧。汇顶科技致力于给员工提供施展才华的空间和舞台，促进员工能力的持续发展，帮助员工获得事业的成就，并通过员工持股的方式与员工共享发展成果。\xa0\xa0\xa0\xa0作为中国本土的高科技企业，汇顶科技积极承载可持续发展的社会责任。持续努力推动中国移动互联网产业技术前进，促进人机交互技术的革新，驱动中国制造转型为中国创造，助力中国创新型科技社会的进步。公司愿景：创新技术 丰富生活（Vision：Enrich Your Life through Innovation）公司使命：成为受人尊敬的世界一流的创新科技公司（Mission：To be respected world-leading innovative corporation）管理理念：以人为本，视员工为事业伙伴遵循科学，追求理性核心价值观：用心、团队、绩效、 创新企业荣誉：国家高新技术企业深圳市高新技术企业通过国际标准化协会ISO9001-2000质量体系认证\xa0薪酬待遇：\xa0\xa0\xa0正值公司高速成长之际，公司求贤若渴，高薪诚聘专业人才。一经录用，将提供具有行业竞争力的薪酬，并给予核心骨干人才诱人的股权激励。企业福利：1、五天7.5小时工作制：上午9:00-12:30，下午14:00-18：002、购买五险一金，解除您的后顾之忧 !3、额外购买人身意外保险，增加双重人身保障！4、提供中餐、晚餐以及点心，让您乐享工作！5、每年提供员工高额的、全面的健康体检，让您得到工作与健康平衡！6、缤彩纷呈的员工活动：年度旅游、户外拓展、社团活动、部门聚会活动、年度晚会等等，让您感受团队的温暖与力量！7、法定节假日之外的带薪假期：带薪年假。8、提供多元化的培训与在职进修机会，不断提升您的软硬实力！9、神秘的生日礼物、贴心的节日礼品、浪漫的结婚大礼包，给您惊喜连连！公司网址：www.goodix.com    简历投递：zhaopin@goodix.com公司总部地址：深圳市福田保税区腾飞工业大厦B座13层\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0海到无边天做岸，山登绝顶我为峰。汇顶正与合作伙伴一起，以澎湃的激情和无限的创造力投入到移动互联网迅猛发展的浪潮中，征服下一座高峰。'],
        '116780939': ['', '', '武汉-洪山区', '无工作经验', '本科', '招若干人', '11-11发布', '通信网优IT开发-技术类（武汉） (职位编号：00xz)', '移动设计院湖北分公司',
                      '专业要求：\n计算机、电子类相关专业\n工作内容：\n1、针对移动通信网络需求，组织开发相应的应用平台。2、根据开发规范和流程完成系统设计，编码，测试及相关文档的编写；协助测试人员完成软件及模块的测试工作3、协调组织各类资源，推进数据产品研发和迭代进度，保障产品交付和运行，推动产品的测试及发布，对产品进行测试并验收；4、负责研究数据应用平台和产品的先进业务流程、技术，为数据产品设计演进规划提供建设性参考。\n任职资格：\n1、了解移动通信和计算机网络专业领域最新技术，熟悉计算机网络组网及协议。2.熟练使用Java，熟悉Spring开发框架,对高并发、分布式、大数据处理有一定的认识与了解。3.熟悉MySql数据库，熟悉tomcat等HTTPServer。4、熟悉软件测试流程和测试方法，具备测试报告编写能力。5、具有可演示的开发案例优先6、有良好的学习能力、积极的攻关意识和高度的责任感。\n职能类别：通信技术工程师\n',
                      '职能类别：通信技术工程师', '移动设计院湖北分公司诚聘'],
        '118207652': ['1.4-2万/月', '五险一金|交通补贴|餐饮补贴|通讯补贴|专业培训|绩效奖金|股票期权|弹性工作|节日福利|体检|', '武汉-东湖新技术产业开发区', '无工作经验', '本科',
                      '招若干人', '10-31发布', '测试开发工程师(J10655)', '绿盟科技',
                      '工作职责:\n1.负责大数据平台的测试工作。\n2.根据软件需求，编写测试方案、计划和测试用例文档。\n3.跟进缺陷的修改，编写测试分析报告。\n4.性能、可靠性等专项测试的设计和执行。\n5.自动化脚本编写和测试\n任职资格:\n1.计算机相关专业，1~3年以上测试经验。有大数据平台测试、安全产品测试、网络设备测试经验者优先。\n2.熟悉项目开发过程、熟悉软件测试方法、熟悉用例设计方法、熟悉常用测试工具。\n3.熟悉Linux操作系统、数据库，能在linux中搭建产品测试环境、进行功能、性能、稳定性等测试。\n4.熟悉各种常见网络协议（TCP、HTTP、DNS等）、网络设备应用\n\n职能类别：软件工程师\n',
                      '上班地址：光谷软件园A9座',
                      '一、公司介绍绿盟科技（nsfocus），成立于2000年4月，公司专注于网络安全的行业，面向全球提供基于自身核心竞争力的企业级网络安全解决方案。\xa0\xa0现有员工1600多人，在全国主要省会城市设有7个分公司、31个办事处和联络处，另在日本和美国建有子公司。自2000年成立，基于我们领先的安全漏洞研究实力、强大的产品研发和创新能力，我们始终保持高速稳健的发展，我们期待更多精英的加入！二、我们的优势1、卓越雇主品牌： 财富fortune 和华信惠悦watsonwyatt授予“卓越雇主：中国最适宜工作的公司”。2、持续快速的增长：成立10年来，公司业务规模保持持续快速的增长，年平均人员增长率为45%。3、一流的基础研究实力，保证在行业始终保持竞争优势：我们是中国网络安全行业的技术领导者，10年来我们协助microsoft、sun、cisco 等公司解决了大量系统安全漏洞问题 。4、强大的研发能力及成功的市场拓展战略。5、具有国际竞争力的安全产品、解决方案： 绿盟科技的安全产品与解决方案覆盖全面，其中的绿盟远程安全评估系统是英国西海岸实验室认证的“全球第六、亚太***”的漏洞扫描产品。6、完善的专业安全服务体系和专业安全服务方法论：绿盟科技在国内率先开展专业安全服务业务，具备国内***安全服务资质。7、国际化发展：基于自身的技术优势，从2008年开始启动国际化发展步伐，我们正稳步前进。三、加入绿盟科技您可以获得什么1、行业领先的薪酬福利水平：绿盟科技尊重并承认每个员工的价值所在，一直致力于提供具有行业竞争力的薪酬福利。\xa0\xa0\xa0加入绿盟，您将获得有竞争力的薪资、全面的法定保障“五险一金”、60万元高额商业保险、以及带薪年假、年度体检等13项周到细致的员工关怀计划。2、专业化的培养体系和方案：绿盟独有的技术氛围，不断健全的内部培训体系，多元化的交流平台让每个员工都有展示才能、分享知识、全面锻炼和提高的机会。3、令人向往的工作环境和团队氛围：“融洽的气氛、良好的团队协作精神和凝聚力、浓厚的学习氛围、乐于分享、充满活力”，在每年的员工满意度调查中，这是绿盟员工经常提到的词语。'],
        '115784314': ['', '', '武汉-东湖新技术产业开发区', '无工作经验', '本科', '招若干人', '08-01发布', '系统测试工程师（武汉）', '上海联影医疗科技有限公司',
                      '工作职责\n1.有效执行集成测试及系统测试，提交测试报告；\n2.负责底层或上层软件测试；\n3.分析并理解软件需求，编写、执行和维护测试用例；\n4.开发测试工具，执行自动化测试，提高测试效率；\n5.跟踪定位产品软件中的缺陷或问题，并提出改进意见。\n任职要求\n1.生物医学工程、计算机科学、自动化及其他相关工科专业，本科及以上学历，硕士优先；\n2.有优秀的学习能力和自我驱动力；\n3.具有良好的团队合作精神和协作能力；\n4.具有编程能力和兴趣，至少熟练掌握一种编程语言，如C/C++/C#/python；\n5.熟悉一种或多种测试工具，有软件开发/测试经验者优先。\n\n职能类别：大学/大专应届毕业生\n',
                      '职能类别：大学/大专应届毕业生',
                      '联影医疗技术集团有限公司是一家全球领先的医疗科技企业，致力于为全球客户提供高性能医学影像、放疗产品及医疗信息化、智能化解决方案。公司于2011年成立，总部位于上海，同时在美国休斯敦、克利夫兰、康科德、波士顿和国内武汉、深圳、常州、贵州等地设立子公司及研发中心。联影拥有一支世界级人才团队，包括140余位海归科学家，500余位深具行业研发及管理经验的专业人士。目前，联影人才梯队总数达3600多人，其中40%以上为研发人员。截至目前，联影已向市场推出掌握完全自主知识产权的63款产品，包括全景动态扫描PET-CT（2米PET-CT）、“时空一体”超清TOF PET/MR、光梭3.0T MR、160层北斗CT、一体化CT-linac等一批世界首创和中国首创产品，整体性能指标达到国际一流水平，部分产品和技术实现世界范围内的引领。\xa0\xa0\xa0\xa0目前，联影产品已进驻美国、日本等全球18个国家和地区的3300多家医疗及科研机构，包括350多家***医院。2016-2018年，联影PET-CT及中高端DR在国内新增市场的产品份额持续3年位列***。基于uCloud联影智慧医疗云，联影结合移动互联网、云计算、人工智能、大数据分析等前沿技术，为政府、医院、科研机构和个人量身定制一系列云端智能化解决方案。2014年至今，联影助力上海、安徽、福建、贵州、湖北等19个省市的地方政府搭建分级诊疗体系，覆盖医院超过1700家，覆盖人群超过1亿。基于uAI智能平台，联影致力于打造“全栈全谱”的跨模态AI解决方案，贯穿疾病成像、筛查、随访、诊断、治疗、评估各环节，为医疗设备和医生赋能，让成像更好、更快、更安全、更经济，大幅提升医生诊断效率和精准度。2017年9月，联影以333.33亿元估值完成A轮融资，融资金额33.33亿元***，成为中国医疗设备行业***单笔私募融资。以“成为世界级医疗创新引领者”为愿景，“创造不同，为健康大同”为使命，联影正在构建一个以预防、诊断、治疗、康复全线产品为基础，以uCloud联影智慧医疗云为桥梁，以第三方精准医学诊断服务为入口，以大数据为智慧，由智能芯片与联影uAI人工智能平台全面赋能的全智能化医疗健康生态。通过与全球高校、医院、研究机构及产业合作伙伴的深度协同，持续提升全球高端医疗设备及服务可及性，为客户创造更多价值。']}
    zlzp_id_url_list = [
        {'id': 'CC144045072J00233452604', 'position': '软件测试工程师（中级）', 'company_name': '上海国响信息技术有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-10 16:40:58', 'money': '8K-12K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC144045072J00233452604.htm'},
        {'id': 'CC451534410J00354769202', 'position': '软件测试工程师(物联网)', 'company_name': '浙江宇视科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-10-22 19:32:19', 'money': '8K-15K', 'education': '本科', 'workyear': '1-3年',
         'id_url': 'https://jobs.zhaopin.com/CC451534410J00354769202.htm'},
        {'id': 'CC451534410J00369259302', 'position': '软件测试工程师(大安防)', 'company_name': '浙江宇视科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-11-15 08:57:09', 'money': '6K-12K', 'education': '本科', 'workyear': '不限',
         'id_url': 'https://jobs.zhaopin.com/CC451534410J00369259302.htm'},
        {'id': 'CC205108417J00198735602', 'position': '系统测试工程师-技术中心-合肥/武汉', 'company_name': '科大讯飞股份有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-12-10 10:23:08', 'money': '10K-15K', 'education': '本科',
         'workyear': '3-5年', 'id_url': 'https://jobs.zhaopin.com/CC205108417J00198735602.htm'},
        {'id': 'CC000544466J00197152709', 'position': '测试主管（非外包）', 'company_name': '软通动力信息技术(集团)有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-11-25 16:44:35', 'money': '7K-12K', 'education': '本科',
         'workyear': '5-10年', 'id_url': 'https://jobs.zhaopin.com/CC000544466J00197152709.htm'},
        {'id': 'CC599223521J00140894209', 'position': 'qa测试工程师', 'company_name': '北京云族佳科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-02 10:22:56', 'money': '10K-15K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC599223521J00140894209.htm'},
        {'id': 'CC152838414J00237402402', 'position': '嵌入式软件工程师', 'company_name': '盛视科技股份有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-11-27 08:27:46', 'money': '10K-15K', 'education': '大专', 'workyear': '1-3年',
         'id_url': 'https://jobs.zhaopin.com/CC152838414J00237402402.htm'},
        {'id': 'CC479050586J00399367703', 'position': '高级测试开发工程师', 'company_name': '江西国泰利民信息科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-06 14:07:01', 'money': '15K-20K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC479050586J00399367703.htm'},
        {'id': 'CC183877520J00192859014', 'position': 'android系统测试工程师', 'company_name': '易视腾科技股份有限公司北京分公司',
         'region': '武汉-洪山区', 'releasetime': '2019-12-11 11:22:23', 'money': '8K-12K', 'education': '本科',
         'workyear': '1-3年', 'id_url': 'https://jobs.zhaopin.com/CC183877520J00192859014.htm'},
        {'id': 'CC144045072J00141821304', 'position': '测试经理', 'company_name': '上海国响信息技术有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-03 10:16:59', 'money': '10K-15K', 'education': '本科', 'workyear': '5-10年',
         'id_url': 'https://jobs.zhaopin.com/CC144045072J00141821304.htm'},
        {'id': 'CC152838414J00351994202', 'position': 'C++前端软件开发工程师', 'company_name': '盛视科技股份有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-05 09:01:39', 'money': '10K-20K', 'education': '大专', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC152838414J00351994202.htm'},
        {'id': 'CC722374080J00095997514', 'position': '高级测试工程师', 'company_name': '北京锦益网络科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-11 10:47:52', 'money': '12K-16K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC722374080J00095997514.htm'},
        {'id': 'CC463581515J00254618708', 'position': '测试工程师(武汉)', 'company_name': '深圳市星商电子商务有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-12 09:31:19', 'money': '7K-14K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC463581515J00254618708.htm'},
        {'id': 'CC451534410J00161867002', 'position': '测试工程师(武汉研究所)', 'company_name': '浙江宇视科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-11 16:54:58', 'money': '6K-12K', 'education': '本科', 'workyear': '1年以下',
         'id_url': 'https://jobs.zhaopin.com/CC451534410J00161867002.htm'},
        {'id': 'CC624677922J00433174901', 'position': '电堆系统测试工程师', 'company_name': '武汉地质资源环境工业技术研究院有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-12-03 19:54:29', 'money': '8K-12K', 'education': '本科',
         'workyear': '3-5年', 'id_url': 'https://jobs.zhaopin.com/CC624677922J00433174901.htm'},
        {'id': 'CC152838414J00365278502', 'position': 'C++软件工程师', 'company_name': '盛视科技股份有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-02 08:30:49', 'money': '10K-20K', 'education': '大专', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC152838414J00365278502.htm'},
        {'id': 'CC120086316J00114035914', 'position': 'C++软件工程师（音视频）', 'company_name': '北京中庆现代技术股份有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-12-11 17:15:06', 'money': '15K-25K', 'education': '本科',
         'workyear': '3-5年', 'id_url': 'https://jobs.zhaopin.com/CC120086316J00114035914.htm'},
        {'id': 'CC603465980J00457225407', 'position': '中级测试工程师--外派中众邦银行', 'company_name': '深圳市睿服科技有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-12-10 10:31:17', 'money': '10K-15K', 'education': '本科',
         'workyear': '3-5年', 'id_url': 'https://jobs.zhaopin.com/CC603465980J00457225407.htm'},
        {'id': 'CC222003919J90250101000', 'position': 'C/C++软件研发工程师', 'company_name': '深圳市财富趋势科技股份有限公司武汉研发中心',
         'region': '武汉-洪山区', 'releasetime': '2019-12-12 14:30:11', 'money': '8K-15K', 'education': '本科',
         'workyear': '不限', 'id_url': 'https://jobs.zhaopin.com/222003919250101.htm'},
        {'id': 'CC265416683J00145338515', 'position': '软件开发工程师', 'company_name': '北京灵思创奇科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-05 14:23:49', 'money': '10K-13K', 'education': '本科', 'workyear': '1-3年',
         'id_url': 'https://jobs.zhaopin.com/CC265416683J00145338515.htm'},
        {'id': 'CC120401617J00201218009', 'position': '中级测试工程师（武汉）', 'company_name': '天地伟业技术有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-11-11 23:16:39', 'money': '8K-12K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC120401617J00201218009.htm'},
        {'id': 'CC120401617J00201218209', 'position': '高级测试工程师（武汉）', 'company_name': '天地伟业技术有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-11-11 23:21:39', 'money': '12K-16K', 'education': '本科', 'workyear': '5-10年',
         'id_url': 'https://jobs.zhaopin.com/CC120401617J00201218209.htm'},
        {'id': 'CC706544827J00424785403', 'position': '嵌入式软件总工程师', 'company_name': '武汉百络优物联科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-17 09:27:30', 'money': '12K-20K', 'education': '本科', 'workyear': '5-10年',
         'id_url': 'https://jobs.zhaopin.com/CC706544827J00424785403.htm'},
        {'id': 'CC222003919J90250160000', 'position': 'C++软件研发工程师', 'company_name': '深圳市财富趋势科技股份有限公司武汉研发中心',
         'region': '武汉-洪山区', 'releasetime': '2019-12-12 14:30:11', 'money': '8K-15K', 'education': '本科',
         'workyear': '不限', 'id_url': 'https://jobs.zhaopin.com/222003919250160.htm'},
        {'id': 'CC120975588J00435406907', 'position': '应用软件开发工程师', 'company_name': '杭州海康威视数字技术股份有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-10-11 17:43:14', 'money': '10K-15K', 'education': '本科',
         'workyear': '1-3年', 'id_url': 'https://jobs.zhaopin.com/CC120975588J00435406907.htm'},
        {'id': 'CC706544827J90250080000', 'position': '单片机软件工程师', 'company_name': '武汉百络优物联科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-17 09:27:29', 'money': '8K-15K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/706544827250080.htm'},
        {'id': 'CC444556219J00135636509', 'position': '测试工程师', 'company_name': '北京华志信科技股份有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-16 10:23:21', 'money': '8K-15K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC444556219J00135636509.htm'},
        {'id': 'CC368629084J00429940005', 'position': '高级嵌入式软件开发工程师', 'company_name': '深圳市智微智能科技开发有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-12-10 10:01:30', 'money': '10K-20K', 'education': '本科',
         'workyear': '5-10年', 'id_url': 'https://jobs.zhaopin.com/CC368629084J00429940005.htm'},
        {'id': 'CC434031920J90250362000', 'position': '武汉测试（中高级）', 'company_name': '上海康嘉信息技术有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-10-29 10:41:14', 'money': '6K-11K', 'education': '大专', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/434031920250362.htm'},
        {'id': 'CC489646430J00213482904', 'position': '高级测试工程师', 'company_name': '上海劳勤信息技术有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-07-04 18:45:14', 'money': '10K-15K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC489646430J00213482904.htm'},
        {'id': 'CC370675037J90250060000', 'position': '仪器软件开发工程师', 'company_name': '武汉市农业科学技术研究院农业环境安全检测研究所',
         'region': '武汉-洪山区', 'releasetime': '2019-11-11 18:01:19', 'money': '10K-15K', 'education': '本科',
         'workyear': '1-3年', 'id_url': 'https://jobs.zhaopin.com/370675037250060.htm'},
        {'id': 'CC377258030J00452997207', 'position': '嵌入式linux工程师', 'company_name': '山东有人信息技术有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-17 12:17:14', 'money': '8K-12K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC377258030J00452997207.htm'},
        {'id': 'CC701358820J00232335303', 'position': 'java开发工程师', 'company_name': '深圳微品致远信息科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-16 09:36:34', 'money': '9K-14K', 'education': '本科', 'workyear': '1-3年',
         'id_url': 'https://jobs.zhaopin.com/CC701358820J00232335303.htm'},
        {'id': 'CC479050586J00384668803', 'position': '高级java开发工程师', 'company_name': '江西国泰利民信息科技有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-11-25 09:18:38', 'money': '8K-15K', 'education': '本科',
         'workyear': '3-5年', 'id_url': 'https://jobs.zhaopin.com/CC479050586J00384668803.htm'},
        {'id': 'CC152838414J00257589302', 'position': '嵌入式驱动开发工程师', 'company_name': '盛视科技股份有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-11-27 08:27:46', 'money': '10K-15K', 'education': '大专', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC152838414J00257589302.htm'},
        {'id': 'CC566202621J00177135815', 'position': '武汉 Java开发工程师', 'company_name': '北京嘉华汇诚科技股份有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-11-20 16:29:13', 'money': '7K-14K', 'education': '本科',
         'workyear': '3-5年', 'id_url': 'https://jobs.zhaopin.com/CC566202621J00177135815.htm'},
        {'id': 'CC542331724J00181604509', 'position': 'java研发工程师', 'company_name': '北京亚鸿世纪科技发展有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-04 09:35:03', 'money': '10K-20K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC542331724J00181604509.htm'},
        {'id': 'CC253673710J00324773004', 'position': '高级C++开发工程师', 'company_name': '武汉精测电子集团股份有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-12-17 10:10:00', 'money': '12K-18K', 'education': '本科',
         'workyear': '5-10年', 'id_url': 'https://jobs.zhaopin.com/CC253673710J00324773004.htm'},
        {'id': 'CC420765026J00253622607', 'position': '销售专员（底薪4800）', 'company_name': '武汉达内职业培训学校', 'region': '武汉-洪山区',
         'releasetime': '2019-12-16 15:32:25', 'money': '10K-15K', 'education': '大专', 'workyear': '1-3年',
         'id_url': 'https://jobs.zhaopin.com/CC420765026J00253622607.htm'},
        {'id': 'CC633142422J00244147003', 'position': '嵌入式开发工程师(J10173)', 'company_name': '朗新科技股份有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-10-17 13:55:19', 'money': '10K-15K', 'education': '本科',
         'workyear': '3-5年', 'id_url': 'https://jobs.zhaopin.com/CC633142422J00244147003.htm'},
        {'id': 'CC722374080J00107370614', 'position': '高级android开发工程师', 'company_name': '北京锦益网络科技有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-12-02 10:43:51', 'money': '15K-20K', 'education': '大专',
         'workyear': '3-5年', 'id_url': 'https://jobs.zhaopin.com/CC722374080J00107370614.htm'},
        {'id': 'CC134637433J00237793508', 'position': '硬件工程师（武汉）', 'company_name': '上海柏飞电子科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-11 17:01:50', 'money': '8K-16K', 'education': '本科', 'workyear': '1-3年',
         'id_url': 'https://jobs.zhaopin.com/CC134637433J00237793508.htm'},
        {'id': 'CC610191783J00435758103', 'position': '漏洞挖掘工程师', 'company_name': '北京北大软件工程股份有限公司武汉分公司',
         'region': '武汉-洪山区', 'releasetime': '2019-11-28 14:44:37', 'money': '15K-30K', 'education': '本科',
         'workyear': '不限', 'id_url': 'https://jobs.zhaopin.com/CC610191783J00435758103.htm'},
        {'id': 'CC409648088J00417678201', 'position': '中级C++开发工程师(武汉)', 'company_name': '武汉华旗思创科技有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-12-16 08:45:58', 'money': '7.5K-15K', 'education': '本科',
         'workyear': '3-5年', 'id_url': 'https://jobs.zhaopin.com/CC409648088J00417678201.htm'},
        {'id': 'CC335741689J00495347901', 'position': '中高级java开发工程师', 'company_name': '武汉数为科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-12-14 19:27:44', 'money': '8K-15K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC335741689J00495347901.htm'},
        {'id': 'CC482493526J00457178301', 'position': '高级JAVA开发工程师', 'company_name': '上海智隆信息技术股份有限公司',
         'region': '武汉-洪山区', 'releasetime': '2019-10-24 17:25:57', 'money': '12K-20K', 'education': '本科',
         'workyear': '5-10年', 'id_url': 'https://jobs.zhaopin.com/CC482493526J00457178301.htm'},
        {'id': 'CC703257328J00183038410', 'position': 'Java开发工程师', 'company_name': '北京博运通达信息技术有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-11-06 14:24:03', 'money': '6.5K-13K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC703257328J00183038410.htm'},
        {'id': 'CC537951725J00392095705', 'position': '中级开发工程师', 'company_name': '深圳竹云科技有限公司', 'region': '武汉-洪山区',
         'releasetime': '2019-10-31 08:27:45', 'money': '8K-12K', 'education': '本科', 'workyear': '3-5年',
         'id_url': 'https://jobs.zhaopin.com/CC537951725J00392095705.htm'}]
    # zlzp_rown_dicts =

    # db.qcwy_insert_html_url_table(qcwy_id_url_dict)
    # db.qcwy_insert_html_content_table(qcwy_rown_dicts)




    db.Close_db()
