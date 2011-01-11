#-*- coding: utf-8 -*-

import time

from kernel import db
from kernel import objects



def do_put_process(parent, data):

	result = data.id()

	print 'PUT', result

	ldb = db.Database('data/pyclient.db')
	ldb.set_element(data)

	# обновление пользовательских источников данных


	# отправка новых компонентов на сервер
	# выборка компонентов из базы данных
	data = ldb.get_elements()


	# формирование XML
	query = objects.QueryMessage()
	for element in data:
		query.add(element)

	query.build()

	# отправка XML

	# отмечаем отправленные компоненты

	# возвращаем результат (что отправлено, что нет)
	return result



def dosmthng(parent, *args, **kwargs):
	print kwargs
	i = 0
	while i < 16:
		print i
		parent.iter(i)
		i = i + 1
		time.sleep(0.2)



