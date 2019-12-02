# -*- coding:utf-8 -*-
import random
import time
import os
import sys
import json
import re

import requests
from bs4 import BeautifulSoup
from urllib import parse  # 用来转换中文和url

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from myconfig import readConfig
from common.PROXY_IP import PROXY
from common.GetHtmlCommon import ReadJson, GatHtml

dbconfig = {
    "host": readConfig.DB_IP,
    "port": readConfig.DB_PORT,
    "user": readConfig.DB_USER,
    "passwd": readConfig.DB_PASSWORD,
    "db": readConfig.DB_DATABASES,
    "charset": readConfig.DB_CHARSET
}


class LgwSpliceUrl:
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
            "Connection": "keep - alive",
            "Content - Length": "19",
            "Host": "www.lagou.com",
            'Referer': 'https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput=',  # 重要
            "Pragma": "no - cache",
            "X - Anit - Forge - Code": "0",
            "X - Anit - Forge - Token": None,
            "X - Requested - With": "XMLHttpRequest"}

    def Lgw_url(self, url_head, keyword, wuhan_area, provide_salary, work_year, education):
        # 城市
        # City = {"city=城市&"}
        # 地区,不限=不添加参数

        url_start = "{0}jobs/list_{1}?{2}px=new&{3}{4}city=%E6%AD%A6%E6%B1%89&{5}#order".format(
            url_head, keyword, education, provide_salary, work_year, wuhan_area)
        url = "{0}jobs/positionAjax.json?{1}px=new&{2}city=%E6%AD%A6%E6%B1%89&{3}{4}needAddtionalResult=false".format(
            url_head, education, provide_salary, wuhan_area, work_year)
        return url_start, url

    def Cookie(self, url_start, proxy_list):
        proxy = eval(random.choice(proxy_list))
        session = requests.Session()
        session.get(url_start, headers=self.headers, timeout=3, proxies=proxy)  # 使用session维持同一个会话
        cookie = session.cookies  # 使用该会话的cookie
        return cookie

    def Recruitment_url(self, url_start, url, keyword, proxies):
        """获取信息及url"""
        id_url_dict = {}
        rown_dicts = {}
        json_lists = []
        error_dicts = {}

        strs = parse.unquote(keyword)
        session = requests.Session()
        session.get(url_start, headers=self.headers, timeout=3, proxies=proxies)  # 使用session维持同一个会话
        cookie = session.cookies  # 使用该会话的cookie

        form_data_page = {'first': 'true', 'pn': 1, 'kd': strs}
        response_page = session.post(url, data=form_data_page, headers=self.headers, cookies=cookie, timeout=3,
                                     proxies=proxies)
        json_dict_page = json.loads(response_page.text)
        recruit_msg_page = json_dict_page["content"]["positionResult"]
        print("获取总招聘信息：{}".format(recruit_msg_page["totalCount"]))

        time.sleep(1)

        if recruit_msg_page["totalCount"] != 0:
            if int(recruit_msg_page["totalCount"]) % len(recruit_msg_page["result"]) == 0:
                count_page = int(int(recruit_msg_page["totalCount"]) / len(recruit_msg_page["result"]))
            else:
                count_page = int(int(recruit_msg_page["totalCount"]) / len(recruit_msg_page["result"])) + 1

            # 获取所有json内容，并拼接成列表
            for n in range(1, count_page + 1):
                form_data = {'first': 'true', 'pn': n, 'kd': strs}
                response = session.post(url, data=form_data, headers=self.headers, cookies=cookie, timeout=3,
                                        proxies=proxies)
                json_lists.append(json.loads(response.text))

            # 循环读取所有json内容，并解析内容
            for json_dict in json_lists:
                recruit_msg = json_dict["content"]["positionResult"]
                showId = json_dict["content"]["showId"]
                for list in recruit_msg["result"]:
                    positionId = list["positionId"]
                    url2 = "https://www.lagou.com/jobs/{0}.html?show={1}".format(positionId, showId)
                    print(url2)
                    id_url_dict[positionId] = url2
                    soup_html = BeautifulSoup(
                        session.get(url2, headers=self.headers, cookies=cookie, timeout=3, proxies=proxies).text,
                        "lxml")

                    # 薪资
                    money = list["salary"]

                    # 福利
                    welfare = list["positionAdvantage"]

                    # 地区
                    region = list["city"]

                    # 工作年限
                    workyear = list["workYear"]

                    # 学历要求
                    education = list["education"]

                    # 招聘人数
                    hiringnumber = ""

                    # 发布时间
                    releasetime = list["createTime"]

                    # 招聘职位
                    position = list["positionName"]

                    # 公司名称
                    company_name = list["companyFullName"]

                    # 岗位职责
                    positioninformation1 = soup_html.find("div", {"class": re.compile("job-detail")})
                    # 工作地址
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

                    time.sleep(random.randint(1, 3))
                    id_url_dict[positionId] = url2
                    rown_dicts[positionId] = [money, welfare, region, workyear, education, hiringnumber, releasetime, position, company_name, positioninformation, workaddress]
                    print("==" * 20)
            return id_url_dict, rown_dicts, error_dicts

    def Analysis_url(self, id_url_list, proxy_list):
        """进入具体url中,读取招聘信息"""
        rown_dicts = {}
        pass


if __name__ == "__main__":
    # 获取代理IP列表
    proxy = PROXY(dbconfig)
    proxy_list = proxy.Get_db_storage_ip()
    if proxy_list is not True:
        ip_list = proxy.Get_ip_list1()
        new_proxy_list = proxy.Get_effective_ip(ip_list)
        proxy.Storage_db(new_proxy_list)
        proxy_list = proxy.Get_db_storage_ip()
    proxies = eval(random.choice(proxy_list))

    # 读取json文件
    read_json = ReadJson()
    read_json.readall()
    all_input = read_json.Connect_url()

    # 获取拉勾网的条件url参数
    l_keyword = read_json.edit_keyword(all_input[0], 2)
    l_wuhan_area = read_json.read_wuhan_area(all_input[1], 2)
    l_provide_salary = read_json.read_provide_salary(all_input[2], 2)
    l_work_year = read_json.read_work_year(all_input[3], 2)
    l_education = read_json.read_education(all_input[4], 2)

    # 获取url_head参数
    GatHtml = GatHtml()
    lgw_url_head = GatHtml.lgw_url

    # 拼接拉勾网的url
    LgwSpliceUrl = LgwSpliceUrl()
    url_start, url, = LgwSpliceUrl.Lgw_url(lgw_url_head, l_keyword, l_wuhan_area, l_provide_salary, l_work_year,l_education)

    id_url_dict, rown_dicts, error_dicts = LgwSpliceUrl.Recruitment_url(url_start, url, l_keyword, proxies)
    print(id_url_dict)
    print(rown_dicts)

    print("错误的")
    print(error_dicts)
    print("**" * 20)