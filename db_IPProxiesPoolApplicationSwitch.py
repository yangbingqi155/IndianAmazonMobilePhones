#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db
import model_IPProxiesPoolApplicationSwitch
import json

def data_2_model(data):
	model=model_IPProxiesPoolApplicationSwitch.IPProxiesPoolApplicationSwitchModel()
	model.Excute=data[0]
	return model

def add(model):
	sql="INSERT INTO `IPProxies`.`IPProxiesPoolApplicationSwitch`(`Excute`)VALUES(%s);"
	paras=(model.Excute,)
	return True if db.excute_no_query(sql,paras)>0 else False

def update(excute):
	sql="update `IPProxies`.`IPProxiesPoolApplicationSwitch` set excute=%s"
	paras=(excute,)
	return True if db.excute_no_query(sql,paras)>0 else False
	
def get():
	models=[]
	sql="select Excute from `IPProxies`.`IPProxiesPoolApplicationSwitch`;"
	data=db.select(sql)
	for item in data:
		model=data_2_model(item)
		models.append(model)
	return models[0]
