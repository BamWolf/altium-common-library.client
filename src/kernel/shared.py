#-*- coding: utf-8 -*-

import time

from kernel import db
from kernel import utils
from kernel import objects
from kernel import transport

###########################


def application_start(application):
	database = db.Database(application.dbname)
	database.init()





def do_put_process(parent, data):

	result = data.id()

	print 'PUT', result

	ldb = db.Database('data/pyclient.db')

	try:
		ldb.set_element(data)
		ldb.commit()

	except Exception, e:
		print e

	# обновление пользовательских источников данных


	# отправка новых компонентов на сервер
	# выборка компонентов из базы данных
	data = ldb.get_elements()


	# формирование XML
	query = objects.QueryMessage()
#	query = objects.QueryMessage('add', 'components')

	for element in data:
		query.add(element)

	xmldata = query.build()

	print xmldata

	# отправка XML
	application = parent.parent()
	answer = transport.send(application, xmldata)

	# отмечаем отправленные компоненты
#	for element in answer:
#		ldb.set_sent(element)


	# возвращаем результат (что отправлено, что нет)


	ldb.close()
	return result



def dosmthng(parent, *args, **kwargs):
	print kwargs
	i = 0
	while i < 16:
		print i
		parent.iter(i)
		i = i + 1
		time.sleep(0.2)



