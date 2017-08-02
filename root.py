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
import threading
import sys

try:
	import cPickle as pickle
except ImportError:
	import pickle
import config
import basic
import models
import httpproxy

has_p_info_pages=0

p_list_url='http://www.amazon.in/s/ref=s9_acss_bw_cts_VodooFS_T1L4_w?rh=n%3A976419031%2Cn%3A!976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cp_98%3A10440597031&qid=1484135102&bbn=1389432031&low-price=&high-price=5%2C000&x=6&y=10&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=8E3TJVQ2D0S8CQR5VAVW&pf_rd_t=101&pf_rd_p=c40a9d88-2a21-4ea6-9319-5a465b910fd7&pf_rd_i=1389401031'

#在产品列表面获取产品详细页面的url,并且返回下一页的URL
def get_product_info_urls(p_list_page_url):
	html,status_code=basic.get_html(p_list_page_url)
	content=etree.HTML(html)
	result=content.xpath("//a[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']")
	
	next_page_element=content.xpath("//a[@id='pagnNextLink']")
	next_page_url= ''
	if len(next_page_element)>0:
		next_page_url=next_page_element[0].get("href")
		next_page_url=config.galobal_domain+next_page_url
	
	return [map(lambda x:x.get("href"),result),next_page_url]

#获取产品详细信息
def get_product_info(p_info_url):
	p_info=models.ProductModel()
	status_code=200
	html=''
	try:
		html,status_code=basic.get_html(p_info_url)
		content=etree.HTML(html)
		asin=content.xpath('//input[@name="ASIN" and @type="hidden"]')[0].get("value")
		name=content.xpath("//span[@id='productTitle']")[0].text.strip()
		score_el=content.xpath("//a[@class='a-popover-trigger a-declarative']/i/span")
		score=score_el[0].text.strip() if len(score_el)>0 else 0
		comments_el=content.xpath("//span[@id='acrCustomerReviewText']")
		comments=comments_el[0].text.strip() if len(comments_el)>0 else 'No comments'
		price_el=content.xpath("//td[@class='a-span12']/span[@class='a-size-medium a-color-price']/text()")
		if len(price_el)>0:
			price=price_el[0].getparent().tail
		else:
			price_el=content.xpath("//div[@id='olp_feature_div']/div/span/span[@class='a-color-price']/text()")
			price=price_el[0].getparent().tail
				
		color_el=content.xpath("//div[@id='variation_color_name']/div[@class='a-row']/span[@class='selection']")
		color=color_el[0].text.strip() if len(color_el)>0 else ''
		
		p_info.name=name
		p_info.asin=asin
		p_info.score=score
		p_info.comments=comments
		p_info.price=price
		p_info.color=color
	except BaseException as e:
		print 'error url:'+p_info_url+',status_code:'+str(status_code)
		logging.exception('error url:'+p_info_url+',status_code:'+str(status_code))
		#访问超时则切换代理
		change_proxy()
		#basic.html_write(html,'abc.html')
		#raise e
	global has_p_info_pages
	has_p_info_pages=has_p_info_pages+1
	return p_info
#分页扑爬取产品列表页
def go_p_list_page(p_list_url):
	#product info page url on the product list page
	p_info_urls,next_page_url=get_product_info_urls(p_list_url)
	
	for info_url in p_info_urls:
		p_data= json.dumps(get_product_info(info_url),default=models.productmodel2dict)
		p_f=open('prduct.txt','a')
		p_f.write(p_data+"\n")
		p_f.close()
	if 	next_page_url!='':
		#每抓取一页切换一次代理
		change_proxy()
		go_p_list_page(next_page_url)

#启用代理
def set_proxy_enable():
	#从http://www.xicidaili.com获取代理并写入verified.txt文件
	httpproxy.get_proxies_from_web()
	set_proxy()
#设置代理信息
def set_proxy():
	#设置代理信息
	print u'开始设置代理信息....\n'
	verified_proxies_num=httpproxy.get_verified_proxies_num()
	if verified_proxies_num==0:
		config.enable_proxy=False
		print u'启用代理失败,没有验证过的代理可用，请查看verified.txt文件\n'
		return
	if config.current_proxy_index!=0 and config.current_proxy_index>=verified_proxies_num:
		config.current_proxy_index=0
	config.proxies=httpproxy.get_verified_proxy(config.current_proxy_index)
	config.enable_proxy=True
	print u'成功设置代理信息，当前代理索引'+str(config.current_proxy_index)+'\n'
#切换代理信息
def change_proxy():
	print u'切换代理信息....\n'
	httpproxy.get_proxies_from_web()
	verified_proxies_num=httpproxy.get_verified_proxies_num()
	if config.current_proxy_index+1>=verified_proxies_num:
		config.current_proxy_index=0
	else:
		config.current_proxy_index=config.current_proxy_index+1
	set_proxy()
	if config.enable_proxy==True:
		print u'已成功切换代理信息！\n' 
set_proxy_enable()
p_f=open('prduct.txt','w')
p_f.write("")
p_f.close()
go_p_list_page(p_list_url)
#print json.dumps(get_product_info('http://www.amazon.in/Feature-Mobile-Torch-light-Red/dp/B06XTP882V/ref=%20sr_1_519/258-8734428-2474330?s=electronics&rps=1&ie=UTF8&qid=1501404792&sr=1-519'),default=models.productmodel2dict)
#html=basic.get_html('http://www.amazon.in/Forme-N9-Selfie-Wireless-Mobile/dp/B071G2DSSC/ref=sr_1_142/257-5514151-9158917?s=electronics&rps=1&ie=UTF8&qid=1501400614&sr=1-142')
#basic.html_write(html,'abc.html')
#print html.encode('utf-8')