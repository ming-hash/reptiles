# -*- coding:utf-8 -*-
import os
import sys
import time
import random
import queue

import pymysql

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from myconfig import readConfig
import common.PROXY_IP
from common.GetHtmlCommon import ReadJson, GatHtml
from Reptiles.GetHtml_qcwy import QcwySpliceUrl
from Reptiles.GetHtml_zlzp import ZlzpSpliceUrl
from Reptiles.GetHtml_lgw import LgwSpliceUrl

if __name__ == "__main__":
    # try:
    times = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(int(time.time())))

    # 获取代理IP列表
    proxy = common.PROXY_IP.PROXY()
    queue = queue.Queue()
    proxy_list = proxy.Get_db_storage_ip()
    if not proxy_list:
        common.PROXY_IP.run_proxy(queue)
        proxy_list = proxy.Get_db_storage_ip()
        proxy.Close_db()

    proxies = {"http": random.choice(proxy_list)}    # 输出：{"http":"http://60.218.172.171:8118"}

    # 读取json文件
    read_json = ReadJson()
    read_json.readall()
    all_input = read_json.Connect_url()

    # 获取前程无忧的条件url参数
    # q_keyword = read_json.edit_keyword(all_input[0], 0)
    # q_wuhan_area = read_json.read_wuhan_area(all_input[1], 0)
    # q_provide_salary = read_json.read_provide_salary(all_input[2], 0)
    # q_work_year = read_json.read_work_year(all_input[3], 0)
    # q_education = read_json.read_education(all_input[4], 0)

    # 获取智联招聘的条件url参数
    # z_keyword = read_json.edit_keyword(all_input[0], 1)
    # z_wuhan_area = read_json.read_wuhan_area(all_input[1], 1)
    # z_provide_salary = read_json.read_provide_salary(all_input[2], 1)
    # z_work_year = read_json.read_work_year(all_input[3], 1)
    # z_education = read_json.read_education(all_input[4], 1)

    # 获取拉勾网的条件url参数
    l_keyword = read_json.edit_keyword(all_input[0], 2)
    l_wuhan_area = read_json.read_wuhan_area(all_input[1], 2)
    l_provide_salary = read_json.read_provide_salary(all_input[2], 2)
    l_work_year = read_json.read_work_year(all_input[3], 2)
    l_education = read_json.read_education(all_input[4], 2)

    # 获取url_head参数
    GatHtml = GatHtml()
    qcwy_url_head = GatHtml.qcwy_url
    zlzp_url_head = GatHtml.zlzp_url
    lgw_url_head = GatHtml.lgw_url

    # 拼接前程无忧的url
    # QcwySpliceUrl = QcwySpliceUrl()
    # QcwySpliceUrl.Qcwy_url(qcwy_url_head, q_keyword, q_wuhan_area, q_provide_salary, q_work_year, q_education)
    # QcwySpliceUrl.Recruitment_url()

    # 拼接智联招聘的url
    # ZlzpSpliceUrl = ZlzpSpliceUrl()
    # zlzp_url = ZlzpSpliceUrl.Zlzp_url(zlzp_url_head, z_keyword, z_wuhan_area, z_provide_salary, z_work_year, z_education)
    # id_url_list = ZlzpSpliceUrl.Recruitment_url(zlzp_url, proxies)
    # rown_dicts = ZlzpSpliceUrl.Analysis_url(id_url_list, proxies)

    # 拼接拉勾网的url
    LgwSpliceUrl = LgwSpliceUrl()
    url_start, url, = LgwSpliceUrl.Lgw_url(lgw_url_head, l_keyword, l_wuhan_area, l_provide_salary, l_work_year, l_education)

    id_url_dict, rown_dicts, error_dicts = LgwSpliceUrl.Recruitment_url(url_start, url, l_keyword, proxies)
    print(id_url_dict)
    print(rown_dicts)

    print("错误的")
    print(error_dicts)
    print("**" * 20)

    # except pymysql.err.InternalError:
    #     print("数据库操作错误，请检查")
    # except Exception as e:
    #     print("ERROR：%s" % e)
    # else:
    #     print("已完成爬虫")

# mysql> select c.numbering,c.money,c.company_name,c.position,u.url from html_content as c left join html_url as u on c.numbering=u.numbering;
# 当发生RuntimeError: cryptography is required for sha256_password or caching_sha2_password报错时，需要安装模块pip install cryptography
