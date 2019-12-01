# -*- coding:utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup


class QcwySpliceUrl:
    """前程无忧：拼接、获取所有的url"""

    def __init__(self):
        self.next_url_list = []
        self.id_url_dict = {}

    def Qcwy_url(self, url_head, keyword, wuhan_area, provide_salary, work_year, education):
        """拼接成完整查询结果url以及nexturl"""

        qcwy_url = "{0}/list/180200,{1},0000,00,9,{2},{3},2,1.html?lang=c&stype=&postchannel=0000&workyear={4}&cotype={5}&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=".format(
            url_head,
            wuhan_area,
            provide_salary,
            keyword,
            work_year,
            education)

        response = requests.get(qcwy_url, timeout=6)
        response.encoding = "gbk"
        soup_select_url = BeautifulSoup(response.text, "lxml")

        # 找出总共多少页。并拼接url
        next_soup = soup_select_url.find("span", {"class": "td"}).text
        compile_str = "[0-9]+"
        next_compile = re.compile(compile_str)
        next_number = int(next_compile.findall(next_soup)[0])
        print("爬虫到 %d 页" % next_number)
        if next_number >= 1:
            for next in range(1, next_number + 1):
                next_url = "{0}/list/180200,{1},0000,00,9,{2},{3},2,{4}.html?lang=c&stype=&postchannel=0000&workyear={5}&cotype={6}&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=".format(
                    url_head,
                    wuhan_area,
                    provide_salary,
                    keyword,
                    next,
                    work_year,
                    education, )
                self.next_url_list.append(next_url)
            return self.next_url_list
        else:
            return "你输入的筛选条件未找到招聘信息"

    def Recruitment_url(self):
        """获取所有的招聘详情url"""
        for i in range(len(self.next_url_list)):
            response = requests.get(self.next_url_list[i], timeout=6)
            response.encoding = "gbk"
            soup_i = BeautifulSoup(response.text, "lxml")

            soup_i1 = soup_i.find("div", {"class": "dw_table"})
            soup_i2 = soup_i1.find_all("div", {"class": "el"})

            for soup_i3 in soup_i2:
                soup_i4 = soup_i3.find("input", {"class": "checkbox"})
                soup_i5 = soup_i3.find("a", {"target": "_blank"})
                if soup_i4 and soup_i5:
                    key_id = soup_i4["value"]
                    value_url = soup_i5["href"]
                    self.id_url_dict[key_id] = value_url
        return self.id_url_dict


class AnalysisHtml:
    """解析招聘信息中的具体信息"""

    def __init__(self):
        self.rown_dicts = {}
        self.rown_lists = []
        self.money = ""
        self.welfare = ""
        self.region = ""
        self.workyear = ""
        self.education = ""
        self.hiringnumber = ""
        self.releasetime = ""
        self.position = ""
        self.company_name = ""
        self.positioninformation = ""
        self.workaddress = ""
        self.companyinformation = ""

    def Analysis_url(self, id_url_dict):
        for id in id_url_dict.keys():
            url = id_url_dict[id]
            # self.rown_lists = []                #在该循环中将该变量置为空，不然这个变量叠加字符串
            if url == "http://51rz.51job.com/sc/show_job_detail.php?jobid=100911781":  # 去除与大部分招聘详细格式不同的招聘页面
                pass
            else:
                print(url)

                self.welfare = ""  # 在该循环中将该变量置为空，不然这个变量叠加字符串
                self.positioninformation = ""  # 在该循环中将该变量置为空，不然这个变量叠加字符串

                response = requests.get(url)
                response.encoding = "gbk"
                soup_html = BeautifulSoup(response.text, "lxml")
                if re.findall(r"class=\"research\"", str(soup_html)):
                    pass
                else:
                    soup_html1 = soup_html.find("div", {"class": "tCompany_center clearfix"})

                    # 职位、薪资、公司、公司地址、工作经验、学历、招聘人数、发布时间、福利（没设置）
                    soup_html2 = soup_html1.find("div", {"class": "cn"})
                    soup_lists = soup_html2.find("p", {"class": "msg ltype"})["title"].split("|")

                    self.money = soup_html2.find("strong").text

                    soup_welfares = soup_html2.find_all("span", {"class": "sp4"})
                    for soup_welfare in soup_welfares:
                        self.welfare = self.welfare + soup_welfare.text + "|"

                    for i in range(len(soup_lists)):
                        soup_lists[i] = soup_lists[i].strip()

                        if re.findall(r"武汉-.+", soup_lists[i]):
                            self.region = soup_lists[i]
                        elif re.findall(r"[无年经验]", soup_lists[i]):
                            self.workyear = soup_lists[i]
                        elif re.findall(r"[中高专本研博]", soup_lists[i]):
                            self.education = soup_lists[i]
                        elif re.findall(r"[招]", soup_lists[i]):
                            self.hiringnumber = soup_lists[i]
                        elif re.findall(r"[发布]", soup_lists[i]):
                            self.releasetime = soup_lists[i]

                    self.position = soup_html2.find("h1", {"title": re.compile(".+")})["title"]
                    self.company_name = soup_html2.find("a", {"class": "catn", "target": "_blank"})["title"]

                    # 岗位职责、任职要求
                    soup_html3 = soup_html1.find("div", {"class": "bmsg job_msg inbox"})
                    soup_html4 = soup_html3.find_all("p")

                    # 岗位职责、任职要求有问题，赋值问题
                    for soup_html5 in soup_html4:
                        p_str = re.sub("\s+", "", soup_html5.text)
                        self.positioninformation = self.positioninformation + p_str + "\n"

                    # 上班地址
                    self.workaddress = soup_html1.find_all("p", {"class": "fp"})[-1].text.strip()

                    # 公司信息
                    self.companyinformation = soup_html1.find("div", {"class": "tmsg inbox"}).text.strip()

                    self.rown_lists = [self.money, self.welfare, self.region, self.workyear, self.education,
                                       self.hiringnumber, self.releasetime, self.position, self.company_name,
                                       self.positioninformation,
                                       self.workaddress, self.companyinformation]
                self.rown_dicts[id] = self.rown_lists
        return self.rown_dicts

# id_url_dict = splice_url.Recruitment_url()
#
# analysis_html = Analysis_Html()  # 创建获取解析内容实例
# rown_dicts = analysis_html.Analysis_url(id_url_dict)
