#!/usr/bin/env python
# -*- coding: utf-8 -*-

def productmodel2dict(product):
	return {
		'id':product.id,
		'name':product.name,
		'score':product.score,
		'comments':product.comments,
		'price':product.price,
		'color':product.color,
		'asin':product.asin,
		'adddate':product.adddate,
		'url':product.url
	}

class ProductModel:
	# def __init__(self,name,score,comments,price,color):
		# pass
		# self.name=name
		# self.score=score
		# self.comments=comments
		# self.price=price
		# self.color=color
	@property
	def id(self):
		return self.id
	@id.setter
	def id(self,value):
		self.id=value

	@property
	def name(self):
		return self.name
	@name.setter
	def name(self,value):
		self.name=value
	
	@property
	def score(self):
		return self.score
	@score.setter
	def score(self,value):
		self.score=value
		
	@property
	def comments(self):
		return self.comments
	@comments.setter
	def comments(self,value):
		self.comments=value
		
	@property
	def price(self):
		return self.price
	@price.setter
	def price(self,value):
		self.price=value
		
	@property
	def color(self):
		return self.color
	@color.setter
	def color(self,value):
		self.color=value
		
	@property
	def asin(self):
		return self.asin
	@asin.setter
	def asin(self,value):
		self.asin=value	

	@property
	def adddate(self):
		return self.adddate
	@adddate.setter
	def adddate(self,value):
		self.adddate=value	
	
	@property
	def url(self):
		return self.url
	@url.setter
	def url(self,value):
		self.url=value	