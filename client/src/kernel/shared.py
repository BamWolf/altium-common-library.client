#-*- coding: utf-8 -*-

import sys
import os

import re
import time
import datetime

import fnmatch

#from kernel import database
#from kernel import utils
from kernel import objects
#from kernel import transport

from kernel.abstract import AppException

###########################


def application_start(application):
	database = db.Database(application.dbname)
	database.init()


def collect_components(repopath):

	components = {}
	symbols = {}
	packages = {}
	models = {}
 
	componentpath = os.path.join(repopath, 'components')
	symbolpath = os.path.join(repopath, 'symbols')
	packagepath = os.path.join(repopath, 'packages')
	modelpath = os.path.join(repopath, 'models')
 
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
				if filename in components:
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

					components[element.id()] = element

	return components


def load_module(modulename):

	##### испортировать приходится именно тут, потому что по другому не работает #####
	import pkg_resources

	print 'using module:', modulename

	try:
		pkg_resources.require(modulename)

	except pkg_resources.DistributionNotFound:
		message = 'not found %s' % (modulename,)
		raise AppException(message)

	for entrypoint in pkg_resources.iter_entry_points(group='db.engine', name=None):

		print entrypoint.dist
		print entrypoint.name

		moduleclass = entrypoint.load()

	if not moduleclass:
		raise AppException('corrupted module')

	module = moduleclass()
	return module


def sync(process):

	### получаем настройки приложения ###
	settings = process.appconfig()

	### подключаем модуль вывода ###
	modulename = settings.option('DATA', 'module')

	if not modulename:
		raise AppException('no output modulename configured')

	module = load_module(modulename)	

	### получаем расположение репозитория ###
	basepath = os.path.abspath(settings.option('DATA', 'repository'))
	repopath = os.path.abspath(os.path.join(basepath, 'xml'))

	print 'repository path:', repopath

	components = collect_components(repopath)

	export_components(module, components.values())


def export_components(module, components):

	if not components:
		raise AppException('nothing to format')

	result = {}

	cfg = module.settings

	for element in components:
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