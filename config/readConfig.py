#-*- coding:utf-8 -*-

import os
import configparser
from configobj import ConfigObj

real_path = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(real_path,"config.ini")
# conf = configparser.ConfigParser()
# conf.read(configPath)
#
#
# """DB"""
# DB_IP = conf.get("DB","IP")
# DB_USER = conf.get("DB","USER")
# DB_PASSWORD = conf.get("DB","PASSWORD")
# DB_DATABASES = conf.get("DB","DATABASES")
# DB_PORT = int(conf.get("DB","PORT"))
# DB_CHARSET = conf.get("DB","CHARSET")
#
# """TABLE"""
# table_proxy_ip = conf.get("TABLE","proxy_ip")


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