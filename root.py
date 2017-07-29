#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import logging
import io
import codecs
import requests
from lxml import etree
import json

try:
	import cPickle as pickle
except ImportError:
	import pickle

import config
import basic
import models

p_list_url='http://www.amazon.in/s/ref=s9_acss_bw_cts_VodooFS_T1L4_w?rh=n%3A976419031%2Cn%3A!976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cp_98%3A10440597031&qid=1484135102&bbn=1389432031&low-price=&high-price=5%2C000&x=6&y=10&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=8E3TJVQ2D0S8CQR5VAVW&pf_rd_t=101&pf_rd_p=c40a9d88-2a21-4ea6-9319-5a465b910fd7&pf_rd_i=1389401031'

#在产品列表面获取产品详细页面的url,并且返回下一页的URL
def get_product_info_urls(p_list_page_url):
	html=basic.get_html(p_list_page_url)
	content=etree.HTML(html)
	result=content.xpath("//a[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']")
	
	next_page_element=content.xpath("//a[@id='pagnNextLink']")
	next_page_url= ''
	if len(next_page_element)>0:
		next_page_url=next_page_element[0].get("href")
		next_page_url=config.galobal_domain+next_page_url
	
	return [map(lambda x:x.get("href"),result),next_page_url]

def get_product_info(p_info_url):
	html=basic.get_html(p_info_url)
	content=etree.HTML(html)
	
	asin=content.xpath("//input[@name='ASIN' and @type='hidden']")[0].get("value")
	name=content.xpath("//span[@id='productTitle']")[0].text.strip()
	score=content.xpath("//a[@class='a-popover-trigger a-declarative']/i/span")[0].text.strip()
	comments=content.xpath("//span[@id='acrCustomerReviewText']")[0].text.strip()
	price=content.xpath("//td[@class='a-span12']/span[@class='a-size-medium a-color-price']/text()")[0].getparent().tail
	color_el=content.xpath("//div[@id='variation_color_name']/div[@class='a-row']/span[@class='selection']")
	color=color_el[0].text.strip() if len(color_el)>0 else ''
	
	p_info=models.ProductModel()
	p_info.name=name
	p_info.asin=asin
	p_info.score=score
	p_info.comments=comments
	p_info.price=price
	p_info.color=color
	
	return p_info
	
#product info page url on the product list page
p_info_urls,next_page_url=get_product_info_urls(p_list_url)

for info_url in p_info_urls:
	print json.dumps(get_product_info(info_url),default=models.productmodel2dict)
	

	
#html_write(html,'abc.html')
#print html.encode('utf-8')