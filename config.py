#!/usr/bin/env python
# -*- coding: utf-8 -*-

#domain
galobal_domain='http://www.amazon.in'
#enable proxy
enable_proxy=False
#proxies-读取verified.txt文件
proxies = {
  "https": "http://41.118.132.69:4433"
}
#proxies当前使用代理的索引
current_proxy_index=0
#web page response time out
response_time_out=100

#抓取产品详细页面的线程数
threads_of_request_product_info=4