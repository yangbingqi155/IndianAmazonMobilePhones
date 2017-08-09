#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db
import model_product
import json

def data_2_model(data):
	model=model_product.ProductModel()
	model.ID=data[0]
	model.name=data[1]
	model.score=data[2]
	model.comments=data[3]
	model.price=data[4]
	model.color=data[5]
	model.asin=data[6]
	model.adddate=data[7]
	model.url=data[8]
	return model

def add(model):
	if len(get(model.id))<=0:
		sql="INSERT INTO `IPProxies`.`product`(`id`,`name`,`score`,`comments`,`price`,`color`,`asin`,`adddate`,`url`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
		paras=(model.id,model.name.encode('utf-8'),model.score,model.comments,model.price,model.color,model.asin,model.adddate,model.url)
		return True if db.excute_no_query(sql,paras)>0 else False
	else:
		return True
def move(ID):
	sql="delete from`IPProxies`.`product` where id=%s"
	paras=(ID)
	return True if db.excute_no_query(sql,paras)>0 else False
	
def remove_by_asin(asin):
	sql="delete from `IPProxies`.`product` where asin=%s"
	paras=(asin,)
	return True if db.excute_no_query(sql,paras)>0 else False
	
def get(ID):
	sql="select *from `IPProxies`.`product` where id=%s"
	paras=(ID,)
	data=db.select(sql,paras)
	return data	
	
def get_by_asin(asin):
	sql="select *from `IPProxies`.`product` where asin=%s"
	paras=(asin,)
	data=db.select(sql,paras)
	return data
