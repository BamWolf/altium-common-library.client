#-*- coding: utf-8 -*-

import pyodbc

from kernel.abstract import AppException
from kernel.utils import OptionManager

#from kernel import i18n

######################################

def _(s):
	return s

class MDBExporter():
	name = 'msaccess'

	def __init__(self):
		self.settings = OptionManager('msaccess.ini')

		if not self.settings.option('SETTINGS', 'outputpath'):
			raise AppException(_('no output path'))

	def set(self, data):
		if not data:
			raise AppException(_('no data to save'))

		for category in data:
			tablename, fieldlist, elements = data[category]

			print tablename
