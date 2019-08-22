#-*- coding:utf-8 -*-

import os
import configparser


real_path = os.path.dirname(os.path.realpath(__file__))
configPath = os.path.join(real_path,"config.ini")
conf = configparser.ConfigParser()
conf.read(configPath)


"""DB"""
DB_IP = conf.get("DB","IP")
DB_USER = conf.get("DB","USER")
DB_PASSWORD = conf.get("DB","PASSWORD")
DB_DATABASES = conf.get("DB","DATABASES")

"""TABLE"""
table_proxy_ip = conf.get("TABLE","proxy_ip")

