#-*- coding: utf-8 -*-

import sys
import os

import re
import time
import datetime

import pkg_resources

from kernel import database
#from kernel import utils
from kernel import objects
#from kernel import transport

from kernel.abstract import AppException

###########################


def application_start(application):
	database = db.Database(application.dbname)
	database.init()


def collector(process):
	pass


def sync(process):
	settings = process.appconfig()

	### подключаем модуль вывода ###
	modulename = settings.option('DATA', 'module')

	if not modulename:
		raise AppException('No modulename')

	print 'Using module:', modulename

	try:
		pkg_resources.require(modulename)

	except pkg_resources.DistributionNotFound:
		message = 'not found %s' % (modulename,)
		raise AppException(message)

#	plugins = {}

	for entrypoint in pkg_resources.iter_entry_points(group='db.engine', name=None):

#		if not entrypoint.dist in plugins:
			print entrypoint.dist
			print entrypoint.name

			plugin = entrypoint.load()

	module = plugin()

	print module

	return module




def format(data):
	if not data:
		print 'nothing to format'
		return

	print



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
