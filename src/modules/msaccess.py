#-*- coding: utf-8 -*-

from kernel import plugin as pyplugin
from kernel import utils

from datetime import datetime
import pyodbc

#from kernel import i18n

def _(s):
	return s


class MDBWriter(pyplugin.plugin):

	def __init__(self):
		self.name = 'MS Access'
		self.cfgfilename = 'data.ini'

		self.db = None
		self.cursor = None

		self.error = None
		self.modified = False

		self.settings = utils.OptionManager(self.cfgfilename)

#		self.initialize()



	def initialize(self):
		if not self.settings.option(self.name, 'outputpath', ''):
			self.error = _('no output')


	def connect(self, database):
		try:
			self.db = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (database,))
			self.cursor = self.db.cursor()

		except pyodbc.Error, e:
			self.error = e



	def set(self, table, fieldlist, data):
		if not data or not fieldlist:
			print _('no data to save')
			self.error = _('no data to save')
			return

		database = self.settings.option(self.name, 'outputpath')
		print _('updating %s') % (database,)

		self.connect(database)

		if self.error:
			return

		print _('connected %s') % (database,)

		fields = ', '.join([''.join(('[', s, ']')) for s in fieldlist])

		print fields

		query = "INSERT INTO %s (%s) VALUES (%s);" % (table, fields, ', '.join('?'*len(fieldlist)))
		print query

		for item in data:
			element = [item[i] for i in fieldlist]
			print element

			try:
				self.cursor.execute(query, element)

			except pyodbc.IntegrityError:
				print _('duplicate entry %s') % (item,)

			except Exception, e:
				self.error = e
				return

		self.close()


	def close(self):
		if self.cursor:
			self.cursor.close()
			self.cursor = None

		if self.db:
			self.db.commit()
			self.db.close()
			self.db = None

		print _('disconnected %s') % (self.settings.option(self.name, 'output database', '', True),)



	def __del__(self):
		if self.cursor:
			self.cursor.close()

		if self.db:
			self.db.close()
