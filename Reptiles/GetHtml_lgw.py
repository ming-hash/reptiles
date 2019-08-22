# -*- coding:utf-8 -*-

import random
import time
import requests
import json
import re
import pymysql
from bs4 import BeautifulSoup
from urllib import parse            #用来转换中文和url
from selenium import webdriver

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


class DB:
    """数据库相关操作"""

    def __init__(self):
        self.IP = "localhost"
        self.USER = "root"
        self.PASSWORD = "admin"
        self.DATABASES = "testdb"

    def Connection_db(self):
        """连接数据库，并返回游标"""
        lists = []
        db1 = pymysql.connect(self.IP,self.USER,self.PASSWORD)
        cursor = db1.cursor()
        cursor.execute("show databases;")
        select_list =list(cursor.fetchall())
        for tuples in select_list:
            lists.append(tuples[0])
        if self.DATABASES in lists:
            db = pymysql.connect(self.IP, self.USER, self.PASSWORD, self.DATABASES)
            return db
        else:
            cursor.execute("create database "+ self.DATABASES)
            db1.commit()
            db1.close()
            db = pymysql.connect(self.IP,self.USER,self.PASSWORD,self.DATABASES)
            return db

    def Select_db(self,sql):
        """查询，并获取所有库表，生成列表"""
        lists = []
        db = self.Connection_db()
        cursor = db.cursor()
        cursor.execute(sql)
        show_database = cursor.fetchall()
        for table_list in list(show_database):
            lists.append(table_list[0])
        db.close()
        return lists

    def Select_table(self,sql):
        """查询表，并获取所有行数数据"""
        db = self.Connection_db()
        cursor = db.cursor()
        cursor.execute(sql)
        show_database = cursor.fetchall()
        db.close()
        return list(show_database)

    def Insert_table(self,sql):
        """创建、插入、更新、删除数据"""
        db = self.Connection_db()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        return True


class Write_DB:

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
                db.Insert_table("""update zlzp_html_url set times = "%s",url = "%s",position = "%s",company_name = "%s",region = "%s",releasetime = "%s",money = "%s",education = "%s",workyear = "%s" where numbering = "%s";""" % (
                    times, id_url["id_url"],id_url["position"],id_url["company_name"],id_url["region"],id_url["releasetime"],id_url["money"],id_url["education"],id_url["workyear"],id_url["id"]))
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
                db.Insert_table("""update zlzp_html_content set times = "%s",welfare = "%s",hiringnumber = "%s",positioninformation = "%s",workaddress = "%s" where numbering = "%s";""" % (
                    times, value[0], value[1], value[2], value[3], key))
            else:
                print("正在写入代号为 {} 的数据".format(key))
                db.Insert_table("""insert into zlzp_html_content(times,numbering,welfare,hiringnumber,positioninformation,workaddress)
                      values("{0}","{1}","{2}","{3}","{4}","{5}");""".format(
                    times, key, value[0], value[1], value[2], value[3]))


class PROXY:
    """获取动态代理IP池，并存入数据库"""
    def __init__(self):
        self.HEADERS = {
                        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                        "accept-encoding": "gzip, deflate",
                        "accept-language": "zh-CN,zh;q=0.9",
                        "cache-control": "no-cache"
                        }

        self.range_n = 1

        self.IP = "localhost"
        self.USER = "root"
        self.PASSWORD = "admin"
        self.DATABASES = "testdb"
        self.TABLE = "proxy_ip"

    #爬取免费代理IP网站上的IP及端口
    def Get_ip_list1(self):
        ip_list = []
        print("正在获取代理列表...")
        for n in range(1,self.range_n+1):
            url = 'http://www.xicidaili.com/nn/'+str(n)
            html = requests.get(url=url, headers=self.HEADERS).text
            soup = BeautifulSoup(html, 'lxml')
            ips = soup.find(id='ip_list').find_all('tr')
            for i in range(1, len(ips)):
                ip_info = ips[i]
                tds = ip_info.find_all('td')
                ip_list.append(tds[1].text + ':' + tds[2].text)
            time.sleep(1)
        print("代理列表抓取成功.")
        return ip_list

    def Get_ip_list2(self):
        ip_list = []
        print("正在获取代理列表...")
        for n in range(1,self.range_n+1):
            url = 'https://www.kuaidaili.com/free/inha/'+str(n) + "/"
            html = requests.get(url=url, headers=self.HEADERS).text
            soup = BeautifulSoup(html, 'lxml')
            soup_html = soup.find_all("tr")
            for soup_html1 in soup_html:
                ip = soup_html1.find("td",{"data-title":"IP"})
                port = soup_html1.find("td", {"data-title": "PORT"})
                if ip and port:
                    ip_list.append(ip.text + ":" +port.text)
            time.sleep(1)
        print("代理列表抓取成功.")
        return ip_list

    def Get_ip_list3(self):
        ip_list = []
        print("正在获取代理列表...")
        for n in range(1,self.range_n+1):
            url = 'http://www.89ip.cn/index_'+str(n) + ".html"
            html = requests.get(url=url, headers=self.HEADERS).text
            soup = BeautifulSoup(html, 'lxml')
            soup_html = soup.find_all("tr")
            for soup_html1 in soup_html:
                re1 = re.sub(r"[ |\t]","",soup_html1.text)
                re2 = re.sub(r"[\n]","|",re1)
                lists = re2.split("|")
                listss = []
                for i in lists:
                    if i:
                        listss.append(i)
                ip = listss[0]
                port = listss[1]
                if ip != "IP地址" and port != "端口":
                    ip_list.append(ip + ":" +port)
            time.sleep(1)
        print("代理列表抓取成功.")
        return ip_list

    #验证代理IP有效性
    def Get_effective_ip(self,ip_list):
        proxy_list = []
        new_proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        print("总共获取 {} 个代理IP".format(len(proxy_list)))
        print("正在设置代理，验证代理有效性")
        for i in range(len(proxy_list)):
            proxy_ip = proxy_list[i]
            proxies = {'http': proxy_ip}
            try:
                #response = requests.get("http://httpbin.org/ip", headers=headers, proxies=proxies,timeout = 3)
                response = requests.get("http://www.baidu.com", headers=self.HEADERS, proxies=proxies, timeout=3)
                if response.status_code == 200:
                    print(proxies)
                    new_proxy_list.append(proxies)
                    time.sleep(1)
            except:
                pass
        print("总共获取 {} 个可用代理IP".format(len(new_proxy_list)))
        return new_proxy_list

    #将有效的代理IP存入数据库
    def Storage_db(self,proxy_list):
        create_table_sql = """create table if not exists `{}` (
                              `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              `proxy` varchar(100));""".format(self.TABLE)
        try:
            count = 0
            db = pymysql.connect(self.IP, self.USER, self.PASSWORD,self.DATABASES)
            cursor = db.cursor()
            print("正在将代理IP写入数据库")
            cursor.execute(create_table_sql)
            cursor.fetchall()
            for proxy in proxy_list:
                insert_table_sql = """insert into {}(proxy) values("{}")""".format(self.TABLE, proxy)
                cursor.execute(insert_table_sql)
                db.commit()
                count += 1
            db.close()
            print("写入 {} 个代理IP成功".format(count))
        except:
            pass

    #从数据库中获取最新时间段内的代理IP
    def Get_db_storage_ip(self):
        show_data_list = []
        select_sql = """select proxy from proxy_ip where unix_timestamp(times) >= (unix_timestamp() - 43200) order by times limit 10;"""

        db = pymysql.connect(self.IP, self.USER, self.PASSWORD, self.DATABASES)
        cursor = db.cursor()
        cursor.execute(select_sql)
        show_database = cursor.fetchall()
        for data in show_database:
            show_data_list.append(data[0])
        db.close()
        return list(show_data_list)


class Splice_Url:
    """获取json文件的url"""
    def __init__(self):
        self.user_agents = random.choice([
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ])
        self.headers = {
            "user-agent": self.user_agents,
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "Connection":"keep - alive",
            "Content - Length": "19",
            "Host": "www.lagou.com",
            'Referer': 'https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput=',    #重要
            "Pragma":"no - cache",
            "X - Anit - Forge - Code": "0",
            "X - Anit - Forge - Token": None,
            "X - Requested - With": "XMLHttpRequest"}


    def Lgw_url(self):
        ## 城市
        ## City = {"city=城市&"}
        # 地区,不限=不添加参数
        WuHanArea = {"洪山区": "district=%E6%B4%AA%E5%B1%B1%E5%8C%BA&", "青山区": "district=%E9%9D%92%E5%B1%B1%E5%8C%BA&",
                     "东湖新技术开发区": "district=%E4%B8%9C%E6%B9%96%E6%96%B0%E6%8A%80%E6%9C%AF%E5%BC%80%E5%8F%91%E5%8C%BA&",
                     "武汉经济技术开发区": "district=%E6%AD%A6%E6%B1%89%E7%BB%8F%E6%B5%8E%E6%8A%80%E6%9C%AF%E5%BC%80%E5%8F%91%E5%8C%BA&",
                     "武昌区": "district=%E6%AD%A6%E6%98%8C%E5%8C%BA&", "江夏区": "district=%E6%B1%9F%E5%A4%8F%E5%8C%BA&",
                     "江汉区": "district=%E6%B1%9F%E6%B1%89%E5%8C%BA&", "江岸区": "district=%E6%B1%9F%E5%B2%B8%E5%8C%BA&",
                     "硚口区": "district=%E7%A1%9A%E5%8F%A3%E5%8C%BA&", "汉阳区": "district=%E6%B1%89%E9%98%B3%E5%8C%BA&",
                     "东西湖区": "district=%E4%B8%9C%E8%A5%BF%E6%B9%96%E5%8C%BA&",
                     "蔡甸区": "district=%E8%94%A1%E7%94%B8%E5%8C%BA&",
                     "黄陂区": "district=%E9%BB%84%E9%99%82%E5%8C%BA&", "汉南区": "district=%E6%B1%89%E5%8D%97%E5%8C%BA&",
                     "新洲区": "district=%E6%96%B0%E6%B4%B2%E5%8C%BA&", "武汉不限": ""}

        # 薪资
        ProvideSalary = {"2k以下": "yx=2k%E4%BB%A5%E4%B8%8B&", "2k-5k": "yx=2k-5k&", "5k-10k": "yx=5k-10k&",
                         "10k-15k": "yx=10k-15k&", "15k-25k": "yx=15k-25k&", "不限": ""}

        # 工作年限,不限=不添加参数
        WorkYear = {"3年及以下": "gj=3%E5%B9%B4%E5%8F%8A%E4%BB%A5%E4%B8%8B&", "3-5年": "gj=3-5%E5%B9%B4&",
                    "5-10年": "gj=5-10%E5%B9%B4&", "10年以上": "gj=10%E5%B9%B4%E4%BB%A5%E4%B8%8A&",
                    "不要求": "gj=%E4%B8%8D%E8%A6%81%E6%B1%82&", "不限": ""}

        # 学历,不限=不添加参数
        Education = {"大专": "xl=%E5%A4%A7%E4%B8%93&", "本科": "xl=%E6%9C%AC%E7%A7%91&", "硕士": "xl=%E7%A1%95%E5%A3%AB&",
                     "博士": "xl=%E5%8D%9A%E5%A3%AB&", "不要求": "xl=%E4%B8%8D%E8%A6%81%E6%B1%82&", "不限": ""}

        # 工作性质,不限=不添加参数
        JobType = {"兼职": "gx=%E5%85%BC%E8%81%8C&", "全职": "gx=%E5%85%A8%E8%81%8C&", "实习": "gx=%E5%AE%9E%E4%B9%A0&",
                   "不限": ""}

        # 搜索关键字
        strs1 = input("请输入搜索工作关键字：").strip()
        if len(strs1) == 0:
            syts_url = ""
        else:
            syts_url = parse.quote(strs1)

        wuhanarea = WuHanArea[input("请输入地区(洪山区/青山区/东湖新技术开发区/武汉经济技术开发区/武昌区/江夏区/江汉区/江岸区/硚口区/汉阳区/东西湖区/蔡甸区/黄陂区/汉南区/新洲区/武汉不限)：").strip()]
        providesalary = ProvideSalary[input("请输入薪资(2k以下/2k-5k/5k-10k/10k-15k/15k-25k/不限)：").strip()]
        workyear = WorkYear[input("请输入工作年限(3年及以下/3-5年/5-10年/10年以上/不要求/不限)：").strip()]
        education = Education[input("请输入学历(大专/本科/硕士/博士/不要求/不限)：").strip()]
        jobtype = JobType[input("请输入工作性质(兼职/全职/实习/不限)：").strip()]

        url_start = "https://www.lagou.com/jobs/list_{0}?{1}px=new&{2}{3}{4}city=%E6%AD%A6%E6%B1%89&{5}#order".format(
            syts_url, education, providesalary, jobtype, workyear, wuhanarea)
        url = "https://www.lagou.com/jobs/positionAjax.json?{0}px=new&{1}{2}city=%E6%AD%A6%E6%B1%89&{3}{4}needAddtionalResult=false".format(
            education, providesalary, jobtype, wuhanarea, workyear)

        return url_start,url,strs1


    def Cookie(self,url_start,proxy_list):
        proxy = eval(random.choice(proxy_list))
        session = requests.Session()
        session.get(url_start, headers=self.headers, timeout=3, proxies=proxy)  # 使用session维持同一个会话
        cookie = session.cookies  # 使用该会话的cookie
        return cookie


    def Recruitment_url(self,url_start,url,strs1,proxy_list):
        """获取信息及url"""
        id_url_dict = {}
        rown_dicts = {}
        json_lists = []
        error_dicts = {}

        proxy = eval(random.choice(proxy_list))

        session = requests.Session()
        session.get(url_start, headers=self.headers, timeout=3, proxies=proxy)  # 使用session维持同一个会话
        cookie = session.cookies  # 使用该会话的cookie

        form_data_page = {'first': 'true', 'pn': 1, 'kd': strs1}
        response_page = session.post(url, data=form_data_page, headers=self.headers, cookies=cookie, timeout=3,
                                     proxies=proxy)
        json_dict_page = json.loads(response_page.text)
        recruit_msg_page = json_dict_page["content"]["positionResult"]
        print("获取总招聘信息：{}".format(recruit_msg_page["totalCount"]))

        time.sleep(1)

        if recruit_msg_page["totalCount"] != 0:
            if int(recruit_msg_page["totalCount"]) % len(recruit_msg_page["result"]) == 0:
                count_page = int(int(recruit_msg_page["totalCount"]) / len(recruit_msg_page["result"]))
            else:
                count_page = int(int(recruit_msg_page["totalCount"]) / len(recruit_msg_page["result"])) + 1

            #获取所有json内容，并拼接成列表
            for n in range(1, count_page + 1):
                form_data = {'first': 'true', 'pn': n, 'kd': strs1}
                response = session.post(url, data=form_data, headers=self.headers, cookies=cookie, timeout=3,proxies=proxy)
                json_lists.append(json.loads(response.text))

            #循环读取所有json内容，并解析内容
            for json_dict in json_lists:
                recruit_msg = json_dict["content"]["positionResult"]
                showId = json_dict["content"]["showId"]
                for list in recruit_msg["result"]:
                    positionId = list["positionId"]
                    url2 = "https://www.lagou.com/jobs/{0}.html?show={1}".format(positionId, showId)
                    print(url2)
                    id_url_dict[positionId] = url2
                    soup_html = BeautifulSoup(session.get(url2,headers=self.headers,cookies=cookie, timeout=3,proxies=proxy).text,"lxml")

                    #薪资
                    money = list["salary"]

                    #福利
                    welfare = list["positionAdvantage"]

                    #地区
                    region = list["city"]

                    #工作年限
                    workyear = list["workYear"]

                    #学历要求
                    education = list["education"]

                    #招聘人数
                    hiringnumber = ""

                    #发布时间
                    releasetime = list["createTime"]

                    #招聘职位
                    position = list["positionName"]

                    #公司名称
                    company_name = list["companyFullName"]

                    #岗位职责
                    positioninformation1 = soup_html.find("div",{"class":re.compile("job-detail")})
                    #工作地址
                    workaddress1 = soup_html.find("div", {"class": "work_addr"})
                    if positioninformation1 and workaddress1:
                        positioninformation = positioninformation1.text
                        workaddress = re.sub(r"[ |\n|查看地图]", "", workaddress1.text)
                    elif positioninformation1 is None and workaddress1:
                        error_dicts[positionId] = url2
                        positioninformation = "错误"
                        print(soup_html)
                        break
                    elif workaddress1 is None and positioninformation1:
                        error_dicts[positionId] = url2
                        workaddress1 = "错误"
                        print(soup_html)
                        break
                    elif workaddress1 is None and positioninformation1 is None:
                        error_dicts[positionId] = url2
                        positioninformation = "错误"
                        workaddress1 = "错误"
                        print(soup_html)
                        break

                    time.sleep(random.randint(1,3))
                    id_url_dict[positionId] = url2
                    rown_dicts[positionId] = [money,welfare,region,workyear,education,hiringnumber,releasetime,position,company_name,positioninformation,workaddress]
                    print("==" * 20)
            return id_url_dict,rown_dicts,error_dicts


    def Analysis_url(self,id_url_list,proxy_list):
        """进入具体url中,读取招聘信息"""
        rown_dicts = {}
        pass



if __name__ == "__main__":

    proxy = PROXY()
    proxy_list = proxy.Get_db_storage_ip()
    if proxy_list:
        pass
    else:
        ip_list = proxy.Get_ip_list1()
        proxy_list = proxy.Get_effective_ip(ip_list)
        proxy.Storage_db(proxy_list)
        proxy_list = proxy.Get_db_storage_ip()
        print(proxy_list)

    splice_url = Splice_Url()
    url_start,url,strs1 = splice_url.Lgw_url()

    print(url_start)
    print(url)

    id_url_dict,rown_dicts,error_dicts = splice_url.Recruitment_url(url_start,url,strs1,proxy_list)
    print(id_url_dict)
    print(rown_dicts)

    print("错误的")
    print(error_dicts)
    print("**" * 20)


