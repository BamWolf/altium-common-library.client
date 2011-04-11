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

from modules import csvfile
from modules import msaccess

###########################


def application_start(application):
	database = db.Database(application.dbname)
	database.init()





def do_put_process(parent, data):

	result = data.id()

#	print 'PUT', result

	db = database.Database('data/pyclient.db')

	try:
		db.set_element(data)
		db.commit()

	except Exception, e:
		print 'Error:', e

#	print db.cursor.execute('SELECT * FROM components').fetchall()

	db.close()

	return result




def do_upload(worker, data=None):

	db = database.Database('data/pyclient.db')

	data = db.get_upload()

	if not data:
		return 'Nothing to upload'

	application = worker.parent()

	tr = transport.Transport(worker.parent())

	request = objects.RequestMessage('identify')
	request.add_value('login', application.settings.option('ACCOUNT', 'login', u'user'))
	request.add_value('password', application.settings.option('ACCOUNT', 'password', u'user'))
	xmlrequest = request.build()

	xmlresponse = tr.send(xmlrequest, 'http://altiumlib.noxius.ru/?page=client&rem=read')

	response = objects.ResponseMessage(xmlresponse)
	response.parse()

	if response.error:
		print response.error
		return 'Parsing answer Error'

	if response.type == 'error':
		try:
			message = response.values['message']
		except:
			message = 'General Error'

		return message

	sessionid = response.values['sessionid']

	# формирование XML
	request = objects.RequestMessage('set_components')
	request.add_value('sessionid', sessionid)

	for element in data:
		request.add_item(element)

	xmlrequest = request.build()

	print xmlrequest

	# отправка XML
	application = worker.parent()
	xmlresponse = tr.send(xmlrequest, 'http://altiumlib.noxius.ru/?page=client&rem=read&PHPSESSID=' + sessionid)

	# отмечаем отправленные компоненты
#	for element in answer:
#		db.set_sent(element)

	db.commit()
	db.close()

	return 'Uploaded %d components' % (len(data),)


def do_download(worker, data):
	# загрузка обновлений с сервера

	application = worker.parent()
	tr = transport.Transport(worker.parent())

#	sessionid = application.settings.option('CONNECTION', 'sessionid')

	try:
		application.sessionid

	except AttributeError:
		request = objects.RequestMessage('identify')
		request.add_value('login', application.settings.option('ACCOUNT', 'login', u'user'))
		request.add_value('password', application.settings.option('ACCOUNT', 'password', u'user'))
		xmlrequest = request.build()

		xmlresponse = tr.send(xmlrequest, 'http://altiumlib.noxius.ru/?page=client&rem=read')

		print xmlresponse
		if not xmlresponse:
			return 'Communication error'

		response = objects.ResponseMessage(xmlresponse)
		response.parse()

		if response.error:
			print response.error
			return 'Parsing error'

		if response.type == 'error':
			try:
				message = response.values['message']
			except:
				message = 'General Error'

			return message

#		application.settings.set_option('CONNECTION', 'sessionid', sessionid)
		application.sessionid = response.values['sessionid']

	since = application.settings.option('DATA', 'lastupdate', datetime.datetime.min)

	request = objects.RequestMessage('get_components')
	request.add_value('sessionid', application.sessionid)
	request.add_value('since', since)

	xmlrequest = request.build()

	xmlresponse = tr.send(xmlrequest, 'http://altiumlib.noxius.ru/?page=client&rem=read&PHPSESSID=' + application.sessionid)

	if not xmlresponse:
		return 'Communication error'

	response = objects.ResponseMessage(xmlresponse)
	response.parse()

	if response.type == 'error':
		print 'Error parsing response:', response.error
		return 'Error parsing response'

	application.settings.set_option('DATA', 'lastupdate', datetime.datetime.utcnow()	.isoformat(' '))

	if not response.data:
		print 'No data fetched'
		return 'Downloaded %d new components' % (len(response.data),)

	db = database.Database('data\pyclient.db')

	for element in response.data:
		db.set_element(element, sent=True)

	db.commit()
	db.close()

	return 'Downloaded %d new components' % (len(response.data),)


def do_export(parent, data):
	# обновление пользовательских источников данных

	db = database.Database('data/pyclient.db')

	for category in systemcategories:
		print 'CATEGORY:', category

		content = db.export(category)

		# костыль для полей Author локальных элементов
		for element in content:
			element['Author'] = element.get('Author', parent.parent().settings.option('ACCOUNT', 'user'))

		print 'content', content
		result = sortupdate(category, content)

		if result:
			table, fieldlist, sorted = result

			print 'sorted', sorted

#			tr = csvfile.CSVWriter()
			tr = msaccess.MDBWriter()
			tr.initialize()

			if tr.error:
				print 'ERROR'
				return tr.error

			tr.set(table, fieldlist, sorted)

			if tr.error:
				print 'ERROR', tr.error
				return tr.error

#			db.set_exported(category, content)
			db.commit()

	db.close()

	return 'Done'


def format(data):
	if not data:
		print 'nothing to format'
		return

	print
	print data
	print

	cfg = utils.OptionManager('data.ini')

	if cfg.error:
		print cfg.error
		return

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
				print fieldvalue


			### получаем строковые значения параметров ###
			for parameter in list2:
				value = element.get(parameter[1:-1])
				fieldvalue = fieldvalue.replace(parameter, value)

			print '%s: "%s" (%s)' % (field, fieldvalue, type(fieldvalue))

			el[field] = fieldvalue

		result[category][2].append(el)

		print

	print 'RESULT:'
	print result

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
	#from pkg_resources import require

	sys.path.insert(0, 'modules')
#	print sys.path

	# находим egg SQLite
	try:
		pkg_resources.require(writername)

	except pkg_resources.DistributionNotFound, e:
		print '%s plugin not found' % (writername,)

	plugins = {}

	for entrypoint in pkg_resources.iter_entry_points(group='db.engine', name=None):

		if not entrypoint.dist in plugins:
			print entrypoint.dist
			print entrypoint.name

		plugin = entrypoint.load()
		tr = plugin()

		print tr.echo('fuck yeah')


#	writer = csvfile.CSVWriter()
#	writer.set(result)

	writer = msaccess.MDBWriter()
	writer.set(result)
