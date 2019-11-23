#-*- coding:utf-8 -*-
import os
import sys

import time
import re
import requests
from bs4 import BeautifulSoup
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.DBOperation import DB
from myconfig import readConfig

dbconfig = {
            "host":readConfig.DB_IP,
            "port":readConfig.DB_PORT,
            "user":readConfig.DB_USER,
            "passwd":readConfig.DB_PASSWORD,
            "db":readConfig.DB_DATABASES,
            "charset":readConfig.DB_CHARSET
            }

class PROXY:
    """获取动态代理IP池，并存入数据库"""

    def __init__(self,dbconfig):
        self.HEADERS = {
                        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                        "accept-encoding": "gzip, deflate",
                        "accept-language": "zh-CN,zh;q=0.9",
                        "cache-control": "no-cache"
                        }
        self.range_n = 1
        self.TABLE = readConfig.table_proxy_ip
        self.DB = DB(dbconfig)


    def Get_ip_list1(self):
        """爬取免费代理IP网站上的IP及端口"""
        ip_list = []
        print("正在获取 西刺免费代理IP网站 代理列表...")
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
        print("正在获取 快代理网站 代理列表...")
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
        print("正在获取 89免费代理网站 代理列表...")
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


    def Get_effective_ip(self,ip_list):
        """验证代理IP有效性"""
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


    def Storage_db(self,proxy_list):
        """将有效的代理IP存入数据库"""

        create_table_sql = """create table if not exists `{}` (
                              `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              `proxy` varchar(100));""".format(self.TABLE)

        # try:
        #     count = 0
        #     self.DB.dml(create_table_sql)
        #     print("正在将代理IP写入数据库")
        #     for proxy in proxy_list:
        #         insert_table_sql = """insert into {}(proxy) values("{}")""".format(self.TABLE, proxy)
        #         self.DB.dml(insert_table_sql)
        #         count += 1
        #     self.DB.close()
        #     print("写入 {} 个代理IP成功".format(count))
        # except:
        #     print("写入数据库异常")

        count = 0
        self.DB.dml(create_table_sql)
        print("正在将代理IP写入数据库")
        for proxy in proxy_list:
            insert_table_sql = """insert into {}(proxy) values("{}")""".format(self.TABLE, proxy)
            self.DB.dml(insert_table_sql)
            count += 1
        self.DB.close()
        print("写入 {} 个代理IP成功".format(count))


    def Get_db_storage_ip(self):
        """从数据库中获取最新时间段内的代理IP"""
        show_data_list = []
        select_sql = """select proxy from proxy_ip order by times limit 10;"""

        show_database = self.DB.select(select_sql)
        for data in show_database:
            show_data_list.append(data[0])
        self.DB.close()
        return list(show_data_list)



if __name__ == "__main__":


    procedure_starttime = time.perf_counter()
    proxy = PROXY(dbconfig)

    # 多线程方法
    # thread_get_ip_list1 = threading.Thread(target = proxy.Get_ip_list1)
    # thread_get_ip_list2 = threading.Thread(target = proxy.Get_ip_list2)
    # thread_get_ip_list3 = threading.Thread(target = proxy.Get_ip_list3)

    # thread_get_ip_list1.start()
    # thread_get_ip_list1.join()



    ip_list1 = proxy.Get_ip_list1()
    print(ip_list1)
    # ip_list2 = proxy.Get_ip_list2()
    # ip_list3 = proxy.Get_ip_list3()
    #
    proxy_list1 = proxy.Get_effective_ip(ip_list1)
    # proxy_list2 = proxy.Get_effective_ip(ip_list2)
    # proxy_list3 = proxy.Get_effective_ip(ip_list3)
    #
    proxy.Storage_db(proxy_list1)
    # proxy.Storage_db(proxy_list2)
    # proxy.Storage_db(proxy_list3)




    procedure_endtime = time.perf_counter()
    print ("程序运行时间：{:.2f} 秒".format(procedure_endtime-procedure_starttime))

