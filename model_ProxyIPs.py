#!/usr/bin/env python
# -*- coding: utf-8 -*-

def proxyidmodel2dict(proxy_ip):
	return {
		'ID':proxy_ip.ID,
		'IP':proxy_ip.IP,
		'Country':proxy_ip.Country,
		'Port':proxy_ip.Port,
		'ServerAddresss':proxy_ip.ServerAddresss,
		'Anonymity':proxy_ip.Anonymity,
		'Protocol':proxy_ip.Protocol,
		'Speed':proxy_ip.Speed,
		'ConnectSpeed':proxy_ip.ConnectSpeed,
		'LastVerifiedTime':proxy_ip.LastVerifiedTime,
		'IsVerified':proxy_ip.IsVerified
	}

class ProxyIPsModel:

	@property
	def ID(self):
		return self.ID
	@ID.setter
	def ID(self,value):
		self.ID=value
	
	@property
	def IP(self):
		return self.IP
	@IP.setter
	def IP(self,value):
		self.IP=value
		
	@property
	def Country(self):
		return self.Country
	@Country.setter
	def Country(self,value):
		self.Country=value
		
	@property
	def Port(self):
		return self.Port
	@Port.setter
	def Port(self,value):
		self.Port=value
		
	@property
	def ServerAddresss(self):
		return self.ServerAddresss
	@ServerAddresss.setter
	def ServerAddresss(self,value):
		self.ServerAddresss=value
		
	@property
	def Anonymity(self):
		return self.Anonymity
	@Anonymity.setter
	def Anonymity(self,value):
		self.Anonymity=value
	
	@property
	def Protocol(self):
		return self.Protocol
	@Protocol.setter
	def Protocol(self,value):
		self.Protocol=value
			
	@property
	def Speed(self):
		return self.Speed
	@Speed.setter
	def Speed(self,value):
		self.Speed=value
			
	@property
	def ConnectSpeed(self):
		return self.ConnectSpeed
	@ConnectSpeed.setter
	def ConnectSpeed(self,value):
		self.ConnectSpeed=value
			
	@property
	def LastVerifiedTime(self):
		return self.LastVerifiedTime
	@LastVerifiedTime.setter
	def LastVerifiedTime(self,value):
		self.LastVerifiedTime=value
			
	@property
	def IsVerified(self):
		return self.IsVerified
	@IsVerified.setter
	def IsVeried(self,value):
		self.IsVerified=value
