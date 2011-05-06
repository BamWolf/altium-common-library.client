#-*- coding: utf-8 -*-

import os
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

		self.db = None
		self.cursor = None

		self.settings = OptionManager('msaccess.ini')

		if not self.settings.option('SETTINGS', 'outputpath'):
			raise AppException(_('no output path'))


	def connect(self):
		database = os.path.abspath(self.settings.option('SETTINGS', 'outputpath'))
		print _('updating %s') % (database,)

		try:
			self.db = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (database,))
			self.cursor = self.db.cursor()

		except pyodbc.Error, e:
			raise AppException(_('connecting error'))

		print _('connected %s') % (database,)


	def set(self, data):
		if not data:
			raise AppException(_('no data to save'))

		self.connect()

		for category in data:
			tablename, fieldlist, elements = data[category]

			columns = ', '.join([''.join(('[', s, ']')) for s in fieldlist])

			query = "INSERT INTO %s (%s) VALUES (%s);" % (tablename, columns, ', '.join('?'*len(fieldlist)))
	                print query

			for element in elements:
				raw = [element[i] for i in fieldlist]

				try:
					self.cursor.execute(query, raw)

				except pyodbc.IntegrityError:
					message = _('duplicate entry %s') % (raw,)
					print message
#					raise AppException(message)

#				except Exception, e:
#					raise AppException('other error')

		self.disconnect()
		print _('disconnected %s') % (self.settings.option('SETTINGS', 'outputpath', '', True),)


	def disconnect(self):
		if self.cursor:
			self.cursor.close()
			self.cursor = None

                if self.db:
			self.db.commit()
			self.db.close()
			self.cursor = None


	def __del__(self):
		if self.cursor:
			self.cursor.close()

		if self.db:
			self.db.close()