# -*- coding:utf-8 -*-
# from __future__ import unicode_literals

import os
import sys
import random
import time
import json

import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from myconfig import readConfig

dbconfig = {
    "host": readConfig.DB_IP,
    "port": readConfig.DB_PORT,
    "user": readConfig.DB_USER,
    "passwd": readConfig.DB_PASSWORD,
    "db": readConfig.DB_DATABASES,
    "charset": readConfig.DB_CHARSET
}


class ZlzpSpliceUrl:
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
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache"
        }

    def Zlzp_url(self, url_head, keyword, wuhan_area, provide_salary, work_year, education):
        """拼接URL"""
        zlzp_url = "{0}{1}{2}{3}{4}&companyType=-1&employmentType=-1&jobWelfareTag=-1{5}&=0&_v=0.46583492&x-zp-page-request-id=5a35fcbeb8dd4979bac9b392a7ae3057-1564133632670-181552&x-zp-client-id=230afb34-ddf6-4f7d-8e91-6edb65afb9c4".format(
            url_head, wuhan_area, provide_salary, work_year, education, keyword)
        return zlzp_url

    def Recruitment_url(self, url, proxies):
        """获取信息及url"""

        id_url_list = []
        sessions = requests.session()
        response = sessions.get(url, headers=self.headers, timeout=6, proxies=proxies)
        soup = response.text
        lists = json.loads(soup)["data"]["results"]
        print("总共获取 {} 条招聘信息".format(len(lists)))
        for list in lists:
            id_url_dicts = {}
            id_url_dicts["id"] = list["number"]
            id_url_dicts["position"] = list["jobName"]
            id_url_dicts["company_name"] = list["company"]["name"]
            id_url_dicts["region"] = list["city"]["display"]
            id_url_dicts["releasetime"] = list["updateDate"]
            id_url_dicts["money"] = list["salary"]
            id_url_dicts["education"] = list["eduLevel"]["name"]
            id_url_dicts["workyear"] = list["workingExp"]["name"]
            id_url_dicts["id_url"] = list["positionURL"]
            id_url_list.append(id_url_dicts)
        return id_url_list

    def Analysis_url(self, id_url_list, proxies):
        """进入具体url中,读取招聘信息"""
        rown_dicts = {}
        for id_url in id_url_list:
            print(id_url["id_url"])
            time.sleep(1)
            response1 = requests.get(id_url["id_url"], headers=self.headers, timeout=6, proxies=proxies)
            soup1 = BeautifulSoup(response1.text, "lxml")

            # 招聘人数
            soup2 = soup1.find("ul", {"class": "summary-plane__info"})
            if soup2:
                hiringnumber = soup2.find_all("li")[-1].text
            else:
                hiringnumber = ""

            # 福利
            welfare = ""
            soup3 = soup1.find("div", {"class": "highlights__content"})
            if soup3:
                for strs in soup3.find_all("span"):
                    welfare = welfare + strs.text + "|"

            # 任职要求
            soup4 = soup1.find("div", {"class": "describtion__detail-content"})
            if soup4:
                positioninformation = soup4.text
            else:
                positioninformation = ""

            # 工作地点
            soup5 = soup1.find("span", {"class": "job-address__content-text"})
            if soup5:
                workaddress = soup5.text
            else:
                workaddress = ""

            rown_litss = [welfare, hiringnumber, positioninformation, workaddress]
            rown_dicts[id_url["id"]] = rown_litss
        return rown_dicts