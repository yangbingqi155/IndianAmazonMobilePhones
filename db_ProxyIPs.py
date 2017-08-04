#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db
import model_ProxyIPs
import json

def data_2_model(data):
	model=model_ProxyIPs.ProxyIPsModel()
	model.ID=data[0]
	model.IP=data[1]
	model.Country=data[2]
	model.Port=data[3]
	model.ServerAddresss=data[4]
	model.Anonymity=data[5]
	model.Protocol=data[6]
	model.Speed=data[7]
	model.ConnectSpeed=data[8]
	model.LastVerifiedTime=data[9]
	model.IsVerified=data[10]
	return model

def add(model):
	if len(get(model.IP,model.Port,model.Protocol))<=0:
		sql="INSERT INTO `IPProxies`.`ProxyIPs`(`ID`,`IP`,`Country`,`Port`,`ServerAddresss`,`Anonymity`,`Protocol`,`Speed`,`ConnectSpeed`,`LastVerifiedTime`,`IsVerified`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
		paras=(model.ID,model.IP,model.Country,model.Port,model.ServerAddresss,model.Anonymity,model.Protocol,model.Speed,model.ConnectSpeed,model.LastVerifiedTime,model.IsVerified)
		return True if db.excute_no_query(sql,paras)>0 else False
	else:
		return True
def move(ID):
	sql="delete from`IPProxies`.`ProxyIPs` where ID=%s"
	paras=(ID)
	return True if db.excute_no_query(sql,paras)>0 else False
	
def remove_by_ip(ip,port):
	sql="delete from `IPProxies`.`ProxyIPs` where ip=%s and port=%s"
	print port
	paras=(ip,port)
	return True if db.excute_no_query(sql,paras)>0 else False

def update_last_verified_time(ID,last_verified_time):
	sql="update `IPProxies`.`ProxyIPs` set LastVerifiedTime=%s,IsVerified=1 where ID=%s"
	paras=(last_verified_time,ID)
	return True if db.excute_no_query(sql,paras)>0 else False
def update_last_verified_time_by_ip(last_verified_time,ip,port):
	sql="update `IPProxies`.`ProxyIPs` set LastVerifiedTime=%s,IsVerified=1 where ip=%s and port=%s"
	paras=(last_verified_time,ip,port)
	return True if db.excute_no_query(sql,paras)>0 else False
	
def get_newest_verified_proxy_ips(top_num=0):
	paras=(int(top_num),)
	models=[]
	data=[]
	sql=''
	if top_num==0:
		sql="select *from `IPProxies`.`ProxyIPs` where IsVerified=1 order by LastVerifiedTime desc"
		data=db.select(sql)
	else:
		sql="select *from `IPProxies`.`ProxyIPs` where IsVerified=1 order by LastVerifiedTime desc  limit 0,%s"
		data=db.select(sql,paras)
	for item in data:
		model=data_2_model(item)
		models.append(model)
	return models
	
def get_verified_proxies_num():
	sql="select *from `IPProxies`.`ProxyIPs` where IsVerified=1"
	effect_rows=db.excute_no_query(sql)
	return effect_rows
	
def get(ip,port,protocol):
	sql="select *from `IPProxies`.`ProxyIPs` where ip=%s and port=%s and protocol=%s"
	paras=(ip,port,protocol)
	data=db.select(sql,paras)
	return data
	
def get_need_verified_proxis(top_num=0):
	sql=''
	data=[]
	paras=(top_num)
	models=[]
	if top_num==0:
		sql="select *from `IPProxies`.`ProxyIPs` order by IsVerified desc,LastVerifiedTime desc"
		data=db.select(sql)
	else:
		sql="select *from `IPProxies`.`ProxyIPs`  order by IsVerified desc,LastVerifiedTime desc limit 0,%d"
		data=db.select(sql,paras)
	for item in data:
		model=data_2_model(item)
		models.append(model)
	return models
	
def get_not_verified_proxis(top_num=0):
	sql=''
	data=[]
	paras=(top_num)
	models=[]
	if top_num==0:
		sql="select *from `IPProxies`.`ProxyIPs` where IsVerified=0 order by LastVerifiedTime desc"
		data=db.select(sql)
	else:
		sql="select *from `IPProxies`.`ProxyIPs` where IsVerified=0 order by LastVerifiedTime desc limit 0,%d"
		data=db.select(sql,paras)
	for item in data:
		model=data_2_model(item)
		models.append(model)
	return models