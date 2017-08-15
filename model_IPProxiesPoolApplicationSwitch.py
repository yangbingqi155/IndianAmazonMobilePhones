#!/usr/bin/env python
# -*- coding: utf-8 -*-

def IPProxiesPoolApplicationSwitchModel2dict(switch):
	return {
		'Excute':switch.Excute
	}

class IPProxiesPoolApplicationSwitchModel:

	@property
	def Excute(self):
		return self.Excute
	@Excute.setter
	def Excute(self,value):
		self.Excute=value
