# -*- coding: utf-8 -*-

################################################################################

import os
import sqlite3
import inspect

from datetime import datetime

from kernel import objects

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
		self.query('CREATE TABLE IF NOT EXISTS components (manufacturer INTEGER, number VARCHAR(64), category VARCHAR(4), sent BOOLEAN, checked BOOLEAN, UNIQUE (manufacturer, number))')
		self.query('CREATE TABLE IF NOT EXISTS parameters (id INTEGER NOT NULL, parameter VARCHAR(64), value VARCHAR(64), type INTEGER NOT NULL)')

		# создание таблицы производителей
		self.query('CREATE TABLE IF NOT EXISTS manufacturers (manufacturer VARCHAR(128))')

		# создание таблицы символов, корпусов и моделей
		self.query('CREATE TABLE IF NOT EXISTS symbols (symbol VARCHAR(64))')
		self.query('CREATE TABLE IF NOT EXISTS packages (package VARCHAR(64))')
		self.query('CREATE TABLE IF NOT EXISTS models (model VARCHAR(64))')

		self.commit()




	def clear(self):
		for table in ('components', 'parameters', 'manufacturers', 'symbols', 'packages', 'models'):
			query = 'DELETE FROM %s' % (table,)
			self.query(query)

		self.commit()

		print 'TRUNCATED'



	### таблица компонентов и параметров ###

	def set_element(self, element, sent=False, exported=False):

		if not isinstance(element, objects.Component):
			raise TypeError, 'objects.Component instance expected, %s instance given' % (type(element),)

		def _convert(value):

			print 'typization'

			print value, type(value)

			if isinstance(value, datetime):
				return 2	#'datetime'

			elif isinstance(value, int):
				print 'int'
				return 1	#'float'

			elif isinstance(value, float):
				print 'float'
				return 1	#'float'

			elif isinstance(value, basestring):
				return 0	#'string'


		man_id = self.get_man(element.manufacturer)

		if not man_id:
			man_id = self.set_man(element.manufacturer)

		category = element.get('Category') or 'A'
		query = 'INSERT INTO components VALUES (?, ?, ?, ?, ?)'

		try:
			self.query(query, (man_id, element.number, category, sent, exported))

		except sqlite3.IntegrityError, e:
			print 'Duplicates Error:', e
			return

		id = self.cursor.lastrowid

		parameters = element.get()

		for parameter in parameters:
			query = 'INSERT INTO parameters VALUES (?, ?, ?, ?)'
			self.query(query, (id, parameter, parameters[parameter], _convert(parameters[parameter])))


	def get_elements(self):

		elements = self.query('SELECT rowid, manufacturer, number, category FROM components').fetchall()

		data = []

		for id, man_id, number, category in elements:

#			symbol = (lambda x: x and x[0] or None)(self.query('SELECT symbol FROM symbols WHERE id = ?', (sid,)).fetchone())
#			package = (lambda x: x and x[0] or None)(self.query('SELECT package FROM packages WHERE id = ?', (pid,)).fetchone())
#			model = (lambda x: x and x[0] or None)(self.query('SELECT model FROM models WHERE id = ?', (mid,)).fetchone())

			manufacturer = self.get_man(id=man_id)# or 'Unknown'

			i = objects.Component(manufacturer, number)
			i.set('Category', category, 'string')

			parameters = self.query('SELECT * FROM parameters where id = ?', str(id)).fetchall()

			def _convert(value, mode):
				if mode == 'datetime':
					return datetime.strptime(value, '%X %x')

				elif mode == 'float':
					return int(value)

				else:
					return value

			for id, parameter, value, mode in parameters:
				i.set(parameter, _convert(value, mode))

			data.append(i)

		return data



	### таблица производителей ###

	def set_man(self, manufacturer):

		self.query('INSERT INTO manufacturers (manufacturer) VALUES (?)', (manufacturer,))
		self.commit()

		result = self.cursor.lastrowid

		return result



	def get_man(self, manufacturer=None, id=None):

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



	def get_symbol(self, symbol=None):

		if symbol:
			query = 'SELECT rowid FROM symbols WHERE symbol = ?'
			answer = self.query(query, (symbol,)).fetchone()

			result = answer and answer[0] or None

		else:
			answer = self.query('SELECT symbol FROM symbols').fetchall()

			result = []
			for i in answer:
				result.append(i[0])

		print result
		return result



### функция, которая призвана заменить get_ symbols, packages, models ####

	def get_property(self, property, value=None):

		if not property in ('symbols', 'packages', 'models'):
			print 'PROPERTY error'
			return


		var = {}
		var['column']

		query = 'SELECT rowid FROM symbols'


		if symbol:
			query = 'SELECT rowid FROM symbols WHERE symbol = ?'
			answer = self.query(query, (symbol,)).fetchone()

			result = answer and answer[0] or None

		else:
			answer = self.query('SELECT symbol FROM symbols').fetchall()

			result = []
			for i in answer:
				result.append(i[0])

		print result
		return result




	### таблица корпусов ###

	def set_package(self, package):

		self.query('INSERT INTO packages (package) VALUES (?)', (package,))
		id = self.cursor.lastrowid
		self.commit()

		return id


	def get_package(self, package=None):

		if package:
			query = 'SELECT rowid FROM packages WHERE package = ?'
			answer = self.query(query, (package,)).fetchone()

			result = answer and answer[0] or None

		else:
			answer = self.query('SELECT package FROM packages').fetchall()

			result = []
			for i in answer:
				result.append(i[0])

		print result
		return result


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



	def get_model(self, model=None):

		if model:
			query = 'SELECT rowid FROM models WHERE model = ?'
			answer = self.query(query, (model,)).fetchone()

			result = answer and answer[0] or None

		else:
			answer = self.query('SELECT model FROM models').fetchall()

			result = []
			for i in answer:
				result.append(i[0])

		print result
		return result



	def get_models(self):
		answer = self.query('SELECT model FROM models').fetchall()

		result = []
		for i in answer:
			result.append(i[0])

		return result



	### получение неэкспортированных элементов ###

	def export(self, category=None, all=False):
		elements = self.query('SELECT rowid, manufacturer, number FROM components WHERE category = ? AND checked = ?', (category, False)).fetchall()

		print 'ELEM', elements

		data = []
		if elements:
			for id, man_id, number in elements:

#				symbol = (lambda x: x and x[0] or None)(self.query('SELECT symbol FROM symbols WHERE id = ?', (sid,)).fetchone())
#				package = (lambda x: x and x[0] or None)(self.query('SELECT package FROM packages WHERE id = ?', (pid,)).fetchone())
#				model = (lambda x: x and x[0] or None)(self.query('SELECT model FROM models WHERE id = ?', (mid,)).fetchone())

				manufacturer = self.get_man(id=man_id)

				element = {}

				parameters = self.query('SELECT * FROM parameters where id = ?', str(id)).fetchall()

				def _convert(value, mode):
					if mode == 2:
						return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

					elif mode == 1:
						return int(value)

					elif mode == 0:
						return value

				for id, parameter, value, mode in parameters:
					print 'MODE', mode, value
					element[parameter] = _convert(value, mode)

				element['Manufacturer'] = manufacturer
				element['PartNumber'] = number
				element['Category'] = category

				element['CreationDate'] = element.get('CreationDate', datetime.utcnow())

				data.append(element)

				self.query('UPDATE components SET checked = ? WHERE manufacturer = ? AND number = ?', (True, man_id, number)).fetchall()

		return data


	### получение неотправленных элементов ###

	def get_upload(self):

		elements = self.query('SELECT rowid, manufacturer, number, category FROM components WHERE sent = ?', (False,)).fetchall()
		data = []

		for id, man_id, number, category in elements:
			manufacturer = self.get_man(id=man_id)# or 'Unknown'

			i = objects.Component(manufacturer, number)
			i.set('Category', category, 'string')

			parameters = self.query('SELECT * FROM parameters where id = ?', str(id)).fetchall()

			def _convert(value, mode):
				if mode == 'datetime':
					return datetime.strptime(value, '%X %x')

				elif mode == 'float':
					return int(value)

				else:
					return value

			for id, parameter, value, mode in parameters:
				i.set(parameter, _convert(value, mode))

			data.append(i)
			self.query('UPDATE components SET sent = ? WHERE manufacturer = ? AND number = ?', (True, man_id, number)).fetchall()

		return data