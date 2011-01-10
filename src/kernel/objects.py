#-*- coding: utf-8 -*-

import datetime
import xml.etree.ElementTree as eltree

#######################


class QueryMessage():
	Name = 'XML Query'

	def __init__(self):

		self.type = 'add'
		self.target = 'components'
		self.items = []


	def type(self):
		pass

	def add(self, item):
		self.items.append(item)


	def build(self):
		xmldata = eltree.TreeBuilder()
		xmldata.start('query', {})

		# header section
		xmldata.start('action', {'type': self.type, 'source': self.target})
		xmldata.end('action')

		# data section
		xmldata.start('data', {})

		for item in self.items:
			xmldata.start('Component', {'man': item.manufacturer, 'num': item.number})


			for parameter in item.parameters.values():

				xmldata.start(parameter.name, {'type': parameter.type})
				xmldata.data(parameter.value)
				xmldata.end(parameter.name)

			xmldata.end('Component')

		xmldata.end('data')

		res = xmldata.end('query')

		res = eltree.tostring(res, encoding="utf-8") 
		print res

		with (open('data/gen.xml', 'wb')) as xmlfile:
			xmlfile.write(res)




class Component():
	Name = 'CAD Component'

	def __init__(self, manufacturer, number):
		self.manufacturer = manufacturer or 'Unknown'
		self.number = number or 'Unknown'

		self.parameters = {}



	def id(self):
		return '.'.join((self.manufacturer, self.number))



	def add_parameter(self, parameter):
		print 'DEPRECATED add_parameter'
		self.set(parameter)



	def set(self, parameter):
		if not isinstance(parameter, cParameter):
			raise TypeError, "should be cParameter object"

		self.parameters[parameter.name] = parameter		



	def get(self, parametername):
		return self.parameters.get(parametername)




class cParameter():
	Name = 'Component Parameter'

	def __init__(self, name, value, mode='string'):
		self.name = name
		self.value = value
		self.type = mode

		def __t(self):

			if isinstance(parameter.type, datetime.datetime):
				atr = {'type': 'datetime'}
#				item[field] = item[field].isoformat(' ')

			elif type(item[field]) == 'int':
				atr = {'type': 'float'}
#				item[field] = str(item[field])

			elif item[field] is None:
				atr = {}
#				item[field] = ''

			else:
				atr = {'type': 'string'}

