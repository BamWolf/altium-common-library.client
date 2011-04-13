#-*- coding: utf-8 -*-

import sys
import os

import re
import time
import datetime

from kernel import database
from kernel import utils
from kernel import objects
from kernel import transport

###########################


def application_start(application):
	database = db.Database(application.dbname)
	database.init()





class Formatter():
	def __init__(self):
		self.config = ''



def sync(process):

	### получаем доступ к настройкам приложения ###
	settings = process.appconfig()

	print settings

	import fnmatch

	### определяем путь к репозиториям ###

	selfpath = os.path.abspath(os.curdir)

	cfg = utils.OptionManager('settings.ini')
	basepath = os.path.abspath(cfg.option('DATA', 'repository'))

	basepath = os.path.abspath(os.path.join(basepath, 'xml'))
	print 'repository path:', basepath
	print

	unique = {}

	symbols = {}
	packages = {}
	models = {}

	componentpath = os.path.join(basepath, 'components')
	symbolpath = os.path.join(basepath, 'symbols')
	packagepath = os.path.join(basepath, 'packages')
	modelpath = os.path.join(basepath, 'models')

	""" составление списка символов """

	for path, dirs, files in os.walk(symbolpath):
		for filename in files:
			if fnmatch.fnmatch(filename, '*.xml'):
				if filename in symbols:
					print 'Duplicate Error:', filename, path

				else:
					symbols[filename[:-4]] = os.path.abspath(os.path.join(path, filename))


	print 'symbols:', symbols
	print


	""" составление списка корпусов """

	for path, dirs, files in os.walk(packagepath):
		for filename in files:
			if fnmatch.fnmatch(filename, '*.xml'):
				if filename in packages:
					print 'Duplicate Error:', filename, path

				else:
					packages[filename[:-4]] = os.path.abspath(os.path.join(path, filename))


	print 'packages:', packages
	print

	""" составление списка моделей """

	for path, dirs, files in os.walk(modelpath):
		for filename in files:
			if fnmatch.fnmatch(filename, '*.xml'):
				if filename in models:
					print 'Duplicate Error:', filename, path

				else:
					models[filename[:-4]] = os.path.abspath(os.path.join(path, filename))


	print 'models:', models
	print


	""" поиск компонентов """

	for path, dirs, files in os.walk(componentpath):
		for filename in files:
			if fnmatch.fnmatch(filename, '*.xml'):
				if filename in unique:
					print 'Duplicate Error:', filename, path

				else:
					with open(os.path.abspath(os.path.join(path, filename))) as xmlfile:
						xmldata = xmlfile.read()

					element = objects.Component()
					element.parse(xmldata)

					print
					print element.id()

					symbol = element.get('Symbol')
					package = element.get('Package')
					model = element.get('Model')

					print
					print '\tSymbol:', symbol
					print '\tPackage:', package
					print '\tModel:', model

					""" добавление параметров символа """

					if symbol and symbol in symbols:
						try:
							with open(symbols[symbol]) as xmlfile:
								xmldata = xmlfile.read()

							symbol = objects.Symbol()
							symbol.parse(xmldata)

							for parameter in symbol:
								element.set(objects.Parameter('.'.join(('Symbol', parameter.name())), parameter.value(), parameter.value()))

						except:
							print 'ERROR 23'

					""" добавление параметров корпуса """

					if package and package in packages:
						try:
							with open(packages[package]) as xmlfile:
								xmldata = xmlfile.read()

							package = objects.Package()
							package.parse(xmldata)

							for parameter in package:
								element.set(objects.Parameter('.'.join(('Package', parameter.name())), parameter.value(), parameter.value()))

						except:
							print 'ERROR 24'

					""" добавление параметров модели """

					if model and model in models:
						try:
							with open(models[model]) as xmlfile:
								xmldata = xmlfile.read()

							model = objects.Model()
							model.parse(xmldata)

							for parameter in model:
								element.set(objects.Parameter('.'.join(('Model', parameter.name())), parameter.value(), parameter.value()))

						except:
							print 'ERROR 25'


					print

					for parameter in element:
						print '%s: %s' % (parameter.name(), parameter.value())

#					unique[filename] = os.path.abspath(os.path.join(path, filename))
					unique[element.id()] = element

	formatted = format(unique.values())




def format(data):
	if not data:
		print 'nothing to format'
		return

	print

	cfg = utils.OptionManager('settings.ini')

	if cfg.error:
		print cfg.error
		return

	writername = cfg.option('DATA', 'output')

	if not writername:
		print 'No writer'
		return


	### плагины ###

	import pkg_resources

	try:
		pkg_resources.require(writername)

	except pkg_resources.DistributionNotFound, e:
		print '%s plugin not found' % (writername,)
		return

	plugins = {}

	for entrypoint in pkg_resources.iter_entry_points(group='db.engine', name=None):

		if not entrypoint.dist in plugins:
			print entrypoint.dist
			print entrypoint.name

			plugin = entrypoint.load()

	module = plugin()


	### поиск файлов

	result = {}

	for element in data:
		category = element.get('Category')

		# наименование таблицы для текущей категории
		table = cfg.option('TABLES', category)

		if not table:
			print 'no table %s' % (category,)
			return

		# dict наименования полей таблицы и их значения
		tablefields = cfg.options(table + '_FIELDS', True) or {}
		# or DEFAULTS {'Part Number': '[Manufacturer].[PartNumber]', 'Library Ref': '[SymbolLib]', 'Footprint Ref': '[FootprintLib]'}

		if not tablefields:
			print 'no fields in %s' % (table,)
			return

#		print tablefields
		print 'COMPONENT'
		print

		if not category in result:
			result[category] = [table, tablefields.keys(), []]

		el = {}

		for field, fieldvalue in tablefields.items():
			pattern = re.compile('^\\{[a-z.]+\\}', re.IGNORECASE)
			pattern2 = re.compile('\\[[a-z.]+\\]', re.IGNORECASE)

	#		list = pattern.finditer(fieldvalue)
	#		list2 = pattern2.finditer(fieldvalue)

			list = pattern.findall(fieldvalue)
			list2 = pattern2.findall(fieldvalue)

			### получаем все неприведенные значения  параметров ###
			for parameter in list:
				value = element.get(parameter[1:-1], True)
				fieldvalue = value

			### получаем строковые значения параметров ###
			for parameter in list2:
				value = element.get(parameter[1:-1])
				fieldvalue = fieldvalue.replace(parameter, value)

#			print '%s: "%s" (%s)' % (field, fieldvalue, type(fieldvalue))

			el[field] = fieldvalue

		result[category][2].append(el)

		print

	print 'RESULT:'
	print result


	module.set(result)
