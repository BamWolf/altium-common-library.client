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
		self.query('CREATE TABLE IF NOT EXISTS components (manufacturer VARCHAR(64), number VARCHAR(64), description VARCHAR(255), link VARCHAR (255), UNIQUE (manufacturer, number))')
		self.query('CREATE TABLE IF NOT EXISTS parameters (id INTEGER NOT NULL, parameter VARCHAR(64), value VARCHAR(64), type INTEGER NOT NULL)')

		# создание таблицы производителей
		self.query('CREATE TABLE IF NOT EXISTS manufacturers (id INTEGER PRIMARY KEY, manufacturer VARCHAR(128))')

		# создание таблицы символов, корпусов и моделей
		self.query('CREATE TABLE IF NOT EXISTS symbols (id INTEGER PRIMARY KEY, symbol VARCHAR(64))')
		self.query('CREATE TABLE IF NOT EXISTS packages (id INTEGER PRIMARY KEY, package VARCHAR(64))')
		self.query('CREATE TABLE IF NOT EXISTS models (id INTEGER PRIMARY KEY, model VARCHAR(64))')

#		self.commit()


	### таблица компонентов и параметров ###

	def set_element(self, element):

		if not isinstance(element, Component):
			raise TypeError, 'should be Component instance'

		query = 'INSERT INTO components VALUES (?, ?, ?, ?)'
		self.query(query, (element.manufacturer, element.number, element.description, None))

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

#		print self.query('SELECT rowid, manufacturer, number, description, link FROM components').fetchall()
#		print self.query('SELECT * FROM parameters').fetchall()




		elements = self.query('SELECT rowid, manufacturer, number, description, link FROM components').fetchall()

		data = []

		for element in elements:
			i = Component(element[1], element[2])

			# добавляем предустановленные параметры (строковый тип)
			i.add_parameter(cParameter('Description', element[3] or '', 'string'))
			i.add_parameter(cParameter('URL', element[4] or '', 'string'))

			id = element[0]
			parameters = self.query('SELECT * FROM parameters where id = ?', str(id)).fetchall()

			for parameter in parameters:
				p = cParameter(parameter[1], parameter[2], parameter[3])
				i.add_parameter(p)

			data.append(i)

		return data


	### таблица производителей ###

	def set_manufacturer(self, manufacturer):
		self.query('INSERT INTO manufacturers (id, manufacturer) VALUES (?, ?)', (None, manufacturer))
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

		self.query('INSERT INTO symbols (id, symbol) VALUES (?, ?)', (None, symbol))
		id = self.cursor.lastrowid

		return id


	def get_symbols(self):
		answer = self.query('SELECT symbol FROM symbols').fetchall()

		result = []
		for i in answer:
			result.append(i[0])

		return result


	### таблица корпусов ###

	def set_package(self, package):

		self.query('INSERT INTO packages (id, package) VALUES (?, ?)', (None, package))
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

		self.query('INSERT INTO models (id, model) VALUES (?, ?)', (None, model))
		id = self.cursor.lastrowid

		return id


	def get_models(self):
		answer = self.query('SELECT model FROM models').fetchall()

		result = []
		for i in answer:
			result.append(i[0])

		return result
