#-*- coding: utf-8 -*-

import time

from kernel import db
from kernel import objects



def do_put_process(parent, data):

	result = data.id
	print 'PUT', result

	ldb = db.Database('data/pyclient.db')
	ldb.init()

	print ldb

	ldb.set_element(data)

	data = ldb.get_elements()

	query = objects.QueryMessage()
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



