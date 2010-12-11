#-*- coding: utf-8 -*-

from kernel import plugin as pyplugin
from kernel.optionmgr import OptionManager

import pyodbc

from kernel import i18n



class SQLDB(pyplugin.plugin):
	name = 'Global DB'

	def __init__(self):
		self.name = 'SOURCE'
		self.cfgfilename = 'pyuploader.ini'

		self.db = None
		self.cursor = None

		self.error = None

		self.cfg = None
		self.modified = False

		self.settings = OptionManager(self.cfgfilename)
		self.initialize()


	def initialize(self):
		if not self.settings.option(self.name, 'database', '', True):
			self.error = _('no output')



	def connect(self):
		database = self.settings.option(self.name, 'database', '', True)
#		print database

		if not database:
			self.error = _('no database')
			return

		self.db = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % (database))
		self.cursor = self.db.cursor()
		print 'Connected to "%s"' % (database,)



	def set(self, category, fieldlist, data):
		pass



	def get(self, category, fieldlist):
		self.connect()

		query = 'SELECT %s FROM %s;' % (', '.join( (''.join( ('[', s, ']') ) for s in fieldlist ) ), ''.join( ('[', category, ']') ))

		print query

		update = self.cursor.execute(query)#, fieldlist)

		return update.fetchall()



	def query(self, *args):
		return self.cursor.execute(*args)



	def commit(self):
		self.db.commit()



	def close(self):
		if self.cursor:
			self.cursor.close()
			self.cursor = None

		if self.db:
#			self.db.commit()
			self.db.close()
			self.db = None

		print 'Disconnected from "%s"' % (self.settings.option(self.name, 'database'),)



	def __del__(self):
		if self.cursor: self.cursor.close()
		if self.db:
			self.db.close()
