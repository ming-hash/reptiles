# -*- coding:utf-8 -*-

import os
from configobj import ConfigObj

real_path = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(real_path, "config.ini")
config = ConfigObj(configPath, encoding='UTF8')

"""DB"""
DB_IP = config["DB"]["IP"]
DB_USER = config["DB"]["USER"]
DB_PASSWORD = config["DB"]["PASSWORD"]
DB_DATABASES = config["DB"]["DATABASES"]
DB_PORT = int(config["DB"]["PORT"])
DB_CHARSET = config["DB"]["CHARSET"]

"""TABLE"""
table_proxy_ip = config["TABLE"]["proxy_ip"]
qcwy_table1 = config["TABLE"]["qcwy_table1"]
qcwy_table2 = config["TABLE"]["qcwy_table2"]
zlzp_table1 = config["TABLE"]["zlzp_table1"]
zlzp_table2 = config["TABLE"]["zlzp_table2"]
lgw_table1 = config["TABLE"]["lgw_table1"]
lgw_table2 = config["TABLE"]["lgw_table2"]