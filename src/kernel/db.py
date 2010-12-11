# -*- coding: utf-8 -*-

################################################################################

import os
import sqlite3

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



	def set(self, data):
		print data

		#data -> [{'id':{}, 'parameters':{}}]

		for element in data:
			print element['id']['m'], element['id']['pn']

			query = 'INSERT INTO components VALUES (?, ?)'
			self.query(query, (element['id']['m'], element['id']['pn']))

			id = self.cursor.lastrowid

			for p in element['parameters']:
				q = 'INSERT INTO parameters VALUES (?, ?, ?, ?)'

				typelist = (basestring, int, datetime)

				for i in xrange(len(typelist)):
					if isinstance(element['parameters'][p], typelist[i]):
						t = i
						break

				self.query(q, (id, p, element['parameters'][p], t))

			print self.query('select rowid, m ,pn from components').fetchall()
			print self.query('select * from parameters').fetchall()



	def get(self):

		pass
		#data -> [{'id':{}, 'parameters':{}}]

#		return data

"""
		for element in data:
			print element['id']['m'], element['id']['pn']

			query = 'INSERT INTO components VALUES (?, ?)'
			self.query(query, (element['id']['m'], element['id']['pn']))

			id = self.cursor.lastrowid

			for p in element['parameters']:
				q = 'INSERT INTO parameters VALUES (?, ?, ?, ?)'

				typelist = (basestring, int, datetime)

				for i in xrange(len(typelist)):
					if isinstance(element['parameters'][p], typelist[i]):
						t = i
						break

				self.query(q, (id, p, element['parameters'][p], t))

			print self.query('select rowid, m ,pn from components').fetchall()
			print self.query('select * from parameters').fetchall()
"""



if __name__ == '__main__':

	print 'TESTING'

	i = database('../data/pyjick.db')

	data = 	[{
			'id':	{
				'm': 'Taiwan',
				'pn': 'cr0805',
				'a': 'Jack Krieger',
				'r': u'Василий'
				},

			'parameters':	{
						'Voltage': 50,
						'Tolerance': 10,
						'Standard': 'IEEE'
						}
			},
			{
			'id':	{
				'm': 'exUSSR',
				'pn': u'С-33Н',
				'a': 'Jack Krieger',
				'r': u'Василий'
				},

			'parameters':	{
						'Voltage': 25,
						'Tolerance': 5
						}
			}]


	i.init()
	i.set(data)
