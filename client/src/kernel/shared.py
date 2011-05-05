#-*- coding: utf-8 -*-

import os
import sys

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

SYMBOL = 'Symbol'
PACKAGE = 'Package'
MODEL = 'Model'

CATEGORY = 'Category'

URL = 'URL'
DESCRIPTION = 'Description'

AUTHOR = 'Author'
CREATIONTIME = 'CreationTime'

###########################


def _(s):
	return s

def application_start(application):
	database = db.Database(application.dbname)
	database.init()



def sync(process):

	### получаем настройки приложения ###
	settings = process.appconfig()

	### подключаем модуль вывода ###
	modulename = settings.option('DATA', 'module')

	if not modulename:
		raise AppException(_('no output modulename configured'))

	module = load_module(modulename)	

	### получаем расположение репозитория ###
	xmlpath = os.path.abspath(settings.option('DATA', 'xmlrepository'))

	print 'XML repository path:', xmlpath
	print

#	components = collect_components(xmlpath)
	components = process.components

	export_components(module, components.values())



def load_module(modulename):

	##### испортировать приходится именно тут, потому что по другому не работает #####
	import pkg_resources

	print 'using module:', modulename

	try:
		pkg_resources.require(modulename)

	except pkg_resources.DistributionNotFound:
		message = _('not found %s') % (modulename,)
		raise AppException(message)

	for entrypoint in pkg_resources.iter_entry_points(group='db.engine', name=None):

		print
		print entrypoint.dist
		print entrypoint.name

		moduleclass = entrypoint.load()

	if not moduleclass:
		raise AppException(_('corrupted module'))

	module = moduleclass()
	return module



def collect_components(xmlpath):

	components = {}
	componentpath = os.path.join(xmlpath, 'components')

	symbols = collect_symbols(xmlpath)
	packages = collect_packages(xmlpath)
	models = collect_models(xmlpath)

	print 'SYMBOLS', symbols
	print
	print 'PACKAGES', packages
	print
	print 'MODELS', models
	print

	""" поиск компонентов """

	for path, dirs, files in os.walk(componentpath):
		for filename in files:
			if fnmatch.fnmatch(filename, '*.xml'):
				if filename in components:
					message = 'duplicate found: %s\\%s' % (path, filename)
					print message
#					raise AppException(message)

				else:
					with open(os.path.abspath(os.path.join(path, filename))) as xmlfile:
						xmldata = xmlfile.read()

					element = objects.Component()
					element.parse(xmldata)

					print element.id()

					symbol = element.get(SYMBOL)
					package = element.get(PACKAGE)
					model = element.get(MODEL)

					print
					print '\tSymbol:', symbol
					print '\tPackage:', package
					print '\tModel:', model

					""" добавление параметров символа """

					if symbol and symbol in symbols:
						for parameter in symbols[symbol][0]:
							element.set(objects.Parameter('.'.join((SYMBOL, parameter.name())), parameter.value(), parameter.value()))

					""" добавление параметров корпуса """

					if package and package in packages:
							for parameter in packages[package][0]:
								element.set(objects.Parameter('.'.join((PACKAGE, parameter.name())), parameter.value(), parameter.value()))


					""" добавление параметров модели """

					if model and model in models:
							for parameter in models[model][0]:
								element.set(objects.Parameter('.'.join((MODEL, parameter.name())), parameter.value(), parameter.value()))


					print

					for parameter in element:
						print '%s: %s' % (parameter.name(), parameter.value())

					components[element.id()] = (element, os.path.abspath(os.path.join(path, filename)))

	return components




def collect_symbols(xmlpath):

	symbols = {}
	symbolpath = os.path.join(xmlpath, 'symbols')

	""" составление списка символов """
	for path, dirs, files in os.walk(symbolpath):
		for filename in files:
			if fnmatch.fnmatch(filename, '*.xml'):
				if filename[:-4] in symbols:
					message = 'duplicate found: %s\\%s' % (path, filename)
					print message
#					raise AppException(message)
 
				else:
					try:
						filename = os.path.abspath(os.path.join(path, filename))
						with open(filename) as xmlfile:
							xmldata = xmlfile.read()

						symbol = objects.Symbol()
						symbol.parse(xmldata)
						symbols[symbol.id()] = (symbol, os.path.abspath(os.path.join(path, filename)))

					except Exception, e:
						message = _('symbol parsing error^ %s') % (e,)
						raise AppException(message)

	return symbols



def collect_packages(xmlpath):

	packages = {}
	packagepath = os.path.join(xmlpath, 'packages')

	""" составление списка корпусов """

	for path, dirs, files in os.walk(packagepath):
		for filename in files:
			if fnmatch.fnmatch(filename, '*.xml'):
				if filename in packages:
					message = 'duplicate found: %s\\%s' % (path, filename)
					print message
#					raise AppException(message)

				else:
					try:
						filename = os.path.abspath(os.path.join(path, filename))
						with open(filename) as xmlfile:
							xmldata = xmlfile.read()

						package = objects.Package()
						package.parse(xmldata)
						packages[package.id()] = (package, os.path.abspath(os.path.join(path, filename)))

					except Exception, e:
						message = _('package parsing error^ %s') % (e,)
						raise AppException(message)

	return packages


def collect_models(xmlpath):

	models = {}
 	modelpath = os.path.join(xmlpath, 'models')

	""" составление списка моделей """

	for path, dirs, files in os.walk(modelpath):
		for filename in files:
			if fnmatch.fnmatch(filename, '*.xml'):
				if filename in models:
					message = 'duplicate found: %s\\%s' % (path, filename)
					print message
#					raise AppException(message)

				else:
					try:
						filename = os.path.abspath(os.path.join(path, filename))
						with open(filename) as xmlfile:
							xmldata = xmlfile.read()

						model = objects.Model()
						model.parse(xmldata)
						models[model.id()] = (model, os.path.abspath(os.path.join(path, filename)))

					except Exception, e:
						message = _('model parsing error^ %s') % (e,)
						raise AppException(message)

	return models




def export_components(module, components):

	if not components:
		raise AppException(_('nothing to format'))

	result = {}

	for element in components:
		category = element.get('Category')

		# наименование таблицы для текущей категории
		table = module.settings.option('TABLES', category)

		if not table:
			print _('no table %s') % (category,)
			return

		# dict наименования полей таблицы и их значения
		tablefields = module.settings.options(table + '_FIELDS', True) or {}
		# or DEFAULTS {'Part Number': '[Manufacturer].[PartNumber]', 'Library Ref': '[SymbolLib]', 'Footprint Ref': '[FootprintLib]'}

		if not tablefields:
			message = _('no fields in %s') % (table,)
			raise AppException(message)

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
