#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import logging
import io
import codecs
import requests
from lxml import etree

#enable proxy
enable_proxy=False
#proxes
proxies = {
  "https": "http://41.118.132.69:4433"
}
#web page response time out
response_time_out=100


url='http://www.amazon.in/s/ref=s9_acss_bw_cts_VodooFS_T1L4_w?rh=n%3A976419031%2Cn%3A!976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cp_98%3A10440597031&qid=1484135102&bbn=1389432031&low-price=&high-price=5%2C000&x=6&y=10&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=8E3TJVQ2D0S8CQR5VAVW&pf_rd_t=101&pf_rd_p=c40a9d88-2a21-4ea6-9319-5a465b910fd7&pf_rd_i=1389401031'


def get_html(url):
	headers = {'content-type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	if enable_proxy==False:
		r=requests.get(url,headers=headers)
	else:
		r=requests.get(url,headers=headers,proxies=proxies)
	return r.text

def use_proxy(enable_proxy,proxy_url):
	proxy_handler=urllib2.ProxyHandler({"http",proxy_url})
	null_proxy_handler=urllib2.ProxyHandler({})
	if enable_proxy:
		opener=urllib2.build_opener(proxy_handler)
	else:
		opener=urllib2.build_opener(null_proxy_handler)
	urllib2.install_opener(opener)

def html_write(html,filename):
	with codecs.open(filename,'w','utf-8') as f:
		f.write(html)

def get_products(html):
	content=etree.HTML(html)
	result=content.xpath("li[@class='s-result-item  celwidget ']")
	return result
	
html=get_html(url)
print get_products(html)
#html_write(html,'abc.html')
#print html.encode('utf-8')