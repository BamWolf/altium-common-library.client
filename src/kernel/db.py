# -*- coding: utf-8 -*-

################################################################################

import os
import sqlite3

import inspect

#from kernel.objects import Component
#from kernel.objects import cParameter

from objects import Component
from objects import cParameter

from datetime import datetime


################################################################################

class database:

	def __init__(self, filename):
#		if not os.access(DBDIR, os.F_OK):
#			os.mkdir(DBDIR)

		self.db = sqlite3.connect(filename)
		self.cursor = self.db.cursor()


 
#	def __del__(self):
#		if self.cursor: self.cursor.close()
#		if self.db:
#			self.db.commit()
#			self.db.close()


 
	def query(self, *args, **kwargs):
		self.cursor.execute(*args, **kwargs)
		return self.cursor
 


	def commit(self):
		self.db.commit()


	def init(self):
		pass
		self.query('CREATE TABLE IF NOT EXISTS components (m VARCHAR(64), pn VARCHAR(64), PRIMARY KEY (m, pn))')
		self.query('CREATE TABLE IF NOT EXISTS parameters (id INTEGER NOT NULL, parameter VARCHAR(64), value VARCHAR(64), type INTEGER NOT NULL)')






	def set_manufacturers(self, manufacturer):
		print manufacturer


	def set_element(self, element):
		print element

		if not isinstance(element, Component):
			raise TypeError, 'should be Component instance'

		query = 'INSERT INTO components VALUES (?, ?)'
		self.query(query, (element.m, element.pn))

		id = self.cursor.lastrowid

		for p in element.parameters:
			q = 'INSERT INTO parameters VALUES (?, ?, ?, ?)'

			typelist = (basestring, int, datetime)

			for i in xrange(len(typelist)):
				if isinstance(p.value, typelist[i]):
					t = i
					break

			self.query(q, (id, p.name, p.value, p.type))




	def get_elements(self):

#		print self.query('select rowid, m ,pn from components').fetchall()
#		print self.query('select * from parameters').fetchall()




		elements = self.query('select rowid, m, pn from components').fetchall()

		data = []

		for element in elements:
			i = Component(element[1], element[2])
			id = element[0]
			parameters = self.query('select * from parameters where id = ?', str(id)).fetchall()

			for parameter in parameters:
				p = cParameter(parameter[1], parameter[2], parameter[3])
				i.add_parameter(p)

			data.append(i)

		return data



if __name__ == '__main__':

	print 'TESTING'

	i = database('../data/pyjick.db')
	i.init()

	el = Component(u'Taiwan', u'cr0805')
	el.add_parameter(cParameter(u'Voltage', u'50', u'float'))
	el.add_parameter(cParameter(u'Tolerance', u'10', u'float'))
	el.add_parameter(cParameter(u'Standard', u'IEEE', u'string'))

	i.set_element(el)

	el = Component(u'exUSSR', u'С-33Н')
	el.add_parameter(cParameter(u'Voltage', u'25', u'float'))
	el.add_parameter(cParameter(u'Tolerance', u'5', u'float'))

	i.set_element(el)

	data = i.get_elements()

	print data

