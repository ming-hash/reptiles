# -*- coding:utf-8 -*-
import os
import sys
import queue

import time
import re
import requests
from bs4 import BeautifulSoup
import threading
import records

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from myconfig import readConfig


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
        self.TABLE = readConfig.table_proxy_ip
        self.DB = records.Database(
            'mysql+pymysql://{}:{}@{}:{}/{}'.format(readConfig.DB_USER, readConfig.DB_PASSWORD, readConfig.DB_IP,
                                                    readConfig.DB_PORT, readConfig.DB_DATABASES))

    def Get_ip_list1(self):
        """爬取免费代理IP网站上的IP及端口"""
        ip_list = []
        print("正在获取 西刺免费代理IP网站 代理列表...")
        for n in range(1, self.range_n + 1):
            url = 'http://www.xicidaili.com/nn/' + str(n)
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
        for n in range(1, self.range_n + 1):
            url = 'https://www.kuaidaili.com/free/inha/' + str(n) + "/"
            html = requests.get(url=url, headers=self.HEADERS).text
            soup = BeautifulSoup(html, 'lxml')
            soup_html = soup.find_all("tr")
            for soup_html1 in soup_html:
                ip = soup_html1.find("td", {"data-title": "IP"})
                port = soup_html1.find("td", {"data-title": "PORT"})
                if ip and port:
                    ip_list.append(ip.text + ":" + port.text)
            time.sleep(1)
        print("代理列表抓取成功.")
        return ip_list

    def Get_ip_list3(self):
        ip_list = []
        print("正在获取 89免费代理网站 代理列表...")
        for n in range(1, self.range_n + 1):
            url = 'http://www.89ip.cn/index_' + str(n) + ".html"
            html = requests.get(url=url, headers=self.HEADERS).text
            soup = BeautifulSoup(html, 'lxml')
            soup_html = soup.find_all("tr")
            for soup_html1 in soup_html:
                re1 = re.sub(r"[ |\t]", "", soup_html1.text)
                re2 = re.sub(r"[\n]", "|", re1)
                lists = re2.split("|")
                listss = []
                for i in lists:
                    if i:
                        listss.append(i)
                ip = listss[0]
                port = listss[1]
                if ip != "IP地址" and port != "端口":
                    ip_list.append(ip + ":" + port)
            time.sleep(1)
        print("代理列表抓取成功.")
        return ip_list

    def Get_effective_ip(self, queue, index, ip_list):
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
                response = requests.get("http://www.baidu.com", headers=self.HEADERS, proxies=proxies, timeout=3)
                if response.status_code == 200:
                    print(proxies)
                    new_proxy_list.append(proxies)
                    time.sleep(1)
            except:
                pass
        print("总共获取 {} 个可用代理IP".format(len(new_proxy_list)))
        queue.put((index, new_proxy_list))
        return new_proxy_list

    def Storage_db(self, proxy_list):
        """将单条有效的代理IP存入数据库,需要传入这类形式：[{'http': 'http://183.146.156.9:9999'}, {'http': 'http://27.43.186.47:9999'}]"""

        create_table_sql = """create table if not exists `{}` (
                              `times` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              `proxy` varchar(100));""".format(self.TABLE)

        try:
            self.DB.query(create_table_sql)
            for proxy in proxy_list:
                insert_table_sql = """insert into {0}(proxy) values("{1}")""".format(self.TABLE, proxy)
                self.DB.query(insert_table_sql)
            print("写入数据库成功")
        except Exception as e:
            print("ERROR:{}".format(e))

    # def Get_db_storage_ip(self):
    #     """从数据库中获取最新时间段内的代理IP"""
    #     show_data_list = []
    #     select_sql = """select proxy from proxy_ip where unix_timestamp(times) >= (unix_timestamp() - 43200) order by times limit 10;"""
    #
    #     show_database = self.DB.query(select_sql)
    #     for data in show_database:
    #         show_data_list.append(data["proxy"])
    #     return list(show_data_list)

    def Close_db(self):
        self.DB.close()


if __name__ == "__main__":
    procedure_starttime = time.perf_counter()
    proxy = PROXY()
    queue = queue.Queue()

    # 多线程方法
    # 抓取IP
    ip_list1 = proxy.Get_ip_list1()
    ip_list2 = proxy.Get_ip_list2()
    ip_list3 = proxy.Get_ip_list3()

    # 创建三个线程实例：验证IP有效性
    thread_get_ip_list1 = threading.Thread(target=proxy.Get_effective_ip, args=[queue, 1, ip_list1])
    thread_get_ip_list2 = threading.Thread(target=proxy.Get_effective_ip, args=[queue, 2, ip_list2])
    thread_get_ip_list3 = threading.Thread(target=proxy.Get_effective_ip, args=[queue, 3, ip_list3])

    # 启动运行、阻塞线程：验证IP有效性
    thread_list = [thread_get_ip_list1, thread_get_ip_list2, thread_get_ip_list3]
    for thread in thread_list: thread.start()
    for thread in thread_list: thread.join()

    # 将线程中的结果传出
    rv = []
    while not queue.empty():  # 如果队列为空，返回True
        rv.append(queue.get())

    # 将所有队列中的内容取出，并重新形成列表，并更新至数据库
    for result in rv:
        if result[1]:
            proxy_list = [proxy_ip for proxy_ip in result[1]]
            print(proxy_list)
            proxy.Storage_db(proxy_list)

    proxy.Close_db()
    procedure_endtime = time.perf_counter()
    print("程序运行时间：{:.2f} 秒".format(procedure_endtime - procedure_starttime))
