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
from datetime import datetime, date
import uuid
import sys
import re
import time

try:
	import cPickle as pickle
except ImportError:
	import pickle
import config
import basic
import model_product
import libhttpproxy
import db_product
import db_IPProxiesPoolApplicationSwitch
import model_IPProxiesPoolApplicationSwitch

sys.setrecursionlimit(1000000) 
has_p_info_pages=0
p_list_url='https://www.amazon.in/s/ref=s9_acss_bw_cts_VodooFS_T1L4_w?rh=n%3A976419031%2Cn%3A!976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cp_98%3A10440597031&qid=1484135102&bbn=1389432031&low-price=&high-price=5%2C000&x=6&y=10&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-7&pf_rd_r=N8FAX8586W73XVCYYS7Y&pf_rd_t=101&pf_rd_p=476f8f1a-15ac-4693-b157-8657b9ebf7e1&pf_rd_i=1389401031'
p_list_url1='https://www.amazon.in/s/ref=s9_acss_bw_cts_VodooFS_T2L4_w?rh=n%3A976419031%2Cn%3A!976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cn%3A1805560031&qid=1484135856&bbn=1805560031&low-price=5%2C000&high-price=10%2C000&x=3&y=12&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-7&pf_rd_r=N8FAX8586W73XVCYYS7Y&pf_rd_t=101&pf_rd_p=476f8f1a-15ac-4693-b157-8657b9ebf7e1&pf_rd_i=1389401031'
p_list_url2='https://www.amazon.in/s/ref=s9_acss_bw_cts_VodooFS_T3L4_w?rh=n%3A976419031%2Cn%3A!976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cn%3A1805560031%2Cp_36%3A1318505031&qid=1484135884&bbn=1805560031&low-price=10%2C000&high-price=15%2C000&x=16&y=9&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-7&pf_rd_r=N8FAX8586W73XVCYYS7Y&pf_rd_t=101&pf_rd_p=476f8f1a-15ac-4693-b157-8657b9ebf7e1&pf_rd_i=1389401031'
p_list_url3='https://www.amazon.in/s/ref=s9_acss_bw_cts_VodooFS_T4L4_w?rh=i%3Aelectronics%2Cn%3A976419031%2Cn%3A%21976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cn%3A1805560031%2Cp_98%3A10440597031%2Cp_36%3A1500000-99999999&bbn=1805560031&rw_html_to_wsrp=1&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-7&pf_rd_r=N8FAX8586W73XVCYYS7Y&pf_rd_t=101&pf_rd_p=476f8f1a-15ac-4693-b157-8657b9ebf7e1&pf_rd_i=1389401031'
#在产品列表面获取产品详细页面的url,并且返回下一页的URL
def get_product_info_urls(p_list_page_url):
	next_page_url= ''
	status_code=''
	is_break=False
	result=[]
	try:
		html,status_code=basic.get_html(p_list_page_url)
		content=etree.HTML(html)
		result=content.xpath("//a[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']")
		
		next_page_element=content.xpath("//a[@id='pagnNextLink']")
		
		if len(next_page_element)>0:
			next_page_url=next_page_element[0].get("href")
			next_page_url=config.galobal_domain+next_page_url
		else:
			#如果最后一页
			if len(content.xpath("//span[@class='pagnRA1']"))>0:
				print 'The end list page :'+p_list_page_url
				logging.info('The end list page :'+p_list_page_url)
				return [map(lambda x:x.get("href"),result) if result!=None and len(result)>0 else None,'',True]
			else:
				#may be server think this request client is a robot
				logging.info('Can\'t find next list page url,but can open the current list page url.')
				print 'Can\'t find next list page url,but can open the current list page url.'
				return [None,'',False]
	except  requests.exceptions.Timeout as e:
		print 'request connection timeout error ,product list error url:'+p_list_page_url
		logging.exception('request connection timeout error ,product list error url:'+p_list_page_url)
		return [None,'',False]
	except  requests.exceptions.ConnectionError as e:
		print 'request connection error ,product list error url:'+p_list_page_url
		logging.exception('request connection error ,product list error url:'+p_list_page_url)
		return [None,'',False]
	except  requests.exceptions.RequestException as e:
		print 'request timeout ,product list error url:'+p_list_page_url+',status_code:'+str(status_code)
		logging.exception('request timeout,product list error url:'+p_list_page_url+',status_code:'+str(status_code))
		return [None,'',False]
	except BaseException as e:
		print 'product list error url:'+p_list_page_url+',status_code:'+str(status_code)
		logging.exception('product list error url:'+p_list_page_url+',status_code:'+str(status_code))
		#basic.html_write(html,'abc.html')
		#raise e
		return [None,'',False]
	return [map(lambda x:x.get("href"),result),next_page_url,is_break]

#获取产品详细信息
def get_product_info(p_info_url):
	p_info=model_product.ProductModel()
	status_code=200
	html=''
	try:
		html,status_code=basic.get_html(p_info_url)
		content=etree.HTML(html)
		#asin=content.xpath('//input[@name="ASIN" and @type="hidden"]')[0].get("value")
		m=re.match('^(http|https)://www\.amazon\.in(/[0-9a-zA-Z\-_]+)?/dp/([0-9a-zA-Z]+)(.+)$',p_info_url)
		asin=m.group(3)
		name=content.xpath("//span[@id='productTitle']")[0].text.strip()
		score_el=content.xpath("//a[@class='a-popover-trigger a-declarative']/i/span")
		score=score_el[0].text.strip() if len(score_el)>0 else '0'
		comments_el=content.xpath("//span[@id='acrCustomerReviewText']")
		comments=comments_el[0].text.strip() if len(comments_el)>0 else '0'
		price_el=content.xpath("//td[@class='a-span12']/span[@class='a-size-medium a-color-price']/text()")
		if len(price_el)>0:
			price=price_el[0].getparent().tail
		else:
			price_el=content.xpath("//div[@id='olp_feature_div']/div/span/span[@class='a-color-price']/text()")
			if len(price_el)>0:
				price=price_el[0].getparent().tail
			else:
				price='0'
			
		price=price.replace(',','')
		
		color_el=content.xpath("//div[@id='variation_color_name']/div[@class='a-row']/span[@class='selection']")
		color=color_el[0].text.strip() if len(color_el)>0 else ''
		
		p_info.id=str(uuid.uuid1())
		p_info.name=name
		p_info.asin=asin
		p_info.score=float(score.replace("out of 5 stars","").strip())
		p_info.comments=int(comments.replace(',','').replace("customer reviews","").replace("customer review","").strip())
		p_info.price=price
		p_info.color=color
		p_info.adddate=str(datetime.now())
		p_info.url=p_info_url;
	except  requests.exceptions.Timeout as e:
		print 'request connection timeout error ,product info error url:'+p_info_url
		logging.exception('request connection timeout error ,product info error url:'+p_info_url)
		return None
	except  requests.exceptions.ConnectionError as e:
		print 'request connection error ,product info error url:'+p_info_url
		logging.exception('request connection error ,product info error url:'+p_info_url)
		return None
	except  requests.exceptions.RequestException as e:
		print 'request timeout ,product info error url:'+p_info_url+',status_code:'+str(status_code)
		logging.exception('request timeout,product info error url:'+p_info_url+',status_code:'+str(status_code))
		return None
	except IndexError as e:
		print e
		time.sleep(5)
		return None
	except BaseException as e:
		print 'product info error url:'+p_info_url+',status_code:'+str(status_code)
		logging.exception('product info error url:'+p_info_url+',status_code:'+str(status_code))
		#basic.html_write(html,'abc.html')
		#raise e
		return None
	global has_p_info_pages
	has_p_info_pages=has_p_info_pages+1
	return p_info
#分页扑爬取产品列表页
def go_p_list_page(p_list_url):
	next_page_url=''
	p_info_urls=''
	url=p_list_url
	p_data=''
	is_break=False
	while True:
		#product info page url on the product list page
		p_info_urls,next_page_url,is_break=get_product_info_urls(url)
		#每抓取一页产品列表页切换一次代理
		change_proxy()
		if p_info_urls==None:
			time.sleep(1)
			continue
		
		all_thread=[]
		
		for info_url in p_info_urls:
			time.sleep(1)
			#add_product(info_url)
			thread=threading.Thread(target=add_product,args=(info_url,))
			all_thread.append(thread)
			thread.start()
		for thread in all_thread:
			thread.join()
		if 	next_page_url=='':
			logging.info('end of product list page,break:'+url)
			print 'end of product list page,break:'+url
			break
		else:
			url=next_page_url
			logging.info('product list next page:'+url+",p_info_urls length:")
			print 'product list next page:'+url+",p_info_urls length:"
#添加产品到数据库
def add_product(info_url):
	while True:
		model=get_product_info(info_url)
		#每抓取一页产品详细页切换一次代理
		change_proxy()
		if model!=None:
			try:
				p_data= json.dumps(model,default=model_product.productmodel2dict)
				db_product.add(model)
			except BaseException as e:
				logging.exception('error product info url:'+info_url)
				logging.exception('error product info data:'+p_data)
				print 'error product info url:'+info_url
				print 'error product info data:'+p_data
				raise e
			logging.info(p_data+"\n")
			print(p_data+"\n")
			break
		else:
			print 'can\'t get product info,product info url:'+info_url
			logging.info('can\'t get product info,product info url:'+info_url)
			continue
	
#启用代理
def set_proxy_enable():
	set_proxy()
#设置代理信息
def set_proxy():
	#设置代理信息
	print 'setting ip proxy for request....\n'
	newest_verified_proxy_ips=libhttpproxy.get_verified_proxies(150)
	verified_proxies_num=len(newest_verified_proxy_ips)
	if verified_proxies_num==0:
		config.enable_proxy=False
		logging.info('Can\' enable proxy,because no verified proxies\n')
		print 'Can\' enable proxy,because no verified proxies\n'
		return
	else:
		config.enable_proxy=True
	if config.current_proxy_index!=0 and config.current_proxy_index>=verified_proxies_num:
		config.current_proxy_index=0
	verified_proxy=newest_verified_proxy_ips[0];
	config.proxies={verified_proxy.Protocol:verified_proxy.IP+":"+str(verified_proxy.Port)}
	config.enable_proxy=True
	logging.info('Success enable proxy:'+str(config.current_proxy_index)+'\n')
	print 'Success enable proxy:'+str(config.current_proxy_index)+'\n'
#切换代理信息
def change_proxy():
	# if config.enable_proxy==False:
		# print 'didn\'t enable ip proxy,can\'t change ip proxy.'
		# return
	logging.info('change ip proxy....\n')
	print 'change ip proxy....\n'
	verified_proxies_num=libhttpproxy.get_verified_proxies_num()
	if config.current_proxy_index+1>=verified_proxies_num:
		config.current_proxy_index=0
	else:
		config.current_proxy_index=config.current_proxy_index+1
	set_proxy()
	if config.enable_proxy==True:
		logging.info('Success change ip proxy.\n' )
		print 'Success change ip proxy.\n' 
def set_logging():
	logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='amazon_mobile.log',
                filemode='w')

try:
	set_logging()
	set_proxy_enable()
	go_p_list_page(p_list_url)
	go_p_list_page(p_list_url1)
	go_p_list_page(p_list_url2)
	go_p_list_page(p_list_url3)
	#get_product_info('http://www.amazon.in/dp/B074PWHB1R/ref=s%20r_1_1014/262-4008005-9308516?s=electronics&ie=UTF8&qid=1502377276&sr=1-1014')
	#print json.dumps(get_product_info('http://www.amazon.in/dp/B074PWHB1R/ref=s%20r_1_1014/262-4008005-9308516?s=electronics&ie=UTF8&qid=1502377276&sr=1-1014'),default=model_product.productmodel2dict)
	#html=basic.get_html('http://www.amazon.in/Forme-N9-Selfie-Wireless-Mobile/dp/B071G2DSSC/ref=sr_1_142/257-5514151-9158917?s=electronics&rps=1&ie=UTF8&qid=1501400614&sr=1-142')
	#basic.html_write(html,'abc.html')
	#print html.encode('utf-8')
except BaseException as e:
	pass
finally:
	db_IPProxiesPoolApplicationSwitch.update(False)