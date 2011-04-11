#-*- coding: utf-8 -*-

from kernel import plugin as pyplugin
from kernel import utils

from datetime import datetime
import os
import sys
import csv
#import codecs
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


	def set(self, data):
		if not data:
			print _('no data to save')
			self.error = _('no data to save')
			return


		for category in data:
			filename, fieldlist, elements = data[category]

			csvfilename = os.path.abspath(os.path.join(self.settings.option(self.name, 'outputpath'), '.'.join((filename, 'csv'))))
			print
			print _('updating %s') % (csvfilename,)

			encoding = self.settings.option(self.name, 'encoding') or 'utf-8'

			try:
				with open(csvfilename, 'wb+') as output:
					self.writer = csv.writer(output, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

					self.writer.writerow(fieldlist)

					for element in elements:
						self.writer.writerow([element[field].encode(encoding) for field in fieldlist])

			except IOError, e:
				self.error = e
				return


