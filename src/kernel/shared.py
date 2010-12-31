#-*- coding: utf-8 -*-

import time

from kernel.db import database

from kernel.objects import QueryMessage

def do_put_process(parent, data):

	print 'PARENT', parent

	result = data.name
	print 'PUT', result

	ldb = database('data/local.db')
	ldb.init()

	ldb.set_element(data)

	data = ldb.get_elements()

	query = QueryMessage()
	for element in data:
		query.additem(element)

	query.build()

	return result



def dosmthng(parent, *args, **kwargs):
	print kwargs
	i = 0
	while i < 16:
		print i
		parent.iter(i)
		i = i + 1
		time.sleep(0.2)



