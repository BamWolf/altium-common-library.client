# -*- coding: utf-8 -*-

################################################################################

import os
import sqlite3
import inspect

from datetime import datetime

from kernel.objects import Component
from kernel.objects import cParameter

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


	def init(self):
#		print u'Инициализация'

		# создание таблицы компонентов и параметров
		self.query('CREATE TABLE IF NOT EXISTS components (manufacturer VARCHAR(64), number VARCHAR(64), UNIQUE (manufacturer, number))')
		self.query('CREATE TABLE IF NOT EXISTS parameters (id INTEGER NOT NULL, parameter VARCHAR(64), value VARCHAR(64), type INTEGER NOT NULL)')

		# создание таблицы производителей
		self.query('CREATE TABLE IF NOT EXISTS manufacturers (id INTEGER PRIMARY KEY, manufacturer VARCHAR(128))')

		# создание таблицы символов, корпусов и моделей
		self.query('CREATE TABLE IF NOT EXISTS symbols (symbol VARCHAR(64))')
		self.query('CREATE TABLE IF NOT EXISTS packages (package VARCHAR(64))')
		self.query('CREATE TABLE IF NOT EXISTS models (model VARCHAR(64))')

#		self.test()

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

		if not isinstance(element, Component):
			raise TypeError, 'should be Component instance'

#		sid = (lambda x: x and x[0] or None)(self.query('SELECT id FROM symbols WHERE symbol = ?', (element.get('SYM').value,)).fetchone())
#		pid = (lambda x: x and x[0] or None)(self.query('SELECT id FROM packages WHERE package = ?', (element.get('PKG').value,)).fetchone())
#		mid = (lambda x: x and x[0] or None)(self.query('SELECT id FROM models WHERE model = ?', (element.get('MDL').value,)).fetchone())

#		print sid, pid, mid

		query = 'INSERT INTO components VALUES (?, ?)'
		self.query(query, (element.manufacturer, element.number))

		id = self.cursor.lastrowid

		for key in element.parameters.keys():
			p = element.parameters[key]
			q = 'INSERT INTO parameters VALUES (?, ?, ?, ?)'

#			for i in xrange(len(typelist)):
#				if isinstance(p.value, typelist[i]):
#					t = i
#					break

			self.query(q, (id, p.name, p.value, p.type))




	def get_elements(self):

		elements = self.query('SELECT rowid, manufacturer, number FROM components').fetchall()

		data = []

		for id, manufacturer, number in elements:

#			symbol = (lambda x: x and x[0] or None)(self.query('SELECT symbol FROM symbols WHERE id = ?', (sid,)).fetchone())
#			package = (lambda x: x and x[0] or None)(self.query('SELECT package FROM packages WHERE id = ?', (pid,)).fetchone())
#			model = (lambda x: x and x[0] or None)(self.query('SELECT model FROM models WHERE id = ?', (mid,)).fetchone())


			i = Component(manufacturer, number)

			parameters = self.query('SELECT * FROM parameters where id = ?', str(id)).fetchall()

			for id, parameter, value, mode in parameters:
				p = cParameter(parameter, value, mode)
				i.set(p)

			data.append(i)

		return data


	### таблица производителей ###

	def set_manufacturer(self, manufacturer):
		self.query('INSERT INTO manufacturers (manufacturer) VALUES (?)', (manufacturer))
		id = self.cursor.lastrowid

		return id



	def get_manufacturers(self):
		answer = self.query('SELECT manufacturer FROM manufacturers').fetchall()

		result = []
		for i in answer:
			result.append(i[0])

		return result





	# таблица символов

	def set_symbol(self, symbol):

		self.query('INSERT INTO symbols (symbol) VALUES (?)', (symbol,))
		id = self.cursor.lastrowid

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

		return id


	def get_models(self):
		answer = self.query('SELECT model FROM models').fetchall()

		result = []
		for i in answer:
			result.append(i[0])

		return result
