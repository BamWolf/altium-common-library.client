#-*- coding: utf-8 -*-

from kernel import plugin as pyplugin
from kernel import utils

from datetime import datetime
import pyodbc
import os

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


	def set(self, data):
		if not data:
			print _('no data to save')
			self.error = _('no data to save')
			return

		for category in data:
			database = os.path.abspath(self.settings.option(self.name, 'outputpath'))
			print
			print _('updating %s') % (database,)

			self.connect(database)

			if self.error:
				return

			print _('connected %s') % (database,)

			table, fieldlist, elements = data[category]
			fields = ', '.join([''.join(('[', s, ']')) for s in fieldlist])

			query = "INSERT INTO %s (%s) VALUES (%s);" % (table, fields, ', '.join('?'*len(fieldlist)))
			print query

			for element in elements:
				try:
					self.cursor.execute(query, [element[i] for i in fieldlist])

				except pyodbc.IntegrityError:
					print _('duplicate entry %s') % (element,)

				except Exception, e:
					self.error = e
					print e
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
