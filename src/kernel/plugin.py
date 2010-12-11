#-*- coding: utf-8 -*-

import ConfigParser

class plugin(object):
	name = 'Plugin Metaclass'

	def __init__(self):
		self.name = 'Plugin'
		self.cfgfilename = 'plugin.ini'

		self.error = None

		self.modified = False
