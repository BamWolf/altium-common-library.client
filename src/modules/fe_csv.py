#-*- coding: utf-8 -*-

from kernel import plugin as pyplugin
from kernel.optionmgr import OptionManager

from datetime import datetime
import sys
import csv
import codecs
import inspect

from kernel import i18n



class CSVWriter(pyplugin.plugin):

	def __init__(self):
		self.name = 'CSV'
		self.cfgfilename = 'plugins.ini'

		self.writer = None

		self.error = None
		self.modified = False

		self.settings = OptionManager(self.cfgfilename)

		self.initialize()



	def initialize(self):
		if not self.settings.option(self.name, 'output file', '', True):
			self.error = _('no output')


	def stringize(self, s):

#		print s
		if isinstance(s, datetime):
			return s.isoformat(' ')

		elif isinstance(s, bool) or isinstance(s, int) or isinstance(s, float):
			return str(s)

		elif s is None:
			return ''

		else:
			return s



	def get(self, date=None):
		print _('not implemented')



	def set(self, category, fieldlist, data):
		if not data or not fieldlist:
			print _('no data to save')
			self.error = _('no data to save')
			return

		print _('updating %s') % (self.settings.option(self.name, 'output file', '', True),)

		try:
			output = open(self.settings.option(self.name, 'output file', '', True), 'wb')
			self.writer = csv.writer(output, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
		except IOError, e:
			self.error = e
			return

#		try:
		self.writer.writerow(fieldlist)

		for item in data:
			self.writer.writerow([self.stringize(s).encode('utf-8') for s in item])
#			self.writer.writerow([s.encode('utf-8') for s in item])

#		except Exception, e:
#			self.error = e
#			return




