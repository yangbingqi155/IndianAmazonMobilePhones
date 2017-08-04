#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import httplib
import threading
import sys
import codecs
from datetime import datetime, date, time
reload(sys)
sys.setdefaultencoding('utf-8')

inFile = open('proxy.txt')
outFile = codecs.open('verified.txt', 'a','utf-8')
lock = threading.Lock()

import db_ProxyIPs
import model_ProxyIPs

def get_verified_proxies_num():
	return db_ProxyIPs.get_verified_proxies_num()
	
def get_verified_proxies(topnum):
	newest_verified_proxy_ips=db_ProxyIPs.get_newest_verified_proxy_ips(topnum)
	return newest_verified_proxy_ips
