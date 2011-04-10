#-*- coding: utf-8 -*-

from kernel import plugin as pyplugin
from kernel import utils

from datetime import datetime
import os
import sys
import csv
import codecs
import inspect

#from kernel import i18n

def _(s):
	return s

class CSVWriter(pyplugin.plugin):

	def __init__(self):
		self.name = 'CSV'
		self.cfgfilename = 'data.ini'

		self.writer = None

		self.error = None
		self.modified = False

		self.settings = utils.OptionManager(self.cfgfilename)

#		self.initialize()



	def initialize(self):
		if not self.settings.option(self.name, 'outputpath', 'data/'):
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


	def set(self, data):
		if not data:
			print _('no data to save')
			self.error = _('no data to save')
			return


		for category in data:

			csvfilename = os.path.abspath(os.path.join(self.settings.option(self.name, 'outputpath'), '.'.join((category, 'csv'))))
			print
			print _('updating %s') % (csvfilename,)

			encoding = self.settings.option(self.name, 'encoding') or 'utf-8'

#			try:
			with open(csvfilename, 'wb+') as output:
				self.writer = csv.writer(output, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

#			except IOError, e:
#				self.error = e
#				return

#			try:
				self.writer.writerow(data[category][0].keys())

				for element in data[category]:
#					self.writer.writerow([self.stringize(element[s]).encode(encoding) for s in fieldlist])
					self.writer.writerow([element[field].encode('utf-8') for field in element])


