# -*- coding: utf-8 -*-

################################################################################

import os
import sqlite3
import inspect

from datetime import datetime

from kernel import objects
#import objects

################################################################################

class Database:

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

	def close(self):
		if self.cursor: self.cursor.close()
		if self.db:
#			self.db.commit()
			self.db.close()


	def init(self):
#		print u'Инициализация'

		# создание таблицы компонентов и параметров
		self.query('CREATE TABLE IF NOT EXISTS components (manufacturer INTEGER, number VARCHAR(64), UNIQUE (manufacturer, number))')
		self.query('CREATE TABLE IF NOT EXISTS parameters (id INTEGER NOT NULL, parameter VARCHAR(64), value VARCHAR(64), type INTEGER NOT NULL)')

		# создание таблицы производителей
		self.query('CREATE TABLE IF NOT EXISTS manufacturers (manufacturer VARCHAR(128))')

		# создание таблицы символов, корпусов и моделей
		self.query('CREATE TABLE IF NOT EXISTS symbols (symbol VARCHAR(64))')
		self.query('CREATE TABLE IF NOT EXISTS packages (package VARCHAR(64))')
		self.query('CREATE TABLE IF NOT EXISTS models (model VARCHAR(64))')

		self.commit()


	def test(self):
		for item in ('CAP', 'RES', 'VD', 'TRANS_PNP'):
			self.set_symbol(item)

		for item in ('D2PAK', 'CR1206', 'CC0805', 'CC1206'):
			self.set_package(item)

		for item in ('CAP', 'RES'):
			self.set_model(item)



	### таблица компонентов и параметров ###

	def set_element(self, element):

		if not isinstance(element, objects.Component):
			raise TypeError, 'Component instance expected, %s instance given' % (type(element),)

		man_id = self.get_man(element.manufacturer)

		print man_id

		if not man_id:
			man_id = self.set_man(element.manufacturer)

		query = 'INSERT INTO components VALUES (?, ?)'
		self.query(query, (man_id, element.number))

		id = self.cursor.lastrowid

		for parameter, value in element.get():
			query = 'INSERT INTO parameters VALUES (?, ?, ?, ?)'
			self.query(query, (id, parameter, value, 'string'))




	def get_elements(self):

		elements = self.query('SELECT rowid, manufacturer, number FROM components').fetchall()

		data = []

		for id, man_id, number in elements:

#			symbol = (lambda x: x and x[0] or None)(self.query('SELECT symbol FROM symbols WHERE id = ?', (sid,)).fetchone())
#			package = (lambda x: x and x[0] or None)(self.query('SELECT package FROM packages WHERE id = ?', (pid,)).fetchone())
#			model = (lambda x: x and x[0] or None)(self.query('SELECT model FROM models WHERE id = ?', (mid,)).fetchone())

			manufacturer = self.get_man(id=man_id)# or 'Unknown'

			i = objects.Component(manufacturer, number)

			parameters = self.query('SELECT * FROM parameters where id = ?', str(id)).fetchall()

			for id, parameter, value, mode in parameters:
				i.set(parameter, value, mode)

			data.append(i)

		return data



	### таблица производителей ###

	def set_man(self, manufacturer):

		self.query('INSERT INTO manufacturers (manufacturer) VALUES (?)', (manufacturer,))
		self.commit()

		result = self.cursor.lastrowid

		return result



	def get_man(self, manufacturer=None, id=None):
		print 'manufacturer', manufacturer
		print 'id', id

#		print 'TABLE', self.query('SELECT * FROM manufacturers').fetchall()

		if manufacturer:
			query = 'SELECT rowid FROM manufacturers WHERE manufacturer = ?'
			answer = self.query(query, (manufacturer,)).fetchone()
			print 'man2id:', answer
			result = answer and answer[0]

		elif id:
			query = 'SELECT manufacturer FROM manufacturers WHERE rowid = ?'
			answer = self.query(query, (id,)).fetchone()
			print 'id2man:', answer
			result = answer and answer[0]

		else:
			answer = self.query('SELECT manufacturer FROM manufacturers').fetchall()

			result = []
			for i in answer:
				result.append(i[0])

		return result





	# таблица символов

	def set_symbol(self, symbol):

		self.query('INSERT INTO symbols (symbol) VALUES (?)', (symbol,))
		id = self.cursor.lastrowid
		self.commit()

		return id


	def get_symbols(self):
		answer = self.query('SELECT symbol FROM symbols').fetchall()

		result = []
		for i in answer:
			result.append(i[0])

		return result



	def get_symbol(self, name):
		answer = self.query('SELECT rowid FROM symbols WHERE symbol = ?', (name,)).fetchone()

		result = answer and answer[0] or None

		print result
		return result


	### таблица корпусов ###

	def set_package(self, package):

		self.query('INSERT INTO packages (package) VALUES (?)', (package,))
		id = self.cursor.lastrowid
		self.commit()

		return id


	def get_packages(self):
		answer = self.query('SELECT package FROM packages').fetchall()

		result = []
		for i in answer:
			result.append(i[0])

		return result

	### таблица моделей ###

	def set_model(self, model):

		self.query('INSERT INTO models (model) VALUES (?)', (model,))
		id = self.cursor.lastrowid
		self.commit()

		return id


	def get_models(self):
		answer = self.query('SELECT model FROM models').fetchall()

		result = []
		for i in answer:
			result.append(i[0])

		return result


if __name__ == '__main__':

	db = Database('data/pyclient.db')
	db.init()
	db.test()
