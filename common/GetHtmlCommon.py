# -*- coding:utf-8 -*-
import json
import os
from urllib import parse  # 用来转换中文和url

import requests
from bs4 import BeautifulSoup


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

class Get_Cookie:
    """获取cookie"""

    def get_cookie(url):
        browser = webdriver.Chrome()
        browser.get(url)
        cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        return cookiestr

        # new_cookie_list = get_cookie(url)
        # for cookie1 in new_cookie_list:
        #     if "expiry" in cookie1.keys():
        #         new_cookie_timestamp = int(cookie1["expiry"])
        #         print(new_cookie_timestamp)
        #         print(cookie1)


class Write_DB:
    """写入前程无忧爬取的数据到数据库"""

    def __init__(self):
        self.createtable_sql = """create table `html_url` (
                        `id` int unsigned auto_increment,
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `numbering` int not null,
                        `url` varchar(150) not null,
                        primary key(`id`));"""

        self.createtable_sql = """create table `html_content` (
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `numbering` int not null,
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
                        );"""

    def insert_html_url_table(self, id_url_dict):
        """将每条招聘的id、url存入htmlurl表中"""
        if "html_url" in db.Select_db("show tables;"):
            pass
        else:
            db.Insert_table(self.createtable_sql)
            print("创建html_url表成功")

        # 插入time,id,url数据，数据库中有则更新
        for key, value in id_url_dict.items():
            if int(key) in db.Select_db("""select numbering from html_url;"""):
                db.Insert_table("""update html_url set times = "%s",url = "%s" where numbering = "%s";""" % (
                    times, value, key))
            else:
                db.Insert_table("""insert into html_url(times,numbering,url) values("%s","%s","%s");""" % (
                    times, key, value))

    def insert_html_content_table(self, rown_dicts):
        """将每条招聘的具体解析内容存入表中"""
        if "html_content" in db.Select_db("show tables;"):
            pass
        else:
            db.Insert_table(self.createtable_sql)
            print("创建html_content表成功")

        # 插入time,id等数据，数据库中有则更新
        for key, value in rown_dicts.items():
            if int(key) in db.Select_db("""select numbering from html_content;"""):
                print("正在更新代号为 {} 的数据".format(key))
                db.Insert_table("""update html_content set times = "%s",money = "%s",welfare = "%s",region = "%s",workyear = "%s",education = "%s",hiringnumber = "%s",releasetime = "%s",position = "%s",company_name = "%s",positioninformation = "%s",
                                    workaddress = "%s",companyinformation = "%s" where numbering = "%s";""" % (
                    times, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8],
                    value[9], value[10],
                    pymysql.escape_string(value[11]), key))
            else:
                print("正在写入代号为 {} 的数据".format(key))
                db.Insert_table("""insert into html_content(times,numbering,money,welfare,region,workyear,education,hiringnumber,releasetime,position,company_name,positioninformation,
                                    workaddress,companyinformation)
                      values("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}");""".format(
                    times, key, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7],
                    value[8], value[9], value[10],
                    pymysql.escape_string(value[11])))


class Write_DB:
    """写入智联招聘爬取的数据到数据库"""

    def __init__(self):
        self.createtable_sql1 = """create table `zlzp_html_url` (
                        `id` int unsigned auto_increment,
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `numbering` VARCHAR(40) not null,
                        `url` varchar(150) not null,
                        `position` VARCHAR(40),
                        `company_name` VARCHAR(40),
                        `region` VARCHAR(30),
                        `releasetime` VARCHAR(30),
                        `money` VARCHAR(30),
                        `education` VARCHAR(30),
                        `workyear` VARCHAR(30),
                        primary key(`id`));"""

        self.createtable_sql2 = """create table `zlzp_html_content` (
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `numbering` VARCHAR(40) not null,
                        `welfare` VARCHAR(100),
                        `hiringnumber` VARCHAR(30),
                        `positioninformation` VARCHAR(6000),
                        `workaddress` VARCHAR(100)
                        );"""

    def insert_html_url_table(self, id_url_dict):
        """将每条招聘的id、url存入htmlurl表中"""
        if "zlzp_html_url" in db.Select_db("show tables;"):
            pass
        else:
            db.Insert_table(self.createtable_sql1)
            print("创建html_url表成功")

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

    def insert_html_content_table(self, rown_dicts):
        """将每条招聘的具体解析内容存入表中"""
        if "zlzp_html_content" in db.Select_db("show tables;"):
            pass
        else:
            db.Insert_table(self.createtable_sql2)
            print("创建html_content表成功")

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


class Write_DB:
    """写入拉勾网爬取的数据到数据库"""

    def __init__(self):
        self.createtable_sql1 = """create table `zlzp_html_url` (
                        `id` int unsigned auto_increment,
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `numbering` VARCHAR(40) not null,
                        `url` varchar(150) not null,
                        `position` VARCHAR(40),
                        `company_name` VARCHAR(40),
                        `region` VARCHAR(30),
                        `releasetime` VARCHAR(30),
                        `money` VARCHAR(30),
                        `education` VARCHAR(30),
                        `workyear` VARCHAR(30),
                        primary key(`id`));"""

        self.createtable_sql2 = """create table `zlzp_html_content` (
                        `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        `numbering` VARCHAR(40) not null,
                        `welfare` VARCHAR(100),
                        `hiringnumber` VARCHAR(30),
                        `positioninformation` VARCHAR(6000),
                        `workaddress` VARCHAR(100)
                        );"""

    def insert_html_url_table(self, id_url_dict):
        """将每条招聘的id、url存入htmlurl表中"""
        if "zlzp_html_url" in db.Select_db("show tables;"):
            pass
        else:
            db.Insert_table(self.createtable_sql1)
            print("创建html_url表成功")

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

    def insert_html_content_table(self, rown_dicts):
        """将每条招聘的具体解析内容存入表中"""
        if "zlzp_html_content" in db.Select_db("show tables;"):
            pass
        else:
            db.Insert_table(self.createtable_sql2)
            print("创建html_content表成功")

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
