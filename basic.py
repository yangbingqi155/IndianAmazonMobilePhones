#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import logging
import io
import codecs
import requests
from lxml import etree

import config

def get_html(url):
	headers = {'content-type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	if config.enable_proxy==False:
		r=requests.get(url,headers=headers,timeout=15)
	else:
		r=requests.get(url,headers=headers,proxies=config.proxies,timeout=15)
	return r.text,r.status_code

def use_proxy(enable_proxy,proxy_url):
	proxy_handler=urllib2.ProxyHandler({"http",proxy_url})
	null_proxy_handler=urllib2.ProxyHandler({})
	if config.enable_proxy:
		opener=urllib2.build_opener(proxy_handler)
	else:
		opener=urllib2.build_opener(null_proxy_handler)
	urllib2.install_opener(opener)

def html_write(html,filename):
	with codecs.open(filename,'w','utf-8') as f:
		f.write(html)